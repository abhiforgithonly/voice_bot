from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import json
import traceback  

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# API Keys 
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
DEEPGRAM_API_KEY = os.environ.get('DEEPGRAM_API_KEY')

# Debug: Print API key status (first few chars only for security)
print(f"OpenRouter API Key loaded: {'Yes' if OPENROUTER_API_KEY else 'No'}")
if OPENROUTER_API_KEY:
    print(f"Key starts with: {OPENROUTER_API_KEY[:10]}...")
print(f"Deepgram API Key loaded: {'Yes' if DEEPGRAM_API_KEY else 'No'}")

# In-memory storage for conversations 
conversations = {}

# Prompt
SYSTEM_PROMPT = """You are an AI assistant representing a job candidate in an interview setting. 
Answer questions naturally and conversationally as if you are the candidate being interviewed. Be authentic, professional, and personable.

Here's the candidate's background:

LIFE STORY: 
I'm a passionate software developer with 3 years of experience in AI and web development. I discovered my love for coding during college when I built my first chatbot project. Since then, I've been fascinated by how AI can solve real-world problems and improve people's lives. I've worked on various projects ranging from NLP applications to full-stack web development, and I'm particularly excited about the intersection of AI agents and practical applications.

SUPERPOWER: 
My #1 superpower is rapid prototyping and learning. I can quickly understand new technologies, experiment with them, and build working prototypes in short timeframes. I'm the person who dives deep into documentation, tests various approaches, and delivers functional solutions fast. This skill has helped me stay current with the fast-evolving AI landscape and contribute effectively to projects with tight deadlines.

TOP 3 GROWTH AREAS:
1. System design and architecture at scale - While I'm good at building prototypes, I want to master designing systems that can handle millions of users and complex distributed architectures.

2. Team leadership and mentoring - I've mostly worked in small teams or independently, and I'd love to develop my skills in leading larger teams and mentoring junior developers.

3. Advanced machine learning theory - I'm strong with practical implementations using existing models and APIs, but I want to deepen my understanding of the mathematical foundations and be able to fine-tune and optimize models from scratch.

MISCONCEPTION: 
People often think I'm very serious and all-business because I'm deeply focused when working on problems. But once you get to know me, I'm actually quite approachable and have a good sense of humor. I love collaborative brainstorming sessions and enjoy building strong relationships with teammates. I just get really absorbed when I'm debugging or building something!

PUSHING BOUNDARIES: 
I push my boundaries by deliberately taking on projects that are slightly outside my comfort zone. For example, I recently challenged myself to build this voice bot using APIs I hadn't worked with before. I also participate in hackathons regularly, contribute to open-source projects, and set aside time each week to learn something new - whether it's a new framework, a research paper, or a different programming paradigm. I believe that consistent discomfort is where real growth happens.

ADDITIONAL CONTEXT:
- I'm passionate about building practical AI solutions that solve real problems
- I thrive in remote work environments and am excellent at async communication
- I value continuous learning and collaboration with talented teams
- I'm excited about opportunities to work on cutting-edge AI agent technology

Answer questions naturally based on this information. Be conversational, authentic, and friendly. If asked something not covered here, draw reasonable inferences based on the personality and background described, or honestly say you'd need to think more about it."""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    """Get all conversations"""
    conv_list = [
        {
            'id': conv_id,
            'title': conv['title'],
            'created_at': conv['created_at'],
            'message_count': len(conv['messages'])
        }
        for conv_id, conv in conversations.items()
    ]
    # Sort by creation time, newest first
    conv_list.sort(key=lambda x: x['created_at'], reverse=True)
    return jsonify({'conversations': conv_list})

@app.route('/api/conversations', methods=['POST'])
def create_conversation():
    """Create a new conversation"""
    data = request.json
    title = data.get('title', 'New Chat')
    
    conv_id = str(len(conversations) + 1)
    conversations[conv_id] = {
        'id': conv_id,
        'title': title,
        'created_at': datetime.now().isoformat(),
        'messages': []
    }
    
    return jsonify({
        'id': conv_id,
        'title': title,
        'created_at': conversations[conv_id]['created_at']
    })

@app.route('/api/conversations/<conv_id>', methods=['GET'])
def get_conversation(conv_id):
    """Get a specific conversation"""
    if conv_id not in conversations:
        return jsonify({'error': 'Conversation not found'}), 404
    
    return jsonify(conversations[conv_id])

@app.route('/api/conversations/<conv_id>', methods=['PUT'])
def update_conversation(conv_id):
    """Update conversation title"""
    if conv_id not in conversations:
        return jsonify({'error': 'Conversation not found'}), 404
    
    data = request.json
    new_title = data.get('title')
    
    if new_title:
        conversations[conv_id]['title'] = new_title
    
    return jsonify(conversations[conv_id])

@app.route('/api/conversations/<conv_id>', methods=['DELETE'])
def delete_conversation(conv_id):
    """Delete a conversation"""
    if conv_id not in conversations:
        return jsonify({'error': 'Conversation not found'}), 404
    
    del conversations[conv_id]
    return jsonify({'success': True})

