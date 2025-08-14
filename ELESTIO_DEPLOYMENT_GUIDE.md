# 🚀 Sendora OCR - Complete Elestio Deployment Guide

## Step-by-Step Live Deployment Instructions

### Prerequisites
- GitHub account
- Elestio account (create at https://elestio.com)
- Google Cloud Project with Document AI enabled
- Google Service Account JSON file

---

## 📋 Step 1: Create GitHub Repository

1. **Go to GitHub.com** and sign in
2. **Click "New Repository"** 
3. **Repository Settings:**
   - Repository name: `sendora-ocr-production`
   - Description: `Sendora OCR V2.0 - 95% accuracy automated Job Order generation`
   - Public repository (for Elestio access)
   - **DO NOT** initialize with README (we have our code ready)

4. **Copy the repository URL** (e.g., `https://github.com/yourusername/sendora-ocr-production.git`)

5. **Push your code:**
```bash
cd "C:\\Users\\USER\\Desktop\\Sendora-OCR-Complete-Project"
git remote add origin https://github.com/yourusername/sendora-ocr-production.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 2: Set Up Elestio Account & Service

### 2.1 Create Elestio Account
1. Go to https://elestio.com
2. Sign up with email
3. Verify your email address
4. Add payment method (they offer free credits for new users)

### 2.2 Create New Service
1. **Click "Create New Service"**
2. **Select "Docker"** from the service catalog
3. **Configuration:**
   - **Service Name:** `sendora-ocr-demo`
   - **Plan:** Choose based on expected load
     - **Starter (1GB RAM, 1 CPU):** $7/month - Good for testing
     - **Standard (2GB RAM, 2 CPU):** $14/month - Recommended for demo
     - **Pro (4GB RAM, 4 CPU):** $28/month - Production ready
   - **Region:** Choose closest to your users
   - **Support Level:** Standard (free)

4. **Advanced Settings:**
   - **Auto-restart:** Enabled
   - **Automatic updates:** Enabled
   - **Backup:** Daily (recommended)

5. **Click "Create Service"**

### 2.3 Get Service Information
After service creation, note down:
- **Service Domain:** (e.g., `sendora-ocr-u123.vm.elestio.app`)
- **Admin Username:** (provided by Elestio)
- **Admin Password:** (provided by Elestio)
- **SSH Access:** Available in service dashboard

---

## 🔧 Step 3: Configure Elestio Service

### 3.1 Access Your VPS
1. **SSH Access:** Use Elestio's web terminal or:
```bash
ssh root@your-service-ip
```
Password: Use the admin password from Elestio dashboard

### 3.2 Clone Your Repository
```bash
cd /opt
git clone https://github.com/yourusername/sendora-ocr-production.git
cd sendora-ocr-production
```

### 3.3 Create Required Directories
```bash
mkdir -p config uploads job_orders temp logs
chmod 755 uploads job_orders temp logs
```

---

## 🔑 Step 4: Configure Google Cloud Credentials

### 4.1 Prepare Google Cloud Service Account
1. **Go to Google Cloud Console:** https://console.cloud.google.com
2. **Select your project:** `my-textbee-sms` (or your project)
3. **Navigate to:** IAM & Admin → Service Accounts
4. **Find your service account** (the one with Document AI permissions)
5. **Click "Actions" → "Create Key"**
6. **Select JSON** and download

### 4.2 Upload Credentials to VPS
**Option A: Using Elestio File Manager**
1. Open Elestio dashboard
2. Go to your service
3. Click "File Manager" 
4. Navigate to `/opt/sendora-ocr-production/config/`
5. Upload your `google-credentials.json` file

**Option B: Using SCP (from your computer)**
```bash
scp path/to/your/google-credentials.json root@your-service-ip:/opt/sendora-ocr-production/config/
```

**Option C: Using nano (copy/paste)**
```bash
cd /opt/sendora-ocr-production/config
nano google-credentials.json
# Paste your JSON content and save (Ctrl+X, Y, Enter)
```

### 4.3 Verify Credentials
```bash
cd /opt/sendora-ocr-production
ls -la config/google-credentials.json
# Should show the file with proper size (not empty)
```

---

## 🚀 Step 5: Deploy to Elestio

### 5.1 Make Deploy Script Executable
```bash
cd /opt/sendora-ocr-production
chmod +x deploy.sh
```

### 5.2 Set Environment Variables
```bash
export ELESTIO_DOMAIN="your-service-domain.vm.elestio.app"
export SECRET_KEY=$(openssl rand -base64 32)
```

### 5.3 Run Deployment
```bash
./deploy.sh
```

**Expected Output:**
```
🚀 Sendora OCR VPS Deployment Starting...
==========================================
[INFO] Starting pre-deployment checks...
[SUCCESS] Docker is installed
[SUCCESS] Docker Compose is available
[SUCCESS] All required files present
[SUCCESS] Google Cloud credentials found
[INFO] Setting up environment...
[SUCCESS] Environment file created
[INFO] Creating required directories...
[SUCCESS] Directories created
[INFO] Building Docker image...
[SUCCESS] Docker image built successfully
[INFO] Starting services...
[SUCCESS] Services started
[INFO] Waiting for services to be ready...
[INFO] Performing health check...
[SUCCESS] Health check passed
[SUCCESS] 🎉 Deployment Successful!
```

### 5.4 Verify Deployment
```bash
# Check running containers
docker-compose ps

# Check logs
docker-compose logs -f sendora-ocr

# Test health endpoint
curl http://localhost:5000/health
```

---

## 🌐 Step 6: Configure Domain & SSL (Automatic with Elestio)

### 6.1 Domain Configuration
Elestio automatically provides:
- **Domain:** `your-service.vm.elestio.app`
- **SSL Certificate:** Let's Encrypt (automatic)
- **Load Balancing:** Built-in
- **CDN:** Available

### 6.2 Custom Domain (Optional)
1. **In Elestio Dashboard:**
   - Go to your service
   - Click "Domains" tab
   - Add your custom domain
   - Update DNS records as shown

---

## 🧪 Step 7: Test Live Deployment

### 7.1 Access Your Demo
1. **Open browser:** `https://your-service.vm.elestio.app`
2. **You should see:** Professional Sendora OCR demo page
3. **Features to test:**
   - File upload (PDF/JPG/PNG)
   - OCR processing with 95% accuracy
   - Job Order generation
   - PDF download

### 7.2 Test with Sample Invoice
1. **Upload a test invoice PDF**
2. **Verify extraction accuracy:**
   - Door size: Should show MM format (e.g., "915MM x 2440MM")
   - Customer details: Properly extracted
   - Specifications: Checkboxes correctly selected

### 7.3 Monitor Performance
```bash
# Check service stats
curl https://your-service.vm.elestio.app/stats

# Check health
curl https://your-service.vm.elestio.app/health

# Monitor logs
docker-compose logs -f --tail=50
```

---

## 📊 Step 8: Production Monitoring

### 8.1 Elestio Built-in Monitoring
- **CPU/RAM Usage:** Available in dashboard
- **Uptime Monitoring:** Automatic
- **SSL Certificate:** Auto-renewal
- **Backups:** Scheduled daily

### 8.2 Application Monitoring
- **Health Check:** `https://your-domain/health`
- **Statistics:** `https://your-domain/stats`
- **Log Monitoring:** Available via SSH

---

## 🔒 Security & Maintenance

### 8.1 Security Features (Already Configured)
- ✅ Rate limiting (10 requests/minute)
- ✅ File type validation
- ✅ Automatic cleanup (2-hour retention)
- ✅ SSL/TLS encryption
- ✅ Input sanitization
- ✅ Docker security best practices

### 8.2 Maintenance Tasks
```bash
# Update application
cd /opt/sendora-ocr-production
git pull origin main
docker-compose build --no-cache
docker-compose up -d

# View logs
docker-compose logs -f

# Clean up old images
docker system prune -f
```

---

## 🎯 Success Checklist

- [ ] GitHub repository created and code pushed
- [ ] Elestio service created and configured
- [ ] Google Cloud credentials uploaded
- [ ] Deployment script executed successfully  
- [ ] Health check passes (`/health` returns 200)
- [ ] Demo page loads (`/` shows professional interface)
- [ ] File upload works with sample invoice
- [ ] OCR processing completes successfully
- [ ] Job Order PDF generates and downloads
- [ ] Statistics endpoint works (`/stats`)
- [ ] SSL certificate active (https://)
- [ ] Rate limiting functional
- [ ] Auto-cleanup working

---

## 📞 Support & Troubleshooting

### Common Issues:
1. **Health Check Fails:**
   ```bash
   docker-compose logs sendora-ocr
   # Check for Google credentials or wkhtmltopdf issues
   ```

2. **OCR Processing Errors:**
   ```bash
   # Verify credentials
   cat config/google-credentials.json | jq .
   ```

3. **File Upload Issues:**
   ```bash
   # Check file permissions
   ls -la uploads/ job_orders/
   ```

### Get Help:
- **Elestio Support:** Available 24/7 via dashboard
- **GitHub Issues:** For application-specific problems
- **Google Cloud Support:** For Document AI issues

---

## 🎉 Congratulations!

Your Sendora OCR system is now live and ready for public testing at:
**https://your-service.vm.elestio.app**

**Key Achievements:**
- ✅ 95% OCR accuracy upgrade (from 70% Azure)
- ✅ Professional public demo interface
- ✅ Production-grade security and monitoring
- ✅ Automatic scaling and SSL
- ✅ Complete documentation and replication ability

**Share your demo URL with stakeholders for testing!**