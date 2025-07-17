# Lexora - AI-Powered Learning Platform

A modern, full-stack learning platform that combines AI-powered content generation with personalized narrated video lessons.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure registration and login system
- **Topic Management**: Create and organize learning subjects
- **Learning Paths**: Structured curriculum creation
- **Lesson Management**: Detailed lesson content and scripts
- **Video Generation**: AI-powered narrated video lessons
- **Voice Cloning**: Custom voice synthesis using ElevenLabs
- **Progress Tracking**: Monitor learning progress and achievements

### AI Integration
- **ElevenLabs Voice Cloning**: Create custom voices for personalized narration
- **Suprath-lipsync Video Generation**: Generate lip-synced videos with avatars
- **Text-to-Speech**: Convert lesson content to natural-sounding audio
- **Avatar Synchronization**: Match lip movements to generated speech

## 🛠 Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping
- **PostgreSQL**: Robust relational database
- **Uvicorn**: ASGI server for production deployment
- **Pydantic**: Data validation using Python type annotations
- **JWT Authentication**: Secure token-based authentication

### Frontend
- **React 18**: Modern JavaScript library for building user interfaces
- **Vite.js**: Next-generation frontend tooling
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Declarative routing for React applications
- **Axios**: Promise-based HTTP client
- **React Hook Form**: Performant forms with easy validation

### AI Services
- **ElevenLabs API**: Voice cloning and text-to-speech
- **Hugging Face Suprath-lipsync**: Lip-sync video generation
- **Custom Video Processing**: Avatar-based video creation

## 📁 Project Structure

```
lexora-redeveloped/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes and endpoints
│   │   ├── core/           # Core configuration and security
│   │   ├── db/             # Database configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # External API integrations
│   │   └── utils/          # Utility functions
│   ├── uploads/            # File storage
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
└── frontend/               # React frontend
    ├── src/
    │   ├── components/     # React components
    │   ├── contexts/       # React contexts
    │   ├── pages/          # Page components
    │   └── services/       # API service layer
    ├── package.json        # Node.js dependencies
    └── vite.config.js      # Vite configuration
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 13+
- ElevenLabs API Key
- Hugging Face API Key

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb lexora_db
   ```

5. **Run database migrations**
   ```bash
   python -m app.db.init_db
   ```

6. **Start the backend server**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   pnpm install
   ```

3. **Start the development server**
   ```bash
   pnpm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5174
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
PROJECT_NAME=Lexora API
VERSION=1.0.0
DESCRIPTION=Lexora AI-Powered Learning Platform API

# Database
DATABASE_URL=postgresql://username:password@localhost/lexora_db

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage
UPLOAD_DIR=/path/to/uploads

# External APIs
ELEVENLABS_API_KEY=your-elevenlabs-api-key
HUGGINGFACE_API_KEY=your-huggingface-api-key
SUPRATH_LIPSYNC_URL=https://suprath-lipsync.hf.space/run/predict
```

#### Frontend
```env
VITE_API_BASE_URL=http://localhost:8000
```

## 📚 API Documentation

The FastAPI backend provides comprehensive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/token` - Token refresh

#### Content Management
- `GET/POST /api/v1/topics/` - Topic management
- `GET/POST /api/v1/learning-paths/` - Learning path management
- `GET/POST /api/v1/lessons/` - Lesson management

#### AI Features
- `POST /api/v1/voices/clone` - Clone voice from audio samples
- `POST /api/v1/voices/generate-speech` - Generate speech from text
- `POST /api/v1/videos/generate` - Generate lip-sync videos

## 🎯 Usage Examples

### Creating a Learning Path

1. **Register/Login** to the platform
2. **Create a Topic** (e.g., "Python Programming")
3. **Generate Learning Path** using AI assistance
4. **Add Lessons** with detailed content and scripts
5. **Generate Videos** with custom voice and avatar
6. **Track Progress** as you complete lessons

### Voice Cloning Workflow

1. **Upload Audio Samples** (3-5 minutes of clear speech)
2. **Clone Voice** using ElevenLabs API
3. **Generate Speech** from lesson text
4. **Create Videos** with lip-sync using Suprath-lipsync

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt password encryption
- **CORS Configuration**: Secure cross-origin requests
- **Input Validation**: Pydantic schema validation
- **File Upload Security**: Secure file handling and storage

## 🚀 Deployment

### Production Deployment

1. **Backend Deployment**
   ```bash
   # Using Docker
   docker build -t lexora-backend .
   docker run -p 8000:8000 lexora-backend
   
   # Or using Gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Frontend Deployment**
   ```bash
   # Build for production
   pnpm run build
   
   # Deploy to static hosting (Netlify, Vercel, etc.)
   # Or serve with nginx/apache
   ```

3. **Database Setup**
   - Configure PostgreSQL for production
   - Set up database backups
   - Configure connection pooling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ElevenLabs** for voice cloning technology
- **Hugging Face** for Suprath-lipsync model
- **FastAPI** for the excellent web framework
- **React** and **Vite** for modern frontend development
- **Tailwind CSS** for beautiful styling

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the troubleshooting section below

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Ensure database exists

2. **API Key Issues**
   - Verify ElevenLabs API key is valid
   - Check Hugging Face API key permissions
   - Ensure API keys are set in environment

3. **File Upload Issues**
   - Check UPLOAD_DIR permissions
   - Verify disk space availability
   - Ensure file size limits are appropriate

4. **CORS Issues**
   - Verify frontend URL in CORS settings
   - Check API base URL configuration
   - Ensure proper headers are set

---

**Built with ❤️ for the future of AI-powered education**

