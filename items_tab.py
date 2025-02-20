from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem

class ItemsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 🌟 Top Bar
        top_bar = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search items...")

        self.add_button = QPushButton("Add New")
        self.toggle_view_button = QPushButton("🔲/📄")  # Grid/List toggle
        self.filter_button = QPushButton("Filter")

        top_bar.addWidget(self.search_bar)
        top_bar.addWidget(self.add_button)
        top_bar.addWidget(self.toggle_view_button)
        top_bar.addWidget(self.filter_button)

        # 📄 Items List
        self.list_widget = QListWidget()
        self.populate_list()

        # 🔹 Add everything to layout
        self.layout.addLayout(top_bar)
        self.layout.addWidget(self.list_widget)

    def populate_list(self):
        """Temporary function to populate with dummy items."""
        for i in range(10):
            item = QListWidgetItem(f"Item {i+1}")
            self.list_widget.addItem(item)

class NewItemsTab(QWidget):
    def __init__(self):
        super.__init__()
        