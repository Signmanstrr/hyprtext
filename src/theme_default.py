"""
HyprText Default Theme
=====================

This file defines the default theme for HyprText.
It serves as a reference for creating custom themes.

To create a custom theme:
1. Copy this file to hyprtext/mods/themes/your_theme_name.py
2. Modify the values as desired
3. Restart HyprText or use the Theme menu to apply the theme
"""

# Theme metadata
THEME_NAME = "Default"
THEME_DESCRIPTION = "Default HyprText theme with Hyprland-inspired aesthetics"
THEME_AUTHOR = "HyprText Team"
THEME_VERSION = "1.0"

# Transparency setting - Default theme uses transparency
USE_TRANSPARENCY = True

# Application settings
APP_NAME = "HyprText"

# Font settings
DEFAULT_FONT = "JetBrains Mono"
DEFAULT_FONT_SIZE = 12

# Theme Colors
DARK_MODE = {
    "background": "rgba(10, 10, 10, 0.85)",  # Semi-transparent background
    "text": "#ffffff",
    "accent": "#64ffda",
    "menu_bg": "rgba(10, 10, 26, 0.85)",     # More transparent
    "menu_hover": "rgba(100, 255, 218, 0.3)", # More visible hover
    "menu_active": "rgba(100, 255, 218, 0.5)", # More visible active state
    "window_bg_gradient_start": "rgba(0, 0, 0, 0.8)",  # More transparent
    "window_bg_gradient_end": "rgba(10, 10, 26, 0.8)",  # More transparent
    "editor_border": "#64ffda",
    "scrollbar_handle": "#64ffda"
}

LIGHT_MODE = {
    "background": "rgba(255, 255, 255, 0.85)",  # Semi-transparent background
    "text": "#0a192f",
    "accent": "#64ffda",
    "menu_bg": "rgba(255, 255, 255, 0.85)",     # More transparent
    "menu_hover": "rgba(100, 255, 218, 0.3)",   # More visible hover
    "menu_active": "rgba(100, 255, 218, 0.5)",  # More visible active state
    "window_bg_gradient_start": "rgba(240, 244, 248, 0.8)",  # More transparent
    "window_bg_gradient_end": "rgba(230, 233, 240, 0.8)",    # More transparent
    "editor_border": "#64ffda",
    "scrollbar_handle": "#64ffda"
}

# Shadow effect settings
SHADOW_EFFECT = {
    "blur_radius": 15,
    "color": "#64ffda",
    "offset_x": 0,
    "offset_y": 0
}

