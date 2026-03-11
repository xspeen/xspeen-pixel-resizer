🖼️ XSPEEN PIXEL RESIZER API

Professional Image & GIF Resizing Service for BotFather

<p align="center">
  <img src="https://iili.io/q7Sztt9.jpg" alt="XSPEEN Pixel Resizer Logo" width="900"/>
</p>

<p align="center">
  <a href="https://github.com/xspeen/xspeen-pixel-resizer">
    <img src="https://img.shields.io/badge/GitHub-xspeen%2Fxspeen--pixel--resizer-181717?style=for-the-badge&logo=github&logoColor=white"/>
  </a>
  <a href="https://xspeen-pixel-resizer.onrender.com">
    <img src="https://img.shields.io/badge/Live%20API-xspeen--pixel--resizer.onrender.com-46E3B7?style=for-the-badge&logo=render&logoColor=white"/>
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0-royalblue?style=flat-square&logo=github"/>
  <img src="https://img.shields.io/badge/License-MIT-emerald?style=flat-square&logo=opensourceinitiative"/>
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pillow-10.1.0-FF6F00?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-2.3.3-000000?style=flat-square&logo=flask&logoColor=white"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Starting%20Up-yellow?style=flat-square"/>
  <img src="https://img.shields.io/badge/Render-Free%20Tier-46E3B7?style=flat-square"/>
  <img src="https://img.shields.io/badge/BotFather-Ready-brightgreen?style=flat-square"/>
</p>

---

📋 PROJECT OVERVIEW

XSPEEN PIXEL RESIZER is a production-ready Flask + Pillow backend service that resizes images and GIFs to exact pixel dimensions required by @BotFather for Telegram bot description pictures.

Why This Service?

· 🎯 Exact Dimensions - Perfect for BotFather requirements
· 🖼️ Image Support - JPG, PNG, WEBP, BMP
· 🎬 GIF Support - Animated GIF frame-by-frame processing
· ⚡ High Quality - 95% JPEG quality, lossless GIF optimization
· 🚀 Simple API - One endpoint does it all

---

📏 SUPPORTED DIMENSIONS

Size Type BotFather Requirement
320×180 GIF Only Bot description animation
640×360 Photos & GIFs Standard bot photo (Recommended)
960×540 Photos & GIFs Large bot photo
1280×720 Photos & GIFs HD bot photo
1920×1080 Photos & GIFs Full HD bot photo

---

🚀 QUICK START

Test the API

```bash
curl https://xspeen-pixel-resizer.onrender.com/health
```

Get Service Info

```bash
curl https://xspeen-pixel-resizer.onrender.com/info
```

Resize an Image

```bash
# First, get an image URL
curl -X POST https://xspeen-pixel-resizer.onrender.com/resize \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/image.jpg",
    "pixel_size": "640x360",
    "media_type": "image"
  }' \
  --output resized.jpg
```

---

🔧 API ENDPOINTS

1. Health Check

```bash
GET https://xspeen-pixel-resizer.onrender.com/health
```

```json
{
  "status": "healthy",
  "service": "Xspeen Pixel Resizer",
  "version": "2.0",
  "available_sizes": ["320x180", "640x360", "960x540", "1280x720", "1920x1080"]
}
```

2. Service Information

```bash
GET https://xspeen-pixel-resizer.onrender.com/info
```

```json
{
  "service": "Xspeen Pixel Resizer",
  "version": "2.0",
  "available_sizes": [
    {"name": "320x180", "description": "GIF only - Small"},
    {"name": "640x360", "description": "Photos & GIFs - Medium (Recommended)"},
    {"name": "960x540", "description": "Photos & GIFs - Large"},
    {"name": "1280x720", "description": "Photos & GIFs - HD"},
    {"name": "1920x1080", "description": "Photos & GIFs - Full HD"}
  ],
  "formats": {
    "image": ["JPEG", "PNG", "WEBP", "BMP"],
    "gif": ["Animated GIF"]
  },
  "powered_by": "Python + Pillow"
}
```

3. Resize Image/GIF

```bash
POST https://xspeen-pixel-resizer.onrender.com/resize
Content-Type: application/json

{
  "image_url": "https://example.com/image.jpg",
  "pixel_size": "640x360",
  "media_type": "image"
}
```

Parameter Description Options
image_url Public URL of the image/GIF Any accessible URL
pixel_size Target dimensions 320x180, 640x360, 960x540, 1280x720, 1920x1080
media_type Type of media image or gif

Response: Returns the resized image file directly.

---

📦 INSTALLATION & DEPLOYMENT

Clone Repository

```bash
git clone https://github.com/xspeen/xspeen-pixel-resizer.git
cd xspeen-pixel-resizer
```

Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python pixel_resizer.py
# Server will start at http://localhost:5000
```

Docker Deployment

```bash
docker build -t xspeen-pixel-resizer .
docker run -d -p 5000:5000 xspeen-pixel-resizer
```

Deploy to Render

https://render.com/images/deploy-to-render-button.svg

Render Configuration:

· Runtime: Docker
· Plan: Free
· Region: Any (auto)

---

🐍 PYTHON USAGE

```python
import requests

BASE_URL = "https://xspeen-pixel-resizer.onrender.com"

def resize_image(image_url, pixel_size="640x360", media_type="image", output="resized.jpg"):
    """Resize an image or GIF using the API"""
    
    response = requests.post(
        f"{BASE_URL}/resize",
        json={
            "image_url": image_url,
            "pixel_size": pixel_size,
            "media_type": media_type
        }
    )
    
    if response.status_code == 200:
        with open(output, "wb") as f:
            f.write(response.content)
        print(f"✅ Resized image saved to {output}")
        return True
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return False

