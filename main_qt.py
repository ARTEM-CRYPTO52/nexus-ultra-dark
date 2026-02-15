import sys
import os
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtNetwork import QNetworkCookie
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLineEdit, QPushButton, QTabWidget, 
                             QProgressBar, QFrame)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage

# 1. ТОТАЛЬНАЯ ТЕМНАЯ ТЕМА (на уровне ядра Chromium)
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--force-dark-mode --enable-features=WebContentsForceDark"

# 2. СКРИПТ ПОЛНОЙ ЗАЧИСТКИ (Вырезает футер и закрашивает всё черным)
ULTRA_BLACK_JS = """
    (function() {
        const nexusStyles = () => {
            // Удаляем нижние плашки (футер, регион, реклама)
            const trash = ['#footer', '#footcnt', '.fbar', '.SFNo6d', '.b04A9e', '.K9v7Gd', '.p8961d', '.v8961d', '.C1N51c', '[role="contentinfo"]'];
            trash.forEach(s => document.querySelectorAll(s).forEach(el => el.remove()));
            
            // Закрашиваем фон в глубокий черный
            document.body.style.backgroundColor = '#0b0b0e';
            document.documentElement.style.setProperty('background-color', '#0b0b0e', 'important');
            
            // Убираем нижние отступы
            document.body.style.marginBottom = '0';
            document.body.style.paddingBottom = '0';
        };

        nexusStyles();
        // Следим за изменениями (если Google подгрузит мусор динамически)
        new MutationObserver(nexusStyles).observe(document.documentElement, { childList: true, subtree: true });
        setInterval(nexusStyles, 300);
    })();
"""

class NexusUltraFinal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nexus Ultra Dark")
        self.resize(1280, 850)

        # ПУТЬ СОХРАНЕНИЯ ДАННЫХ (Для сохранения входа в Google)
        data_path = os.path.join(os.environ["LOCALAPPDATA"], "NexusBrowser_Store")
        if not os.path.exists(data_path): os.makedirs(data_path)
        
        self.profile = QWebEngineProfile("NexusProfile", self)
        self.profile.setPersistentStoragePath(data_path)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        
        # Сигнал Google на темную тему через Куки
        self.force_dark_mode()

        self.setup_ui()
        self.apply_styles()
        self.add_new_tab(QUrl("https://www.google.com"))

    def force_dark_mode(self):
        cookie = QNetworkCookie(b"PREF", b"f6=400")
        cookie.setDomain(".google.com")
        cookie.setPath("/")
        self.profile.cookieStore().setCookie(cookie)

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Верхняя панель управления
        self.top_bar = QFrame()
        self.top_bar.setFixedHeight(55)
        nav = QHBoxLayout(self.top_bar)
        
        self.btn_back = QPushButton("‹")
        self.url_bar = QLineEdit()
        self.btn_add = QPushButton("+")

        nav.addWidget(self.btn_back)
        nav.addWidget(self.url_bar)
        nav.addWidget(self.btn_add)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)

        layout.addWidget(self.top_bar)
        layout.addWidget(self.tabs)

        # Навигация
        self.btn_back.clicked.connect(lambda: self.current_browser().back() if self.current_browser() else None)
        self.btn_add.clicked.connect(lambda: self.add_new_tab(QUrl("https://www.google.com")))
        self.url_bar.returnPressed.connect(self.navigate)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.sync_url)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #0b0b0e; }
            QFrame { background-color: #111; border-bottom: 1px solid #222; }
            QLineEdit { background: #000; border: 1px solid #333; border-radius: 12px; color: #00ffcc; padding: 6px 15px; }
            QPushButton { color: #888; border: none; font-size: 28px; min-width: 45px; }
            QPushButton:hover { color: #00ffcc; background: #222; border-radius: 10px; }
            QTabBar::tab { background: #111; color: #555; padding: 12px 25px; border-right: 1px solid #000; }
            QTabBar::tab:selected { background: #0b0b0e; color: #00ffcc; border-bottom: 2px solid #00ffcc; }
        """)

    def add_new_tab(self, url):
        browser = QWebEngineView()
        browser.setPage(QWebEnginePage(self.profile, browser))
        browser.setUrl(url)
        
        idx = self.tabs.addTab(browser, "Google")
        self.tabs.setCurrentIndex(idx)

        # Инъекция полной черноты и зачистки
        browser.loadFinished.connect(lambda: browser.page().runJavaScript(ULTRA_BLACK_JS))
        browser.urlChanged.connect(self.sync_url)

    def current_browser(self):
        return self.tabs.currentWidget()

    def sync_url(self):
        if self.current_browser():
            self.url_bar.setText(self.current_browser().url().toString())

    def navigate(self):
        t = self.url_bar.text().strip()
        if not t: return
        url = QUrl(t if "." in t and " " not in t else f"https://www.google.com{t}")
        if url.scheme() == "": url.setScheme("https")
        if self.current_browser(): self.current_browser().setUrl(url)

    def close_tab(self, i):
        if self.tabs.count() > 1: self.tabs.removeTab(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NexusUltraFinal()
    window.show()
    sys.exit(app.exec())
