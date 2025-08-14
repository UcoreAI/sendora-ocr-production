# 🚀 Sendora OCR VPS Deployment Plan

## 🎯 Objective: Deploy Sendora OCR on Elestio VPS for Public Testing

**Goal**: Make the 95% accuracy OCR system accessible online for testing by stakeholders, clients, and team members without requiring local installation.

---

## 📊 Deployment Strategy Overview

### 🏗️ **Architecture Choice: Dockerized Flask Application**
- **Platform**: Elestio VPS (Docker-based cloud hosting)
- **Container Strategy**: Multi-stage Docker build
- **Web Server**: Gunicorn + Nginx (production-ready)
- **Storage**: Persistent volumes for uploads and outputs
- **Security**: Environment variables, secure file handling

### 🌐 **Access Model: Demo/Testing Platform**
- **URL**: `https://sendora-ocr.elestio.app` (example)
- **Authentication**: Simple access control for testing
- **Usage Limits**: Rate limiting and file size controls
- **Monitoring**: Basic usage analytics and health checks

---

## 🐳 Phase 1: Dockerization Strategy

### **Multi-Stage Dockerfile Architecture**

#### **Stage 1: Base Python Environment**
```dockerfile
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    xvfb \
    fonts-liberation \
    libjpeg-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app user (security)
RUN useradd --create-home --shell /bin/bash app
WORKDIR /app
USER app
```

#### **Stage 2: Dependencies Installation**
```dockerfile
FROM base as dependencies

# Copy requirements first (Docker layer caching)
COPY requirements_v2.txt .
RUN pip install --user --no-cache-dir -r requirements_v2.txt
```

#### **Stage 3: Application Assembly**
```dockerfile
FROM dependencies as application

# Copy application code
COPY --chown=app:app backend/ backend/
COPY --chown=app:app frontend/ frontend/
COPY --chown=app:app config/ config/
COPY --chown=app:app *.py ./

# Create required directories
RUN mkdir -p uploads job_orders job_orders/pdf temp

# Environment variables
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PATH=/home/app/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expose port
EXPOSE 5000

# Production startup command
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "backend.app_v2:app"]
```

---

## 🔧 Phase 2: Production Configuration

### **Production Flask Configuration**
```python
# config/production.py
import os

class ProductionConfig:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # File handling
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = '/app/uploads'
    OUTPUT_FOLDER = '/app/job_orders'
    
    # Google Cloud
    GOOGLE_APPLICATION_CREDENTIALS = '/app/config/google-credentials.json'
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_DEFAULT = "10 per minute"
    
    # Logging
    LOG_LEVEL = 'INFO'
    
    # Demo mode settings
    DEMO_MODE = True
    MAX_FILES_PER_SESSION = 5
    CLEANUP_INTERVAL = 3600  # 1 hour
```

### **Enhanced Flask Application (app_v2_production.py)**
```python
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import os

# Production Flask app
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.production.ProductionConfig')
    
    # Rate limiting
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["100 per hour", "10 per minute"]
    )
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'version': '2.0',
            'ocr_accuracy': '95%'
        })
    
    # Demo info endpoint
    @app.route('/demo-info')
    def demo_info():
        return jsonify({
            'title': 'Sendora OCR Demo',
            'description': '95% accuracy OCR for Job Order generation',
            'features': [
                'Google Document AI integration',
                'Feet-to-MM conversion',
                'Professional template generation',
                'Human-in-the-loop validation'
            ],
            'limits': {
                'max_file_size': '16MB',
                'max_files_per_hour': '10',
                'supported_formats': ['PDF', 'JPG', 'PNG']
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
```

---

## 🌐 Phase 3: Elestio Deployment Configuration

### **Elestio Docker Compose (docker-compose.yml)**
```yaml
version: '3.8'

services:
  sendora-ocr:
    build: .
    container_name: sendora-ocr-app
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - GOOGLE_APPLICATION_CREDENTIALS=/app/config/google-credentials.json
    volumes:
      - ./uploads:/app/uploads
      - ./job_orders:/app/job_orders
      - ./config/google-credentials.json:/app/config/google-credentials.json:ro
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.sendora-ocr.rule=Host(\`sendora-ocr.elestio.app\`)"
      - "traefik.http.routers.sendora-ocr.tls=true"
      - "traefik.http.routers.sendora-ocr.tls.certresolver=letsencrypt"

  nginx:
    image: nginx:alpine
    container_name: sendora-ocr-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - sendora-ocr
    labels:
      - "traefik.enable=false"
```

