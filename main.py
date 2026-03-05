from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.audio import SoundLoader 
from screens.start_screen import StartScreen
from screens.result_screen import ResultScreen
from screens.game_screen import GameScreen

class KingOfFruitApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(ResultScreen(name='result'))
        sm.current = 'start'
        
        self.bgm = SoundLoader.load('assets/sounds/bgm.mp3')
        if self.bgm:
            self.bgm.loop = True  # สั่งให้วนซ้ำ
            self.bgm.volume = 0.5 # ปรับความดัง (0.0 ถึง 1.0)
            self.bgm.play()       # เริ่มเล่นเลย
            print(">> BGM Started!")
        else:
            print("!! Warning: หาไฟล์ bgm.mp3 ไม่เจอ")
            
        return sm

    # เพิ่มฟังก์ชันปิดเพลงตอนปิดแอป (กันเพลงค้าง)
    def on_stop(self):
        if hasattr(self, 'bgm') and self.bgm:
            self.bgm.stop()

if __name__ == '__main__':
    KingOfFruitApp().run()