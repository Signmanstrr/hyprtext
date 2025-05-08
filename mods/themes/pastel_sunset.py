"""
Pastel Sunset Theme for HyprText
================================

A soft, pastel-themed style with red and pink accents.
This theme features clean edges without shadows or blurring.
"""

# Theme metadata
THEME_NAME = "Pastel Sunset"
THEME_DESCRIPTION = "A soft, pastel-themed style with red and pink accents and clean edges"
THEME_AUTHOR = "Spike"
THEME_VERSION = "1.0"

# Transparency setting - set to False for solid background
USE_TRANSPARENCY = False

# Font settings
DEFAULT_FONT = "JetBrains Mono"
DEFAULT_FONT_SIZE = 12

# Theme Colors
DARK_MODE = {
    "background": "#331F2D",  
    "text": "#ffffff",        
    "accent": "#FF8AAE",      
    "menu_bg": "#331F2D",     
    "menu_hover": "#4A2E42",  
    "menu_active": "#5D3B53",  
    "window_bg_gradient_start": "#331F2D",  
    "window_bg_gradient_end": "#442A3B",    
    "editor_border": "#FF8AAE",  # Accent color for borders
    "scrollbar_handle": "#FF8AAE"  # Accent color for scrollbars
}

LIGHT_MODE = {
    "background": "#FFF0F3",   
    "text": "#331F2D",         
    "accent": "#FF5984",       
    "menu_bg": "#FFF0F3",      
    "menu_hover": "#FFE0E6",   
    "menu_active": "#FFD0D9",  
    "window_bg_gradient_start": "#FFF0F3",  
    "window_bg_gradient_end": "#FFDFE7",    
    "editor_border": "#FF5984",  
    "scrollbar_handle": "#FF5984"  
}

# Shadow effect settings
SHADOW_EFFECT = {
    "blur_radius": 0,
    "color": "#00000000",  # Transparent color
    "offset_x": 0,
    "offset_y": 0
}

# Stylesheet template for dark mode - modified for solid background
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
        border: 2px solid %(editor_border)s;
        border-radius: 8px;
        padding: 8px;
    }
    QTextEdit:focus, QPlainTextEdit:focus {
        border: 2px solid %(editor_border)s;
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
        border-radius: 6px;
        top: -1px;
        background-color: %(background)s;
    }
    QTabBar::tab {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-bottom-color: %(menu_bg)s;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 6px 12px;
        margin-right: 2px;
    }
    QTabBar::tab:selected {
        background-color: %(menu_active)s;
        color: %(accent)s;
    }
    QTabBar::tab:!selected {
        margin-top: 2px;
    }
    
    /* ProgressBar styling */
    QProgressBar {
        border: 1px solid %(accent)s;
        border-radius: 6px;
        background-color: %(background)s;
        color: %(text)s;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: %(accent)s;
        width: 1px;
    }
    
    /* ToolTip styling */
    QToolTip {
        background-color: %(menu_bg)s;
        color: %(text)s;
        border: 1px solid %(accent)s;
        border-radius: 4px;
        padding: 4px;
    }
    
    /* StatusBar styling */
    QStatusBar {
        background-color: %(menu_bg)s;
        color: %(text)s;
    }
    
    /* GroupBox styling */
    QGroupBox {
        background-color: transparent;
        border: 1px solid %(accent)s;
        border-radius: 6px;
        margin-top: 20px;
        padding-top: 24px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 10px;
        color: %(text)s;
    }
"""

# Stylesheet template for light mode - same as dark mode template
LIGHT_STYLESHEET_TEMPLATE = DARK_STYLESHEET_TEMPLATE 
