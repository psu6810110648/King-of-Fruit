from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.audio import SoundLoader 

# นำเข้าหน้าจอต่างๆ ของเกม (Screens)
from screens.start_screen import StartScreen
from screens.result_screen import ResultScreen
from screens.game_screen import GameScreen
from screens.settings_screen import SettingsScreen
from screens.level_select_screen import LevelSelectScreen

class KingOfFruitApp(App):
    def build(self):
        # 🟢 ตัวแปรส่วนกลาง (Global State) สำหรับใช้ทุกหน้าจอ
        self.bgm_volume = 0.5    # ความดังเพลงพื้นหลัง
        self.sfx_volume = 1.0    # ความดังเอฟเฟกต์
        self.is_muted = False    # สถานะเปิด/ปิดเสียง
        self.unlocked_level = 1  # ด่านสูงสุดที่ปลดล็อคแล้ว

        # 🖥️ ตัวจัดการหน้าจอ (ScreenManager)
        sm = ScreenManager()
        # นำหน้าเจอแต่ละหน้าเข้ามาในระบบ
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(ResultScreen(name='result'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(LevelSelectScreen(name='level_select'))
        sm.current = 'start'  # ตั้งค่าให้เริ่มที่หน้าเมนูหลัก
        
        # 🎵 ระบบเสียงเพลงพื้นหลัง (BGM)
        self.bgm = SoundLoader.load('assets/sounds/bgm.mp3')
        if self.bgm:
            self.bgm.loop = True               # เล่นวนซ้ำ
            self.bgm.volume = self.bgm_volume  # ระดับเสียงตอนเริ่ม
            self.bgm.play()                    # เริ่มเล่นเพลง
            print(">> BGM Started!")
        else:
            print("!! Warning: หาไฟล์ bgm.mp3 ไม่เจอ")
            
        return sm

    def on_stop(self):
        # ฟังก์ชันทำงานเมื่อแอปปิด หยุดเสียงเพลงอัตโนมัติ
        if hasattr(self, 'bgm') and self.bgm:
            self.bgm.stop()

# 🚀 จุดรันโปรแกรมหลัก
if __name__ == '__main__':
    KingOfFruitApp().run()