# Stylesheet template for dark mode
DARK_STYLESHEET_TEMPLATE = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                  stop:0 %(window_bg_gradient_start)s,
                                  stop:1 %(window_bg_gradient_end)s);
    }
    QWidget {
        background: transparent;
        color: %(text)s;
    }
    QTextEdit, QPlainTextEdit {
        background-color: %(background)s;
        color: %(text)s;
        border: 1px solid %(editor_border)s;
        border-radius: 8px;
        padding: 8px;
    }
    QTextEdit:focus, QPlainTextEdit:focus {
        border: 1px solid %(editor_border)s;
        border-radius: 8px;
        background-color: %(background)s;
    }
    QMenuBar {
        background-color: transparent;
        color: %(text)s;
        border: none;
    }
    QMenuBar::item {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border-radius: 12px;
        padding: 8px 16px;
        margin: 4px;
    }
    QMenuBar::item:selected {
        background-color: %(menu_hover)s;
        color: %(accent)s;
    }
    QMenuBar::item:checked {
        background-color: %(menu_active)s;
        color: %(accent)s;
    }
    QMenu {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-radius: 8px;
        padding: 4px;
    }
    QMenu::item {
        padding: 8px 24px 8px 12px;
        border-radius: 6px;
    }
    QMenu::item:selected {
        background-color: %(menu_hover)s;
        color: %(accent)s;
    }
    QMenu::separator {
        height: 1px;
        background-color: %(accent)s;
        margin: 4px 8px;
    }
    QScrollBar:vertical {
        border: none;
        background-color: transparent;
        width: 12px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background-color: %(scrollbar_handle)s;
        border-radius: 6px;
        min-height: 20px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar:horizontal {
        border: none;
        background-color: transparent;
        height: 12px;
        margin: 0px;
    }
    QScrollBar::handle:horizontal {
        background-color: %(scrollbar_handle)s;
        border-radius: 6px;
        min-width: 20px;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }
    
    /* Dialog styling */
    QDialog, QMessageBox, QFileDialog {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-radius: 8px;
    }
    
    /* Button styling */
    QPushButton {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-radius: 6px;
        padding: 6px 12px;
        min-width: 80px;
    }
    QPushButton:hover {
        background-color: %(menu_hover)s;
        color: %(accent)s;
    }
    QPushButton:pressed {
        background-color: %(menu_active)s;
    }
    QPushButton:focus {
        border: 2px solid %(accent)s;
    }
    
    /* Label styling */
    QLabel {
        color: %(text)s;
        background: transparent;
    }
    
    /* CheckBox styling */
    QCheckBox {
        color: %(text)s;
        spacing: 5px;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 1px solid %(accent)s;
    }
    QCheckBox::indicator:checked {
        background-color: %(accent)s;
    }
    
    /* RadioButton styling */
    QRadioButton {
        color: %(text)s;
        spacing: 5px;
    }
    QRadioButton::indicator {
        width: 18px;
        height: 18px;
        border-radius: 9px;
        border: 1px solid %(accent)s;
    }
    QRadioButton::indicator:checked {
        background-color: %(accent)s;
    }
    
    /* ComboBox styling */
    QComboBox {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-radius: 6px;
        padding: 4px 8px;
        min-width: 100px;
    }
    QComboBox:hover {
        border: 1px solid %(accent)s;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid %(accent)s;
    }
    QComboBox QAbstractItemView {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-radius: 0px;
        selection-background-color: %(menu_hover)s;
        selection-color: %(accent)s;
    }
    
    /* LineEdit styling */
    QLineEdit {
        background-color: %(background)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-radius: 6px;
        padding: 4px 8px;
    }
    QLineEdit:focus {
        border: 2px solid %(accent)s;
    }
    
    /* TabWidget styling */
    QTabWidget::pane {
        border: 1px solid %(accent)s;
        border-radius: 8px;
        background-color: %(menu_bg)s;
    }
    QTabBar::tab {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-bottom: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 6px 12px;
        margin-right: 2px;
    }
    QTabBar::tab:selected {
        background-color: %(menu_active)s;
        color: %(accent)s;
    }
    QTabBar::tab:hover:!selected {
        background-color: %(menu_hover)s;
    }
    
    /* GroupBox styling */
    QGroupBox {
        border: 1px solid %(accent)s;
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 15px;
        padding-bottom: 5px;
        color: %(text)s;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 5px;
        color: %(accent)s;
    }
"""

# Stylesheet template for light mode
LIGHT_STYLESHEET_TEMPLATE = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                  stop:0 %(window_bg_gradient_start)s,
                                  stop:1 %(window_bg_gradient_end)s);
    }
    QWidget {
        background: transparent;
        color: %(text)s;
    }
    QTextEdit, QPlainTextEdit {
        background-color: %(background)s;
        color: %(text)s;
        border: 1px solid %(editor_border)s;
        border-radius: 8px;
        padding: 8px;
    }
    QTextEdit:focus, QPlainTextEdit:focus {
        border: 1px solid %(editor_border)s;
        border-radius: 8px;
        background-color: %(background)s;
    }
    QMenuBar {
        background-color: transparent;
        color: %(text)s;
        border: none;
    }
    QMenuBar::item {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border-radius: 12px;
        padding: 8px 16px;
        margin: 4px;
    }
    QMenuBar::item:selected {
        background-color: %(menu_hover)s;
        color: %(accent)s;
    }
    QMenuBar::item:checked {
        background-color: %(menu_active)s;
        color: %(accent)s;
    }
    QMenu {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-radius: 8px;
        padding: 4px;
    }
    QMenu::item {
        padding: 8px 24px 8px 12px;
        border-radius: 6px;
    }
    QMenu::item:selected {
        background-color: %(menu_hover)s;
        color: %(accent)s;
    }
    QMenu::separator {
        height: 1px;
        background-color: %(accent)s;
        margin: 4px 8px;
    }
    QScrollBar:vertical {
        border: none;
        background-color: transparent;
        width: 12px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background-color: %(scrollbar_handle)s;
        border-radius: 6px;
        min-height: 20px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar:horizontal {
        border: none;
        background-color: transparent;
        height: 12px;
        margin: 0px;
    }
    QScrollBar::handle:horizontal {
        background-color: %(scrollbar_handle)s;
        border-radius: 6px;
        min-width: 20px;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }
    
    /* Dialog styling */
    QDialog, QMessageBox, QFileDialog {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-radius: 8px;
    }
    
    /* Button styling */
    QPushButton {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-radius: 6px;
        padding: 6px 12px;
        min-width: 80px;
    }
    QPushButton:hover {
        background-color: %(menu_hover)s;
        color: %(accent)s;
    }
    QPushButton:pressed {
        background-color: %(menu_active)s;
    }
    QPushButton:focus {
        border: 2px solid %(accent)s;
    }
    
    /* Label styling */
    QLabel {
        color: %(text)s;
        background: transparent;
    }
    
    /* CheckBox styling */
    QCheckBox {
        color: %(text)s;
        spacing: 5px;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 1px solid %(accent)s;
    }
    QCheckBox::indicator:checked {
        background-color: %(accent)s;
    }
    
    /* RadioButton styling */
    QRadioButton {
        color: %(text)s;
        spacing: 5px;
    }
    QRadioButton::indicator {
        width: 18px;
        height: 18px;
        border-radius: 9px;
        border: 1px solid %(accent)s;
    }
    QRadioButton::indicator:checked {
        background-color: %(accent)s;
    }
    
    /* ComboBox styling */
    QComboBox {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-radius: 6px;
        padding: 4px 8px;
        min-width: 100px;
    }
    QComboBox:hover {
        border: 1px solid %(accent)s;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid %(accent)s;
    }
    QComboBox QAbstractItemView {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-radius: 0px;
        selection-background-color: %(menu_hover)s;
        selection-color: %(accent)s;
    }
    
    /* LineEdit styling */
    QLineEdit {
        background-color: %(background)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-radius: 6px;
        padding: 4px 8px;
    }
    QLineEdit:focus {
        border: 2px solid %(accent)s;
    }
    
    /* TabWidget styling */
    QTabWidget::pane {
        border: 1px solid %(accent)s;
        border-radius: 8px;
        background-color: %(menu_bg)s;
    }
    QTabBar::tab {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-bottom: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 6px 12px;
        margin-right: 2px;
    }
    QTabBar::tab:selected {
        background-color: %(menu_active)s;
        color: %(accent)s;
    }
    QTabBar::tab:hover:!selected {
        background-color: %(menu_hover)s;
    }
    
    /* GroupBox styling */
    QGroupBox {
        border: 1px solid %(accent)s;
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 15px;
        padding-bottom: 5px;
        color: %(text)s;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 5px;
        color: %(accent)s;
    }
""" 