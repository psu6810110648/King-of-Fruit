from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.graphics import Color, RoundedRectangle
from kivy.app import App

# ✅ ฟอนต์เดียวกับทั้งเกม
CUSTOM_FONT = 'assets/fonts/cute.ttf'


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()

        # --- 1. 🖼️ พื้นหลัง ---
        self.bg = Image(
            source='assets/images/bg.png',
            allow_stretch=True,
            keep_ratio=False,
        )
        self.layout.add_widget(self.bg)

        # --- 2. กล่องการ์ดตรงกลาง (พื้นหลังโปร่งแสง) ---
        self.card = FloatLayout(
            size_hint=(None, None), size=(500, 520),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        with self.card.canvas.before:
            Color(0, 0, 0, 0.55)
            self.card_bg = RoundedRectangle(
                pos=self.card.pos, size=self.card.size, radius=[30]
            )
        self.card.bind(pos=self._update_card_bg, size=self._update_card_bg)
        self.layout.add_widget(self.card)

        # --- 3. Content ภายในการ์ด ---
        content = BoxLayout(
            orientation='vertical', spacing=18, padding=[40, 30, 40, 30],
            size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # --- Title ---
        lbl_title_shadow = Label(
            text="SETTINGS", font_size='48sp', font_name=CUSTOM_FONT,
            bold=True, color=(0, 0, 0, 0.5),
            size_hint_y=None, height=70,
        )
        lbl_title = Label(
            text="SETTINGS", font_size='48sp', font_name=CUSTOM_FONT,
            bold=True, color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1), outline_width=3,
            size_hint_y=None, height=70,
        )
        # ใช้ FloatLayout เพื่อซ้อน shadow + title
        title_container = FloatLayout(size_hint_y=None, height=70)
        lbl_title_shadow.pos_hint = {'center_x': 0.505, 'center_y': 0.47}
        lbl_title.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        title_container.add_widget(lbl_title_shadow)
        title_container.add_widget(lbl_title)
        content.add_widget(title_container)

        # --- BGM Volume ---
        lbl_bgm = Label(
            text="🎵  BGM Volume", font_size='22sp', font_name=CUSTOM_FONT,
            bold=True, color=(1, 0.95, 0.6, 1),
            halign='left', valign='middle',
            size_hint_y=None, height=35,
        )
        lbl_bgm.bind(size=lbl_bgm.setter('text_size'))
        content.add_widget(lbl_bgm)

        bgm_row = BoxLayout(orientation='horizontal', spacing=10,
                            size_hint_y=None, height=40)
        self.slider_bgm = Slider(
            min=0, max=100, value=50, step=1,
            cursor_size=(28, 28),
            value_track=True,
            value_track_color=(0.3, 0.85, 0.3, 1),
        )
        self.slider_bgm.bind(value=self.on_bgm_change)
        self.lbl_bgm_val = Label(
            text="50%", font_size='18sp', font_name=CUSTOM_FONT,
            bold=True, color=(1, 1, 1, 1),
            size_hint_x=None, width=60,
        )
        bgm_row.add_widget(self.slider_bgm)
        bgm_row.add_widget(self.lbl_bgm_val)
        content.add_widget(bgm_row)

        # --- SFX Volume ---
        lbl_sfx = Label(
            text="🔊  SFX Volume", font_size='22sp', font_name=CUSTOM_FONT,
            bold=True, color=(1, 0.95, 0.6, 1),
            halign='left', valign='middle',
            size_hint_y=None, height=35,
        )
        lbl_sfx.bind(size=lbl_sfx.setter('text_size'))
        content.add_widget(lbl_sfx)

        sfx_row = BoxLayout(orientation='horizontal', spacing=10,
                            size_hint_y=None, height=40)
        self.slider_sfx = Slider(
            min=0, max=100, value=100, step=1,
            cursor_size=(28, 28),
            value_track=True,
            value_track_color=(0.3, 0.6, 1, 1),
        )
        self.slider_sfx.bind(value=self.on_sfx_change)
        self.lbl_sfx_val = Label(
            text="100%", font_size='18sp', font_name=CUSTOM_FONT,
            bold=True, color=(1, 1, 1, 1),
            size_hint_x=None, width=60,
        )
        sfx_row.add_widget(self.slider_sfx)
        sfx_row.add_widget(self.lbl_sfx_val)
        content.add_widget(sfx_row)

        # --- Mute Toggle ---
        self.btn_mute = Button(
            text="🔇  MUTE ALL", font_size='24sp', font_name=CUSTOM_FONT,
            bold=True,
            background_normal='', background_color=(0, 0, 0, 0),
            size_hint_y=None, height=65,
        )
        with self.btn_mute.canvas.before:
            self.mute_btn_color = Color(0.85, 0.25, 0.25, 1)  # แดง = unmuted state
            self.mute_btn_bg = RoundedRectangle(
                pos=self.btn_mute.pos, size=self.btn_mute.size, radius=[20]
            )
        self.btn_mute.bind(pos=self._update_mute_bg, size=self._update_mute_bg)
        self.btn_mute.bind(on_press=self.toggle_mute)
        content.add_widget(self.btn_mute)

        # --- Back Button ---
        self.btn_back = Button(
            text="⬅  BACK", font_size='24sp', font_name=CUSTOM_FONT,
            bold=True,
            background_normal='', background_color=(0, 0, 0, 0),
            size_hint_y=None, height=65,
        )
        with self.btn_back.canvas.before:
            Color(0.2, 0.55, 0.2, 1)  # เขียวเข้ม
            self.back_btn_bg = RoundedRectangle(
                pos=self.btn_back.pos, size=self.btn_back.size, radius=[20]
            )
        self.btn_back.bind(pos=self._update_back_bg, size=self._update_back_bg)
        self.btn_back.bind(on_press=self.go_back)
        content.add_widget(self.btn_back)

        self.card.add_widget(content)
        self.add_widget(self.layout)

    # --- เมื่อเข้าหน้า Settings ให้ sync ค่าจาก App ---
    def on_enter(self):
        app = App.get_running_app()
        self.slider_bgm.value = int(app.bgm_volume * 100)
        self.slider_sfx.value = int(app.sfx_volume * 100)
        self._update_mute_visual(app.is_muted)

    # --- Callbacks ---
    def on_bgm_change(self, instance, value):
        app = App.get_running_app()
        app.bgm_volume = value / 100.0
        self.lbl_bgm_val.text = f"{int(value)}%"
        # อัปเดตเสียง BGM ทันที
        if app.bgm and not app.is_muted:
            app.bgm.volume = app.bgm_volume

    def on_sfx_change(self, instance, value):
        app = App.get_running_app()
        app.sfx_volume = value / 100.0
        self.lbl_sfx_val.text = f"{int(value)}%"

    def toggle_mute(self, instance):
        app = App.get_running_app()
        app.is_muted = not app.is_muted
        self._update_mute_visual(app.is_muted)

        if app.bgm:
            if app.is_muted:
                app.bgm.volume = 0
            else:
                app.bgm.volume = app.bgm_volume

    def _update_mute_visual(self, is_muted):
        if is_muted:
            self.btn_mute.text = "🔈  UNMUTE"
            self.mute_btn_color.rgba = (0.2, 0.6, 0.8, 1)  # ฟ้า = muted
        else:
            self.btn_mute.text = "🔇  MUTE ALL"
            self.mute_btn_color.rgba = (0.85, 0.25, 0.25, 1)  # แดง = unmuted

    def go_back(self, instance):
        self.manager.current = 'start'

    # --- Graphics update helpers ---
    def _update_card_bg(self, *args):
        self.card_bg.pos = self.card.pos
        self.card_bg.size = self.card.size

    def _update_mute_bg(self, *args):
        self.mute_btn_bg.pos = self.btn_mute.pos
        self.mute_btn_bg.size = self.btn_mute.size

    def _update_back_bg(self, *args):
        self.back_btn_bg.pos = self.btn_back.pos
        self.back_btn_bg.size = self.btn_back.size
