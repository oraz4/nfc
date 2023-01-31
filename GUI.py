from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'height', 500)
Config.set('graphics', 'width', 400)

Builder.load_string("""
<StartScreen>:
    ModalView:
        background: 'C:/Users/giyoe/Desktop/Project/Background.jfif'
        BoxLayout:
            orientation: 'vertical'
            padding: [30,15,30,15]
            spacing: 15
            Button:
                text: 'Start'
                background_normal: 'C:/Users/giyoe/Desktop/Project/button normal.jpg'
                background_down: 'C:/Users/giyoe/Desktop/Project/button down.jpg'
                bold: True
                font_size: 50
                on_press: root.manager.current = 'attendance'
<AttendanceScreen>:
    ModalView:
        background: 'C:/Users/giyoe/Desktop/Project/Background.jfif'
        BoxLayout:
            orientation: 'vertical'
            padding: [30,15,30,15]
            spacing: 15
            Label:
                text: 'Counter: 0'
                bold: True
                font_size: 50
            Button:
                text: 'Stop'
                background_normal: 'C:/Users/giyoe/Desktop/Project/button normal.jpg'
                background_down: 'C:/Users/giyoe/Desktop/Project/button down.jpg'
                bold: True
                font_size: 50
                on_press: root.manager.current = 'send'
<SendScreen>:
    ModalView:
        background: 'C:/Users/giyoe/Desktop/Project/Background.jfif'
        BoxLayout:
            orientation: 'vertical'
            padding: [30,15,30,15]
            spacing: 15
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Enter your e-mail:'
                    bold: True
                    font_size: 25
                TextInput:
                    id: email
                    multiline: False
                    font_size: 25
            Button:
                text: 'Send'
                background_normal: 'C:/Users/giyoe/Desktop/Project/button normal.jpg'
                background_down: 'C:/Users/giyoe/Desktop/Project/button down.jpg'
                bold: True
                font_size: 50
                on_press: app.send_email(email.text)
            Button:
                text: 'Restart'
                background_normal: 'C:/Users/giyoe/Desktop/Project/button normal.jpg'
                background_down: 'C:/Users/giyoe/Desktop/Project/button down.jpg'
                bold: True
                font_size: 50
                on_press: root.manager.current = 'start' 
""")

class StartScreen(Screen):
    pass

class AttendanceScreen(Screen):
    pass

class SendScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget (StartScreen(name = 'start'))
sm.add_widget(AttendanceScreen(name='attendance'))
sm.add_widget(SendScreen(name='send'))

class RFIDApp (App):
    def send_email(self, receiver_email):
        message = MIMEMultipart()
        message['From'] = 'rfidbasedattendance@gmail.com'
        message['To'] = receiver_email
        message['Subject'] = 'Attendance'

        filename = 'C:/Users/giyoe/Desktop/Project/xxx.docx'

        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header('Content-Disposition', f'attachment; filename = {filename}', )

        message.attach(part)
        text = message.as_string()

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login('rfidbasedattendance@gmail.com', 'nicksaka')
            server.sendmail('rfidbasedattendance@gmail.com', receiver_email, text)

    def build(self):
        return sm

if __name__ == '__main__':
    RFIDApp().run()
