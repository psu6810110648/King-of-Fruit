from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# ดึงหน้าจอ StartScreen ที่บิวสร้างไว้มาใช้งาน
from screens.start_screen import StartScreen
# from screens.game_screen import GameScreen  # (บรรทัดนี้ใส่ # ปิดไว้ก่อน รอนะดาทำเสร็จ)

class KingOfFruitApp(App):
    def build(self):
        # สร้างตัวจัดการหน้าจอ
        sm = ScreenManager()
        
        # เอาหน้าจอของบิวใส่เข้าไปในระบบ แล้วตั้งชื่อให้มันว่า 'start'
        sm.add_widget(StartScreen(name='start'))
        
        # ถ้าเพื่อนทำหน้าเกมเสร็จ ก็จะเอามาต่อตรงนี้
        # sm.add_widget(GameScreen(name='game'))
        
        # สั่งให้แอปเปิดมาเจอหน้า 'start' เป็นหน้าแรกเสมอ
        sm.current = 'start'
        
        return sm

if __name__ == '__main__':
    KingOfFruitApp().run()