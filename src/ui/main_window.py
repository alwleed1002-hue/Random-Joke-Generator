from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QComboBox, QLabel, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from src.joke_handler import JokeHandler
import asyncio

class JokeFetcher(QThread):
    joke_fetched = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, api_source, category=None):
        super().__init__()
        self.api_source = api_source
        self.category = category
        self.handler = JokeHandler()
    
    def run(self):
        try:
            joke = asyncio.run(self.handler.fetch_joke(self.api_source, self.category))
            self.joke_fetched.emit(joke)
        except Exception as e:
            self.error_occurred.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Random Joke Generator')
        self.setGeometry(100, 100, 700, 600)
        self.handler = JokeHandler()
        self.fetcher = None
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        title_label = QLabel('Random Joke Generator')
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel('API Source:'))
        self.api_combo = QComboBox()
        self.api_combo.addItems(['JokeAPI', 'Official Joke API', 'Ninja Jokes'])
        self.api_combo.currentTextChanged.connect(self.update_categories)
        api_layout.addWidget(self.api_combo)
        layout.addLayout(api_layout)
        
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel('Category:'))
        self.category_combo = QComboBox()
        self.category_combo.addItem('Random')
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)
        
        joke_label = QLabel('Joke:')
        joke_font = QFont()
        joke_font.setBold(True)
        joke_label.setFont(joke_font)
        layout.addWidget(joke_label)
        
        self.joke_display = QTextEdit()
        self.joke_display.setReadOnly(True)
        self.joke_display.setMinimumHeight(300)
        self.joke_display.setFont(QFont('Arial', 12))
        self.joke_display.setText('Click Get Joke to fetch a random joke!')
        layout.addWidget(self.joke_display)
        
        btn_layout = QHBoxLayout()
        
        self.get_btn = QPushButton('Get Joke')
        self.get_btn.setMinimumHeight(40)
        self.get_btn.clicked.connect(self.get_joke)
        btn_layout.addWidget(self.get_btn)
        
        self.copy_btn = QPushButton('Copy Joke')
        self.copy_btn.setMinimumHeight(40)
        self.copy_btn.clicked.connect(self.copy_joke)
        btn_layout.addWidget(self.copy_btn)
        
        self.clear_btn = QPushButton('Clear')
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.clicked.connect(self.clear_display)
        btn_layout.addWidget(self.clear_btn)
        
        layout.addLayout(btn_layout)
        central_widget.setLayout(layout)
    
    def update_categories(self):
        api_source = self.api_combo.currentText()
        self.category_combo.clear()
        self.category_combo.addItem('Random')
        
        categories = {
            'JokeAPI': ['Programming', 'General', 'Knock-knock'],
            'Official Joke API': ['General', 'Knock-knock'],
            'Ninja Jokes': ['General']
        }
        
        if api_source in categories:
            for cat in categories[api_source][1:]:
                self.category_combo.addItem(cat)
    
    def get_joke(self):
        api_source = self.api_combo.currentText()
        category = self.category_combo.currentText()
        if category == 'Random':
            category = None
        
        self.get_btn.setEnabled(False)
        self.get_btn.setText('Loading...')
        
        self.fetcher = JokeFetcher(api_source, category)
        self.fetcher.joke_fetched.connect(self.display_joke)
        self.fetcher.error_occurred.connect(self.handle_error)
        self.fetcher.start()
    
    def display_joke(self, joke):
        self.joke_display.setText(joke)
        self.get_btn.setEnabled(True)
        self.get_btn.setText('Get Joke')
    
    def handle_error(self, error):
        QMessageBox.critical(self, 'Error', f'Failed to fetch joke: {error}')
        self.get_btn.setEnabled(True)
        self.get_btn.setText('Get Joke')
    
    def copy_joke(self):
        text = self.joke_display.toPlainText()
        if text and text != 'Click Get Joke to fetch a random joke!':
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, 'Success', 'Joke copied to clipboard!')
        else:
            QMessageBox.warning(self, 'Warning', 'No joke to copy!')
    
    def clear_display(self):
        self.joke_display.setText('Click Get Joke to fetch a random joke!')