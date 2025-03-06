import sys
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QAction, QFileDialog, QMenuBar
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QIcon

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DogDay Browser")
        self.setGeometry(100, 100, 1024, 768)

        # Criar o layout principal
        self.layout = QVBoxLayout()

        # Barra de pesquisa (QLineEdit)
        self.address_bar = QLineEdit(self)
        self.address_bar.returnPressed.connect(self.load_url)
        self.layout.addWidget(self.address_bar)

        # Botão para pesquisar
        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.load_url)
        self.layout.addWidget(self.search_button)

        # Botões de navegação
        self.reload_button = QPushButton('Reload', self)
        self.reload_button.clicked.connect(self.reload_page)
        self.layout.addWidget(self.reload_button)

        # Histórico de navegação
        self.history = []

        # Barra de menus
        self.create_menu()

        # Criação do QWebEngineView para exibir a página
        self.browser = QWebEngineView(self)
        self.layout.addWidget(self.browser)

        # Conectar o sinal de mudança de URL
        self.browser.urlChanged.connect(self.update_address_bar)

        # Conectar o sinal de download ao perfil
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.handle_download)

        # Criar o widget principal
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Carregar uma página inicial
        self.browser.setUrl(QUrl("https://www.google.com"))

    def create_menu(self):
        """Criar o menu de navegação e histórico"""
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')

        # Opções de histórico
        history_action = QAction('View History', self)
        history_action.triggered.connect(self.view_history)
        file_menu.addAction(history_action)

        # Opção de download
        download_action = QAction('Download File', self)
        download_action.triggered.connect(self.handle_download)  # Alterado para o método correto
        file_menu.addAction(download_action)

    def load_url(self):
        """Carregar URL a partir da barra de pesquisa."""
        url = self.address_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url  # Adiciona https:// se não for fornecido
        self.browser.setUrl(QUrl(url))
        self.history.append(url)

    def update_address_bar(self, qurl):
        """Atualizar a barra de endereços sempre que a URL mudar."""
        self.address_bar.setText(qurl.toString())

    def reload_page(self):
        """Recarregar a página atual."""
        self.browser.reload()

    def view_history(self):
        """Mostrar o histórico de navegação."""
        print("Histórico de navegação:")
        for index, url in enumerate(self.history):
            print(f"{index + 1}. {url}")

    def handle_download(self, download):
        """Manipular downloads e salvar o arquivo."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", QDir.rootPath())
        if file_path:
            download.setPath(file_path)
            download.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
