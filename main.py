import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from sidebar import Sidebar  # Import Sidebar class
from items_tab import ItemsTab
from cart import Cart

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Store Manager")

        self.setWindowIcon(QIcon("./assets/icon.ico"))


        self.setGeometry(0,0,self.maximumWidth(),self.maximumHeight())
        # 🌟 Main Layout (Vertical)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 🔹 1. Top Bar
        top_widget = QWidget()
        top_widget.setStyleSheet("background-color: #3498db;")  # Blue
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        self.toggle_button = QPushButton("☰")
        self.toggle_button.setFixedSize(40, 40)
        self.toggle_button.setStyleSheet("background-color: #f1cfff; border: none;")
        self.toggle_button.clicked.connect(self.toggle_sidebar)

        top_label = QLabel("Top Bar")
        top_button = QPushButton("Settings")

        top_layout.addWidget(self.toggle_button)
        top_layout.addWidget(top_label)
        top_layout.addStretch(1)
        top_layout.addWidget(top_button)

        # 🔹 2. Main Content Area
        self.main_content = QStackedWidget()

        # 🔹 3. Sidebar (Initially Hidden)
        self.sidebar = Sidebar()
        self.sidebar.setFixedWidth(200)  # Adjust width as needed
        self.sidebar.setVisible(True)  # Hide initially

        #Items Tab
        self.itemsTab = ItemsTab()

        self.main_content.addWidget(self.itemsTab)

        self.cart = Cart()

        self.main_content.addWidget(self.cart)

        # 🔹 4. Overlay Container (Parent for both)
        overlay_widget = QWidget(self)
        overlay_layout = QHBoxLayout(overlay_widget)
        overlay_layout.setContentsMargins(0, 0, 0, 0)
        overlay_layout.addWidget(self.sidebar)
        overlay_layout.addWidget(self.main_content)
        overlay_layout.setStretch(1, 1)

        self.sidebar.Inventory_sub_button_1.clicked.connect(lambda: self.main_content.setCurrentWidget(self.itemsTab))
        self.sidebar.cart_button.clicked.connect(lambda: self.main_content.setCurrentWidget(self.cart))

        # 🔹 Add Widgets to Main Layout
        main_layout.addWidget(top_widget, 1)  # Fixed Top Bar
        main_layout.addWidget(overlay_widget, 20)  # Main Content & Sidebar

        self.sidebar_visible = False  # Track sidebar state

    def toggle_sidebar(self):
        """Toggle sidebar visibility (overlay effect)."""
        self.sidebar.setVisible(not self.sidebar.isVisible())
        self.sidebar_visible = not self.sidebar_visible

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
