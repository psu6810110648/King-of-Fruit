from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.image import Image
import random

# โหลดไฟล์หน้าตา UI
Builder.load_file('ui.kv')

class GameScreen(Screen):
    # Properties สำหรับ bind กับ UI
    slot_display = StringProperty("ช่องว่าง: 7/7")
    slot_fruits = ListProperty([])
    
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
         
        self.fruit_types = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10']
        
        # กองเก็บไพ่ (สูงสุด 7 ใบ)
        self.MAX_SLOTS = 7
        self.slots = []  # เก็บไพ่ที่ถูกคลิก
        
        # ข้อมูลไพ่ทั้งหมดในเกม
        self.tiles = []
        
        # คะแนน
        self.score = 0
        self.game_over_flag = False  
    
    def on_enter(self):
        """เรียกทุกครั้งที่เข้าหน้านี้ - เริ่มเกมใหม่"""
        self.score = 0
        self.game_over_flag = False
        self.generate_tiles()
    
    def generate_tiles(self):
        """สุ่มและสร้างไพ่บนกระดาน"""
        # ล้างไพ่เก่าออก
        game_board = self.ids.game_board
        game_board.clear_widgets()
        self.tiles = []
        self.slots = []
        self.update_slot_display()
        
        # สุ่มไพ่ - สร้าง 21 ใบ (7 ชนิด x 3 ใบ)
        tile_list = []
        for i in range(7):  # เลือก 7 ชนิดจาก 10 ชนิด
            fruit = self.fruit_types[i]
            for _ in range(3):  # ชนิดละ 3 ใบ
                tile_list.append(fruit)
        
        # สุ่มลำดับไพ่
        random.shuffle(tile_list)
        
        # สร้าง widget ไพ่
        for i, fruit in enumerate(tile_list):
            # สร้างปุ่มที่มีรูปภาพ
            tile_btn = Button(
                size_hint=(None, None),
                size=(80, 80),
                background_normal=f'assets/images/picgame/{fruit}.png',
                background_down=f'assets/images/picgame/{fruit}.png'
            )
            
            # คำนวณตำแหน่ง (วางแบบ grid และเลื่อนให้ดูซ้อนกัน)
            row = i // 7
            col = i % 7
            x = 50 + col * 90  # เว้นระยะ 90
            y = 400 - row * 60  # ซ้อนกันในแนวตั้ง เว้นระยะ 60
            
            tile_btn.pos = (x, y)
            
            # ผูกฟังก์ชันคลิก
            tile_btn.bind(on_press=lambda btn, f=fruit: self.on_tile_click_new(btn, f))
            
            # เพิ่มเข้า board
            game_board.add_widget(tile_btn)
            
            # เก็บข้อมูล
            self.tiles.append({
                'fruit': fruit,
                'widget': tile_btn,
                'visible': True
            })
        
        print(f"🎮 สร้างไพ่ {len(tile_list)} ใบเสร็จแล้ว!")
    
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
            self.game_over(is_win=False)
            return False
        
        # เพิ่มไพ่เข้ากอง
        self.slots.append(fruit_name)
        print(f"เพิ่ม {fruit_name} เข้ากอง | กองตอนนี้: {self.slots}")
        
        # อัพเดท UI
        self.update_slot_display()
        return True
    
    def on_tile_click_new(self, btn_instance, fruit_type):
        """ฟังก์ชันทำงานเมื่อคลิกไพ่ (ใช้กับระบบใหม่)"""
        if self.game_over_flag:
            return
            
        print(f"คลิกไพ่: {fruit_type}")
        
        # เพิ่มไพ่เข้ากอง
        if not self.add_to_slots(fruit_type):
            # ถ้ากองเต็ม = แพ้
            return
        
        # ซ่อนไพ่ที่ถูกคลิก
        btn_instance.disabled = True
        btn_instance.opacity = 0
        
        # เช็คว่ามีเซ็ต 3 ใบหรือยัง
        self.check_match()
        
        # เช็คว่าชนะหรือยัง
        self.check_win()
        
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
                
                # เพิ่มคะแนน
                self.score += 100
                
                # อัพเดท UI
                self.update_slot_display()
                return True
        
        return False
    
    def check_win(self):
        """เช็คว่าไพ่หมดจากกระดานหรือยัง (ชนะ)"""
        # นับไพ่ที่ยังเหลืออยู่ (ไม่ถูกซ่อน)
        visible_tiles = [t for t in self.tiles if t['widget'].opacity > 0]
        
        if len(visible_tiles) == 0:
            print("🏆 ชนะ! ไพ่หมดจากกระดาน")
            self.game_over(is_win=True)
    
    def game_over(self, is_win):
        """ฟังก์ชันจบเกม - ไปหน้า result"""
        self.game_over_flag = True
        print(f"เกมจบ! {'ชนะ' if is_win else 'แพ้'} | คะแนน: {self.score}")
        
        # ส่งข้อมูลไปหน้า result
        result_screen = self.manager.get_screen('result')
        result_screen.update_result(is_win=is_win, score=self.score)
        
        # เปลี่ยนไปหน้า result
        self.manager.current = 'result'
    
    def back_to_menu(self):
        # ฟังก์ชันปุ่มกลับหน้าเมนู
        print("กลับเมนูหลัก")