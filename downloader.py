import ssl
import yt_dlp

# Disable ssl checking
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


class DownloaderDlp:
    def __init__(self, url: str):
        self.url = url

    def fetch_streams(self):
        ydl_options = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True
        }

        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            formats = info_dict.get('formats', [])

        reduced_formats = []

        for f in formats:
            reduced_formats.append({
                'id': f['format_id'],
                'note': f['format_note'],
                'video_ext': f['video_ext'],
                'format': f['format']
            })

        return reduced_formats
    
    def download(self, format_id):
        ydl_options = {
            'format': format_id
        }
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([self.url])
