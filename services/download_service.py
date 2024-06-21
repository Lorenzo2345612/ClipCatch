from abc import abstractmethod
from typing import List, Optional, Set
from db.database_script import db
from pathlib import Path
from os.path import join
from asyncio import sleep

from utils.video import this_video_exists

output_path = join(Path.home(), "Downloads")

# Check if the output path exists, if not create it
if not Path(output_path).exists():
    Path(output_path).mkdir()


class DownloadDatasource:
    @abstractmethod
    async def download(self, url: str, output_path: str) -> Optional[str]:
        pass
    
    @abstractmethod
    def get_video_info(self, url: str) -> dict:
        pass

class VideoInfo:
    def __init__(self, title: str, thumbnail_url: str, youtube_url: str, is_downloading: bool, path: Optional[str] = None):
        self.title = title
        self.thumbnail_url = thumbnail_url
        self.path = path
        self.youtube_url = youtube_url
        self.is_downloading = is_downloading
        
class DownloadService:
    
    def __init__(self, datasource: DownloadDatasource, update_callback):
        self.downloading: Set[str] = set()
        self.datasource = datasource
        self.downloads: List[VideoInfo] = self.__load_downloads()
        self.update_callback = update_callback

    async def __download(self, url: str) -> Optional[str]:
        return await self.datasource.download(url, output_path)
    
    async def download(self, url: str) -> None:
        video_id = self.check_video(url)
        if video_id:
            if this_video_exists(db.get_video_path(video_id)):
                return
            self.__set_downloading(url)
            self.downloads = self.__load_downloads()
            self.update_callback()
            video_path = await self.__download(url)
            db.update_path(video_id, video_path)
            self.__delete_downloading(url)
            self.downloads = self.__load_downloads()
            self.update_callback()
            return
        video_info = self.datasource.get_video_info(url)
        self.__set_downloading(url)
        video = VideoInfo(video_info["title"], video_info["thumbnail_url"], url, True)
        self.downloads.append(video)
        video_id = db.add_video(video.title, video.thumbnail_url, video.youtube_url)
        self.update_callback()
        video_path = await self.__download(url)
        db.update_path(video_id, video_path)
        self.__delete_downloading(url)
        self.downloads = self.__load_downloads()
        self.update_callback()
            
    def check_video(self, url: str) -> Optional[int]:
        return db.check_video(url)
    
    def __set_downloading(self, url: str):
        self.downloading.add(url)
    
    def is_downloading(self, url: str) -> bool:
        return url in self.downloading
    
    def __delete_downloading(self, url: str):
        self.downloading.remove(url)
        
    def __load_downloads(self):
        return [VideoInfo(i.title, i.thumbnail_url, i.youtube_url, self.is_downloading(i.youtube_url), i.path) for i in db.get_videos()]
    
    def get_downloads(self):
        return self.downloads