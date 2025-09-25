# main.py
from fastapi import FastAPI, HTTPException
import yt_dlp
import os
import tempfile
import shutil
import time

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Backend siap uji"}

@app.post("/analyze-subtitle-only")
async def analyze_subtitle_only(request: dict):
    url = request.get("url")
    if not url:
        raise HTTPException(400, "URL diperlukan")
    
    temp_dir = tempfile.mkdtemp()
    start_time = time.time()
    
    try:
        # HANYA download subtitle, TIDAK download video/audio
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en', 'id', 'auto'],
            'skip_download': True,
            'outtmpl': os.path.join(temp_dir, 'video'),
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Cari file subtitle yang berhasil diunduh
        subtitle_files = [f for f in os.listdir(temp_dir) if f.endswith('.vtt') or f.endswith('.srt')]
        duration = time.time() - start_time
        
        return {
            "success": True,
            "duration_seconds": round(duration, 2),
            "subtitle_found": len(subtitle_files) > 0,
            "subtitle_files": subtitle_files,
            "url": url
        }
    
    except Exception as e:
        duration = time.time() - start_time
        return {
            "success": False,
            "duration_seconds": round(duration, 2),
            "error": str(e),
            "url": url
        }
    
    finally:
        # HAPUS SEMUA — jangan tinggalkan jejak
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)