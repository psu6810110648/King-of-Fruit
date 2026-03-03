from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty

# โหลดไฟล์หน้าตา UI
Builder.load_file('ui.kv')

class GameScreen(Screen):
    # Properties สำหรับ bind กับ UI
    slot_display = StringProperty("ช่องว่าง: 7/7")
    slot_fruits = ListProperty([])
    
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        
        # รายการผลไม้ที่ใช้ในเกม
        self.fruit_types = ['ทุเรียน', 'มังคุด', 'กล้วย', 'สตรอว์เบอร์รี่', 'แอปเปิล', 'ส้ม', 'องุ่น']
        
        # กองเก็บไพ่ (สูงสุด 7 ใบ)
        self.MAX_SLOTS = 7
        self.slots = []  # เก็บไพ่ที่ถูกคลิก
    
    def update_slot_display(self):
        """อัพเดทข้อความแสดงจำนวนช่อง"""
        remaining = self.MAX_SLOTS - len(self.slots)
        self.slot_display = f"ช่องว่าง: {remaining}/{self.MAX_SLOTS}"
        self.slot_fruits = self.slots.copy()
    
    def add_to_slots(self, fruit_name):
        """เพิ่มไพ่เข้ากองเก็บ"""
        # เช็คว่ากองเต็มหรือยัง
        if len(self.slots) >= self.MAX_SLOTS:
            print("กองเต็มแล้ว! แพ้!")
            return False
        
        # เพิ่มไพ่เข้ากอง
        self.slots.append(fruit_name)
        print(f"เพิ่ม {fruit_name} เข้ากอง | กองตอนนี้: {self.slots}")
        
        # อัพเดท UI
        self.update_slot_display()
        return True
        
    def on_tile_click(self, instance):
        # ฟังก์ชันทำงานเมื่อกดโดนไพ่ผลไม้
        print(f"คลิกไพ่: {instance.text}")
        fruit_name = instance.text
        
        # เพิ่มไพ่เข้ากอง
        if not self.add_to_slots(fruit_name):
            # ถ้ากองเต็ม = แพ้
            return
        
        # เช็คว่ามีเซ็ต 3 ใบหรือยัง
        self.check_match()
        
    def check_match(self):
        """ฟังก์ชันเช็คว่าผลไม้เหมือนกัน 3 ใบหรือยัง"""
        from collections import Counter
        
        # นับจำนวนผลไม้แต่ละชนิดในกอง
        fruit_count = Counter(self.slots)
        
        # เช็คว่ามีผลไม้ไหนครบ 3 ใบหรือไม่
        for fruit, count in fruit_count.items():
            if count >= 3:
                # เจอเซ็ต 3 ใบ! ลบออก 3 ใบ
                print(f"🎉 เจอเซ็ต! {fruit} x3 - ลบออกจากกอง")
                for _ in range(3):
                    self.slots.remove(fruit)
                print(f"กองหลังลบ: {self.slots}")
                
                # อัพเดท UI
                self.update_slot_display()
                return True
        
        return False
    
    def back_to_menu(self):
        # ฟังก์ชันปุ่มกลับหน้าเมนู
        print("กลับเมนูหลัก")