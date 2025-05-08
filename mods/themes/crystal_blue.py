"""
Crystal Blue Theme for HyprText
==============================

A transparent blue theme with glass-like effects.
This theme features translucent backgrounds and soft blue accents.
"""

# Theme metadata
THEME_NAME = "Crystal Blue"
THEME_DESCRIPTION = "A transparent blue theme with glass-like effects"
THEME_AUTHOR = "Spike"
THEME_VERSION = "1.0"

# Transparency setting - enabled for glass effect
USE_TRANSPARENCY = True

# Font settings
DEFAULT_FONT = "JetBrains Mono"
DEFAULT_FONT_SIZE = 12

# Theme Colors - blue palette with glass effects
DARK_MODE = {
    "background": "rgba(16, 24, 44, 0.85)",  # Semi-transparent deep blue
    "text": "#ffffff",                        # White text
    "accent": "#64B5F6",                      # Light blue accent
    "menu_bg": "rgba(16, 24, 44, 0.85)",      # Same as background
    "menu_hover": "rgba(100, 181, 246, 0.3)", # Transparent accent for hover
    "menu_active": "rgba(100, 181, 246, 0.5)",# More opaque for active state
    "window_bg_gradient_start": "rgba(16, 24, 44, 0.8)",  # Darker transparent blue
    "window_bg_gradient_end": "rgba(25, 42, 80, 0.8)",    # Lighter transparent blue
    "editor_border": "#64B5F6",              # Accent color for borders
    "scrollbar_handle": "#64B5F6"            # Accent color for scrollbars
}

LIGHT_MODE = {
    "background": "rgba(236, 246, 255, 0.85)", # Semi-transparent very light blue
    "text": "#10182C",                          # Dark blue text
    "accent": "#2196F3",                        # Stronger blue accent
    "menu_bg": "rgba(236, 246, 255, 0.85)",     # Same as background
    "menu_hover": "rgba(33, 150, 243, 0.3)",    # Transparent accent for hover
    "menu_active": "rgba(33, 150, 243, 0.5)",   # More opaque for active state
    "window_bg_gradient_start": "rgba(236, 246, 255, 0.8)", # Light blue gradient start
    "window_bg_gradient_end": "rgba(220, 235, 250, 0.8)",   # Slightly darker blue gradient end
    "editor_border": "#2196F3",                # Accent color for borders
    "scrollbar_handle": "#2196F3"              # Accent color for scrollbars
}

# Shadow effect settings - subtle shadow for glass effect
SHADOW_EFFECT = {
    "blur_radius": 10,
    "color": "#64B5F6",  # Light blue shadow
    "offset_x": 0,
    "offset_y": 0
}

# Stylesheet template for dark mode - designed for transparency
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
"""

# Stylesheet template for light mode - same as dark mode template
LIGHT_STYLESHEET_TEMPLATE = DARK_STYLESHEET_TEMPLATE 