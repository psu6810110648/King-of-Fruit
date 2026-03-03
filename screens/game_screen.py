from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Rectangle
import random
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

# --- 1. คลาสหลอดเวลาแนวตั้ง (เหมือนเดิม) ---
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
        
        # แนวตั้ง
        self.fg_rect.pos = self.pos
        self.fg_rect.size = (self.width, self.height * percent)
        
        # เปลี่ยนสี
        if percent > 0.5:
            self.fg_color.rgba = (0.2, 0.8, 0.2, 1)
        elif percent > 0.2:
            self.fg_color.rgba = (1, 0.8, 0, 1)
        else:
            self.fg_color.rgba = (1, 0.2, 0.2, 1)

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

# --- 3. หน้าจอเกมหลัก ---
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.fruit_types = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10']
        self.MAX_SLOTS = 7
        self.GAME_TIME = 60
        self.slots = []
        self.tiles = []
        self.score = 0
        self.game_over_flag = False
        self.time_left = self.GAME_TIME
        
        self.layout = FloatLayout()
        
        # 1. Background
        self.bg = Image(source='assets/images/bg.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.bg)
        
        # 2. Game Board
        self.game_board = GridLayout(cols=7, spacing=10, padding=20,
                                     size_hint=(0.85, 0.6),
                                     pos_hint={'center_x': 0.45, 'center_y': 0.55})
        self.layout.add_widget(self.game_board)
        
        # 3. Slot Bar Background
        with self.layout.canvas.after:
            Color(0.2, 0.2, 0.2, 0.9)
            self.slot_bg = RoundedRectangle(pos=(40, 20), size=(650, 100), radius=[20])

        # 4. หลอดเวลาแนวตั้ง
        self.time_bar = TimeBar(max_value=self.GAME_TIME, 
                                size_hint=(None, None), size=(30, 400),
                                pos_hint={'right': 0.96, 'center_y': 0.5})
        self.layout.add_widget(self.time_bar)
            
        # 5. 👇 แก้ตรงนี้: เพิ่มคำว่า Time และจัดกึ่งกลาง (halign='center')
        self.lbl_time = Label(
            text=f"Time\n{self.GAME_TIME}",  # ขึ้นบรรทัดใหม่
            font_size='24sp', bold=True,
            halign='center',  # จัดกึ่งกลางตัวหนังสือ
            color=(1, 1, 1, 1), outline_color=(0, 0, 0, 1), outline_width=2,
            pos_hint={'center_x': 0.945, 'center_y': 0.85}
        )
        self.layout.add_widget(self.lbl_time)

        # Slot Label
        self.lbl_slots = Label(
            text="Slots: 0/7", font_size='24sp', bold=True,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.45, 'y': 0.05}
        )
        self.layout.add_widget(self.lbl_slots)

        self.add_widget(self.layout)

    def on_enter(self):
        self.score = 0
        self.game_over_flag = False
        self.time_left = self.GAME_TIME
        # 👇 อัปเดตข้อความตอนเริ่ม
        self.lbl_time.text = f"Time\n{self.time_left}"
        self.time_bar.update_bar(self.time_left)
        self.generate_tiles()
        self.timer_event = Clock.schedule_interval(self.update_time, 1)

    def update_time(self, dt):
        if self.game_over_flag: return
        self.time_left -= 1
        
        # 👇 อัปเดตข้อความตอนนับถอยหลัง
        self.lbl_time.text = f"Time\n{self.time_left}"
        self.time_bar.update_bar(self.time_left)
        
        if self.time_left <= 0:
            self.game_over(is_win=False)

    def generate_tiles(self):
        self.game_board.clear_widgets()
        self.tiles = []
        self.slots = []
        self.update_slot_label()
        
        tile_list = []
        for i in range(7):
            fruit = self.fruit_types[i]
            for _ in range(3):
                tile_list.append(fruit)
        random.shuffle(tile_list)
        
        for fruit in tile_list:
            tile_btn = TileButton(fruit_source=f'assets/images/picgame/{fruit}.png', 
                                  size_hint=(None, None), size=(80, 80))
            tile_btn.bind(on_press=lambda btn, f=fruit: self.on_tile_click_new(btn, f))
            self.game_board.add_widget(tile_btn)
            self.tiles.append({'fruit': fruit, 'widget': tile_btn})

    def on_tile_click_new(self, btn_instance, fruit_type):
        if self.game_over_flag: return
        self.play_sound('click.wav')
        
        if len(self.slots) >= self.MAX_SLOTS: return

        self.slots.append(fruit_type)
        btn_instance.disabled = True
        btn_instance.opacity = 0
        
        self.update_slot_label()
        self.check_match()
        self.check_win()

    def update_slot_label(self):
        self.lbl_slots.text = f"Slots: {len(self.slots)}/{self.MAX_SLOTS}"

    def check_match(self):
        from collections import Counter
        fruit_count = Counter(self.slots)
        for fruit, count in fruit_count.items():
            if count >= 3:
                self.play_sound('match.wav')
                for _ in range(3): self.slots.remove(fruit)
                self.score += 100
                self.update_slot_label()
                return True
        return False

    def check_win(self):
        visible_tiles = [t for t in self.tiles if t['widget'].opacity > 0]
        if len(visible_tiles) == 0:
            self.game_over(is_win=True)

    def game_over(self, is_win):
        self.game_over_flag = True
        result_screen = self.manager.get_screen('result')
        result_screen.update_result(is_win=is_win, score=self.score)
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