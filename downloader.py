import ssl
import yt_dlp

# Disable ssl checking
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


class DownloaderDlp:
    def __init__(self, url: str, ui_progress, ui_progress_label):
        self.url = url
        self.ui_progress = ui_progress
        self.ui_progress_label = ui_progress_label

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
            'format': format_id,
            'progress_hooks': [self.update_progress]
        }
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([self.url])

    def update_progress(self, progress):
        """
        Callback for the progress of download.

        Args:
            progress (dict): Dictionary of the progress, automatically passed.
        """
        if progress['status'] == 'downloading':
            downloaded_bytes = progress['downloaded_bytes']  # Get the current downloaded bytes
            total_bytes = progress['total_bytes_estimate']  # Get the estimated total bytes

            percent = 0.0

            if total_bytes:
                percent = round(downloaded_bytes / total_bytes * 100, 2)

                if self.ui_progress:
                    self.ui_progress.master.after(10, self.update_uis(percent))

    def update_uis(self, percent: float):
        """
        Update the label and progress bar of the UI.

        Args:
            percent (float): The percentage of the download.
        """
        self.ui_progress.config(value=percent)
        self.ui_progress_label.config(text=f'Status: {percent}%')
