# ไฟล์: game_screen.py
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# โหลดไฟล์หน้าตา UI
Builder.load_file('ui.kv')

class GameScreen(Screen):
    def on_tile_click(self, instance):
        # ฟังก์ชันทำงานเมื่อกดโดนไพ่ผลไม้ (ตอนนี้ให้ print เทสไปก่อน)
        print(f"คลิกไพ่: {instance.text}")
        
    def check_match(self):
        # ฟังก์ชันเช็คว่าผลไม้เหมือนกัน 3 ใบหรือยัง
        pass
        
    def back_to_menu(self):
        # ฟังก์ชันปุ่มกลับหน้าเมนู
        print("กลับเมนูหลัก")