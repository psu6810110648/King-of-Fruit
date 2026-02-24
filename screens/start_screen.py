from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle # นำเข้าเครื่องมือวาดรูปขอบมนเพิ่ม

# --- 1. สร้างคลาสปุ่มขอบมน (Custom Widget) ---
class RoundedButton(Button):
    def __init__(self, bg_color=(0.2, 0.8, 0.2, 1), radius=25, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        # ลบภาพสี่เหลี่ยมพื้นฐานของ Kivy ออกให้โปร่งใส
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        
        # วาดสี่เหลี่ยมขอบมนลงไปเป็นพื้นหลังแทน
        with self.canvas.before:
            Color(rgba=bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
            
        # สั่งให้ขอบมนขยับตามเวลาหน้าจอเปลี่ยนขนาด
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# --- 2. หน้าจอ StartScreen ---
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        # รูปพื้นหลัง
        bg_image = Image(source='assets/images/bg.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(bg_image)

        # เงาชื่อเกม
        title_shadow = Label(
            text='[b]KING OF FRUIT[/b]', markup=True,
            font_size='60sp', color=(0, 0, 0, 0.8),
            size_hint=(1, 0.2), pos_hint={'center_x': 0.505, 'center_y': 0.795}
        )
        layout.add_widget(title_shadow)
        
        # ชื่อเกมสีทอง
        title_main = Label(
            text='[b]KING OF FRUIT[/b]', markup=True,
            font_size='60sp', color=(1, 1, 1, 1),
            size_hint=(1, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        layout.add_widget(title_main)

        
        # ปุ่ม START GAME
        btn_start = RoundedButton(
            bg_color=(0.1, 0.5, 0.1, 1), # สีเขียว
            radius=30, # ปรับความมนตรงนี้ (เลขยิ่งเยอะ ยิ่งมนมาก)
            text='START GAME', font_size='26sp', bold=True,
            size_hint=(0.4, 0.12), pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        btn_start.bind(on_press=self.go_to_game)
        layout.add_widget(btn_start)

        # ปุ่ม EXIT
        btn_exit = RoundedButton(
            bg_color=(0.6, 0.1, 0.1, 1), # สีแดง
            radius=20, # ปรับความมน
            text='EXIT', font_size='20sp', bold=True,
            size_hint=(0.2, 0.08), pos_hint={'right': 0.98, 'y': 0.02}
        )
        btn_exit.bind(on_press=self.exit_game)
        layout.add_widget(btn_exit)

        self.add_widget(layout)

    def go_to_game(self, instance):
        print(">> กดปุ่มเริ่มเกม!")

    def exit_game(self, instance):
        print(">> กดปุ่มออกแอป!")
        App.get_running_app().stop()
