import flet as ft

from services.download_service import DownloadService, VideoInfo
from services.pythube_service.pythube_service import PythubeDatasource
import asyncio as aio

from components.download_tile import DownloadTile
from constants.constants import ROOT_DIRECTORY
from images.logo import LOGO_IMAGE


class DownloadPage(ft.Column):
    url: ft.TextField
    downloadService: DownloadService

    def on_url_change(self, textRef: ft.ControlEvent):
        print(textRef.control.value.strip())

    def __init__(self, updatePage):
        super().__init__()
        self.downloadService = DownloadService(PythubeDatasource(), self.__on_update)
        self.updatePage = updatePage
        self.downloadList = self.__download_section()
        self.controls = [
            ft.Container(
                height=20,
            ),
            ft.Image(
                src_base64=LOGO_IMAGE, height=100, fit=ft.ImageFit.CONTAIN
            ),
            self.__url_section(),
            self.downloadList,
        ]
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 30

    def __url_section(self):
        self.url = ft.TextField(
            hint_text="URL", on_change=self.on_url_change, expand=True, height=60
        )
        return ft.Row(
            controls=[
                self.url,
                ft.ElevatedButton(
                    "Download",
                    height=50,
                    width=150,
                    on_click=self.__on_download_click,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            height=70,
        )

    def __download_section(self):
        return ft.ListView(
            controls=self.__get_download_section_controls(),
            spacing=10,
            height=400,
            auto_scroll=True,
        )

    def __get_download_section_controls(self):
        return [
            DownloadTile(
                download=download, download_callback=self.__on_tile_download_click
            )
            for download in self.downloadService.get_downloads()
        ]
    
    def __clean_url(self):
        self.url.value = ""

    def __on_download_click(self, a):
        print(f"Downloading {self.url.value.strip()}...")
        url = self.url.value.strip()
        if not url:
            return
        self.__clean_url()
        aio.run(self.downloadService.download(url))

    def __on_update(self):
        self.downloadList.controls = self.__get_download_section_controls()
        self.updatePage()

    def __on_tile_download_click(self, url: str):
        aio.run(self.downloadService.download(url))
