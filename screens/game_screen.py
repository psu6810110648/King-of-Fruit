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

# ✅ ชื่อฟอนต์น่ารัก
CUSTOM_FONT = 'assets/fonts/cute.ttf' 

# --- 1. คลาสหลอดเวลา ---
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

# --- 2. คลาสปุ่มไพ่ ---
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

# --- 3. คลาสช่องด้านล่าง ---
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

# --- 4. หน้าจอเกมหลัก (Final Fix: Sticker Layer Order) ---
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.fruit_types = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10']
        self.MAX_SLOTS = 7
        self.current_level = 1 
        self.slots = []
        self.tiles = []
        self.score = 0
        self.game_over_flag = False
        self.is_paused = False
        
        self.layout = FloatLayout()
        
        # Background
        self.bg = Image(source='assets/images/bg.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.bg)
        
        # Game Board
        self.game_board = GridLayout(spacing=10, padding=20,
                                     size_hint=(0.85, 0.6),
                                     pos_hint={'center_x': 0.45, 'center_y': 0.55})
        self.layout.add_widget(self.game_board)
        
        # Slot Grid
        self.slot_grid = GridLayout(rows=1, cols=7, spacing=10, padding=10,
                                    size_hint=(None, None), size=(650, 100),
                                    pos_hint={'center_x': 0.45, 'y': 0.025})
        self.layout.add_widget(self.slot_grid)

        # Time Bar
        self.time_bar = TimeBar(max_value=60, size_hint=(None, None), size=(30, 400),
                                pos_hint={'right': 0.96, 'center_y': 0.5})
        self.layout.add_widget(self.time_bar)
            
        self.lbl_time = Label(
            text="Time", font_size='24sp', bold=True, halign='center',
            color=(1, 1, 1, 1), outline_color=(0, 0, 0, 1), outline_width=2,
            pos_hint={'center_x': 0.945, 'center_y': 0.85}
        )
        self.layout.add_widget(self.lbl_time)

        # Level Label
        self.lbl_level = Label(
            text="LEVEL 1", font_size='24sp', bold=True,
            color=(1, 1, 0, 1), outline_color=(0, 0, 0, 1), outline_width=2,
            size_hint=(None, None), size=(150, 50),
            pos_hint={'center_x': 0.945, 'top': 0.98} 
        )
        self.layout.add_widget(self.lbl_level)

        # Pause Button
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
        if self.pause_menu.parent: self.layout.remove_widget(self.pause_menu)
        self.is_paused = False
        self.manager.current = 'start'

    def on_enter(self):
        if not hasattr(self, 'target_level'):
            self.target_level = 1
        self.start_level(self.target_level)

    def start_level(self, level):
        self.current_level = level
        self.score = 0
        self.game_over_flag = False
        self.is_paused = False
        
        if hasattr(self, 'result_popup') and self.result_popup.parent:
            self.layout.remove_widget(self.result_popup)
        if self.pause_menu.parent: 
            self.layout.remove_widget(self.pause_menu)
        
        self.lbl_level.text = f"LEVEL {self.current_level}"

        if self.current_level == 1:
            self.GAME_TIME = 60
            self.cols_num = 7 
            self.bg.source = 'assets/images/bg.png'
        elif self.current_level == 2:
            self.GAME_TIME = 50 
            self.cols_num = 8
            self.bg.source = 'assets/images/bg2.png'
        
        self.time_left = self.GAME_TIME
        self.lbl_time.text = f"Time\n{self.time_left}"
        self.time_bar.max_value = self.GAME_TIME
        self.time_bar.update_bar(self.time_left)
        
        self.game_board.cols = self.cols_num
        self.game_board.clear_widgets()
        
        self.generate_tiles()
        
        if hasattr(self, 'timer_event'): self.timer_event.cancel()
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
        
        total_tiles = self.cols_num * 3 
        tile_list = []
        current_fruit_idx = 0
        while len(tile_list) < total_tiles:
            fruit = self.fruit_types[current_fruit_idx % len(self.fruit_types)]
            for _ in range(3): tile_list.append(fruit)
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
        if self.game_over_flag: return 
        self.game_over_flag = True
        if hasattr(self, 'timer_event'): self.timer_event.cancel()
        self.show_popup(is_win)

    # --- ✨ Popup System (Cute & Correct Layer Order) ✨ ---
    def show_popup(self, is_win):
        popup = FloatLayout()
        self.result_popup = popup
        
        # 1. ฉากหลัง Dim
        with popup.canvas.before:
            Color(0, 0, 0, 0.6)
            popup.bg_rect = Rectangle(pos=(0, 0), size=(2000, 2000))
            
        def update_dim_bg(instance, value):
            if hasattr(instance, 'bg_rect'):
                instance.bg_rect.pos = instance.pos
                instance.bg_rect.size = instance.size
        popup.bind(pos=update_dim_bg, size=update_dim_bg)

        # Container
        popup_container = FloatLayout(size_hint=(None, None), size=(450, 420),
                                      pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # --- 2. สร้างกล่องเนื้อหาหลัก (แต่ยังไม่ Add ลง Container) ---
        content_box = BoxLayout(orientation='vertical', spacing=15, padding=30,
                                size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        with content_box.canvas.before:
            Color(1, 1, 1, 1)
            content_box.bg_rect = RoundedRectangle(pos=content_box.pos, size=content_box.size, radius=[35]) 
            Color(1, 0.85, 0.4, 1) # ขอบส้มทอง
            content_box.border_line = Line(rounded_rectangle=(content_box.x, content_box.y, content_box.width, content_box.height, 35), width=5)
            
        def update_content_bg(instance, value):
            if hasattr(instance, 'bg_rect'):
                instance.bg_rect.pos = instance.pos
                instance.bg_rect.size = instance.size
                instance.border_line.rounded_rectangle = (instance.x, instance.y, instance.width, instance.height, 35)
        content_box.bind(pos=update_content_bg, size=update_content_bg)

        # ใส่ข้อความ ปุ่ม ต่างๆ ลงใน Content Box
        title_text = "YOU WIN! 🎉" if is_win else "GAME OVER 💀"
        title_color = (0, 0.7, 0, 1) if is_win else (0.9, 0.3, 0.3, 1)
        lbl_title = Label(text=title_text, font_size='40sp', bold=True, color=title_color, font_name=CUSTOM_FONT)
        content_box.add_widget(lbl_title)

        lbl_score = Label(text=f"Score: {self.score}", font_size='32sp', bold=True, color=(0.4, 0.4, 0.4, 1), font_name=CUSTOM_FONT)
        content_box.add_widget(lbl_score)

        btn_action = Button(font_size='28sp', bold=True, size_hint=(1, None), height=75,
                            background_normal='', background_color=(0, 0, 0, 0), font_name=CUSTOM_FONT)
        if is_win:
            if self.current_level == 1:
                btn_action.text = "NEXT LEVEL >>"
                btn_action.bind(on_press=self.action_next_level)
                btn_color = (0.3, 0.8, 0.3, 1) 
            else:
                btn_action.text = "PLAY AGAIN"
                btn_action.bind(on_press=self.action_restart)
                btn_color = (0.3, 0.7, 1, 1)
        else:
            btn_action.text = "TRY AGAIN"
            btn_action.bind(on_press=self.action_restart)
            btn_color = (1, 0.5, 0.5, 1)

        with btn_action.canvas.before:
            Color(*btn_color)
            btn_action.bg_rect = RoundedRectangle(pos=btn_action.pos, size=btn_action.size, radius=[25])
        
        def update_btn(inst, val): 
            if hasattr(inst, 'bg_rect'):
                inst.bg_rect.pos = inst.pos
                inst.bg_rect.size = inst.size
        btn_action.bind(pos=update_btn, size=update_btn)
        content_box.add_widget(btn_action)

        btn_home = Button(text="HOME", font_size='22sp', bold=True, 
                          color=(0.6, 0.6, 0.6, 1), 
                          background_normal='', background_color=(0,0,0,0),
                          size_hint=(1, None), height=45, font_name=CUSTOM_FONT)
        btn_home.bind(on_press=self.go_to_menu)
        content_box.add_widget(btn_home)

        # -----------------------------------------------
        # 🔑 จุดสำคัญอยู่ตรงนี้ครับ! (สลับลำดับการ Add)
        # -----------------------------------------------
        
        # 1. ใส่ "กล่องขาว" ลงไปก่อน (ให้มันอยู่ข้างหลัง)
        popup_container.add_widget(content_box)

        # 2. ค่อยใส่ "สติกเกอร์" ตามลงไปทีหลัง (มันจะทับอยู่ข้างบน)
        deco_fruits = random.sample(self.fruit_types, 4)
        
        deco1 = Image(source=f'assets/images/picgame/{deco_fruits[0]}.png', size_hint=(None, None), size=(80, 80), pos_hint={'x': -0.08, 'top': 1.08})
        popup_container.add_widget(deco1) # 👈 สติกเกอร์อยู่บน

        deco2 = Image(source=f'assets/images/picgame/{deco_fruits[1]}.png', size_hint=(None, None), size=(80, 80), pos_hint={'right': 1.08, 'top': 1.08})
        popup_container.add_widget(deco2) # 👈 สติกเกอร์อยู่บน
        
        deco3 = Image(source=f'assets/images/picgame/{deco_fruits[2]}.png', size_hint=(None, None), size=(70, 70), pos_hint={'x': -0.06, 'y': -0.06})
        popup_container.add_widget(deco3) # 👈 สติกเกอร์อยู่บน

        deco4 = Image(source=f'assets/images/picgame/{deco_fruits[3]}.png', size_hint=(None, None), size=(90, 90), pos_hint={'right': 1.06, 'y': -0.04})
        popup_container.add_widget(deco4) # 👈 สติกเกอร์อยู่บน

        popup.add_widget(popup_container)

        if popup.parent is None:
            self.layout.add_widget(popup)

    # --- Action Buttons ---
    def action_next_level(self, instance):
        if hasattr(self, 'result_popup') and self.result_popup.parent:
            self.layout.remove_widget(self.result_popup)
        self.start_level(self.current_level + 1)

    def action_restart(self, instance):
        if hasattr(self, 'result_popup') and self.result_popup.parent:
            self.layout.remove_widget(self.result_popup)
        self.start_level(1)

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