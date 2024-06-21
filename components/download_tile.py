from services.download_service import VideoInfo
from flet import (
    Container,
    Image,
    Row,
    Column,
    Text,
    colors,
    border,
    ImageFit,
    TextThemeStyle,
    IconButton,
    Icon, icons, ProgressRing
)
import os

TILE_HEIGHT = 100
TILE_PADDING = 10
TILE_BORDER_RADIUS_EXT = 15
TILE_BORDER_RADIUS_INT = 10


class DownloadTile(Container):
    def __init__(self, download: VideoInfo, download_callback=None):
        self.download = download
        self.download_callback = download_callback
        controls = [
                    Container(
                        content=Image(download.thumbnail_url, fit=ImageFit.COVER, border_radius=TILE_BORDER_RADIUS_INT/2),
                        width=TILE_HEIGHT - TILE_PADDING,
                        height=TILE_HEIGHT - TILE_PADDING,
                        bgcolor=colors.BLUE_GREY_500,
                        border_radius=TILE_BORDER_RADIUS_INT,
                        padding=TILE_PADDING/2,
                    ),
                    Column(
                        controls=[
                            Text(
                                download.title,
                                expand=True,
                                max_lines=2,
                                theme_style=TextThemeStyle.TITLE_SMALL,
                            ),
                        ],
                        expand=2,
                    )
                ]
        if download.path:
            controls.append(
                IconButton(
                    icon=icons.PLAY_CIRCLE_FILL,
                    on_click=self.__play_video,
                )
            )
        elif download.is_downloading:
            controls.append(
                ProgressRing()
            )
        else:
            controls.append(
                IconButton(
                    icon=icons.DOWNLOAD,
                    on_click=self.__on_download_click,
                )
            )
        super().__init__(
            content=Row(
                controls= controls,
                expand=True,
            ),
            height=TILE_HEIGHT,
            bgcolor=colors.BLUE_GREY_900,
            padding=TILE_PADDING,
            border_radius=TILE_BORDER_RADIUS_EXT,
            border=border.all(3, colors.BLUE_GREY_400),
        )
    
    def __play_video(self, e):
        print(e)
        os.startfile(self.download.path)
    
    def __on_download_click(self, e):
        # TODO: Implement download logic
        if self.download_callback:
            self.download_callback(self.download.youtube_url)