### **Nginx Configuration (nginx.conf)**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream sendora_app {
        server sendora-ocr:5000;
    }
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=upload:10m rate=5r/m;
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/m;
    
    server {
        listen 80;
        server_name sendora-ocr.elestio.app;
        client_max_body_size 20M;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
        
        # API endpoints with rate limiting
        location /upload {
            limit_req zone=upload burst=2 nodelay;
            proxy_pass http://sendora_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_read_timeout 300s;
        }
        
        location /api/ {
            limit_req zone=api burst=10 nodelay;
            proxy_pass http://sendora_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        
        # Static files and general routing
        location / {
            proxy_pass http://sendora_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        
        # Health check (no rate limiting)
        location /health {
            proxy_pass http://sendora_app;
        }
    }
}
```

---

## 🔒 Phase 4: Security & Access Control

### **Environment Variables (.env)**
```bash
# Security
SECRET_KEY=your-super-secret-key-here-change-in-production
FLASK_ENV=production

# Google Cloud
GOOGLE_PROJECT_ID=my-textbee-sms
GOOGLE_APPLICATION_CREDENTIALS=/app/config/google-credentials.json

# Rate Limiting
RATE_LIMIT_ENABLED=true
MAX_REQUESTS_PER_MINUTE=10
MAX_FILES_PER_HOUR=20

# Demo Settings
DEMO_MODE=true
AUTO_CLEANUP_HOURS=2
MAX_FILE_SIZE=16777216

# Monitoring
ENABLE_ANALYTICS=true
LOG_LEVEL=INFO
```

### **Security Enhancements**

#### **File Upload Security**
```python
# Enhanced file validation
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def secure_filename_validation(filename):
    """Enhanced filename security"""
    if not filename or '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False
    
    # Check for malicious patterns
    dangerous_patterns = ['../', '..\\', '<script', '<?php']
    if any(pattern in filename.lower() for pattern in dangerous_patterns):
        return False
    
    return True
```

#### **Demo Mode Restrictions**
```python
class DemoModeMiddleware:
    def __init__(self, app):
        self.app = app
        
    def __call__(self, environ, start_response):
        # Add demo mode headers
        def new_start_response(status, response_headers):
            response_headers.extend([
                ('X-Demo-Mode', 'true'),
                ('X-Rate-Limited', 'true'),
                ('X-Max-File-Size', '16MB')
            ])
            return start_response(status, response_headers)
        
        return self.app(environ, new_start_response)
```

---

## 📱 Phase 5: Frontend Enhancements for Online Demo

### **Demo Landing Page (frontend/demo.html)**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sendora OCR Demo - 95% Accuracy</title>
    <style>
        .demo-banner {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        .feature-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1.5rem;
            text-align: center;
        }
        .accuracy-badge {
            background: #28a745;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin: 1rem 0;
        }
        .demo-limits {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
    </style>
</head>
<body>
    <div class="demo-banner">
        <h1>🚀 Sendora OCR Demo</h1>
        <div class="accuracy-badge">95% OCR Accuracy</div>
        <p>Automated Job Order Generation from Invoice PDFs</p>
    </div>
    
    <div class="container">
        <div class="demo-limits">
            <h3>🎯 Demo Limits</h3>
            <ul>
                <li>Maximum file size: 16MB</li>
                <li>Supported formats: PDF, JPG, PNG</li>
                <li>Rate limit: 10 files per hour</li>
                <li>Files auto-deleted after 2 hours</li>
            </ul>
        </div>
        
        <div class="feature-grid">
            <div class="feature-card">
                <h3>🤖 Google Document AI</h3>
                <p>95% accuracy OCR processing with intelligent pattern recognition</p>
            </div>
            <div class="feature-card">
                <h3>📐 Smart Conversion</h3>
                <p>Automatic feet-to-MM conversion (3FT × 8FT → 915MM × 2440MM)</p>
            </div>
            <div class="feature-card">
                <h3>✅ Checkbox Logic</h3>
                <p>Intelligent checkbox selection based on extracted specifications</p>
            </div>
            <div class="feature-card">
                <h3>📋 Professional Templates</h3>
                <p>Two-page Job Order generation with company branding</p>
            </div>
        </div>
        
        <!-- Original upload form -->
        <div id="upload-section">
            <!-- Include existing upload form here -->
        </div>
    </div>
</body>
</html>
```

### **Real-time Progress Tracking**
```javascript
// frontend/js/demo-progress.js
class DemoProgressTracker {
    constructor() {
        this.socket = null;
        this.setupWebSocket();
    }
    
    setupWebSocket() {
        // Real-time processing updates
        this.socket = new WebSocket('wss://sendora-ocr.elestio.app/ws');
        
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.updateProgress(data);
        };
    }
    
    updateProgress(data) {
        const progressBar = document.getElementById('progress-bar');
        const statusText = document.getElementById('status-text');
        
        switch(data.stage) {
            case 'upload_complete':
                statusText.textContent = 'File uploaded successfully...';
                progressBar.style.width = '20%';
                break;
            case 'ocr_processing':
                statusText.textContent = 'Processing with Google Document AI...';
                progressBar.style.width = '50%';
                break;
            case 'template_generation':
                statusText.textContent = 'Generating Job Order template...';
                progressBar.style.width = '80%';
                break;
            case 'complete':
                statusText.textContent = 'Job Order generated successfully!';
                progressBar.style.width = '100%';
                this.showResults(data.result_url);
                break;
        }
    }
    
    showResults(url) {
        window.location.href = url;
    }
}
```

---

## 📊 Phase 6: Monitoring & Analytics

### **Basic Analytics Dashboard**
```python
# analytics.py
from flask import Blueprint, jsonify, render_template
from datetime import datetime, timedelta
import json
import os

analytics_bp = Blueprint('analytics', __name__)

class AnalyticsTracker:
    def __init__(self):
        self.stats_file = 'logs/analytics.json'
        self.ensure_stats_file()
    
    def track_upload(self, file_size, file_type, processing_time):
        stats = self.load_stats()
        
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in stats['daily']:
            stats['daily'][today] = {
                'uploads': 0,
                'total_size': 0,
                'avg_processing_time': 0,
                'file_types': {}
            }
        
        # Update statistics
        stats['daily'][today]['uploads'] += 1
        stats['daily'][today]['total_size'] += file_size
        stats['daily'][today]['file_types'][file_type] = stats['daily'][today]['file_types'].get(file_type, 0) + 1
        
        # Update totals
        stats['totals']['uploads'] += 1
        stats['totals']['total_processing_time'] += processing_time
        
        self.save_stats(stats)

@analytics_bp.route('/analytics')
def analytics_dashboard():
    """Simple analytics dashboard for demo"""
    tracker = AnalyticsTracker()
    stats = tracker.load_stats()
    
    return render_template('analytics.html', stats=stats)

@analytics_bp.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    tracker = AnalyticsTracker()
    stats = tracker.load_stats()
    
    return jsonify({
        'total_uploads': stats['totals']['uploads'],
        'average_processing_time': stats['totals']['avg_processing_time'],
        'daily_uploads': stats['daily']
    })
```

### **Health Monitoring**
```python
# health_monitor.py
import psutil
import os
from datetime import datetime

class HealthMonitor:
    @staticmethod
    def get_system_health():
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'active_processes': len(psutil.pids()),
            'uptime_seconds': psutil.boot_time(),
            'google_api_status': HealthMonitor.check_google_api(),
            'wkhtmltopdf_status': HealthMonitor.check_wkhtmltopdf()
        }
    
    @staticmethod
    def check_google_api():
        try:
            from backend.google_document_ai import GoogleDocumentProcessor
            processor = GoogleDocumentProcessor()
            return processor.client is not None
        except:
            return False
    
    @staticmethod
    def check_wkhtmltopdf():
        return os.path.exists('/usr/bin/wkhtmltopdf')
```

---

## 🚀 Phase 7: Deployment Scripts

### **Elestio Deployment Script (deploy.sh)**
```bash
#!/bin/bash
set -e

echo "🚀 Deploying Sendora OCR to Elestio VPS..."

# Environment setup
export FLASK_ENV=production
export SECRET_KEY=$(openssl rand -base64 32)

# Build and deploy
echo "📦 Building Docker image..."
docker build -t sendora-ocr:latest .

echo "🔧 Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to be healthy..."
sleep 30

# Health check
echo "🏥 Checking service health..."
curl -f http://localhost:5000/health || {
    echo "❌ Health check failed!"
    docker-compose logs
    exit 1
}

echo "✅ Deployment successful!"
echo "🌐 Access your demo at: https://sendora-ocr.elestio.app"
echo "📊 View analytics at: https://sendora-ocr.elestio.app/analytics"
```

### **Environment Configuration Script**
```bash
#!/bin/bash
# setup_environment.sh

echo "⚙️ Setting up Elestio environment..."

# Create necessary directories
mkdir -p uploads job_orders job_orders/pdf temp logs config

# Set permissions
chmod 755 uploads job_orders temp
chmod 600 config/google-credentials.json

# Generate secure secret key
SECRET_KEY=$(openssl rand -base64 32)
echo "SECRET_KEY=$SECRET_KEY" > .env

# Configure log rotation
cat > /etc/logrotate.d/sendora-ocr << EOF
/app/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 app app
}
EOF

echo "✅ Environment setup complete!"
```

---

## 💰 Phase 8: Cost Management & Resource Planning

### **Elestio Resource Requirements**
```yaml
# Recommended VPS Configuration
VPS_SPECS:
  CPU: 2 vCPUs (minimum)
  RAM: 4GB (recommended 8GB)
  Storage: 50GB SSD
  Bandwidth: 1TB/month
  Estimated Cost: $25-40/month

# Google Cloud API Costs
GOOGLE_DOCUMENT_AI:
  Document Processing: $0.50 per 1,000 pages
  Monthly Budget Estimate: $50-100 (for demo usage)
  Rate Limits: 600 requests per minute
```

### **Cost Optimization Strategies**
```python
# Cost monitoring and alerts
class CostMonitor:
    def __init__(self):
        self.daily_budget = 5.0  # $5 per day
        self.monthly_budget = 100.0  # $100 per month
    
    def track_api_usage(self, api_calls, cost_per_call):
        daily_cost = api_calls * cost_per_call
        
        if daily_cost > self.daily_budget:
            self.send_alert(f"Daily budget exceeded: ${daily_cost:.2f}")
    
    def implement_usage_limits(self):
        # Implement progressive limits
        return {
            'free_tier': {'calls_per_hour': 10, 'max_file_size': '16MB'},
            'rate_limited': {'calls_per_hour': 5, 'max_file_size': '8MB'},
            'suspended': {'calls_per_hour': 0}
        }
```

---

## 📋 Phase 9: Testing & Validation Plan

### **Pre-Deployment Testing Checklist**
- [ ] ✅ Docker container builds successfully
- [ ] ✅ All dependencies install correctly
- [ ] ✅ Google Document AI connection works
- [ ] ✅ wkhtmltopdf generates PDFs
- [ ] ✅ File upload and processing pipeline works
- [ ] ✅ Rate limiting functions correctly
- [ ] ✅ Health checks return positive status
- [ ] ✅ Demo UI loads and functions
- [ ] ✅ SSL certificate configured
- [ ] ✅ Analytics tracking works

### **Load Testing Strategy**
```bash
# Load testing with Apache Bench
ab -n 100 -c 10 -T 'multipart/form-data' https://sendora-ocr.elestio.app/upload

# Monitor resource usage during testing
docker stats sendora-ocr-app

# Test rate limiting
for i in {1..20}; do
  curl -X POST https://sendora-ocr.elestio.app/upload
  sleep 1
done
```

---

## 🎯 Final Deployment Timeline

### **Week 1: Preparation**
- [ ] Create Dockerfiles and configurations
- [ ] Set up Google Cloud credentials for production
- [ ] Test Docker builds locally
- [ ] Create demo frontend enhancements

### **Week 2: VPS Setup** 
- [ ] Set up Elestio VPS account
- [ ] Configure domain and SSL
- [ ] Deploy initial version
- [ ] Configure monitoring and alerts

### **Week 3: Testing & Optimization**
- [ ] Conduct load testing
- [ ] Optimize performance
- [ ] Implement security hardening
- [ ] Set up automated backups

### **Week 4: Go Live**
- [ ] Final production deployment
- [ ] Share demo URL with stakeholders
- [ ] Monitor usage and performance
- [ ] Gather feedback for improvements

---

**🎯 Expected Outcome: A fully functional online demo at `https://sendora-ocr.elestio.app` showcasing 95% OCR accuracy with professional Job Order generation, accessible to anyone for testing and evaluation.**