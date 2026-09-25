from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Backend is running!"}

@app.get("/download")
def get_download_links(url: str):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            
            return {
                "title": info_dict.get('title', 'Video'),
                "thumbnail": info_dict.get('thumbnail', ''),
                "url": info_dict.get('url', ''),
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
