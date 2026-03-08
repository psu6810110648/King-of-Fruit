from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

CUSTOM_FONT = 'assets/fonts/cute.ttf'

class LoseScreen(Screen):
    def __init__(self, **kwargs):
        super(LoseScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        
        # พื้นหลัง
        self.bg = Image(source='assets/images/bg.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.bg)

        # กล่องเนื้อหาตรงกลาง
        self.content_box = FloatLayout(size_hint=(None, None), size=(400, 350),
                                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
        with self.content_box.canvas.before:
            Color(1, 1, 1, 0.9) # พื้นหลังสีขาวโปร่งแสงนิดๆ
            self.box_bg = RoundedRectangle(pos=self.content_box.pos, size=self.content_box.size, radius=[30])
        self.content_box.bind(pos=self.update_bg, size=self.update_bg)

        # ข้อความ Game Over
        self.lbl_title = Label(
            text="GAME OVER", 
            font_size='50sp', 
            font_name=CUSTOM_FONT,
            bold=True, 
            color=(0.9, 0.2, 0.2, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        self.content_box.add_widget(self.lbl_title)

        # ข้อความ Score
        self.lbl_score = Label(
            text="Score: 0", 
            font_size='35sp', 
            font_name=CUSTOM_FONT,
            bold=True, 
            color=(0.4, 0.4, 0.4, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )
        self.content_box.add_widget(self.lbl_score)

        # ปุ่ม TRY AGAIN
        self.btn_retry = Button(
            text="TRY AGAIN",
            font_size='28sp', 
            font_name=CUSTOM_FONT,
            bold=True,
            background_normal='', background_color=(0, 0, 0, 0),
            size_hint=(None, None), size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )
        with self.btn_retry.canvas.before:
            Color(1, 0.5, 0.5, 1) # สีแดงส้ม
            self.retry_bg = RoundedRectangle(pos=self.btn_retry.pos, size=self.btn_retry.size, radius=[20])
        self.btn_retry.bind(pos=self.update_retry_bg, size=self.update_retry_bg)
        self.btn_retry.bind(on_press=self.retry_game)
        self.content_box.add_widget(self.btn_retry)

        # ปุ่ม HOME
        self.btn_home = Button(
            text="HOME",
            font_size='22sp', 
            font_name=CUSTOM_FONT,
            bold=True,
            background_normal='', background_color=(0, 0, 0, 0),
            size_hint=(None, None), size=(150, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.1}
        )
        with self.btn_home.canvas.before:
            Color(0.6, 0.6, 0.6, 1) # สีเทา
            self.home_bg = RoundedRectangle(pos=self.btn_home.pos, size=self.btn_home.size, radius=[20])
        self.btn_home.bind(pos=self.update_home_bg, size=self.update_home_bg)
        self.btn_home.bind(on_press=self.go_home)
        self.content_box.add_widget(self.btn_home)

        self.layout.add_widget(self.content_box)
        self.add_widget(self.layout)

    def on_enter(self):
        # ดึงคะแนนจากหน้าเกมมาแสดงตอนเข้าหน้าแพ้
        game_screen = self.manager.get_screen('game')
        if game_screen:
            self.lbl_score.text = f"Score: {game_screen.score}"

    def update_bg(self, *args):
        self.box_bg.pos = self.content_box.pos
        self.box_bg.size = self.content_box.size

    def update_retry_bg(self, *args):
        self.retry_bg.pos = self.btn_retry.pos
        self.retry_bg.size = self.btn_retry.size

    def update_home_bg(self, *args):
        self.home_bg.pos = self.btn_home.pos
        self.home_bg.size = self.btn_home.size

    def retry_game(self, instance):
        game_screen = self.manager.get_screen('game')
        if game_screen:
            # ลบ popup win เก่าที่อาจจะค้างอยู่
            if hasattr(game_screen, 'result_popup') and game_screen.result_popup.parent:
                game_screen.layout.remove_widget(game_screen.result_popup)
            game_screen.start_level(game_screen.current_level)
        self.manager.current = 'game'

    def go_home(self, instance):
        self.manager.current = 'start'
