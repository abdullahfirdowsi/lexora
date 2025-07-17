# Lexora Deployment Guide

This guide provides step-by-step instructions for deploying the Lexora platform in production.

## 🚀 Quick Deployment Options

### Option 1: Local Development
- **Frontend**: http://localhost:5174
- **Backend**: http://localhost:8000
- **Best for**: Development and testing

### Option 2: Production Deployment
- **Frontend**: Deploy to Vercel/Netlify
- **Backend**: Deploy to Railway/Heroku/DigitalOcean
- **Database**: PostgreSQL on cloud provider
- **Best for**: Production use

## 📋 Prerequisites

### Required Services
1. **ElevenLabs Account**: For voice cloning
   - Sign up at https://elevenlabs.io
   - Get API key from dashboard
   - Minimum plan required for voice cloning

2. **Hugging Face Account**: For video generation
   - Sign up at https://huggingface.co
   - Get API token from settings
   - Access to Suprath-lipsync model

3. **Database**: PostgreSQL 13+
   - Local installation or cloud service
   - Recommended: Railway, Supabase, or AWS RDS

## 🔧 Environment Configuration

### Backend Environment Variables

Create `/backend/.env`:

```env
# Application
PROJECT_NAME=Lexora API
VERSION=1.0.0
DESCRIPTION=Lexora AI-Powered Learning Platform API

# Database
DATABASE_URL=postgresql://username:password@host:port/database

# Security
SECRET_KEY=your-super-secret-key-min-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage
UPLOAD_DIR=/app/uploads

# External APIs
ELEVENLABS_API_KEY=sk_your_elevenlabs_api_key
HUGGINGFACE_API_KEY=hf_your_huggingface_token
SUPRATH_LIPSYNC_URL=https://suprath-lipsync.hf.space/run/predict

# CORS (adjust for your frontend domain)
ALLOWED_ORIGINS=["http://localhost:5174", "https://your-frontend-domain.com"]
```

### Frontend Environment Variables

Create `/frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
# For production: VITE_API_BASE_URL=https://your-backend-domain.com
```

## 🐳 Docker Deployment

### Backend Dockerfile

Create `/backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads/audio uploads/videos uploads/avatars

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

Create `/frontend/Dockerfile`:

```dockerfile
FROM node:20-alpine as builder

WORKDIR /app

# Install dependencies
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

# Copy source code
COPY . .

# Build the application
RUN pnpm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

Create `/docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: lexora_db
      POSTGRES_USER: lexora_user
      POSTGRES_PASSWORD: lexora_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://lexora_user:lexora_password@postgres:5432/lexora_db
    volumes:
      - ./backend/uploads:/app/uploads
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

## ☁️ Cloud Deployment

### Railway Deployment

1. **Backend on Railway**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login and deploy
   railway login
   cd backend
   railway init
   railway up
   ```

2. **Add Environment Variables**
   - Go to Railway dashboard
   - Add all required environment variables
   - Connect PostgreSQL database

3. **Frontend on Vercel**
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Deploy
   cd frontend
   vercel
   ```

### Manual Server Deployment

1. **Server Setup** (Ubuntu 22.04)
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install dependencies
   sudo apt install -y python3.11 python3-pip nodejs npm postgresql nginx
   
   # Install pnpm
   npm install -g pnpm
   ```

2. **Database Setup**
   ```bash
   # Configure PostgreSQL
   sudo -u postgres createuser --interactive lexora_user
   sudo -u postgres createdb lexora_db -O lexora_user
   ```

3. **Backend Deployment**
   ```bash
   # Clone and setup
   git clone <repository>
   cd lexora-redeveloped/backend
   
   # Install dependencies
   pip3 install -r requirements.txt
   
   # Configure environment
   cp .env.example .env
   # Edit .env with production values
   
   # Run with Gunicorn
   pip3 install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

4. **Frontend Deployment**
   ```bash
   # Build frontend
   cd ../frontend
   pnpm install
   pnpm run build
   
   # Configure Nginx
   sudo cp dist/* /var/www/html/
   ```

5. **Nginx Configuration**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       # Frontend
       location / {
           root /var/www/html;
           try_files $uri $uri/ /index.html;
       }
       
       # Backend API
       location /api/ {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 🔒 Security Considerations

### Production Security Checklist

- [ ] Use strong SECRET_KEY (32+ characters)
- [ ] Enable HTTPS with SSL certificates
- [ ] Configure proper CORS origins
- [ ] Set up database connection pooling
- [ ] Implement rate limiting
- [ ] Configure file upload limits
- [ ] Set up monitoring and logging
- [ ] Regular security updates
- [ ] Backup strategy for database and files

### SSL Certificate Setup

```bash
# Using Certbot for Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 📊 Monitoring and Maintenance

### Health Checks

The backend provides health check endpoints:
- `GET /health` - Basic health check
- `GET /api/v1/health` - Detailed system status

### Logging

Configure logging in production:

```python
# In app/core/config.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
```

### Database Backups

```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump lexora_db > backup_$DATE.sql
```

## 🚨 Troubleshooting

### Common Deployment Issues

1. **Database Connection Failed**
   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql
   
   # Test connection
   psql -h localhost -U lexora_user -d lexora_db
   ```

2. **API Keys Not Working**
   - Verify environment variables are loaded
   - Check API key permissions and quotas
   - Test API endpoints manually

3. **File Upload Issues**
   ```bash
   # Check permissions
   sudo chown -R www-data:www-data /app/uploads
   sudo chmod -R 755 /app/uploads
   ```

4. **CORS Errors**
   - Update ALLOWED_ORIGINS in backend config
   - Verify frontend API base URL
   - Check browser network tab for errors

### Performance Optimization

1. **Database Optimization**
   - Add database indexes
   - Configure connection pooling
   - Regular VACUUM and ANALYZE

2. **File Storage**
   - Use CDN for static files
   - Implement file compression
   - Set up file cleanup jobs

3. **Caching**
   - Redis for session storage
   - API response caching
   - Static file caching

## 📞 Support

For deployment support:
1. Check logs for error messages
2. Verify all environment variables
3. Test each component individually
4. Create GitHub issue with deployment details

---

**Happy Deploying! 🚀**

