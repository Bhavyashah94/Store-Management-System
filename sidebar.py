# sidebar.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

MainButtonHeight = 50
SubButtonHeight = 50

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #f1c40f;")  # Yellow Sidebar
        self.setMinimumWidth(50)  # Minimum width to prevent complete collapse
        self.setContentsMargins(0, 0, 0, 0)

        # 🌟 Sidebar Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar Buttons
        self.cart_button = QPushButton("Cart")
        self.inventory_button = QPushButton("Inventory")
        self.sales_button = QPushButton("Sales")
        self.purchases_button = QPushButton("Purchases")

        self.cart_button.setMinimumHeight(MainButtonHeight)
        self.inventory_button.setMinimumHeight(MainButtonHeight)
        self.sales_button.setMinimumHeight(MainButtonHeight)
        self.purchases_button.setMinimumHeight(MainButtonHeight)

        # Expandable Inventory Section
        self.Inventory_sub_button_1 = QPushButton("  - Items")
        self.Inventory_sub_button_2 = QPushButton("  - Group Items")
        self.Inventory_sub_button_1.setVisible(False)
        self.Inventory_sub_button_2.setVisible(False)

        self.Inventory_sub_button_1.setMinimumHeight(SubButtonHeight)
        self.Inventory_sub_button_2.setMinimumHeight(SubButtonHeight)

        self.Inventory_sub_button_1.setStyleSheet("background-color: #f1c4Ff;")
        self.Inventory_sub_button_2.setStyleSheet("background-color: #f1c4Ff;")

        self.inventory_button.clicked.connect(self.toggle_inventory)



        # Add buttons to layout
        self.layout.addWidget(self.cart_button)
        self.layout.addWidget(self.inventory_button)
        self.layout.addWidget(self.Inventory_sub_button_1)
        self.layout.addWidget(self.Inventory_sub_button_2)
        self.layout.addWidget(self.sales_button)
        self.layout.addWidget(self.purchases_button)
        self.layout.addStretch(1)

    def toggle_inventory(self):
        """Show or hide the inventory options."""
        state = not self.Inventory_sub_button_1.isVisible()
        self.Inventory_sub_button_1.setVisible(state)
        self.Inventory_sub_button_2.setVisible(state)
