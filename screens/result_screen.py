from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle

# --- คลาสปุ่มขอบมน (ปรับสีเริ่มต้นให้สดใสขึ้น) ---
class RoundedButton(Button):
    def __init__(self, bg_color=(0.3, 0.9, 0.3, 1), radius=25, **kwargs): # สีเขียวสด
        super(RoundedButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        with self.canvas.before:
            Color(rgba=bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# --- หน้าจอสรุปผล (Result Screen) ---
class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        
        layout = FloatLayout()

        # 1. พื้นหลัง (ใช้ AsyncImage เพื่อให้โหลดรูปใหม่ได้)
        self.bg_image = AsyncImage(source='assets/images/bg.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.bg_image)
        
        # 2. พื้นหลังสีดำจางๆ (Overlay) - เพิ่มให้ตัวหนังสือเด่นขึ้น
        with layout.canvas.after:
            Color(0, 0, 0, 0.4)
        
        # 3. ข้อความแสดงผล (YOU WIN!) - ปรับสีให้สดใส
        # สร้างเงาสีดำก่อน
        self.result_shadow = Label(
            text='[b]YOU WIN![/b]', markup=True,
            font_size='85sp', color=(0, 0, 0, 0.4),
            pos_hint={'center_x': 0.51, 'center_y': 0.65},
            outline_color=(0,0,0,1), outline_width=2 # เพิ่มขอบดำให้เงา
        )
        layout.add_widget(self.result_shadow)

        # สร้างตัวหนังสือจริง (สีเหลืองทอง ขอบเขียว)
        self.result_label = Label(
            text='[b]YOU WIN![/b]', markup=True,
            font_size='85sp', color=(1, 0.9, 0.1, 1), # สีเหลืองทองสว่าง
            pos_hint={'center_x': 0.5, 'center_y': 0.66},
            outline_color=(1, 0.6, 0, 1), outline_width=2 # ขอบสีเขียวเข้ม
        )
        layout.add_widget(self.result_label)

        # 4. ข้อความบอกคะแนน (สีขาว ขอบดำ ให้อ่านง่าย)
        self.score_label = Label(
            text='Score: 0', font_size='50sp', bold=True,
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1), outline_width=2,
            pos_hint={'center_x': 0.5, 'center_y': 0.53}
        )
        layout.add_widget(self.score_label)

        # 5. ปุ่ม PLAY AGAIN (สีเขียวสด)
        btn_restart = RoundedButton(
            text='PLAY AGAIN', font_size='24sp', bold=True,
            bg_color=(0.2, 0.8, 0.2, 1), # เขียวสด
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        btn_restart.bind(on_press=self.restart_game)
        layout.add_widget(btn_restart)

        # 6. ปุ่ม MAIN MENU (สีส้มสด)
        btn_home = RoundedButton(
            text='MAIN MENU', font_size='20sp', bold=True,
            bg_color=(1, 0.5, 0, 1), # ส้มสด
            size_hint=(0.3, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.22}
        )
        btn_home.bind(on_press=self.go_home)
        layout.add_widget(btn_home)

        self.add_widget(layout)

    # --- ฟังก์ชันอัปเดตผลลัพธ์ ---
    def update_result(self, is_win, score):
        if is_win:
            # 🏆 ชนะ: ใช้รูปปาร์ตี้, ตัวหนังสือสีทองขอบเขียว
            self.bg_image.source = 'assets/images/bg3.png' 
            self.result_label.text = "[b]YOU WIN![/b]"
            self.result_label.color = (1, 0.9, 0.1, 1)
            self.result_label.outline_color = (0, 0.5, 0, 1)
        else:
            # 💀 แพ้: ใช้รูปเดิม, ตัวหนังสือสีแดงขอบดำ
            self.bg_image.source = 'assets/images/bg4.png'
            self.result_label.text = "[b]GAME OVER[/b]"
            self.result_label.color = (0.9, 0.1, 0.1, 1)
            self.result_label.outline_color = (0, 0, 0, 1)
            
        self.score_label.text = f"Score: {score:,}"
        self.result_shadow.text = self.result_label.text
        self.result_shadow.outline_color = (0,0,0,1) # เงาใช้ขอบดำเสมอ

    # --- Callbacks ---
    def restart_game(self, instance):
        print(">> กดปุ่มเล่นอีกครั้ง")
        self.manager.current = 'game'

    def go_home(self, instance):
        print(">> กดปุ่มกลับหน้าเมนู")
        self.manager.current = 'start'

# --- ส่วนทดสอบรัน ---
if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager
    
    TEST_WIN = False # ลองแก้เป็น False เพื่อเทสหน้าแพ้

    class TestResultApp(App):
        def build(self):
            sm = ScreenManager()
            result_screen = ResultScreen(name='result')
            sm.add_widget(result_screen)
            # จำลองการส่งค่าคะแนน
            result_screen.update_result(is_win=TEST_WIN, score=2500)
            return sm

    TestResultApp().run()