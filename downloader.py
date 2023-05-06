import ssl
import yt_dlp

# Disable ssl checking
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


class DownloaderDlp:
    def __init__(self, url: str):
        self.url = url

    def fetch_streams(self):
        """
        Fetch the list of available stream formats.
        """
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
    
    def get_title(self):
        """
        Fetch the video title.
        """
        ydl_options = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True
        }
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            title = info_dict.get('title', '')

        return title
    
    def download(self, format_id):
        """
        Download the video.

        Args:
            format_id (str): The format id selected.
        """
        ydl_options = {
            'format': format_id
        }
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([self.url])
