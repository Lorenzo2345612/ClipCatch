from typing import Optional
from services.download_service import DownloadDatasource
from pytube import YouTube



class PythubeDatasource(DownloadDatasource):
    async def download(self, url: str, output_path: str, on_progress_callback = None, on_download_end_callback = None, on_error_callback = None) -> Optional[str]:
        try:
            yt = YouTube(url, on_progress_callback = on_progress_callback, on_complete_callback=on_download_end_callback)
            print(yt.streams.filter(only_audio=True))
            return yt.streams.get_audio_only().download(output_path)
        except Exception as e:
            if on_error_callback:
                on_error_callback(e)
            else:
                raise e
    def get_video_info(self, url: str):
        yt = YouTube(url)
        return {
            "title": yt.title,
            "thumbnail_url": yt.thumbnail_url
        }