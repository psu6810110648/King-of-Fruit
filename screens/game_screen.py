from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
import random
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.animation import Animation

# --- 1. คลาสหลอดเวลา (เหมือนเดิม) ---
class TimeBar(Widget):
    def __init__(self, max_value=60, **kwargs):
        super().__init__(**kwargs)
        self.max_value = max_value
        self.value = max_value
        with self.canvas:
            Color(0.2, 0.2, 0.2, 0.8)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
            self.fg_color = Color(0, 0.8, 0, 1)
            self.fg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.update_bar(self.value)

    def update_bar(self, current_value):
        self.value = current_value
        percent = max(0, min(1, current_value / self.max_value))
        self.fg_rect.pos = self.pos
        self.fg_rect.size = (self.width, self.height * percent)
        if percent > 0.5: self.fg_color.rgba = (0.2, 0.8, 0.2, 1)
        elif percent > 0.2: self.fg_color.rgba = (1, 0.8, 0, 1)
        else: self.fg_color.rgba = (1, 0.2, 0.2, 1)

# --- 2. คลาสปุ่มไพ่ (เหมือนเดิม) ---
class TileButton(Button):
    def __init__(self, fruit_source, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        with self.canvas.before:
            Color(0, 0, 0, 0.2)
            self.shadow = RoundedRectangle(pos=(self.x+3, self.y-3), size=self.size, radius=[15])
            Color(0.95, 0.95, 0.9, 1)
            self.card_bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        with self.canvas.after:
            Color(1, 1, 1, 1)
            pad = 10
            self.fruit_rect = Rectangle(source=fruit_source, 
                                      pos=(self.x+pad, self.y+pad), 
                                      size=(self.width-pad*2, self.height-pad*2))
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.shadow.pos = (self.x+3, self.y-3)
        self.shadow.size = self.size
        self.card_bg.pos = self.pos
        self.card_bg.size = self.size
        pad = 10
        self.fruit_rect.pos = (self.x+pad, self.y+pad)
        self.fruit_rect.size = (self.width-pad*2, self.height-pad*2)

# --- 3. คลาสช่องด้านล่าง (เหมือนเดิม) ---
class EmptySlot(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1, 0.2) 
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
            Color(1, 1, 1, 0.5)
            self.line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 10), width=1.5)
        self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.line.rounded_rectangle=(self.x, self.y, self.width, self.height, 10)

