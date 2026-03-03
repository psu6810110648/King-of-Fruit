from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.game_screen import GameScreen
from screens.start_screen import StartScreen
from screens.result_screen import ResultScreen

class KingOfFruitApp(App):
    def build(self):
        # สร้างตัวจัดการหน้าจอ
        sm = ScreenManager()
        
        # เอาหน้าจอของบิวใส่เข้าไปในระบบ แล้วตั้งชื่อให้มันว่า 'start'
        sm.add_widget(StartScreen(name='start'))
        
        # ถ้าเพื่อนทำหน้าเกมเสร็จ ก็จะเอามาต่อตรงนี้
        sm.add_widget(GameScreen(name='game'))
        
        # เพิ่มหน้าสรุปผล (Result Screen)
        sm.add_widget(ResultScreen(name='result'))
        
        # สั่งให้แอปเปิดมาเจอหน้า 'start' เป็นหน้าแรกเสมอ
        sm.current = 'start'
        
        return sm

if __name__ == '__main__':
    KingOfFruitApp().run()