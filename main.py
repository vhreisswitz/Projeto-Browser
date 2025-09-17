import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Navegador
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Barra de navegação
        navbar = QToolBar()
        navbar.setMovable(False)
        self.addToolBar(navbar)

        # Botões
        back_btn = QAction("⬅️", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction("➡️", self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction("🔄️", self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # Barra de URL
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        # Tema Dark QSS para a interface
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QToolBar {
                background: #1f1f1f;
                padding: 5px;
                border-bottom: 2px solid #333;
            }
            QLineEdit {
                background: #2c2c2c;
                color: #ffffff;
                padding: 6px;
                border-radius: 12px;
                border: 1px solid #555;
                min-width: 400px;
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
            }
            QToolButton:hover {
                background: #333333;
                border-radius: 8px;
            }
        """)

        # Abrir página inicial com background customizado
        self.navigate_home()

    def navigate_home(self):
        # Página inicial customizada com fundo dark gradient
        html = """
        <html>
        <body style="
            margin:0;
            height:100vh;
            background: linear-gradient(to bottom right, #0f0f0f, #1a1a1a);
            display:flex;
            justify-content:center;
            align-items:center;
            color:#ffffff;
            font-family:Arial, sans-serif;
            text-align:center;">
            <div>
                <h1>🌑 Infinity Browser</h1>
                <p>Digite uma URL acima ou use a pesquisa DuckDuckGo</p>
            </div>
        </body>
        </html>
        """
        self.browser.setHtml(html, QUrl("about:blank"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Infinity Browser Dark")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
