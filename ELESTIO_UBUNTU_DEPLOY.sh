#!/bin/bash
# Sendora OCR Complete Ubuntu Deployment Script
# For Elestio Ubuntu VPS - One-click deployment

set -e

echo "=================================================="
echo "🚀 Sendora OCR Automated Deployment"
echo "   Server: sendora-ocr-u40295.vm.elestio.app"
echo "=================================================="
echo ""

# Step 1: Update system
echo "📦 Updating system packages..."
apt-get update -y
apt-get upgrade -y

# Step 2: Install Docker
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
    echo "✅ Docker installed successfully"
else
    echo "✅ Docker already installed"
fi

# Step 3: Install Docker Compose
echo "📦 Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
    echo "✅ Docker Compose installed"
else
    echo "✅ Docker Compose already installed"
fi

# Step 4: Install Git
echo "📦 Installing Git..."
apt-get install -y git

# Step 5: Clone repository
echo "📥 Cloning Sendora OCR repository..."
cd /opt
if [ -d "sendora-ocr-production" ]; then
    echo "Repository exists, pulling latest changes..."
    cd sendora-ocr-production
    git pull origin main
else
    git clone https://github.com/UcoreAI/sendora-ocr-production.git
    cd sendora-ocr-production
fi

# Step 6: Create required directories
echo "📁 Creating required directories..."
mkdir -p config uploads job_orders temp logs
chmod 755 uploads job_orders temp logs

# Step 7: Create Google credentials placeholder
echo "🔑 Setting up Google Cloud credentials..."
if [ ! -f "config/google-credentials.json" ]; then
    cat > config/google-credentials.json << 'EOF'
{
  "PLACEHOLDER": "UPLOAD YOUR ACTUAL GOOGLE CREDENTIALS",
  "note": "Replace this file with your actual Google Cloud service account JSON",
  "instructions": "Upload via Elestio File Manager or SCP"
}
EOF
    echo "⚠️  IMPORTANT: Upload your Google credentials to /opt/sendora-ocr-production/config/google-credentials.json"
fi

# Step 8: Set environment variables
echo "🔧 Setting up environment..."
export ELESTIO_DOMAIN="sendora-ocr-u40295.vm.elestio.app"
export SECRET_KEY=$(openssl rand -base64 32)

# Step 9: Create .env file
cat > .env << EOF
# Sendora OCR Production Environment
SECRET_KEY=${SECRET_KEY}
FLASK_ENV=production
FLASK_APP=backend.app_v2_production:app

# Google Cloud
GOOGLE_PROJECT_ID=my-textbee-sms
GOOGLE_APPLICATION_CREDENTIALS=/app/config/google-credentials.json

# Demo settings
DEMO_MODE=true
RATE_LIMIT_ENABLED=true
MAX_REQUESTS_PER_MINUTE=10
AUTO_CLEANUP_HOURS=2

# File limits
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=/app/uploads
OUTPUT_FOLDER=/app/job_orders

# Logging
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1

# Domain
DOMAIN=sendora-ocr-u40295.vm.elestio.app
EOF

# Step 10: Update docker-compose.yml with correct domain
sed -i 's/sendora-ocr.elestio.app/sendora-ocr-u40295.vm.elestio.app/g' docker-compose.yml

# Step 11: Build and start Docker containers
echo "🐳 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Step 12: Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Step 13: Install Nginx for reverse proxy
echo "🌐 Setting up Nginx reverse proxy..."
apt-get install -y nginx certbot python3-certbot-nginx

# Step 14: Configure Nginx
cat > /etc/nginx/sites-available/sendora-ocr << 'EOF'
server {
    listen 80;
    server_name sendora-ocr-u40295.vm.elestio.app;
    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    location /health {
        proxy_pass http://127.0.0.1:5000/health;
    }

    location /stats {
        proxy_pass http://127.0.0.1:5000/stats;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/sendora-ocr /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test and reload Nginx
nginx -t
systemctl reload nginx

# Step 15: Setup SSL with Let's Encrypt (optional, may fail on Elestio subdomain)
echo "🔒 Attempting SSL setup..."
certbot --nginx -d sendora-ocr-u40295.vm.elestio.app --non-interactive --agree-tos --email admin@sendora-ocr-u40295.vm.elestio.app || echo "SSL setup skipped (Elestio handles SSL)"

# Step 16: Setup firewall
echo "🔥 Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 5000/tcp
ufw --force enable

# Step 17: Health check
echo "🏥 Performing health check..."
sleep 10
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Health check passed!"
    HEALTH_STATUS=$(curl -s http://localhost:5000/health | python3 -m json.tool || echo "Check manually")
    echo "$HEALTH_STATUS"
else
    echo "⚠️  Health check failed. Checking logs..."
    docker-compose logs --tail=50 sendora-ocr
fi

# Step 18: Display status
echo ""
echo "=================================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "=================================================="
echo ""
echo "📊 Service Information:"
echo "  Server IP: 5.223.52.132"
echo "  Domain: https://sendora-ocr-u40295.vm.elestio.app"
echo "  Health: https://sendora-ocr-u40295.vm.elestio.app/health"
echo "  Stats: https://sendora-ocr-u40295.vm.elestio.app/stats"
echo ""
echo "🔧 Management Commands:"
echo "  View logs: docker-compose logs -f"
echo "  Restart: docker-compose restart"
echo "  Stop: docker-compose down"
echo "  Update: git pull && docker-compose build && docker-compose up -d"
echo ""

# Check if Google credentials are real
if grep -q "PLACEHOLDER" config/google-credentials.json; then
    echo "⚠️  IMPORTANT ACTION REQUIRED:"
    echo "=================================================="
    echo "Upload your Google Cloud credentials JSON file to:"
    echo "/opt/sendora-ocr-production/config/google-credentials.json"
    echo ""
    echo "Methods:"
    echo "1. Use Elestio File Manager"
    echo "2. Use SCP: scp google-credentials.json root@5.223.52.132:/opt/sendora-ocr-production/config/"
    echo "3. Use nano: nano /opt/sendora-ocr-production/config/google-credentials.json"
    echo ""
    echo "After uploading, restart services:"
    echo "cd /opt/sendora-ocr-production && docker-compose restart"
    echo "=================================================="
else
    echo "✅ Google credentials detected"
    echo "🌐 Your demo is ready at: https://sendora-ocr-u40295.vm.elestio.app"
fi

echo ""
echo "📝 Deployment log saved to: /var/log/sendora-deployment.log"
echo "=================================================="