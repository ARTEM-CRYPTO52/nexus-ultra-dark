"""
Nexus Ultra Dark - Android версия (Kivy)
Компилируется в APK через: buildozer android debug
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.webview import WebView
from kivy.core.window import Window
from kivy.garden.webview import WebView as KivyWebView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.image import Image
from android.runnable import run_on_ui_thread
import requests

# Размер окна для тестирования на компьютере (не влияет на APK)
Window.size = (720, 1280)

# Темная тема - основные цвета
DARK_BG = (0.043, 0.043, 0.055, 1)          # #0b0b0e
DARK_GRAY = (0.067, 0.067, 0.067, 1)        # #111
DARK_BORDER = (0.133, 0.133, 0.133, 1)      # #222
CYAN_ACCENT = (0, 1, 0.8, 1)                # #00ffcc
TEXT_DARK = (0.533, 0.533, 0.533, 1)        # #888

ULTRA_BLACK_JS = """
    (function() {
        const nexusStyles = () => {
            const trash = ['#footer', '#footcnt', '.fbar', '.SFNo6d', '.b04A9e', '.K9v7Gd', '.p8961d', '.v8961d', '.C1N51c', '[role="contentinfo"]'];
            trash.forEach(s => document.querySelectorAll(s).forEach(el => el.remove()));
            
            document.body.style.backgroundColor = '#0b0b0e';
            document.documentElement.style.setProperty('background-color', '#0b0b0e', 'important');
            
            document.body.style.marginBottom = '0';
            document.body.style.paddingBottom = '0';
            document.body.style.margin = '0';
            document.body.style.padding = '0';
        };

        nexusStyles();
        new MutationObserver(nexusStyles).observe(document.documentElement, { childList: true, subtree: true });
        setInterval(nexusStyles, 300);
    })();
"""


class NexusAndroidBrowser(App):
    """Nexus Ultra Dark браузер для Android"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Nexus Ultra Dark"
        self.tabs = {}
        self.current_tab = None
        
    def build(self):
        """Создание интерфейса приложения"""
        
        # Главный контейнер (вертикальный)
        main_layout = BoxLayout(orientation='vertical', spacing=0)
        main_layout.canvas.clear()
        
        with main_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*DARK_BG)
            self.bg_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        
        main_layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # ============ ВЕРХНЯЯ ПАНЕЛЬ УПРАВЛЕНИЯ ============
        nav_panel = BoxLayout(size_hint_y=0.08, spacing=5, padding=5)
        nav_panel.canvas.before.clear()
        with nav_panel.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*DARK_GRAY)
            nav_panel.bg_rect = Rectangle(size=nav_panel.size, pos=nav_panel.pos)
        nav_panel.bind(size=self._update_nav_bg, pos=self._update_nav_bg)
        
        # Кнопка "Назад"
        btn_back = Button(text='<', size_hint_x=0.1, 
                         background_normal='', background_color=DARK_GRAY,
                         color=TEXT_DARK, font_size='24sp', bold=True)
        btn_back.bind(on_press=self.go_back)
        nav_panel.add_widget(btn_back)
        self.btn_back = btn_back
        
        # Адресная строка
        self.url_bar = TextInput(
            text='https://www.google.com',
            multiline=False,
            size_hint_x=0.8,
            background_color=DARK_BG,
            foreground_color=CYAN_ACCENT,
            hint_text='Enter URL...',
            hint_text_color=(0.3, 0.3, 0.3, 1)
        )
        self.url_bar.bind(on_text_validate=self.navigate_to_url)
        nav_panel.add_widget(self.url_bar)
        
        # Кнопка "Новая вкладка"
        btn_add = Button(text='+', size_hint_x=0.1,
                        background_normal='', background_color=DARK_GRAY,
                        color=TEXT_DARK, font_size='24sp', bold=True)
        btn_add.bind(on_press=self.add_new_tab)
        nav_panel.add_widget(btn_add)
        
        main_layout.add_widget(nav_panel)
        
        # ============ ВКЛАДКИ ============
        self.tabbed_panel = TabbedPanel(
            do_default_tab=False,
            size_hint_y=0.92,
            background_color=DARK_BG
        )
        self.tabbed_panel.canvas.before.clear()
        with self.tabbed_panel.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*DARK_BG)
            self.tabbed_panel.bg_rect = Rectangle(size=self.tabbed_panel.size, 
                                                   pos=self.tabbed_panel.pos)
        
        main_layout.add_widget(self.tabbed_panel)
        
        # Создаем первую вкладку Google
        Clock.schedule_once(lambda dt: self.add_new_tab(None), 0.5)
        
        return main_layout
    
    def _update_bg(self, instance, value):
        """Обновление фонового прямоугольника"""
        try:
            self.bg_rect.pos = instance.pos
            self.bg_rect.size = instance.size
        except:
            pass
    
    def _update_nav_bg(self, instance, value):
        """Обновление фона навбара"""
        try:
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        except:
            pass
    
    def add_new_tab(self, instance):
        """Добавление новой вкладки с Google"""
        
        tab_content = BoxLayout(orientation='vertical')
        
        try:
            # Попытка использовать встроенный WebView (может не работать на всех устройствах)
            from kivy.garden.webview import WebView
            webview = WebView()
            webview.url = 'https://www.google.com'
            tab_content.add_widget(webview)
        except ImportError:
            # Резервный вариант - использование встроенного браузера
            from kivy.uix.label import Label
            fallback = Label(
                text='[color=00ffcc]WebView требует установки:\npython -m pip install kivy-garden\ngarden install webview\n\nДля сборки APK используйте buildozer.spec\n\n[/color][color=888888]Откройте в браузере вручную:\nhttps://www.google.com[/color]',
                markup=True,
                size_hint_y=1
            )
            tab_content.add_widget(fallback)
        
        # Создаем вкладку
        tab_label = 'Google'
        panel_item = TabbedPanelItem(text=tab_label)
        panel_item.content = tab_content
        panel_item.background_normal = ''
        panel_item.background_color = DARK_GRAY
        
        self.tabbed_panel.add_widget(panel_item)
        self.tabbed_panel.switch_to(panel_item)
        self.current_tab = panel_item
        
        self.tabs[tab_label] = {
            'panel': panel_item,
            'content': tab_content,
            'url': 'https://www.google.com'
        }
    
    def navigate_to_url(self, instance):
        """Навигация по URL из адресной строки"""
        url = self.url_bar.text.strip()
        
        if not url:
            return
        
        # Добавляем https://, если схемы нет
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        if self.current_tab and self.current_tab.content:
            try:
                # Пытаемся найти WebView и обновить URL
                for widget in self.current_tab.content.walk():
                    if hasattr(widget, 'url'):
                        widget.url = url
                        break
            except:
                pass
    
    def go_back(self, instance):
        """Кнопка "Назад" - (требует эмуляции истории)"""
        try:
            if self.current_tab and self.current_tab.content:
                for widget in self.current_tab.content.walk():
                    if hasattr(widget, 'go_back'):
                        widget.go_back()
                        break
        except:
            pass


class NexusBrowserApp(App):
    """Главное приложение"""
    
    def build(self):
        return NexusAndroidBrowser().build()


if __name__ == '__main__':
    NexusBrowserApp().run()
