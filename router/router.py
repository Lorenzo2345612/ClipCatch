from flet import Page, SafeArea, View

from pages.download_page import DownloadPage


def onChangeRoute(page: Page, route: str):
    page.views.append(View("/", [SafeArea(DownloadPage(page.update))]))
    page.update()


def pop_route(page: Page, view: View):
    page.views.pop()
    if len(page.views) == 0:
        onChangeRoute(page, "/")
    else:
        page.update()
