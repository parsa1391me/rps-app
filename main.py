from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import random

# تنظیمات اولیه پنجره
Window.clearcolor = get_color_from_hex('#1A1A2E')

class StyledButton(Button):
    """دکمه سفارشی با گوشه‌های گرد"""
    def __init__(self, bg_color='#0F3460', **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # شفاف کردن پس‌زمینه پیش‌فرض
        self.bg_color = get_color_from_hex(bg_color)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15,])

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=15)
        
        layout.add_widget(Label(text='RPS ULTIMATE', font_size='45sp', bold=True, color=get_color_from_hex('#E94560')))

        # بخش دریافت نام‌ها
        self.p1_input = TextInput(text='Player 1', multiline=False, size_hint_y=None, height=50, halign='center')
        self.p2_input = TextInput(text='Player 2', multiline=False, size_hint_y=None, height=50, halign='center')
        
        layout.add_widget(Label(text="Enter Names:", font_size='18sp'))
        layout.add_widget(self.p1_input)
        layout.add_widget(self.p2_input)

        btn_ai = StyledButton(text='VS COMPUTER', bg_color='#16213E', size_hint_y=0.2)
        btn_ai.bind(on_press=self.start_ai)
        
        btn_pvp = StyledButton(text='MULTIPLAYER', bg_color='#E94560', size_hint_y=0.2)
        btn_pvp.bind(on_press=self.start_pvp)

        layout.add_widget(btn_ai)
        layout.add_widget(btn_pvp)
        self.add_widget(layout)

    def start_ai(self, instance):
        self.manager.get_screen('game').setup_game('AI', self.p1_input.text, "AI Bot")
        self.manager.current = 'game'

    def start_pvp(self, instance):
        self.manager.get_screen('game').setup_game('PvP', self.p1_input.text, self.p2_input.text)
        self.manager.current = 'game'

class GameScreen(Screen):
    def setup_game(self, mode, p1, p2):
        self.game_mode = mode
        self.p1_name = p1
        self.p2_name = p2
        self.p1_choice = None
        self.status_label.text = f"Welcome {p1}!\nMake your move."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        self.status_label = Label(text='Ready?', font_size='28sp', halign='center')
        self.layout.add_widget(self.status_label)

        self.btns = GridLayout(cols=3, spacing=15, size_hint_y=0.4)
        choices = [('Rock', '#E94560'), ('Paper', '#0F3460'), ('Scissors', '#533483')]
        
        for text, color in choices:
            btn = StyledButton(text=text, bg_color=color, font_size='20sp')
            btn.bind(on_press=self.handle_choice)
            self.btns.add_widget(btn)
        
        self.layout.add_widget(self.btns)

        btn_back = StyledButton(text='Exit to Menu', bg_color='#333333', size_hint_y=0.15)
        btn_back.bind(on_press=self.go_back)
        self.layout.add_widget(btn_back)
        self.add_widget(self.layout)

    def handle_choice(self, instance):
        if self.game_mode == 'AI':
            p2_choice = random.choice(['Rock', 'Paper', 'Scissors'])
            self.show_result(instance.text, p2_choice)
        else:
            if self.p1_choice is None:
                self.p1_choice = instance.text
                self.status_label.text = f"{self.p2_name}'s Turn!\n(Choose secretly)"
            else:
                self.show_result(self.p1_choice, instance.text)
                self.p1_choice = None

    def show_result(self, c1, c2):
        if c1 == c2:
            res = "DRAW!"
        elif (c1 == 'Rock' and c2 == 'Scissors') or (c1 == 'Paper' and c2 == 'Rock') or (c1 == 'Scissors' and c2 == 'Paper'):
            res = f"{self.p1_name} WINS!"
        else:
            res = f"{self.p2_name} WINS!"
        
        self.status_label.text = f"{self.p1_name}: {c1}\n{self.p2_name}: {c2}\n--- {res} ---"

    def go_back(self, instance):
        self.manager.current = 'menu'

class RPSApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    RPSApp().run()
