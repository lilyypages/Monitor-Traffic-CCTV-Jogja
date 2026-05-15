import yt_dlp

def get_youtube_stream_url(youtube_url):
    ydl_opts = {
        'format': 'best',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info['url']