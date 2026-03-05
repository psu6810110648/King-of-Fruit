from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.current_level = 1 # เก็บด่านล่าสุดที่เล่น

        # Background
        self.bg = Image(source='assets/images/bg.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.bg)

        # Result Label (WIN/LOSE)
        self.lbl_result = Label(
            text="YOU WIN!", 
            font_size='60sp', 
            bold=True, 
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1), outline_width=4,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        self.layout.add_widget(self.lbl_result)

        # Score Label
        self.lbl_score = Label(
            text="Score: 0", 
            font_size='40sp', 
            bold=True,
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1), outline_width=2,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )
        self.layout.add_widget(self.lbl_score)

        # --- ปุ่ม Restart / Next Level (จะเปลี่ยนข้อความตามสถานการณ์) ---
        self.btn_action = Button(
            text="PLAY AGAIN",
            font_size='30sp', bold=True,
            background_normal='', background_color=(0, 0, 0, 0),
            size_hint=(None, None), size=(250, 80),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        with self.btn_action.canvas.before:
            Color(0.2, 0.6, 0.2, 1) # สีเขียว
            self.btn_bg = RoundedRectangle(pos=self.btn_action.pos, size=self.btn_action.size, radius=[40])
            
        self.btn_action.bind(pos=self.update_btn, size=self.update_btn)
        self.btn_action.bind(on_press=self.on_action_click)
        self.layout.add_widget(self.btn_action)

        # ปุ่ม Home
        self.btn_home = Button(
            text="HOME",
            font_size='25sp', bold=True,
            background_normal='', background_color=(0, 0, 0, 0),
            size_hint=(None, None), size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.20}
        )
        with self.btn_home.canvas.before:
            Color(0.2, 0.4, 0.8, 1) # สีน้ำเงิน
            self.home_bg = RoundedRectangle(pos=self.btn_home.pos, size=self.btn_home.size, radius=[30])
        
        self.btn_home.bind(pos=self.update_home_btn, size=self.update_home_btn)
        self.btn_home.bind(on_press=self.go_home)
        self.layout.add_widget(self.btn_home)

        self.add_widget(self.layout)

    def update_result(self, is_win, score, current_level=1):
        self.current_level = current_level
        self.is_win = is_win
        
        self.lbl_score.text = f"Score: {score}"
        
        if is_win:
            self.lbl_result.text = "YOU WIN! 🎉"
            self.lbl_result.color = (0.2, 1, 0.2, 1) # เขียวอ่อน
            
            # ถ้าชนะด่าน 1 -> ปุ่มเป็น "NEXT LEVEL"
            if self.current_level == 1:
                self.btn_action.text = "NEXT LEVEL >>"
            else:
                self.btn_action.text = "PLAY AGAIN" # ชนะด่านสุดท้าย
                
        else:
            self.lbl_result.text = "GAME OVER 💀"
            self.lbl_result.color = (1, 0.2, 0.2, 1) # แดง
            self.btn_action.text = "TRY AGAIN"

    def on_action_click(self, instance):
        game_screen = self.manager.get_screen('game')
        
        if self.is_win and self.current_level == 1:
            # ถ้าชนะด่าน 1 ให้ไปด่าน 2
            game_screen.target_level = 2
        else:
            # นอกนั้น (แพ้ หรือ จบด่าน 2) ให้เล่นใหม่ด่าน 1
            game_screen.target_level = 1
            
        self.manager.current = 'game'

    def go_home(self, instance):
        self.manager.current = 'start'

    def update_btn(self, *args):
        self.btn_bg.pos = self.btn_action.pos
        self.btn_bg.size = self.btn_action.size

    def update_home_btn(self, *args):
        self.home_bg.pos = self.btn_home.pos
        self.home_bg.size = self.btn_home.size