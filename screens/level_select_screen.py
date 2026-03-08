from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.app import App

CUSTOM_FONT = 'assets/fonts/cute.ttf'

# --- ข้อมูลด่าน ---
LEVEL_DATA = [
    {'level': 1, 'name': 'ทุ่งผลไม้',   'desc': '7 ชุด / 60 วินาที'},
    {'level': 2, 'name': 'ป่าลึกลับ',   'desc': '12 ชุด / 80 วินาที'},
    {'level': 3, 'name': 'ดงผลไม้',     'desc': '15 ชุด / 70 วินาที'},
    {'level': 4, 'name': 'หุบเขาซ้อน',  'desc': '18 ชุด / 75 วินาที'},
    {'level': 5, 'name': 'นรกผลไม้',    'desc': '20 ชุด / 60 วินาที'},
    {'level': 6, 'name': 'ทะเลทรายแอปเปิ้ล', 'desc': '22 ชุด / 80 วินาที'},
    {'level': 7, 'name': 'โอเอซิสกล้วย', 'desc': '25 ชุด / 90 วินาที'},
    {'level': 8, 'name': 'ถ้ำมังคุด', 'desc': '28 ชุด / 85 วินาที'},
    {'level': 9, 'name': 'เกาะมะพร้าว', 'desc': '30 ชุด / 90 วินาที'},
    {'level': 10, 'name': 'สวรรค์ผลไม้', 'desc': '35 ชุด / 100 วินาที'},
]


