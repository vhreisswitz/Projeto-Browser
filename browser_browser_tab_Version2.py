from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserTab(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings().setAttribute(self.settings().PluginsEnabled, True)
        self.settings().setAttribute(self.settings().JavascriptEnabled, True)
        self.settings().setAttribute(self.settings().FullScreenSupportEnabled, True)