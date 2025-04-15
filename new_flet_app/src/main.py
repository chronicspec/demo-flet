import flet as ft

def main(page: ft.Page):
    page.title = "Map Viewer with WebView"
    page.add(
        ft.Column(
            [
                ft.Text("🗺 Map (Leaflet in WebView)", size=24, weight="bold"),
                ft.WebView(
                    url="http://localhost:8000/src/map.html",  # must be served via http
                    width=800,
                    height=600
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
