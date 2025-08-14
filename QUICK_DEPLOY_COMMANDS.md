# 🚀 Quick Deploy Commands - Copy & Paste Ready

## Step 1: Create GitHub Repository

1. **Go to:** https://github.com/new
2. **Repository name:** `sendora-ocr-production`
3. **Description:** `Sendora OCR V2.0 - 95% accuracy automated Job Order generation`
4. **Public repository**
5. **DO NOT check "Initialize with README"**
6. **Click "Create repository"**

After creating, GitHub will show commands like:
```
…or push an existing repository from the command line

git remote add origin https://github.com/YOURUSERNAME/sendora-ocr-production.git
git branch -M main
git push -u origin main
```

**Copy those commands and replace YOURUSERNAME with your actual GitHub username**

## Step 2: Push to GitHub (Run these commands)

```bash
cd "C:\Users\USER\Desktop\Sendora-OCR-Complete-Project"

# Add your GitHub repository (REPLACE with your actual URL)
git remote add origin https://github.com/YOURUSERNAME/sendora-ocr-production.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Create Elestio Service

1. **Go to:** https://elestio.com/register
2. **Sign up** with your email
3. **Verify email** and add payment method
4. **Click "Create New Service"**
5. **Select "Docker"**
6. **Configure:**
   - Service Name: `sendora-ocr-demo`
   - Plan: **Standard (2GB RAM, 2 CPU)** - $14/month
   - Region: Choose closest to you
   - Click "Create Service"

7. **After creation, note down:**
   - Service Domain: (e.g., `sendora-ocr-u123.vm.elestio.app`)
   - Admin credentials from dashboard

## Step 4: Deploy to Elestio (SSH Commands)

### Connect to your VPS:
```bash
# Use the SSH details from Elestio dashboard
ssh root@YOUR-SERVICE-IP
# Enter password from Elestio dashboard
```

### Clone and setup:
```bash
# Clone your repository
cd /opt
git clone https://github.com/YOURUSERNAME/sendora-ocr-production.git
cd sendora-ocr-production

# Create directories
mkdir -p config uploads job_orders temp logs
chmod 755 uploads job_orders temp logs
```

### Upload Google Credentials:
**Option A: Use Elestio File Manager**
1. Go to Elestio dashboard → Your service → File Manager
2. Navigate to `/opt/sendora-ocr-production/config/`
3. Upload your `google-credentials.json` file

**Option B: Copy-paste via nano**
```bash
cd /opt/sendora-ocr-production/config
nano google-credentials.json
# Paste your Google credentials JSON content
# Press Ctrl+X, then Y, then Enter to save
```

### Deploy the application:
```bash
# Make deploy script executable
chmod +x deploy.sh

# Set your domain (REPLACE with your actual Elestio domain)
export ELESTIO_DOMAIN="sendora-ocr-u123.vm.elestio.app"

# Deploy
./deploy.sh
```

## Step 5: Verify Deployment

### Check if it's working:
```bash
# Check running containers
docker-compose ps

# Check health
curl http://localhost:5000/health

# Check logs
docker-compose logs -f sendora-ocr
```

### Test in browser:
Visit: `https://YOUR-ELESTIO-DOMAIN.vm.elestio.app`

You should see the professional Sendora OCR demo page!

## Step 6: Test Upload

1. **Upload a sample invoice PDF/JPG**
2. **Verify it processes and shows:**
   - Door size in MM format (e.g., "915MM x 2440MM")
   - Proper customer extraction
   - Job Order generation works

## Emergency Troubleshooting

### If health check fails:
```bash
docker-compose logs sendora-ocr
# Look for errors and fix
```

### If Google AI doesn't work:
```bash
# Verify credentials file
cat config/google-credentials.json | head -5
# Should show valid JSON
```

### Restart services:
```bash
docker-compose restart
```

## Success Confirmation

✅ **Your demo is live when:**
- Health check returns: `{"status": "healthy", "version": "2.0", "ocr_accuracy": "95%"}`
- Demo page loads with professional UI
- File upload works end-to-end
- PDF download works
- Statistics page shows data: `/stats`

**Share your live URL:** `https://your-domain.vm.elestio.app`