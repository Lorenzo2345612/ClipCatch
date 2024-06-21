from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()

class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    thumbnail_url = Column(String)
    path = Column(String, nullable=True)
    youtube_url = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Video(title={self.title}, url={self.thumbnail_url}, path={self.path})>'
    
class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def add_video(self, title, url, youtube_url):
        session = self.Session()
        video = Video(title=title, thumbnail_url=url, youtube_url=youtube_url)
        session.add(video)
        # Get the id of the video
        session.flush()
        video_id = video.id
        session.commit()
        session.close()
        return video_id
    
    def update_path(self, id, path):
        session = self.Session()
        video = session.query(Video).filter_by(id=id).first()
        video.path = path
        session.commit()
        session.close()
    
    def get_videos(self):
        session = self.Session()
        videos = session.query(Video).all()
        session.close()
        return videos
    
    def get_video(self, id):
        session = self.Session()
        video = session.query(Video).filter_by(id=id).first()
        session.close()
        return video
    
    def delete_video(self, id):
        session = self.Session()
        video = session.query(Video).filter_by(id=id).first()
        session.delete(video)
        session.commit()
        session.close()
    
    def delete_all_videos(self):
        session = self.Session()
        session.query(Video).delete()
        session.commit()
        session.close()
        
    def check_video(self, youtube_url):
        session = self.Session()
        video = session.query(Video).filter_by(youtube_url=youtube_url).first()
        session.close()
        return video.id if video else None

    def get_video_path(self, id):
        session = self.Session()
        video = session.query(Video).filter_by(id=id).first()
        path = video.path
        session.close()
        return path
        
    def __del__(self):
        self.engine.dispose()
        
db = Database('sqlite:///videos.db')