@app.route('/api/conversations/<conv_id>/messages', methods=['POST'])
def add_message(conv_id):
    """Add a message to a conversation"""
    if conv_id not in conversations:
        return jsonify({'error': 'Conversation not found'}), 404
    
    data = request.json
    message = {
        'id': str(len(conversations[conv_id]['messages']) + 1),
        'role': data.get('role'),
        'content': data.get('content'),
        'timestamp': datetime.now().isoformat()
    }
    
    conversations[conv_id]['messages'].append(message)
    
    # Auto-update conversation title if it's the first user message
    if len(conversations[conv_id]['messages']) == 1 and message['role'] == 'user':
        # Use first 50 chars of first message as title
        conversations[conv_id]['title'] = message['content'][:50] + ('...' if len(message['content']) > 50 else '')
    
    return jsonify(message)

@app.route('/api/conversations/<conv_id>/messages/<msg_id>', methods=['PUT'])
def update_message(conv_id, msg_id):
    """Update a message"""
    if conv_id not in conversations:
        return jsonify({'error': 'Conversation not found'}), 404
    
    data = request.json
    new_content = data.get('content')
    
    for msg in conversations[conv_id]['messages']:
        if msg['id'] == msg_id:
            msg['content'] = new_content
            msg['edited'] = True
            return jsonify(msg)
    
    return jsonify({'error': 'Message not found'}), 404

@app.route('/api/conversations/<conv_id>/messages/<msg_id>', methods=['DELETE'])
def delete_message(conv_id, msg_id):
    """Delete a message"""
    if conv_id not in conversations:
        return jsonify({'error': 'Conversation not found'}), 404
    
    conversations[conv_id]['messages'] = [
        msg for msg in conversations[conv_id]['messages'] 
        if msg['id'] != msg_id
    ]
    
    return jsonify({'success': True})

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe audio using Deepgram"""
    try:
        audio_file = request.files.get('audio')
        
        if not audio_file:
            return jsonify({'error': 'No audio file provided'}), 400
        
        # Deepgram API endpoint
        url = "https://api.deepgram.com/v1/listen"
        
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
        }
        
        params = {
            "model": "nova-2",
            "smart_format": "true"
        }
        
        response = requests.post(
            url,
            headers=headers,
            params=params,
            data=audio_file.read()
        )
        
        if response.status_code == 200:
            result = response.json()
            transcript = result['results']['channels'][0]['alternatives'][0]['transcript']
            return jsonify({'transcript': transcript})
        else:
            return jsonify({'error': 'Transcription failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Get AI response using OpenRouter"""
    try:
        print("\n=== CHAT REQUEST DEBUG ===")
        
        # Check API key
        if not OPENROUTER_API_KEY:
            error_msg = "OpenRouter API key not configured"
            print(f"ERROR: {error_msg}")
            return jsonify({'error': error_msg}), 500
        
        data = request.json
        print(f"Request data: {data}")
        
        conv_id = data.get('conversation_id')
        print(f"Conversation ID: {conv_id}")
        
        if conv_id and conv_id in conversations:
            # Build message history for context
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            
            for msg in conversations[conv_id]['messages']:
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
            print(f"Built message history with {len(messages)} messages")
        else:
            # Single message without context
            user_message = data.get('message', '')
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
            print(f"Single message mode: {user_message[:50]}...")
        
        # OpenRouter API endpoint
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",  # Optional but recommended
            "X-Title": "AI Interview Bot"  # Optional but recommended
        }
        
        payload = {
            "model": "openai/gpt-3.5-turbo",  # Using GPT-3.5 Turbo
            "messages": messages
        }
        
        print(f"Sending request to OpenRouter...")
        print(f"Payload: {json.dumps(payload, indent=2)[:500]}...")
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"OpenRouter response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success! Response: {json.dumps(result, indent=2)[:500]}...")
            ai_response = result['choices'][0]['message']['content']
            return jsonify({'response': ai_response})
        else:
            error_detail = response.text
            print(f"ERROR Response: {error_detail}")
            return jsonify({
                'error': f'AI response failed with status {response.status_code}',
                'detail': error_detail
            }), 500
            
    except requests.exceptions.Timeout:
        error_msg = "Request to OpenRouter timed out"
        print(f"ERROR: {error_msg}")
        return jsonify({'error': error_msg}), 500
    except requests.exceptions.RequestException as e:
        error_msg = f"Request error: {str(e)}"
        print(f"ERROR: {error_msg}")
        print(traceback.format_exc())
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"ERROR: {error_msg}")
        print(traceback.format_exc())
        return jsonify({'error': error_msg}), 500

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    """Convert text to speech using Deepgram Aura TTS"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Deepgram TTS API endpoint
        url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"
        
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            # Return audio as base64
            import base64
            audio_base64 = base64.b64encode(response.content).decode('utf-8')
            return jsonify({'audio': audio_base64})
        else:
            return jsonify({'error': 'Text-to-speech failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable (for Render deployment)
    port = int(os.environ.get('PORT', 5000))
    # Disable debug in production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
