from flet import Page, app, View
import flet_core as ftc
import os 
import db.database_script as db

from pages.download_page import DownloadPage
from router.router import onChangeRoute, pop_route

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 750


def main(page: Page):
    # Check the path to save the downloaded files
    print(os.getcwd())
    
    def on_route_change(route: str):
        onChangeRoute(page, route)
    
    def on_view_pop(view: View):
        pop_route(page, view)
    
    page.on_route_change = on_route_change
    page.on_view_pop = on_view_pop
    page.go("/")
    page.window_resizable = False
    page.window_width = WINDOW_WIDTH
    page.window_height = WINDOW_HEIGHT

    page.title = "ClipCatch Downloader"
    page.update()


if __name__ == "__main__":
    app(main, assets_dir="assets")
