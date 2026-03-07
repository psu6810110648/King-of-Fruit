from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
import sys

# ✅ ชื่อฟอนต์ (ถ้าไม่มีให้แก้เป็น None)
CUSTOM_FONT = 'assets/fonts/cute.ttf' 

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()

        # --- 1. 🖼️ พื้นหลัง (ขยับซูมเข้าออก) ---
        self.bg = Image(
            source='assets/images/bg.png',
            allow_stretch=True, 
            keep_ratio=False,
            size_hint=(1.2, 1.2), # เผื่อขอบไว้สำหรับซูม
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(self.bg)

        # --- 2. 👑 ชื่อเกม (Title) นิ่งๆ ---
        # เงา (สีดำจางๆ)
        self.title_shadow = Label(
            text="KING OF FRUIT",
            font_size='70sp',
            font_name=CUSTOM_FONT,
            color=(0, 0, 0, 0.5),
            pos_hint={'center_x': 0.505, 'center_y': 0.745}
        )
        self.layout.add_widget(self.title_shadow)

        # ตัวหนังสือจริง (สีขาว ขอบดำ)
        self.title_label = Label(
            text="KING OF FRUIT",
            font_size='70sp',
            font_name=CUSTOM_FONT,
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1), # ขอบดำ
            outline_width=4,
            pos_hint={'center_x': 0.5, 'center_y': 0.75}
        )
        self.layout.add_widget(self.title_label)

        # --- 3. ▶️ ปุ่ม Start (แบบดั้งเดิม: เขียวเข้ม) ---
        self.btn_start = Button(
            text="START GAME",
            font_size='30sp', # ขนาดตัวหนังสือเดิม
            font_name=CUSTOM_FONT,
            bold=True,
            background_normal='', background_color=(0,0,0,0),
            size_hint=(None, None), size=(300, 80), # ขนาดปุ่มเดิม
            pos_hint={'center_x': 0.5, 'center_y': 0.25}
        )
        with self.btn_start.canvas.before:
            # สีเขียวเข้ม (Classic)
            Color(0.1, 0.6, 0.1, 1) 
            self.btn_bg = RoundedRectangle(pos=self.btn_start.pos, size=self.btn_start.size, radius=[40])
            
            # ขอบขาวจางๆ ข้างใน (เหมือนในรูปเป๊ะ)
            Color(1, 1, 1, 0.3) 
            self.btn_border = RoundedRectangle(pos=(self.btn_start.x+5, self.btn_start.y+5), 
                                             size=(290, 70), radius=[35])
            
        self.btn_start.bind(pos=self.update_btn_graphics, size=self.update_btn_graphics)
        self.btn_start.bind(on_press=self.start_game)
        self.layout.add_widget(self.btn_start)

        # --- 4. 🚪 ปุ่ม Exit (แบบดั้งเดิม: แดงเข้ม) ---
        self.btn_exit = Button(
            text="EXIT",
            font_size='20sp',
            font_name=CUSTOM_FONT,
            bold=True,
            background_normal='', background_color=(0,0,0,0),
            size_hint=(None, None), size=(120, 50),
            pos_hint={'right': 0.95, 'y': 0.05}
        )
        with self.btn_exit.canvas.before:
            # สีแดงเข้ม (Classic)
            Color(0.8, 0.2, 0.2, 1) 
            self.exit_bg = RoundedRectangle(pos=self.btn_exit.pos, size=self.btn_exit.size, radius=[15])

        self.btn_exit.bind(pos=self.update_exit_graphics, size=self.update_exit_graphics)
        self.btn_exit.bind(on_press=self.exit_game)
        self.layout.add_widget(self.btn_exit)

        # --- 5. ⚙️ ปุ่ม Settings ---
        self.btn_settings = Button(
            text="SETTINGS",
            font_size='20sp',
            font_name=CUSTOM_FONT,
            bold=True,
            background_normal='', background_color=(0,0,0,0),
            size_hint=(None, None), size=(150, 50),
            pos_hint={'x': 0.05, 'y': 0.05}
        )
        with self.btn_settings.canvas.before:
            Color(0.3, 0.3, 0.7, 1)  # สีม่วงน้ำเงิน
            self.settings_bg = RoundedRectangle(pos=self.btn_settings.pos, size=self.btn_settings.size, radius=[15])

        self.btn_settings.bind(pos=self.update_settings_graphics, size=self.update_settings_graphics)
        self.btn_settings.bind(on_press=self.open_settings)
        self.layout.add_widget(self.btn_settings)

        self.add_widget(self.layout)

    # --- ✨ Animation Zone ---
    def on_enter(self):
        """เรียกเมื่อเข้าหน้านี้"""
        self.animate_background()   # ✅ พื้นหลังยังขยับอยู่
        # ❌ ลบ Animation ชื่อและปุ่มออก ให้มันนิ่งๆ ตามที่ขอครับ

    def animate_background(self):
        """พื้นหลังซูมเข้า-ออก (Ken Burns)"""
        anim = Animation(size_hint=(1.35, 1.35), duration=15, t='in_out_sine') + \
               Animation(size_hint=(1.2, 1.2), duration=15, t='in_out_sine')
        anim.repeat = True 
        anim.start(self.bg)

    def update_btn_graphics(self, *args):
        self.btn_bg.pos = self.btn_start.pos
        self.btn_bg.size = self.btn_start.size
        self.btn_border.pos = (self.btn_start.x+5, self.btn_start.y+5)
        self.btn_border.size = (self.btn_start.width-10, self.btn_start.height-10)

    def update_exit_graphics(self, *args):
        self.exit_bg.pos = self.btn_exit.pos
        self.exit_bg.size = self.btn_exit.size

    def update_settings_graphics(self, *args):
        self.settings_bg.pos = self.btn_settings.pos
        self.settings_bg.size = self.btn_settings.size

    def start_game(self, instance):
        Animation.cancel_all(self.bg)
        self.manager.current = 'game'

    def open_settings(self, instance):
        Animation.cancel_all(self.bg)
        self.manager.current = 'settings'

    def exit_game(self, instance):
        sys.exit()