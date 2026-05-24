import yt_dlp
import subprocess
import os

NODE_PATH = r"C:\Program Files\nodejs\node.exe"

def get_youtube_stream_url(youtube_url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
    }

    if os.path.isfile(NODE_PATH):
        ydl_opts['js_runtimes'] = {'node': {'path': NODE_PATH}}
    ydl_opts['remote_components'] = {'ejs': 'github'}
    ydl_opts['extractor_args'] = {'youtube': {'skip': ['dash', 'webpage']}}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info['url']