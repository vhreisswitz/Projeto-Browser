import sys
import os
from PyQt5.QtCore import QUrl, QSettings
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, QAction, 
                             QLineEdit, QMenu, QMessageBox, QTabWidget, QProgressBar)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QIcon, QKeySequence

# Classe para cada aba do navegador
class BrowserTab(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Habilitar plugins e JavaScript
        self.settings().setAttribute(self.settings().PluginsEnabled, True)
        self.settings().setAttribute(self.settings().JavascriptEnabled, True)

# Classe principal do navegador
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.setWindowTitle("Infinity Browser Dark")
        
        # Sistema de abas
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.setCentralWidget(self.tabs)
        
        # Barra de progresso
        self.progress = QProgressBar()
        self.progress.setMaximumHeight(3)
        self.progress.setVisible(False)
        self.progress.setMaximum(100)
        
        # Criar interface
        self.create_navigation_bar()
        self.create_menus()
        self.add_new_tab()
        self.showMaximized()
        
        # Configurações
        self.settings = QSettings("InfinityBrowser", "Settings")
        self.load_settings()
        
        # Aplicar tema dark
        self.apply_dark_theme()

    def create_navigation_bar(self):
        navbar = QToolBar()
        navbar.setMovable(False)
        self.addToolBar(navbar)
        
        # Botão Voltar
        back_btn = QAction("⬅️", self)
        back_btn.setShortcut(QKeySequence("Alt+Left"))
        back_btn.triggered.connect(lambda: self.current_browser().back())
        back_btn.setToolTip("Voltar (Alt+Left)")
        navbar.addAction(back_btn)

        # Botão Avançar
        forward_btn = QAction("➡️", self)
        forward_btn.setShortcut(QKeySequence("Alt+Right"))
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        forward_btn.setToolTip("Avançar (Alt+Right)")
        navbar.addAction(forward_btn)

        # Botão Recarregar
        reload_btn = QAction("🔄", self)
        reload_btn.setShortcut(QKeySequence("F5"))
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        reload_btn.setToolTip("Recarregar (F5)")
        navbar.addAction(reload_btn)

        # Botão Home
        home_btn = QAction("🏠", self)
        home_btn.setShortcut(QKeySequence("Alt+Home"))
        home_btn.triggered.connect(self.navigate_home)
        home_btn.setToolTip("Página Inicial (Alt+Home)")
        navbar.addAction(home_btn)

        # Botão Nova Aba
        new_tab_btn = QAction("➕", self)
        new_tab_btn.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_btn.triggered.connect(self.add_new_tab)
        new_tab_btn.setToolTip("Nova Aba (Ctrl+T)")
        navbar.addAction(new_tab_btn)

        # Barra de URL
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Digite uma URL ou termo de busca...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        
        # Barra de progresso
        navbar.addWidget(self.progress)

    def create_menus(self):
        menubar = self.menuBar()
        
        # Menu Arquivo
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
        
        # Menu Exibir
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

    def add_new_tab(self, url=None):
        browser = BrowserTab()
        tab_index = self.tabs.addTab(browser, "Nova Aba")
        self.tabs.setCurrentIndex(tab_index)
        
        # Conectar sinais
        browser.titleChanged.connect(lambda title: self.update_tab_title(tab_index, title))
        browser.urlChanged.connect(self.update_url_bar)
        browser.loadProgress.connect(self.update_progress)
        browser.loadStarted.connect(lambda: self.progress.setVisible(True))
        browser.loadFinished.connect(lambda: self.progress.setVisible(False))
        
        if url:
            browser.setUrl(QUrl(url))
        else:
            self.navigate_home()
            
        return browser

    def navigate_home(self):
        # Página inicial customizada com fundo dark gradient
        html = """
        <html>
        <head>
            <title>Infinity Browser</title>
            <style>
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
                }
                .container {
                    background: rgba(30, 30, 30, 0.8);
                    padding: 40px;
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                    border: 1px solid #333;
                }
                h1 {
                    font-size: 2.5em;
                    margin-bottom: 20px;
                    background: linear-gradient(45deg, #00aaff, #ff00aa);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }
                p {
                    font-size: 1.2em;
                    color: #cccccc;
                    margin-bottom: 10px;
                }
                .shortcuts {
                    margin-top: 30px;
                    font-size: 0.9em;
                    color: #888;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌑 Infinity Browser</h1>
                <p>Digite uma URL acima ou use a busca integrada</p>
                <p>Ctrl+T = Nova Aba | Ctrl+Q = Sair | F5 = Recarregar</p>
                <div class="shortcuts">
                    Alt+Left/Right = Navegar | Ctrl++/- = Zoom
                </div>
            </div>
        </body>
        </html>
        """
        self.current_browser().setHtml(html, QUrl("about:blank"))

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        
        # Se for vazio, vai para home
        if not url:
            self.navigate_home()
            return
            
        # Se for termo de busca (contém espaços ou não parece uma URL)
        if ' ' in url or ('.' not in url and not any(proto in url.lower() for proto in ['http://', 'https://', 'ftp://'])):
            if not url.startswith(('http://', 'https://')):
                url = f"https://duckduckgo.com/?q={url.replace(' ', '+')}"
        
        # Adiciona protocolo se necessário
        elif not url.startswith(('http://', 'https://', 'ftp://', 'file://')):
            url = 'https://' + url
            
        self.current_browser().setUrl(QUrl(url))

    def update_url_bar(self, url):
        if self.current_browser() == self.sender():
            self.url_bar.setText(url.toString())

    def update_tab_title(self, index, title):
        if title:
            # Limita o tamanho do título na aba
            short_title = (title[:25] + "...") if len(title) > 25 else title
            self.tabs.setTabText(index, short_title)
            self.tabs.setTabToolTip(index, title)

    def update_progress(self, progress):
        self.progress.setValue(progress)

    def current_browser(self):
        return self.tabs.currentWidget()

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def current_tab_changed(self, index):
        if index >= 0:
            browser = self.tabs.widget(index)
            if browser:
                self.url_bar.setText(browser.url().toString())

    def zoom_in(self):
        current_zoom = self.current_browser().zoomFactor()
        self.current_browser().setZoomFactor(current_zoom + 0.1)

    def zoom_out(self):
        current_zoom = self.current_browser().zoomFactor()
        if current_zoom > 0.3:  # Zoom mínimo
            self.current_browser().setZoomFactor(current_zoom - 0.1)

    def zoom_reset(self):
        self.current_browser().setZoomFactor(1.0)

    def new_window(self):
        # Criar uma nova instância do navegador
        new_window = MainWindow()
        new_window.show()

    def load_settings(self):
        # Carrega configurações salvas
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

    def save_settings(self):
        # Salva configurações atuais
        self.settings.setValue("geometry", self.saveGeometry())

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color: #ffffff;
            }
            QToolBar {
                background: #1f1f1f;
                padding: 5px;
                border-bottom: 2px solid #333;
                spacing: 5px;
            }
            QLineEdit {
                background: #2c2c2c;
                color: #ffffff;
                padding: 8px 12px;
                border-radius: 15px;
                border: 1px solid #555;
                min-width: 500px;
                font-size: 14px;
                selection-background-color: #00aaff;
            }
            QLineEdit:focus {
                border: 1px solid #00aaff;
                background: #1a1a1a;
            }
            QToolButton {
                background: transparent;
                color: #ffffff;
                padding: 6px;
                font-size: 16px;
                border: none;
            }
            QToolButton:hover {
                background: #333333;
                border-radius: 8px;
            }
            QTabWidget::pane {
                border: none;
                background: #1a1a1a;
            }
            QTabBar::tab {
                background: #2a2a2a;
                color: #cccccc;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                border: 1px solid #333;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background: #3a3a3a;
                color: #ffffff;
                border-color: #555;
            }
            QTabBar::tab:hover:!selected {
                background: #333333;
            }
            QTabBar::close-button {
                image: url(none);
                subcontrol-origin: padding;
                subcontrol-position: right;
            }
            QTabBar::close-button:hover {
                background: #ff4444;
                border-radius: 8px;
            }
            QProgressBar {
                background: transparent;
                color: transparent;
                border: none;
                min-width: 100px;
                max-width: 100px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00aaff, stop:0.5 #ff00aa, stop:1 #00ffaa);
                border-radius: 1px;
            }
            QMenuBar {
                background: #1f1f1f;
                color: #ffffff;
                border-bottom: 1px solid #333;
            }
            QMenuBar::item {
                background: transparent;
                padding: 4px 8px;
            }
            QMenuBar::item:selected {
                background: #333333;
                border-radius: 4px;
            }
            QMenu {
                background: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
            }
            QMenu::item {
                padding: 6px 24px 6px 20px;
            }
            QMenu::item:selected {
                background: #00aaff;
            }
            QMenu::separator {
                height: 1px;
                background: #444;
            }
        """)

    def closeEvent(self, event):
        # Salva configurações ao fechar
        self.save_settings()
        super().closeEvent(event)

# Ponto de entrada da aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Infinity Browser Dark")
    QApplication.setApplicationVersion("2.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())