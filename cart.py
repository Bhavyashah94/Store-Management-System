from PySide6.QtWidgets import *

class Cart(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)

        cart_items = QWidget()

        button_holder = QHBoxLayout

        top_bar = QHBoxLayout(self)
        