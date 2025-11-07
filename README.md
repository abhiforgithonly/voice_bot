# 🎤 AI Interview Voice Bot

A real-time voice-powered interview assistant that uses AI to answer questions as a job candidate. Talk naturally, get authentic responses, and experience the future of AI-powered interviews.

## ✨ What It Does

This bot acts as your digital representative in interviews, answering questions based on a predefined background story. It listens to your questions, transcribes them, generates natural responses using AI, and speaks back to you—all in real-time.

## 🚀 Live Demo

Deployed on Render: [https://voice-bot-jl0z.onrender.com]

## 🛠️ Tech Stack

- **Frontend**: Vanilla JS with a ChatGPT-inspired UI
- **Backend**: Flask (Python)
- **Speech-to-Text**: Deepgram Nova-2
- **Text-to-Speech**: Deepgram Aura TTS
- **AI Model**: OpenAI GPT-3.5 Turbo via OpenRouter
- **Hosting**: Render

## 🎯 Key Features

- 🎙️ **Voice Recording** - Click to start/stop recording
- 💬 **Real-time Transcription** - Instant speech-to-text conversion
- 🤖 **Contextual AI Responses** - Maintains conversation history
- 🔊 **Natural Voice Synthesis** - AI speaks responses aloud
- 📝 **Edit Conversations** - Modify messages and titles
- 💾 **Multi-conversation Support** - Manage multiple interview sessions

## 📦 Local Setup

1. Clone the repository
```bash
git clone <your-repo-url>
cd ai-interview-bot
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create `.env` file
```env
OPENROUTER_API_KEY=your_openrouter_key
DEEPGRAM_API_KEY=your_deepgram_key
```

4. Run the app
```bash
python app.py
```

5. Open `http://localhost:5000` in your browser

## 🌐 Deployment on Render

1. Push code to GitHub
2. Connect repository to Render
3. Add environment variables in Render dashboard:
   - `OPENROUTER_API_KEY`
   - `DEEPGRAM_API_KEY`
4. Deploy using `render.yaml` configuration

## 🔮 Future Improvements

### High Priority
- [ ] **Persistent Storage** - Replace in-memory storage with PostgreSQL/MongoDB
- [ ] **User Authentication** - Add login system for multi-user support
- [ ] **Export Transcripts** - Download conversations as PDF/TXT
- [ ] **Voice Selection** - Multiple TTS voice options (male/female, accents)
- [ ] **Real-time Streaming** - Stream AI responses instead of waiting for complete text

### Nice to Have
- [ ] **Mobile App** - React Native version for iOS/Android
- [ ] **Custom Personalities** - Create and switch between different candidate profiles
- [ ] **Interview Analytics** - Track common questions, response times, sentiment analysis
- [ ] **Background Noise Reduction** - Better audio preprocessing
- [ ] **Video Avatar** - Add a visual talking avatar using D-ID or similar
- [ ] **Multi-language Support** - Interview in different languages
- [ ] **Practice Mode** - Mock interview with feedback on answers
- [ ] **Resume Upload** - Auto-generate candidate profile from resume

### Technical Enhancements
- [ ] **WebSocket Support** - For real-time bidirectional communication
- [ ] **Rate Limiting** - Prevent API abuse
- [ ] **Error Recovery** - Auto-retry failed API calls
- [ ] **Caching Layer** - Redis for frequently asked questions
- [ ] **CI/CD Pipeline** - Automated testing and deployment

## 📄 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

**Note**: This is a prototype built for demonstration purposes. API keys and sensitive data should be properly secured in production environments.
