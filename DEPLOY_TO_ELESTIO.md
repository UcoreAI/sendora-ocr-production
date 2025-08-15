# Deploy to Elestio VPS - Final Steps

## 1. SSH to your Elestio server
```bash
ssh root@5.223.52.132
```

## 2. Navigate to project directory
```bash
cd /opt/app
```

## 3. Pull latest code from GitHub
```bash
git pull origin main
```

## 4. Stop existing containers
```bash
docker-compose down
```

## 5. Rebuild with latest code (no cache to ensure fresh build)
```bash
docker-compose build --no-cache
```

## 6. Start the application
```bash
docker-compose up -d
```

## 7. Check container status
```bash
docker-compose ps
docker-compose logs sendora-ocr
```

## 8. Test the application
```bash
curl -f http://localhost:5000/health
```

## 9. Access your live application
- **Live URL**: http://sendora-ocr-u40295.vm.elestio.app:5000
- **Health Check**: http://sendora-ocr-u40295.vm.elestio.app:5000/health
- **Demo Info**: http://sendora-ocr-u40295.vm.elestio.app:5000/demo-info

## Troubleshooting Commands

### View real-time logs
```bash
docker-compose logs -f sendora-ocr
```

### Check container health
```bash
docker-compose exec sendora-ocr curl -f http://localhost:5000/health
```

### Restart if needed
```bash
docker-compose restart sendora-ocr
```

### Clean rebuild if issues persist
```bash
docker-compose down
docker system prune -f
docker-compose build --no-cache
docker-compose up -d
```

## Success Indicators
- Container shows "healthy" status
- Health endpoint returns 200 OK
- Application accessible via browser
- File upload functionality working