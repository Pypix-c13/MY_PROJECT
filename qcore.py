import flet as ft
import qrcode
import base64
from io import BytesIO

def main(page: ft.Page):
    page.title = "QR Code Viewer"
    page.window.width = 250
    page.window.height = 300
    page.window.resizable = True
    
    page.window.min_width = 250
    page.window.min_height = 300
    
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data("https://github.com/Pypix-c13/MY_PROJECT")
    qr.make(fit=True)
    
    pil_img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    pil_img.save(buffered, format="PNG")
    
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    page.add(
        ft.Column(
            [
                ft.Text("Your QR Code:", weight="bold", size=16),
                ft.Image(
                    src=f"data:image/png;base64,{qr_base64}",
                    width=250, 
                    height=250
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)