class LevelButton(FloatLayout):
    """ปุ่มกลมแสดงด่าน พร้อมสถานะ locked/unlocked"""
    def __init__(self, level_info, is_unlocked, on_select_cb, **kwargs):
        super().__init__(**kwargs)
        self.level = level_info['level']
        self.is_unlocked = is_unlocked
        self.select_callback = on_select_cb

        # --- วงกลมพื้นหลัง ---
        with self.canvas.before:
            # เงา
            Color(0, 0, 0, 0.3)
            self.shadow = Ellipse(pos=(self.x + 4, self.y - 4), size=self.size)
            # วงกลมหลัก
            if is_unlocked:
                self.circle_color = Color(0.2, 0.7, 0.2, 1)  # เขียว
            else:
                self.circle_color = Color(0.45, 0.45, 0.45, 1)  # เทา
            self.circle = Ellipse(pos=self.pos, size=self.size)

        self.bind(pos=self._update, size=self._update)

        # --- เลขด่าน หรือ 🔒 ---
        if is_unlocked:
            display_text = str(level_info['level'])
        else:
            display_text = "🔒"

        self.lbl_num = Label(
            text=display_text, font_size='42sp', font_name=CUSTOM_FONT,
            bold=True, color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1), outline_width=2,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )
        self.add_widget(self.lbl_num)

        # --- ชื่อด่าน ---
        self.lbl_name = Label(
            text=level_info['name'], font_size='18sp', font_name=CUSTOM_FONT,
            bold=True, color=(1, 1, 0.7, 1) if is_unlocked else (0.7, 0.7, 0.7, 1),
            pos_hint={'center_x': 0.5, 'center_y': -0.15}
        )
        self.add_widget(self.lbl_name)

        # --- คำอธิบาย ---
        self.lbl_desc = Label(
            text=level_info['desc'], font_size='13sp', font_name=CUSTOM_FONT,
            color=(1, 1, 1, 0.8) if is_unlocked else (0.6, 0.6, 0.6, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': -0.32}
        )
        self.add_widget(self.lbl_desc)

    # 🔥 จัดการ touch โดยตรง ไม่ต้องใช้ปุ่มโปร่งใส
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.is_unlocked:
            self.select_callback(self.level)
            return True
        return super().on_touch_down(touch)

    def _update(self, *args):
        self.shadow.pos = (self.x + 4, self.y - 4)
        self.shadow.size = self.size
        self.circle.pos = self.pos
        self.circle.size = self.size

    def refresh_state(self, is_unlocked):
        """อัปเดตสถานะ lock/unlock ตอน on_enter"""
        self.is_unlocked = is_unlocked
        if is_unlocked:
            self.circle_color.rgba = (0.2, 0.7, 0.2, 1)
            self.lbl_num.text = str(self.level)
            self.lbl_name.color = (1, 1, 0.7, 1)
            self.lbl_desc.color = (1, 1, 1, 0.8)
        else:
            self.circle_color.rgba = (0.45, 0.45, 0.45, 1)
            self.lbl_num.text = "🔒"
            self.lbl_name.color = (0.7, 0.7, 0.7, 1)
            self.lbl_desc.color = (0.6, 0.6, 0.6, 0.8)


class LevelSelectScreen(Screen):
    def __init__(self, **kwargs):
        super(LevelSelectScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()

        # --- พื้นหลัง ---
        self.bg = Image(
            source='assets/images/bg.png',
            allow_stretch=True, keep_ratio=False,
        )
        self.layout.add_widget(self.bg)

        # --- Dim overlay ---
        dim = FloatLayout()
        with dim.canvas.before:
            Color(0, 0, 0, 0.35)
            dim.rect = RoundedRectangle(pos=(0, 0), size=(2000, 2000))
        self.layout.add_widget(dim)

        # --- Title (เงา + ตัวจริง) ---
        title_shadow = Label(
            text="SELECT LEVEL", font_size='52sp', font_name=CUSTOM_FONT,
            bold=True, color=(0, 0, 0, 0.5),
            pos_hint={'center_x': 0.505, 'center_y': 0.875}
        )
        self.layout.add_widget(title_shadow)

        title = Label(
            text="SELECT LEVEL", font_size='52sp', font_name=CUSTOM_FONT,
            bold=True, color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1), outline_width=4,
            pos_hint={'center_x': 0.5, 'center_y': 0.88}
        )
        self.layout.add_widget(title)

        # --- Level Buttons ---
        self.level_buttons = []
        total = len(LEVEL_DATA)
        for i, ldata in enumerate(LEVEL_DATA):
            # จัดเป็น 2 แถว: แถวบน 3 ปุ่ม, แถวล่าง 2 ปุ่ม
            if i < 3:
                row_count = 3
                row_idx = i
                cy = 0.6
            else:
                row_count = 2
                row_idx = i - 3
                cy = 0.35
            
            spacing = 0.22
            start_x = 0.5 - (row_count - 1) * spacing / 2
            cx = start_x + row_idx * spacing

            lb = LevelButton(
                level_info=ldata,
                is_unlocked=(ldata['level'] <= 1),  # ค่าเริ่มต้น unlock แค่ด่าน 1
                on_select_cb=self.select_level,
                size_hint=(None, None), size=(120, 120),
                pos_hint={'center_x': cx, 'center_y': cy}
            )
            self.layout.add_widget(lb)
            self.level_buttons.append(lb)

        # --- ปุ่ม BACK ---
        self.btn_back = Button(
            text="⬅  BACK", font_size='22sp', font_name=CUSTOM_FONT,
            bold=True,
            background_normal='', background_color=(0, 0, 0, 0),
            size_hint=(None, None), size=(180, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.15}
        )
        with self.btn_back.canvas.before:
            Color(0.7, 0.25, 0.25, 1)
            self.back_bg = RoundedRectangle(
                pos=self.btn_back.pos, size=self.btn_back.size, radius=[20]
            )
        self.btn_back.bind(pos=self._update_back, size=self._update_back)
        self.btn_back.bind(on_press=self.go_back)
        self.layout.add_widget(self.btn_back)

        self.add_widget(self.layout)

    def on_enter(self):
        """Sync สถานะ unlock จาก App ทุกครั้งที่เข้าหน้านี้"""
        app = App.get_running_app()
        for lb in self.level_buttons:
            lb.refresh_state(lb.level <= app.unlocked_level)

    def select_level(self, level):
        game_screen = self.manager.get_screen('game')
        game_screen.target_level = level
        self.manager.current = 'game'

    def go_back(self, instance):
        self.manager.current = 'start'

    def _update_back(self, *args):
        self.back_bg.pos = self.btn_back.pos
        self.back_bg.size = self.btn_back.size