# Example usage
resize_image(
    "https://example.com/photo.jpg",
    pixel_size="640x360",
    media_type="image",
    output="botfather_photo.jpg"
)

# Resize GIF
resize_image(
    "https://example.com/animation.gif",
    pixel_size="320x180",
    media_type="gif",
    output="botfather_animation.gif"
)
```

---

🔧 CROSS-PLATFORM USAGE

Termux 📱

```bash
pkg update && pkg upgrade -y
pkg install curl -y

# Resize image
curl -X POST https://xspeen-pixel-resizer.onrender.com/resize \
  -H "Content-Type: application/json" \
  -d '{"image_url":"https://example.com/image.jpg","pixel_size":"640x360","media_type":"image"}' \
  --output resized.jpg
```

Linux / Ubuntu / Kali / Parrot 🐧

```bash
# Install jq for JSON formatting
sudo apt install curl jq -y

# Get service info
curl -s https://xspeen-pixel-resizer.onrender.com/info | jq .

# Resize image
curl -X POST https://xspeen-pixel-resizer.onrender.com/resize \
  -H "Content-Type: application/json" \
  -d '{"image_url":"https://example.com/image.jpg","pixel_size":"640x360","media_type":"image"}' \
  --output resized.jpg
```

Windows PowerShell 🪟

```powershell
$body = @{
    image_url = "https://example.com/image.jpg"
    pixel_size = "640x360"
    media_type = "image"
} | ConvertTo-Json

curl.exe -X POST https://xspeen-pixel-resizer.onrender.com/resize `
  -H "Content-Type: application/json" `
  -d $body `
  -o resized.jpg
```

macOS 🍎

```bash
brew install curl

curl -X POST https://xspeen-pixel-resizer.onrender.com/resize \
  -H "Content-Type: application/json" \
  -d '{"image_url":"https://example.com/image.jpg","pixel_size":"640x360","media_type":"image"}' \
  --output resized.jpg
```

Arch Linux 🏹

```bash
sudo pacman -S curl jq

curl -X POST https://xspeen-pixel-resizer.onrender.com/resize \
  -H "Content-Type: application/json" \
  -d '{"image_url":"https://example.com/image.jpg","pixel_size":"640x360","media_type":"image"}' \
  --output resized.jpg
```

---

🎯 BOTFATHER INTEGRATION

Step-by-Step Guide

1. Resize your image using this API
2. Save the resized image to your device
3. Open Telegram and go to @BotFather
4. Select your bot: /mybots → Choose bot → "Edit Bot"
5. Choose option: "Edit Description Picture"
6. Upload the resized image
7. Done! Your bot now has the perfect description picture

---

📁 REPOSITORY STRUCTURE

```
📦 xspeen-pixel-resizer
├── 📄 pixel_resizer.py        # Flask application
├── 📄 requirements.txt        # Python dependencies
├── 📄 Dockerfile              # Docker configuration
├── 📄 render.yaml             # Render deployment config
├── 📄 .gitignore              # Git ignore rules
└── 📄 README.md               # This documentation
```

---

🔧 DOCKERFILE

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pixel_resizer.py .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "pixel_resizer:app"]
```

---

📦 REQUIREMENTS.TXT

```txt
Flask==2.3.3
Flask-CORS==4.0.0
Pillow==10.1.0
requests==2.31.0
gunicorn==21.2.0
```

---

⏱️ PERFORMANCE NOTES

· First request: 30-50 seconds (Render cold start)
· Subsequent requests: 1-3 seconds
· Keep alive: Use cron-job.org to ping /health every 15 minutes
· File size limit: 50MB (Render free tier limit)

---

🤝 CONTRIBUTING

1. 🍴 Fork the repository
2. 🌿 Create feature branch (git checkout -b feature/amazing)
3. 💾 Commit changes (git commit -m 'Add amazing feature')
4. 📤 Push to branch (git push origin feature/amazing)
5. ✅ Open a Pull Request

---

📜 LICENSE

```
MIT License

Copyright (c) 2026 XSPEEN

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

📞 SUPPORT & CONTACT

<p align="center">
  <a href="https://github.com/xspeen/xspeen-pixel-resizer">
    <img src="https://img.shields.io/badge/Repository-GitHub-181717?style=for-the-badge&logo=github"/>
  </a>
  <a href="https://github.com/xspeen/xspeen-pixel-resizer/issues">
    <img src="https://img.shields.io/badge/Report%20Issue-GitHub-red?style=for-the-badge&logo=github"/>
  </a>
  <a href="https://t.me/xspeen_chatter">
    <img src="https://img.shields.io/badge/Contact-Telegram-26A5E4?style=for-the-badge&logo=telegram"/>
  </a>
</p>

---

<p align="center">
  <img src="https://iili.io/q7Sztt9.jpg" width="150"/>
  <br/>
  <strong>⚡ Created by XSPEEN</strong>
  <br/>
  <a href="https://github.com/xspeen">github.com/xspeen</a>
  <br/><br/>
  <sub>📦 Repository: <a href="https://github.com/xspeen/xspeen-pixel-resizer">github.com/xspeen/xspeen-pixel-resizer</a></sub>
  <br/>
  <sub>🌐 Live API: <a href="https://xspeen-pixel-resizer.onrender.com">xspeen-pixel-resizer.onrender.com</a></sub>
  <br/><br/>
  <sub>⚠️ Note: Render free tier sleeps after 15 minutes of inactivity.</sub>
  <br/>
  <sub>First request may take 30-50 seconds to wake up.</sub>
  <br/><br/>
  <sub>© 2026 XSPEEN Pixel Resizer. All rights reserved.</sub>
</p>
