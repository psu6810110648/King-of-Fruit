from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# โหลดไฟล์หน้าตา UI
Builder.load_file('ui.kv')

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        
        # รายการผลไม้ที่ใช้ในเกม
        self.fruit_types = ['ทุเรียน', 'มังคุด', 'กล้วย', 'สตรอว์เบอร์รี่', 'แอปเปิล', 'ส้ม', 'องุ่น']
        
        # กองเก็บไพ่ (สูงสุด 7 ใบ)
        self.MAX_SLOTS = 7
        self.slots = []  # เก็บไพ่ที่ถูกคลิก
    
    def add_to_slots(self, fruit_name):
        """เพิ่มไพ่เข้ากองเก็บ"""
        # เช็คว่ากองเต็มหรือยัง
        if len(self.slots) >= self.MAX_SLOTS:
            print("กองเต็มแล้ว! แพ้!")
            return False
        
        # เพิ่มไพ่เข้ากอง
        self.slots.append(fruit_name)
        print(f"เพิ่ม {fruit_name} เข้ากอง | กองตอนนี้: {self.slots}")
        return True
        
    def on_tile_click(self, instance):
        # ฟังก์ชันทำงานเมื่อกดโดนไพ่ผลไม้
        print(f"คลิกไพ่: {instance.text}")
        fruit_name = instance.text
        
        # เพิ่มไพ่เข้ากอง
        self.add_to_slots(fruit_name)
        
    def check_match(self):
        # ฟังก์ชันเช็คว่าผลไม้เหมือนกัน 3 ใบหรือยัง
        pass
        
    def back_to_menu(self):
        # ฟังก์ชันปุ่มกลับหน้าเมนู
        print("กลับเมนูหลัก")