class FilledSlot(Widget):
    def __init__(self, fruit_source, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
            Color(1, 1, 1, 1)
            self.img = Rectangle(source=fruit_source, pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        pad = 5
        self.img.pos = (self.x + pad, self.y + pad)
        self.img.size = (self.width - pad*2, self.height - pad*2)

# --- 4. หน้าจอเกมหลัก (รองรับหลายด่าน) ---
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.fruit_types = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10']
        self.MAX_SLOTS = 7
        self.current_level = 1 # เก็บด่านปัจจุบัน
        self.slots = []
        self.tiles = []
        self.score = 0
        self.game_over_flag = False
        self.is_paused = False
        
        self.layout = FloatLayout()
        
        # Background
        self.bg = Image(source='assets/images/bg.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.bg)
        
        # Game Board (Grid จะถูกตั้งค่าใหม่ตอนเริ่มด่าน)
        self.game_board = GridLayout(spacing=10, padding=20,
                                     size_hint=(0.85, 0.6),
                                     pos_hint={'center_x': 0.45, 'center_y': 0.55})
        self.layout.add_widget(self.game_board)
        
        # Grid สำหรับช่องด้านล่าง
        self.slot_grid = GridLayout(rows=1, cols=7, spacing=10, padding=10,
                                    size_hint=(None, None), size=(650, 100),
                                    pos_hint={'center_x': 0.45, 'y': 0.025})
        self.layout.add_widget(self.slot_grid)

        # Time Bar & Label
        self.time_bar = TimeBar(max_value=60, size_hint=(None, None), size=(30, 400),
                                pos_hint={'right': 0.96, 'center_y': 0.5})
        self.layout.add_widget(self.time_bar)
            
        self.lbl_time = Label(
            text="Time", font_size='24sp', bold=True, halign='center',
            color=(1, 1, 1, 1), outline_color=(0, 0, 0, 1), outline_width=2,
            pos_hint={'center_x': 0.945, 'center_y': 0.85}
        )
        self.layout.add_widget(self.lbl_time)

        # Level Label (บอกว่าอยู่ด่านไหน)
        self.lbl_level = Label(
            text="LEVEL 1", font_size='30sp', bold=True,
            color=(1, 1, 0, 1), outline_color=(0, 0, 0, 1), outline_width=2,
            # 👇 แก้ตรงนี้: กำหนดขนาดกล่อง (สำคัญ!) และย้ายไปไว้ข้างบน
            size_hint=(None, None), size=(200, 50),
            pos_hint={'center_x': 0.5, 'top': 0.96} 
        )
        self.layout.add_widget(self.lbl_level)

        # ปุ่ม Pause
        self.btn_pause = Button(
            text="II", font_size='24sp', bold=True,
            background_color=(1, 0.6, 0, 1),
            size_hint=(None, None), size=(60, 60),
            pos_hint={'x': 0.02, 'top': 0.98}
        )
        self.btn_pause.bind(on_press=self.toggle_pause)
        self.layout.add_widget(self.btn_pause)

        self.create_pause_overlay()
        self.add_widget(self.layout)

    def create_pause_overlay(self):
        self.pause_menu = FloatLayout()
        with self.pause_menu.canvas.before:
            Color(0, 0, 0, 0.7)
            Rectangle(pos=(0,0), size=(2000, 2000))

        menu_box = BoxLayout(orientation='vertical', spacing=20, size_hint=(None, None), size=(300, 250),
                             pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        lbl_paused = Label(text="PAUSED", font_size='40sp', bold=True, color=(1, 1, 1, 1))
        menu_box.add_widget(lbl_paused)

        btn_resume = Button(text="RESUME", font_size='20sp', background_color=(0.2, 0.8, 0.2, 1))
        btn_resume.bind(on_press=self.toggle_pause)
        menu_box.add_widget(btn_resume)

        btn_exit = Button(text="EXIT TO MENU", font_size='20sp', background_color=(0.8, 0.2, 0.2, 1))
        btn_exit.bind(on_press=self.go_to_menu)
        menu_box.add_widget(btn_exit)

        self.pause_menu.add_widget(menu_box)

    def toggle_pause(self, instance):
        if self.game_over_flag: return
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.layout.add_widget(self.pause_menu)
        else:
            self.layout.remove_widget(self.pause_menu)

    def go_to_menu(self, instance):
        self.layout.remove_widget(self.pause_menu)
        self.is_paused = False
        self.manager.current = 'start'

    def on_enter(self):
        # 👇 เช็คว่าต้องเริ่มด่านไหน
        # ถ้าไม่มีการส่งค่ามา ให้เริ่มด่าน 1
        if not hasattr(self, 'target_level'):
            self.target_level = 1
        
        self.start_level(self.target_level)

    def start_level(self, level):
        self.current_level = level
        self.score = 0
        self.game_over_flag = False
        self.is_paused = False
        if self.pause_menu.parent: self.layout.remove_widget(self.pause_menu)
        
        self.lbl_level.text = f"LEVEL {self.current_level}"

        # --- ⚙️ ตั้งค่าความยากแต่ละด่าน ---
        if self.current_level == 1:
            self.GAME_TIME = 60
            self.cols_num = 7  # กระดาน 7 แถว (21 ใบ)
            self.bg.source = 'assets/images/bg.png' # พื้นหลังด่าน 1
        elif self.current_level == 2:
            self.GAME_TIME = 50 # เวลาลดลง!
            self.cols_num = 8   # กระดานกว้างขึ้นเป็น 8 แถว (24 ใบ)
            self.bg.source = 'assets/images/bg2.png' # พื้นหลังด่าน 2 ⚠️ อย่าลืมหาไฟล์นี้นะ!
        # -------------------------------

        self.time_left = self.GAME_TIME
        self.lbl_time.text = f"Time\n{self.time_left}"
        self.time_bar.max_value = self.GAME_TIME
        self.time_bar.update_bar(self.time_left)
        
        # ตั้งค่า Grid Layout ใหม่ตามความยาก
        self.game_board.cols = self.cols_num
        self.game_board.clear_widgets()
        
        self.generate_tiles()
        self.timer_event = Clock.schedule_interval(self.update_time, 1)

    def update_time(self, dt):
        if self.game_over_flag or self.is_paused: return
        self.time_left -= 1
        self.lbl_time.text = f"Time\n{self.time_left}"
        self.time_bar.update_bar(self.time_left)
        if self.time_left <= 0:
            self.game_over(is_win=False)

    def generate_tiles(self):
        self.tiles = []
        self.slots = []
        self.update_visual_slots() 
        
        # คำนวณจำนวนไพ่ตามขนาดกระดาน
        # ด่าน 1: 7x3 = 21 ใบ
        # ด่าน 2: 8x3 = 24 ใบ
        total_tiles = self.cols_num * 3 
        
        tile_list = []
        # สุ่มผลไม้ให้ครบจำนวน (ต้องหาร 3 ลงตัวเสมอ)
        current_fruit_idx = 0
        while len(tile_list) < total_tiles:
            fruit = self.fruit_types[current_fruit_idx % len(self.fruit_types)]
            for _ in range(3): # เพิ่มทีละ 3 ใบ (1 ชุด)
                tile_list.append(fruit)
            current_fruit_idx += 1
            
        random.shuffle(tile_list)
        
        for fruit in tile_list:
            tile_btn = TileButton(fruit_source=f'assets/images/picgame/{fruit}.png', 
                                  size_hint=(None, None), size=(80, 80))
            tile_btn.bind(on_press=lambda btn, f=fruit: self.on_tile_click_new(btn, f))
            self.game_board.add_widget(tile_btn)
            self.tiles.append({'fruit': fruit, 'widget': tile_btn})

    def on_tile_click_new(self, btn_instance, fruit_type):
        if self.game_over_flag or self.is_paused: return
        self.play_sound('click.wav')
        if len(self.slots) >= self.MAX_SLOTS: return

        self.slots.append(fruit_type)
        btn_instance.disabled = True
        btn_instance.opacity = 0
        
        self.update_visual_slots()
        self.check_match()
        
        if len(self.slots) >= self.MAX_SLOTS:
            self.game_over(is_win=False)
            return

        self.check_win()

    def update_visual_slots(self):
        self.slot_grid.clear_widgets()
        for fruit in self.slots:
            slot = FilledSlot(fruit_source=f'assets/images/picgame/{fruit}.png',
                              size_hint=(None, None), size=(80, 80))
            self.slot_grid.add_widget(slot)
        remaining = self.MAX_SLOTS - len(self.slots)
        for _ in range(remaining):
            slot = EmptySlot(size_hint=(None, None), size=(80, 80))
            self.slot_grid.add_widget(slot)

    def check_match(self):
        from collections import Counter
        fruit_count = Counter(self.slots)
        for fruit, count in fruit_count.items():
            if count >= 3:
                self.play_sound('match.wav')
                for _ in range(3): self.slots.remove(fruit)
                self.score += 100
                self.update_visual_slots()
                return True
        return False

    def check_win(self):
        visible_tiles = [t for t in self.tiles if t['widget'].opacity > 0]
        if len(visible_tiles) == 0:
            self.game_over(is_win=True)

    def game_over(self, is_win):
        self.game_over_flag = True
        if hasattr(self, 'timer_event'): self.timer_event.cancel()
        
        result_screen = self.manager.get_screen('result')
        # ส่งข้อมูลไปด้วยว่าตอนนี้อยู่ Level ไหน
        result_screen.update_result(is_win=is_win, score=self.score, current_level=self.current_level)
        self.manager.current = 'result'

    def on_leave(self):
        if hasattr(self, 'timer_event'): self.timer_event.cancel()

    def play_sound(self, sound_file):
        try:
            sound = SoundLoader.load(f'assets/sounds/{sound_file}')
            if sound: 
                sound.volume = 1.0
                sound.play()
        except:
            pass