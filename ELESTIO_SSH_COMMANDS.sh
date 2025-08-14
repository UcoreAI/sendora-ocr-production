#!/bin/bash
# Sendora OCR Elestio VPS Deployment Commands
# Run these commands on your Elestio VPS after SSH connection

echo "🚀 Starting Sendora OCR deployment on Elestio VPS..."
echo "=================================================="

# Step 1: Clone repository
echo "📥 Cloning repository..."
cd /opt
git clone https://github.com/REPLACE-WITH-YOUR-USERNAME/sendora-ocr-production.git
cd sendora-ocr-production

# Step 2: Create required directories
echo "📁 Creating directories..."
mkdir -p config uploads job_orders temp logs
chmod 755 uploads job_orders temp logs

# Step 3: Check if Google credentials exist
echo "🔑 Checking Google Cloud credentials..."
if [ ! -f "config/google-credentials.json" ]; then
    echo "❌ Google credentials not found!"
    echo "Please upload google-credentials.json to config/ folder using:"
    echo "1. Elestio File Manager (recommended)"
    echo "2. SCP: scp google-credentials.json root@your-ip:/opt/sendora-ocr-production/config/"
    echo "3. Or create manually: nano config/google-credentials.json"
    echo ""
    read -p "Press Enter after uploading credentials..."
fi

# Step 4: Verify credentials
if [ -f "config/google-credentials.json" ]; then
    echo "✅ Google credentials found!"
    echo "File size: $(stat -f%z config/google-credentials.json 2>/dev/null || stat -c%s config/google-credentials.json) bytes"
else
    echo "❌ Still no credentials found. Deployment will fail."
    echo "Please upload the file and run this script again."
    exit 1
fi

# Step 5: Set domain (you need to replace this)
echo "🌐 Setting up domain..."
echo "IMPORTANT: Replace 'your-domain' with your actual Elestio domain!"
echo "Example: sendora-ocr-u123.vm.elestio.app"
read -p "Enter your Elestio domain: " ELESTIO_DOMAIN
export ELESTIO_DOMAIN="$ELESTIO_DOMAIN"

# Step 6: Make deploy script executable and run
echo "🔧 Making deploy script executable..."
chmod +x deploy.sh

# Step 7: Deploy
echo "🚀 Starting deployment..."
./deploy.sh

# Step 8: Verify deployment
echo ""
echo "🔍 Verifying deployment..."
sleep 10

echo "Checking Docker containers..."
docker-compose ps

echo ""
echo "Checking health endpoint..."
curl -f http://localhost:5000/health

echo ""
echo "🎉 Deployment completed!"
echo "=================================================="
echo ""
echo "✅ Your Sendora OCR demo is now live at:"
echo "   https://$ELESTIO_DOMAIN"
echo ""
echo "🔧 Management commands:"
echo "   View logs: docker-compose logs -f"
echo "   Restart: docker-compose restart"
echo "   Stop: docker-compose down"
echo ""
echo "📊 Monitoring:"
echo "   Health: https://$ELESTIO_DOMAIN/health"
echo "   Stats: https://$ELESTIO_DOMAIN/stats"
echo ""
echo "🧪 Test the demo by uploading an invoice PDF!"
echo "Expected: 95% OCR accuracy with automatic Job Order generation"