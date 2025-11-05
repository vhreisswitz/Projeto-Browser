import re
from PyQt5.QtCore import QUrl, QSettings, Qt
from PyQt5.QtWidgets import (
    QMainWindow, QToolBar, QAction, QLineEdit, QMessageBox,
    QTabWidget, QProgressBar
)

from .hover_button import HoverButton
from .browser_tab import BrowserTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        from PyQt5.QtWidgets import QApplication
        QApplication.setStyle('Fusion')
        self.setWindowTitle("Infinity Browser Dark")
        self.setMinimumSize(800, 600)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.setCentralWidget(self.tabs)
        self.progress = QProgressBar()
        self.progress.setMaximumHeight(3)
        self.progress.setVisible(False)
        self.progress.setMaximum(100)
        self.create_navigation_bar()
        self.create_menus()
        self.add_new_tab()
        self.settings = QSettings("InfinityBrowser", "Settings")
        self.load_settings()
        self.apply_enhanced_dark_theme()

    def create_navigation_bar(self):
        navbar = QToolBar()
        navbar.setMovable(False)
        navbar.setFixedHeight(50)
        self.addToolBar(navbar)
        back_btn = HoverButton("⬅️")
        back_btn.setToolTip("Voltar (Alt+Left)")
        back_btn.clicked.connect(lambda: self.current_browser().back())
        navbar.addWidget(back_btn)
        forward_btn = HoverButton("➡️")
        forward_btn.setToolTip("Avançar (Alt+Right)")
        forward_btn.clicked.connect(lambda: self.current_browser().forward())
        navbar.addWidget(forward_btn)
        reload_btn = HoverButton("🔄")
        reload_btn.setToolTip("Recarregar (F5)")
        reload_btn.clicked.connect(lambda: self.current_browser().reload())
        navbar.addWidget(reload_btn)
        home_btn = HoverButton("🏠")
        home_btn.setToolTip("Página Inicial (Alt+Home)")
        home_btn.clicked.connect(self.navigate_home)
        navbar.addWidget(home_btn)
        new_tab_btn = HoverButton("➕")
        new_tab_btn.setToolTip("Nova Aba (Ctrl+T)")
        new_tab_btn.clicked.connect(self.add_new_tab)
        navbar.addWidget(new_tab_btn)
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Digite uma URL ou termo de busca...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        navbar.addWidget(self.progress)

    def create_menus(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&Arquivo")
        new_tab_action = QAction("Nova Aba", self)
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_tab_action)
        new_window_action = QAction("Nova Janela", self)
        new_window_action.setShortcut("Ctrl+N")
        new_window_action.triggered.connect(self.new_window)
        file_menu.addAction(new_window_action)
        file_menu.addSeparator()
        quit_action = QAction("Sair", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        view_menu = menubar.addMenu("&Exibir")
        zoom_in = QAction("Zoom +", self)
        zoom_in.setShortcut("Ctrl++")
        zoom_in.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in)
        zoom_out = QAction("Zoom -", self)
        zoom_out.setShortcut("Ctrl+-")
        zoom_out.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out)
        reset_zoom = QAction("Zoom Normal", self)
        reset_zoom.setShortcut("Ctrl+0")
        reset_zoom.triggered.connect(self.zoom_reset)
        view_menu.addAction(reset_zoom)
        view_menu.addSeparator()
        fullscreen_action = QAction("Tela Cheia", self)
        fullscreen_action.setShortcut("F11")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        help_menu = menubar.addMenu("&Ajuda")
        about_action = QAction("Sobre", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def add_new_tab(self, url=None, set_current=True):
        browser = BrowserTab()
        browser.titleChanged.connect(
            lambda title, browser=browser: self.update_tab_title(browser, title))
        browser.urlChanged.connect(self.update_url_bar)
        browser.loadProgress.connect(self.update_progress)
        browser.loadStarted.connect(self.page_load_started)
        browser.loadFinished.connect(self.page_load_finished)
        tab_index = self.tabs.addTab(browser, "🔄 Carregando...")
        if set_current:
            self.tabs.setCurrentIndex(tab_index)
        if url:
            browser.setUrl(QUrl(url))
        else:
            self.navigate_home()
        return browser

    def navigate_home(self):
        html = """
        <html>
        <head>
            <title>Infinity Browser</title>
            <style>
                * {margin: 0;padding: 0;box-sizing: border-box;}
                body {
                    margin: 0;
                    height: 100vh;
                    background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #2d1b69 100%);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: #ffffff;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    text-align: center;
                    overflow: hidden;
                }
                .container {
                    background: rgba(30, 30, 30, 0.95);
                    padding: 50px;
                    border-radius: 25px;
                    backdrop-filter: blur(15px);
                    border: 1px solid #444;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                    transition: all 0.3s ease;
                    position: relative;
                    overflow: hidden;
                    max-width: 90%;
                }
                .container::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(106, 90, 205, 0.1), transparent);
                    transition: left 0.6s ease;
                }
                .container:hover::before {
                    left: 100%;
                }
                .container:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
                    border-color: #6a5acd;
                }
                h1 {
                    font-size: 3em;
                    margin-bottom: 25px;
                    background: linear-gradient(45deg, #00aaff, #ff00aa, #6a5acd);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    background-size: 200% 200%;
                    animation: gradientShift 3s ease infinite;
                }
                @keyframes gradientShift {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }
                p {
                    font-size: 1.3em;
                    color: #cccccc;
                    margin-bottom: 15px;
                    transition: color 0.3s ease;
                }
                .container:hover p {
                    color: #ffffff;
                }
                .shortcuts {
                    margin-top: 35px;
                    font-size: 1em;
                    color: #888;
                    transition: color 0.3s ease;
                }
                .container:hover .shortcuts {
                    color: #aaa;
                }
                .feature-grid {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 15px;
                    margin-top: 30px;
                }
                .feature {
                    background: rgba(106, 90, 205, 0.1);
                    padding: 15px;
                    border-radius: 10px;
                    transition: all 0.3s ease;
                    border: 1px solid transparent;
                }
                .feature:hover {
                    background: rgba(106, 90, 205, 0.2);
                    border-color: #6a5acd;
                    transform: scale(1.05);
                }
                @media (max-width: 768px) {
                    .container {
                        padding: 30px;
                    }
                    h1 {
                        font-size: 2em;
                    }
                    .feature-grid {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌑 Infinity Browser</h1>
                <p>Digite uma URL acima ou use a busca integrada</p>
                <p>Ctrl+T = Nova Aba | Ctrl+Q = Sair | F5 = Recarregar</p>
                <div class="feature-grid">
                    <div class="feature">🚀 Navegação Rápida</div>
                    <div class="feature">🎨 Tema Escuro</div>
                    <div class="feature">🔒 Navegação Segura</div>
                    <div class="feature">⚙️ Personalizável</div>
                </div>
                <div class="shortcuts">
                    Alt+Left/Right = Navegar | Ctrl++/- = Zoom | Alt+Home = Início
                </div>
            </div>
        </body>
        </html>
        """
        self.current_browser().setHtml(html, QUrl("about:blank"))

    def is_localhost_with_port(self, text):
        patterns = [
            r'^\d+\.\d+\.\d+\.\d+:\d+$',
            r'^localhost:\d+$',
            r'^[\w\-]+:\d+$',
            r'^\d+\.\d+\.\d+\.\d+$',
            r'^localhost$'
        ]
        for pattern in patterns:
            if re.match(pattern, text):
                return True
        return False

    def looks_like_url(self, text):
        url_indicators = ['.com', '.org', '.net', '.br', '.io', '.gov', '.edu', 
                         'localhost', 'http', 'https', 'www.', 'ftp:']
        return any(indicator in text.lower() for indicator in url_indicators)

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url:
            self.navigate_home()
            return
        if self.is_localhost_with_port(url):
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            self.current_browser().setUrl(QUrl(url))
            return
        if ' ' in url or not self.looks_like_url(url):
            url = f"https://duckduckgo.com/?q={url.replace(' ', '+')}"
        elif not url.startswith(('http://', 'https://', 'ftp://', 'file://')):
            url = 'https://' + url
        self.current_browser().setUrl(QUrl(url))

    def update_url_bar(self, url):
        current_browser = self.current_browser()
        if current_browser and current_browser == self.sender():
            self.url_bar.setText(url.toString())

    def update_tab_title(self, browser, title):
        index = self.tabs.indexOf(browser)
        if index != -1 and title:
            short_title = (title[:20] + "...") if len(title) > 20 else title
            self.tabs.setTabText(index, short_title)
            self.tabs.setTabToolTip(index, title)

    def update_progress(self, progress):
        self.progress.setValue(progress)

    def page_load_started(self):
        self.progress.setVisible(True)
        browser = self.sender()
        if browser:
            index = self.tabs.indexOf(browser)
            if index != -1:
                self.tabs.setTabText(index, "🔄 Carregando...")

    def page_load_finished(self, ok):
        self.progress.setVisible(False)
        browser = self.sender()
        if browser and ok:
            index = self.tabs.indexOf(browser)
            if index != -1 and not browser.title():
                self.tabs.setTabText(index, "Nova Aba")

    def current_browser(self):
        return self.tabs.currentWidget()

    def close_tab(self, index):
        if self.tabs.count() > 1:
            widget = self.tabs.widget(index)
            if widget:
                widget.deleteLater()
            self.tabs.removeTab(index)
        else:
            self.close()

    def current_tab_changed(self, index):
        if index >= 0:
            browser = self.tabs.widget(index)
            if browser:
                self.update_url_bar(browser.url())
                self.update_navigation_buttons()

    def update_navigation_buttons(self):
        pass

    def zoom_in(self):
        current_browser = self.current_browser()
        if current_browser:
            current_zoom = current_browser.zoomFactor()
            current_browser.setZoomFactor(current_zoom + 0.1)

    def zoom_out(self):
        current_browser = self.current_browser()
        if current_browser:
            current_zoom = current_browser.zoomFactor()
            if current_zoom > 0.3:
                current_browser.setZoomFactor(current_zoom - 0.1)

    def zoom_reset(self):
        current_browser = self.current_browser()
        if current_browser:
            current_browser.setZoomFactor(1.0)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def new_window(self):
        from .main_window import MainWindow
        new_window = MainWindow()
        new_window.show()

    def show_about(self):
        QMessageBox.about(self, "Sobre Infinity Browser",
                         "<h3>Infinity Browser Dark</h3>"
                         "<p>Versão 2.0</p>"
                         "<p>Um navegador web moderno com tema escuro</p>"
                         "<p>Desenvolvido com PyQt5 e QWebEngine</p>")

    def load_settings(self):
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.showMaximized()

    def save_settings(self):
        self.settings.setValue("geometry", self.saveGeometry())

    def apply_enhanced_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color: #ffffff;
            }
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a1a, stop:1 #0f0f0f);
                padding: 8px;
                border-bottom: 2px solid #2d1b69;
                spacing: 8px;
            }
            QLineEdit {
                background: #2c2c2c;
                color: #ffffff;
                padding: 10px 15px;
                border-radius: 20px;
                border: 2px solid #444;
                font-size: 14px;
                selection-background-color: #6a5acd;
            }
            QLineEdit:focus {
                border: 2px solid #6a5acd;
                background: #1a1a1a;
            }
            QLineEdit:hover {
                border: 2px solid #555;
                background: #252525;
            }
            QTabWidget::pane {
                border: none;
                background: #1a1a1a;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a2a2a, stop:1 #1f1f1f);
                color: #cccccc;
                padding: 10px 20px;
                margin-right: 3px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 1px solid #333;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a3a3a, stop:1 #2d1b69);
                color: #ffffff;
                border-color: #6a5acd;
            }
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #333333, stop:1 #252525);
                color: #ffffff;
            }
            QTabBar::close-button {
                image: url(none);
                subcontrol-origin: padding;
                subcontrol-position: right;
                padding: 4px;
                border-radius: 10px;
                background: transparent;
            }
            QTabBar::close-button:hover {
                background: #ff4444;
            }
            QProgressBar {
                background: transparent;
                color: transparent;
                border: none;
                min-width: 120px;
                max-width: 120px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6a5acd, stop:0.3 #00aaff, stop:0.7 #ff00aa, stop:1 #00ffaa);
                border-radius: 2px;
            }
            QMenuBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1f1f1f, stop:1 #151515);
                color: #ffffff;
                border-bottom: 1px solid #2d1b69;
            }
            QMenuBar::item {
                background: transparent;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QMenuBar::item:selected {
                background: rgba(106, 90, 205, 0.3);
            }
            QMenu {
                background: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
            }
            QMenu::item {
                padding: 8px 30px 8px 25px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6a5acd, stop:1 #8a75ed);
            }
            QMenu::separator {
                height: 1px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 transparent, stop:0.5 #6a5acd, stop:1 transparent);
                margin: 5px 10px;
            }
        """)

    def closeEvent(self, event):
        self.save_settings()
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if widget:
                widget.deleteLater()
        super().closeEvent(event)