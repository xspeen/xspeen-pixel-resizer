import os
import io
import logging
from PIL import Image, ImageSequence
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tempfile
import requests
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Pixel options - BotFather exact requirements
PIXEL_OPTIONS = {
    "320x180": (320, 180),
    "640x360": (640, 360),
    "960x540": (960, 540),
    "1280x720": (1280, 720),
    "1920x1080": (1920, 1080)
}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Xspeen Pixel Resizer",
        "version": "2.0",
        "available_sizes": list(PIXEL_OPTIONS.keys())
    })

@app.route('/resize', methods=['POST'])
def resize_image():
    """Resize image or GIF to exact dimensions"""
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] Processing resize request")
    
    try:
        # Get parameters
        data = request.json
        if not data:
            logger.error(f"[{request_id}] No JSON data provided")
            return jsonify({"error": "No JSON data provided"}), 400
        
        image_url = data.get('image_url')
        pixel_size = data.get('pixel_size', '640x360')
        media_type = data.get('media_type', 'image')
        
        logger.info(f"[{request_id}] URL: {image_url}, Size: {pixel_size}, Type: {media_type}")
        
        if not image_url:
            return jsonify({"error": "No image_url provided"}), 400
        
        if pixel_size not in PIXEL_OPTIONS:
            return jsonify({"error": f"Invalid pixel size. Choose from: {list(PIXEL_OPTIONS.keys())}"}), 400
        
        target_size = PIXEL_OPTIONS[pixel_size]
        
        # Download image from URL
        logger.info(f"[{request_id}] Downloading image...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(image_url, timeout=30, headers=headers)
        if response.status_code != 200:
            logger.error(f"[{request_id}] Failed to download image: {response.status_code}")
            return jsonify({"error": "Failed to download image"}), 400
        
        image_bytes = response.content
        logger.info(f"[{request_id}] Downloaded {len(image_bytes)} bytes")
        
        if media_type == 'image':
            # Process static image
            logger.info(f"[{request_id}] Processing static image...")
            
            with Image.open(io.BytesIO(image_bytes)) as img:
                # Log original size
                logger.info(f"[{request_id}] Original size: {img.size}")
                
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    bg = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    bg.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = bg
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Calculate resize to maintain aspect ratio
                img.thumbnail(target_size, Image.Resampling.LANCZOS)
                logger.info(f"[{request_id}] After thumbnail: {img.size}")
                
                # Create new image with exact size
                new_img = Image.new('RGB', target_size, (255, 255, 255))
                paste_x = (target_size[0] - img.size[0]) // 2
                paste_y = (target_size[1] - img.size[1]) // 2
                new_img.paste(img, (paste_x, paste_y))
                logger.info(f"[{request_id}] Final size: {new_img.size}")
                
                # Save to bytes
                output = io.BytesIO()
                new_img.save(output, format='JPEG', quality=95, optimize=True)
                output.seek(0)
                
                logger.info(f"[{request_id}] Resize complete, size: {output.getbuffer().nbytes} bytes")
                
                # Return resized image
                return send_file(
                    output,
                    mimetype='image/jpeg',
                    as_attachment=True,
                    download_name=f'xspeen_{pixel_size}.jpg'
                )
        
        elif media_type == 'gif':
            # Process GIF
            logger.info(f"[{request_id}] Processing GIF...")
            
            with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as tmp_input:
                tmp_input.write(image_bytes)
                tmp_input_path = tmp_input.name
            
            tmp_output_path = tempfile.mktemp(suffix='.gif')
            
            try:
                with Image.open(tmp_input_path) as img:
                    frames = []
                    durations = []
                    
                    # Get total frames
                    total_frames = 0
                    for frame in ImageSequence.Iterator(img):
                        total_frames += 1
                    
                    logger.info(f"[{request_id}] Processing {total_frames} frames...")
                    
                    for i, frame in enumerate(ImageSequence.Iterator(img)):
                        if i % 10 == 0:
                            logger.info(f"[{request_id}] Processing frame {i}/{total_frames}")
                        
                        # Convert frame to RGB
                        if frame.mode in ('RGBA', 'LA', 'P'):
                            bg = Image.new('RGB', frame.size, (255, 255, 255))
                            if frame.mode == 'P':
                                frame = frame.convert('RGBA')
                            bg.paste(frame, mask=frame.split()[-1] if frame.mode == 'RGBA' else None)
                            frame = bg
                        elif frame.mode != 'RGB':
                            frame = frame.convert('RGB')
                        
                        # Resize frame
                        frame.thumbnail(target_size, Image.Resampling.LANCZOS)
                        
                        # Create new frame with exact size
                        new_frame = Image.new('RGB', target_size, (255, 255, 255))
                        paste_x = (target_size[0] - frame.size[0]) // 2
                        paste_y = (target_size[1] - frame.size[1]) // 2
                        new_frame.paste(frame, (paste_x, paste_y))
                        
                        frames.append(new_frame)
                        durations.append(frame.info.get('duration', 100))
                    
                    # Save resized GIF
                    logger.info(f"[{request_id}] Saving resized GIF...")
                    frames[0].save(
                        tmp_output_path,
                        save_all=True,
                        append_images=frames[1:],
                        duration=durations,
                        loop=0,
                        disposal=2,
                        optimize=False
                    )
                    
                    logger.info(f"[{request_id}] GIF processing complete")
                
                # Return resized GIF
                return send_file(
                    tmp_output_path,
                    mimetype='image/gif',
                    as_attachment=True,
                    download_name=f'xspeen_{pixel_size}.gif'
                )
            
            finally:
                # Clean up temp files
                if os.path.exists(tmp_input_path):
                    os.unlink(tmp_input_path)
                if os.path.exists(tmp_output_path):
                    os.unlink(tmp_output_path)
        
        else:
            return jsonify({"error": "Invalid media_type"}), 400
    
    except Exception as e:
        logger.error(f"[{request_id}] Error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/info', methods=['GET'])
def get_info():
    """Get service information"""
    return jsonify({
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
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
