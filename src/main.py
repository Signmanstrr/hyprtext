#!/usr/bin/env python3

import sys
import os
import traceback
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, 
    QMenuBar, QMenu, QMessageBox, QHBoxLayout, QTextEdit,
    QPushButton, QToolButton, QGraphicsOpacityEffect, QLabel, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QAction, QPalette, QColor, QActionGroup, QIcon
from PyQt6.QtCore import Qt, QSettings, QSize, QPoint, QPropertyAnimation, QEasingCurve

# Import our modules
from theme_manager import ThemeManager, APP_NAME
from animation import AnimatedTextEdit, MenuFader
from file_manager import FileManager
from mode_manager import mode_manager
from extension_manager import extension_manager
from icon_manager import get_icon, ICON_FILE, ICON_EDIT, ICON_MODE, ICON_THEME, ICON_EXTENSION

class CircularMenuButton(QToolButton):
    """Custom circular button for menu activation"""
    
    def __init__(self, icon_name, tooltip, parent=None):
        super().__init__(parent)
        self.setToolTip(tooltip)
        
        # Store the icon name as a property for theme changes
        self.setProperty("icon_name", icon_name)
        
        # Set properties for circular appearance
        self.setFixedSize(40, 40)
        self.setIconSize(QSize(24, 24))
        
        # Set the icon using our icon manager instead of system icons
        if icon_name == "file":
            self.setIcon(get_icon(ICON_FILE, self.style().standardIcon(self.style().StandardPixmap.SP_FileIcon)))
        elif icon_name == "edit":
            self.setIcon(get_icon(ICON_EDIT, self.style().standardIcon(self.style().StandardPixmap.SP_FileDialogContentsView)))
        elif icon_name == "mode":
            self.setIcon(get_icon(ICON_MODE, self.style().standardIcon(self.style().StandardPixmap.SP_FileDialogDetailedView)))
        elif icon_name == "theme":
            self.setIcon(get_icon(ICON_THEME, self.style().standardIcon(self.style().StandardPixmap.SP_DesktopIcon)))
        elif icon_name == "extension":
            self.setIcon(get_icon(ICON_EXTENSION, self.style().standardIcon(self.style().StandardPixmap.SP_FileDialogContentsView)))
        
        # Apply theme-based styling
        self.updateStyle()
        
        # Add drop shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)
    
    def updateStyle(self):
        """Update styling based on current theme"""
        # Get theme colors
        is_dark = ThemeManager.is_dark_mode()
        
        # Import directly from theme_default to avoid circular imports
        from theme_default import DARK_MODE, LIGHT_MODE
        
        # Get the appropriate colors
        colors = DARK_MODE if is_dark else LIGHT_MODE
        
        # Use textbox colors for styling (more sleek and consistent)
        background_color = colors.get("background", "#282c34")
        border_color = colors.get("border", "#3f4451") 
        text_color = colors.get("text", "#abb2bf")
        hover_color = colors.get("menu_hover", "#353b45")
        active_color = colors.get("menu_active", "#3f4451")
        
        # Set rounded style via stylesheet with theme colors
        self.setStyleSheet(f"""
            QToolButton {{
                border-radius: 20px;
                background-color: {background_color};
                color: {text_color};
                border: 1px solid {border_color};
            }}
            QToolButton:hover {{
                background-color: {hover_color};
                border: 1px solid {text_color};
            }}
            QToolButton:pressed {{
                background-color: {active_color};
            }}
        """)
        
        # Colorize the icon to match text color
        icon_name = self.property("icon_name")
        if icon_name:
            fallback_icon = self.icon()
            if icon_name == "file":
                self.setIcon(get_icon(ICON_FILE, 
                    fallback=self.style().standardIcon(self.style().StandardPixmap.SP_FileIcon), 
                    textColor=text_color))
            elif icon_name == "edit":
                self.setIcon(get_icon(ICON_EDIT, 
                    fallback=self.style().standardIcon(self.style().StandardPixmap.SP_FileDialogContentsView),
                    textColor=text_color))
            elif icon_name == "mode":
                self.setIcon(get_icon(ICON_MODE, 
                    fallback=self.style().standardIcon(self.style().StandardPixmap.SP_FileDialogDetailedView),
                    textColor=text_color))
            elif icon_name == "theme":
                self.setIcon(get_icon(ICON_THEME, 
                    fallback=self.style().standardIcon(self.style().StandardPixmap.SP_DesktopIcon),
                    textColor=text_color))
            elif icon_name == "extension":
                self.setIcon(get_icon(ICON_EXTENSION, 
                    fallback=self.style().standardIcon(self.style().StandardPixmap.SP_FileDialogContentsView),
                    textColor=text_color))
    
    def showEvent(self, event):
        """Update styling when shown"""
        self.updateStyle()
        super().showEvent(event)

class HyprText(QMainWindow):
    """Main application window for HyprText editor"""
    
    def __init__(self):
        super().__init__()
        try:
            # Set window flags - always use frameless window for Hyprland
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            
            # We'll handle transparency during theme application
            # For now, start with transparency OFF by default
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
            
            # Create a background widget to control opacity
            self.background_widget = QWidget(self)
            self.setCentralWidget(self.background_widget)
            
            self.current_mode = None
            self.current_file = None
            self.app_name = APP_NAME
            
            # Discover available modes
            mode_manager.discover_modes()
            
            self.initUI()
            self.loadSettings()
            
            # Check for temporary file from previous session
            self.checkForRecoveryFile()
        except Exception as e:
            self._show_error("Failed to initialize application", e)
            sys.exit(1)
        
    def initUI(self):
        """Initialize the user interface"""
        try:
            # Set window properties
            self.setWindowTitle(f'{self.app_name} - Untitled')
            self.setGeometry(100, 100, 800, 600)
            
            # Create layout for the background widget
            main_layout = QVBoxLayout(self.background_widget)
            main_layout.setContentsMargins(10, 10, 10, 10)
            
            # Create top navigation bar with circular buttons
            top_bar = QWidget()
            top_layout = QHBoxLayout(top_bar)
            top_layout.setContentsMargins(5, 5, 5, 0)
            
            # Enable mouse tracking for window drag functionality
            top_bar.setMouseTracking(True)
            top_bar.mousePressEvent = self.topBarMousePressEvent
            top_bar.mouseMoveEvent = self.topBarMouseMoveEvent
            
            # Left side buttons (File and Edit)
            left_buttons = QWidget()
            left_layout = QHBoxLayout(left_buttons)
            left_layout.setContentsMargins(10, 10, 10, 10)  # Add padding to prevent shadow cutoff
            left_layout.setSpacing(15)  # Increase spacing between buttons
            
            # Create File button
            self.file_button = CircularMenuButton("file", "File Menu", self)
            self.file_button.clicked.connect(self.showFileMenu)
            left_layout.addWidget(self.file_button)
            
            # Create Edit button
            self.edit_button = CircularMenuButton("edit", "Edit Menu", self)
            self.edit_button.clicked.connect(self.showEditMenu)
            left_layout.addWidget(self.edit_button)
            
            left_layout.addStretch()
            
            # Center file name label
            self.file_label = QLabel("New File -- Spike's HyprText")
            self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.file_label.setMinimumWidth(300)
            ThemeManager.apply_shadow_effect(self.file_label)
            
            # Mode and theme info label below the file name
            self.info_label = QLabel("Standard Mode -- in Default")
            self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.info_label.setMinimumWidth(300)
            
            # Create a container for the labels
            labels_container = QWidget()
            labels_layout = QVBoxLayout(labels_container)
            labels_layout.setContentsMargins(0, 0, 0, 0)
            labels_layout.setSpacing(1)  # Minimal spacing between labels
            
            # Add labels to container
            labels_layout.addWidget(self.file_label)
            labels_layout.addWidget(self.info_label)
            
            # Right side buttons (Modes and Themes)
            right_buttons = QWidget()
            right_layout = QHBoxLayout(right_buttons)
            right_layout.setContentsMargins(10, 10, 10, 10)  # Add padding to prevent shadow cutoff
            right_layout.setSpacing(15)  # Increase spacing between buttons
            
            right_layout.addStretch()
            
            # Create Modes button
            self.modes_button = CircularMenuButton("mode", "Modes Menu", self)
            self.modes_button.clicked.connect(self.showModesMenu)
            right_layout.addWidget(self.modes_button)
            
            # Create Themes button
            self.themes_button = CircularMenuButton("theme", "Themes Menu", self)
            self.themes_button.clicked.connect(self.showThemesMenu)
            right_layout.addWidget(self.themes_button)
            
            # Create Extensions button
            self.extensions_button = CircularMenuButton("extension", "Extensions Menu", self)
            self.extensions_button.clicked.connect(self.showExtensionsMenu)
            right_layout.addWidget(self.extensions_button)
            
            # Add left, center, and right components to top bar
            top_layout.addWidget(left_buttons)
            top_layout.addWidget(labels_container, 1)  # 1 for stretch factor
            top_layout.addWidget(right_buttons)
            
            # Add top bar to main layout
            main_layout.addWidget(top_bar)
            
            # Create content area
            self.content_widget = QWidget()
            content_layout = QVBoxLayout(self.content_widget)
            content_layout.setContentsMargins(0, 0, 0, 0)
            
            # Create default text editor
            self.text_edit = AnimatedTextEdit()
            self.text_edit.setFont(ThemeManager.get_editor_font())
            content_layout.addWidget(self.text_edit)
            
            # Add content area to main layout
            main_layout.addWidget(self.content_widget)
            
            # Set layout for central widget
            self.layout = content_layout
            
            # Dictionary to store editor widgets for each mode
            self.mode_editors = {}
            
            # Create menus (invisible until triggered by buttons)
            self.createMenus()
            
            # Apply theme
            self.applyTheme()
            
            # Ensure we're in Standard Mode by default
            self.text_edit.setVisible(True)
            self.current_mode = None
            
            # Update window title to reflect Standard Mode
            theme_name = ThemeManager.get_current_theme()
            self.setWindowTitle(f'{self.app_name} - Untitled (Standard Mode) [{theme_name}]')
            
            # Initialize the drag position for moving the window
            self.drag_position = None
            
            # Update the info label for the initial state
            self.updateInfoLabel()
            
            # Apply active extensions' layout modifications
            self.refreshExtensionLayouts()
        except Exception as e:
            self._show_error("Failed to initialize UI", e)
        
    def createMenus(self):
        """Create application menus (without menubar)"""
        try:
            # Get the theme's text color for icons
            is_dark = ThemeManager.is_dark_mode()
            icon_color = "#FFFFFF" if is_dark else "#000000"
            
            # File menu
            self.file_menu = QMenu(self)
            
            new_action = QAction('New', self)
            new_action.setShortcut('Ctrl+N')
            new_action.triggered.connect(self.newFile)
            new_action.setIcon(get_icon("new", self.style().standardIcon(self.style().StandardPixmap.SP_FileIcon), textColor=icon_color))
            self.file_menu.addAction(new_action)
            
            open_action = QAction('Open', self)
            open_action.setShortcut('Ctrl+O')
            open_action.triggered.connect(self.openFile)
            open_action.setIcon(get_icon("open", self.style().standardIcon(self.style().StandardPixmap.SP_DialogOpenButton), textColor=icon_color))
            self.file_menu.addAction(open_action)
            
            save_action = QAction('Save', self)
            save_action.setShortcut('Ctrl+S')
            save_action.triggered.connect(self.saveFile)
            save_action.setIcon(get_icon("save", self.style().standardIcon(self.style().StandardPixmap.SP_DialogSaveButton), textColor=icon_color))
            self.file_menu.addAction(save_action)
            
            self.file_menu.addSeparator()
            
            exit_action = QAction('Exit', self)
            exit_action.setShortcut('Ctrl+Q')
            exit_action.triggered.connect(self.close)
            exit_action.setIcon(get_icon("exit", self.style().standardIcon(self.style().StandardPixmap.SP_DialogCloseButton), textColor=icon_color))
            self.file_menu.addAction(exit_action)
            
            # Edit menu
            self.edit_menu = QMenu(self)
            
            undo_action = QAction('Undo', self)
            undo_action.setShortcut('Ctrl+Z')
            undo_action.triggered.connect(self.undo)
            undo_action.setIcon(get_icon("undo", self.style().standardIcon(self.style().StandardPixmap.SP_ArrowBack), textColor=icon_color))
            self.edit_menu.addAction(undo_action)
            
            redo_action = QAction('Redo', self)
            redo_action.setShortcut('Ctrl+Y')
            redo_action.triggered.connect(self.redo)
            redo_action.setIcon(get_icon("redo", self.style().standardIcon(self.style().StandardPixmap.SP_ArrowForward), textColor=icon_color))
            self.edit_menu.addAction(redo_action)
            
            self.edit_menu.addSeparator()
            
            cut_action = QAction('Cut', self)
            cut_action.setShortcut('Ctrl+X')
            cut_action.triggered.connect(self.cut)
            cut_action.setIcon(get_icon("cut", self.style().standardIcon(self.style().StandardPixmap.SP_DialogResetButton), textColor=icon_color))
            self.edit_menu.addAction(cut_action)
            
            copy_action = QAction('Copy', self)
            copy_action.setShortcut('Ctrl+C')
            copy_action.triggered.connect(self.copy)
            copy_action.setIcon(get_icon("copy", self.style().standardIcon(self.style().StandardPixmap.SP_FileLinkIcon), textColor=icon_color))
            self.edit_menu.addAction(copy_action)
            
            paste_action = QAction('Paste', self)
            paste_action.setShortcut('Ctrl+V')
            paste_action.triggered.connect(self.paste)
            paste_action.setIcon(get_icon("paste", self.style().standardIcon(self.style().StandardPixmap.SP_ArrowDown), textColor=icon_color))
            self.edit_menu.addAction(paste_action)
            
            # Modes menu
            self.modes_menu = QMenu(self)
            
            # Add refresh action first
            refresh_action = QAction('Refresh Modes', self)
            refresh_action.setShortcut('Ctrl+R')
            refresh_action.triggered.connect(self.refreshModes)
            refresh_action.setIcon(get_icon("refresh", self.style().standardIcon(self.style().StandardPixmap.SP_BrowserReload), textColor=icon_color))
            self.modes_menu.addAction(refresh_action)
            
            self.modes_menu.addSeparator()
            
            # Build the modes menu
            self.buildModesMenu()
            
            # Themes menu
            self.themes_menu = QMenu(self)
            
            # Add refresh action first
            refresh_themes_action = QAction('Refresh Themes', self)
            refresh_themes_action.setShortcut('Ctrl+T')
            refresh_themes_action.triggered.connect(self.refreshThemes)
            refresh_themes_action.setIcon(get_icon("refresh", self.style().standardIcon(self.style().StandardPixmap.SP_BrowserReload), textColor=icon_color))
            self.themes_menu.addAction(refresh_themes_action)
            
            self.themes_menu.addSeparator()
            
            # Build the themes menu
            self.buildThemesMenu()
            
            # Extensions menu
            self.extensions_menu = QMenu(self)
            
            # Add refresh action first
            refresh_extensions_action = QAction('Refresh Extensions', self)
            refresh_extensions_action.setShortcut('Ctrl+E')
            refresh_extensions_action.triggered.connect(self.refreshExtensions)
            refresh_extensions_action.setIcon(get_icon("refresh", self.style().standardIcon(self.style().StandardPixmap.SP_BrowserReload), textColor=icon_color))
            self.extensions_menu.addAction(refresh_extensions_action)
            
            self.extensions_menu.addSeparator()
            
            # Build the extensions menu
            self.buildExtensionsMenu()
            
        except Exception as e:
            self._show_error("Failed to create menus", e)
    
    def showFileMenu(self):
        """Show the file menu when the file button is clicked"""
        # Position the menu below the button (like other menus)
        pos = self.file_button.mapToGlobal(QPoint(0, self.file_button.height()))
        self.file_menu.popup(pos)
        # Connect aboutToHide signal to reset button state
        self.file_menu.aboutToHide.connect(lambda: self.resetButtonState(self.file_button))
    
    def showEditMenu(self):
        """Show the edit menu when the edit button is clicked"""
        # Position the menu below the button (like other menus)
        pos = self.edit_button.mapToGlobal(QPoint(0, self.edit_button.height()))
        self.edit_menu.popup(pos)
        # Connect aboutToHide signal to reset button state
        self.edit_menu.aboutToHide.connect(lambda: self.resetButtonState(self.edit_button))
    
    def showModesMenu(self):
        """Show the modes menu when the modes button is clicked"""
        # Position the menu below the button
        pos = self.modes_button.mapToGlobal(QPoint(0, self.modes_button.height()))
        self.modes_menu.popup(pos)
        # Connect aboutToHide signal to reset button state
        self.modes_menu.aboutToHide.connect(lambda: self.resetButtonState(self.modes_button))
    
    def showThemesMenu(self):
        """Show the themes menu when the themes button is clicked"""
        # Position the menu below the button
        pos = self.themes_button.mapToGlobal(QPoint(0, self.themes_button.height()))
        self.themes_menu.popup(pos)
        # Connect aboutToHide signal to reset button state
        self.themes_menu.aboutToHide.connect(lambda: self.resetButtonState(self.themes_button))
    
    def showExtensionsMenu(self):
        """Show the extensions menu when the extensions button is clicked"""
        # Position the menu below the button
        pos = self.extensions_button.mapToGlobal(QPoint(0, self.extensions_button.height()))
        self.extensions_menu.popup(pos)
        # Connect aboutToHide signal to reset button state
        self.extensions_menu.aboutToHide.connect(lambda: self.resetButtonState(self.extensions_button))
    
    def buildModesMenu(self):
        """Build or rebuild the modes menu items"""
        try:
            # Clear existing mode actions (except the refresh and separator)
            for action in self.modes_menu.actions()[2:]:
                self.modes_menu.removeAction(action)
            
            # Create a new action group
            self.mode_group = QActionGroup(self)
            self.mode_group.setExclusive(True)
            
            # Add standard mode first
            standard_action = QAction('Standard Mode', self)
            standard_action.setCheckable(True)
            standard_action.setChecked(self.current_mode is None)
            standard_action.triggered.connect(lambda: self.switchToMode(None))
            self.mode_group.addAction(standard_action)
            self.modes_menu.addAction(standard_action)
            
            # Add other available modes
            for mode_name in mode_manager.get_mode_names():
                action = QAction(mode_name, self)
                action.setCheckable(True)
                action.setChecked(self.current_mode == mode_name)
                action.setToolTip(mode_manager.get_mode_description(mode_name))
                action.triggered.connect(lambda checked, name=mode_name: self.switchToMode(name))
                self.mode_group.addAction(action)
                self.modes_menu.addAction(action)
        except Exception as e:
            self._show_error("Failed to build modes menu", e)
    
    def buildThemesMenu(self):
        """Build or rebuild the themes menu items"""
        try:
            # Clear existing theme actions (except the refresh and separator)
            for action in self.themes_menu.actions()[2:]:
                self.themes_menu.removeAction(action)
            
            # Create a new action group
            self.theme_group = QActionGroup(self)
            self.theme_group.setExclusive(True)
            
            # Add available themes
            current_theme = ThemeManager.get_current_theme()
            for theme_name in ThemeManager.get_available_themes():
                action = QAction(theme_name, self)
                action.setCheckable(True)
                action.setChecked(current_theme == theme_name)
                action.setToolTip(ThemeManager.get_theme_description(theme_name))
                action.triggered.connect(lambda checked, name=theme_name: self.switchTheme(name))
                self.theme_group.addAction(action)
                self.themes_menu.addAction(action)
        except Exception as e:
            self._show_error("Failed to build themes menu", e)
    
    def buildExtensionsMenu(self):
        """Build or rebuild the extensions menu items"""
        try:
            # Clear existing extension actions (except the refresh and separator)
            for action in self.extensions_menu.actions()[2:]:
                self.extensions_menu.removeAction(action)
            
            # Add available extensions
            for ext_name in extension_manager.get_available_extensions():
                action = QAction(ext_name, self)
                action.setCheckable(True)
                action.setChecked(extension_manager.is_extension_active(ext_name))
                action.setToolTip(extension_manager.get_extension_description(ext_name))
                action.triggered.connect(lambda checked, name=ext_name: self.toggleExtension(name, checked))
                self.extensions_menu.addAction(action)
            
            # If no extensions found, add a placeholder action
            if len(self.extensions_menu.actions()) <= 2:  # Only refresh and separator
                no_extensions_action = QAction('No Extensions Found', self)
                no_extensions_action.setEnabled(False)
                self.extensions_menu.addAction(no_extensions_action)
        except Exception as e:
            self._show_error("Failed to build extensions menu", e)
    
    def refreshModes(self):
        """Refresh the available modes"""
        try:
            # Remember current mode
            current_mode = self.current_mode
            
            # Rescan for modes
            mode_manager.discover_modes()
            
            # Rebuild the modes menu
            self.buildModesMenu()
            
            # Get debug information
            modes = mode_manager.get_mode_names()
            debug_info = f"Found {len(modes)} editor modes:\n"
            if modes:
                for mode in modes:
                    debug_info += f"• {mode}: {mode_manager.get_mode_description(mode)}\n"
            else:
                debug_info += "No modes found. Check the paths:\n"
                debug_info += f"Working directory: {os.getcwd()}\n"
                src_dir = os.path.dirname(os.path.abspath(__file__))
                app_dir = os.path.dirname(src_dir)
                modes_dir = os.path.join(app_dir, "mods", "modes")
                debug_info += f"Expected modes directory: {modes_dir}\n"
                if os.path.exists(modes_dir):
                    debug_info += "Directory exists. Contents:\n"
                    for f in os.listdir(modes_dir):
                        debug_info += f"  - {f}\n"
                else:
                    debug_info += "Directory does not exist!\n"
                    
                # Try the current working directory path
                modes_dir = os.path.join(os.getcwd(), "mods", "modes")
                debug_info += f"Alternative modes directory: {modes_dir}\n"
                if os.path.exists(modes_dir):
                    debug_info += "Directory exists. Contents:\n"
                    for f in os.listdir(modes_dir):
                        debug_info += f"  - {f}\n"
                else:
                    debug_info += "Directory does not exist!\n"
            
            # Show a message about the refresh with debug info
            QMessageBox.information(self, 'Modes Refreshed', debug_info)
            
            # If current mode is no longer available, switch to standard
            if current_mode is not None and current_mode not in mode_manager.get_mode_names():
                self.switchToMode(None)
                
        except Exception as e:
            self._show_error("Failed to refresh modes", e)
    
    def refreshThemes(self):
        """Refresh the available themes"""
        try:
            # Remember current theme
            current_theme = ThemeManager.get_current_theme()
            
            # Rescan for themes
            ThemeManager.discover_themes()
            
            # Rebuild the themes menu
            self.buildThemesMenu()
            
            # Get debug information
            themes = ThemeManager.get_available_themes()
            debug_info = f"Found {len(themes)} themes:\n"
            if themes:
                for theme in themes:
                    debug_info += f"• {theme}: {ThemeManager.get_theme_description(theme)}\n"
            else:
                debug_info += "No themes found. Check the paths:\n"
                debug_info += f"Working directory: {os.getcwd()}\n"
                src_dir = os.path.dirname(os.path.abspath(__file__))
                app_dir = os.path.dirname(src_dir)
                themes_dir = os.path.join(app_dir, "mods", "themes")
                debug_info += f"Expected themes directory: {themes_dir}\n"
                if os.path.exists(themes_dir):
                    debug_info += "Directory exists. Contents:\n"
                    for f in os.listdir(themes_dir):
                        debug_info += f"  - {f}\n"
                else:
                    debug_info += "Directory does not exist!\n"
            
            # Show a message about the refresh with debug info
            QMessageBox.information(self, 'Themes Refreshed', debug_info)
            
            # If current theme is no longer available, switch to default
            if current_theme not in ThemeManager.get_available_themes():
                self.switchTheme("Default")
                
        except Exception as e:
            self._show_error("Failed to refresh themes", e)
    
    def refreshExtensions(self):
        """Refresh the available extensions"""
        try:
            # Re-initialize the extension manager (discovers new extensions)
            extension_manager._discover_extensions()
            
            # Rebuild the extensions menu
            self.buildExtensionsMenu()
            
            # Get debug information
            extensions = extension_manager.get_available_extensions()
            debug_info = f"Found {len(extensions)} extensions:\n"
            if extensions:
                for ext in extensions:
                    is_active = extension_manager.is_extension_active(ext)
                    status = "Active" if is_active else "Inactive"
                    debug_info += f"• {ext}: {extension_manager.get_extension_description(ext)} ({status})\n"
            else:
                debug_info += "No extensions found. Check the paths:\n"
                debug_info += f"Working directory: {os.getcwd()}\n"
                src_dir = os.path.dirname(os.path.abspath(__file__))
                app_dir = os.path.dirname(src_dir)
                extensions_dir = os.path.join(app_dir, "mods", "extensions")
                debug_info += f"Expected extensions directory: {extensions_dir}\n"
                if os.path.exists(extensions_dir):
                    debug_info += "Directory exists. Contents:\n"
                    for f in os.listdir(extensions_dir):
                        debug_info += f"  - {f}\n"
                else:
                    debug_info += "Directory does not exist!\n"
            
            # Show a message about the refresh with debug info
            QMessageBox.information(self, 'Extensions Refreshed', debug_info)
            
        except Exception as e:
            self._show_error("Failed to refresh extensions", e)
    
    def switchTheme(self, theme_name):
        """Switch to the specified theme"""
        try:
            if ThemeManager.load_theme(theme_name):
                # Apply the new theme
                self.applyTheme()
                
                # Update window title to show current theme
                file_name = "Untitled" if self.current_file is None else os.path.basename(self.current_file)
                mode_display = "Standard Mode" if self.current_mode is None else self.current_mode
                self.setWindowTitle(f'{self.app_name} - {file_name} ({mode_display}) [{theme_name}]')
                
                # Update info label
                self.updateInfoLabel()
                
                # If the current mode has a post_theme_change hook, call it directly
                if self.current_mode is not None:
                    mode_module = mode_manager.modes.get(self.current_mode)
                    if mode_module and hasattr(mode_module, 'post_theme_change'):
                        print(f"Calling mode-specific post_theme_change for {self.current_mode}")
                        mode_module.post_theme_change(self, theme_name)
                
                # Call post_theme_change hook for extensions
                extension_manager.call_hook_for_all('post_theme_change', self, theme_name)
                
                # Show a message indicating the theme change with styled dialog
                QMessageBox.information(self, 'Theme Changed', f'Switched to the {theme_name} theme')
        except Exception as e:
            self._show_error(f"Failed to switch to theme: {theme_name}", e)
    
    def switchToMode(self, mode_name):
        """Switch to the specified editor mode"""
        try:
            current_text = ""
            
            # Get text from current editor
            if self.current_mode is None:
                current_text = self.text_edit.toPlainText()
            elif self.current_mode in self.mode_editors:
                current_text = self.mode_editors[self.current_mode].toPlainText()
            
            # Hide all editors
            self.text_edit.setVisible(False)
            for editor in self.mode_editors.values():
                editor.setVisible(False)
            
            if mode_name is None:
                # Switch to standard mode
                self.text_edit.setVisible(True)
                self.text_edit.setText(current_text)
                self.current_mode = None
            else:
                # Switch to custom mode
                if mode_name not in self.mode_editors:
                    # Create editor for this mode if not exist
                    editor = mode_manager.create_editor_for_mode(mode_name, self)
                    self.mode_editors[mode_name] = editor
                    # Add to content layout instead of the old layout reference
                    self.layout.addWidget(editor)
                    ThemeManager.apply_shadow_effect(editor)
                
                # Show the editor for this mode
                self.mode_editors[mode_name].setVisible(True)
                self.mode_editors[mode_name].setPlainText(current_text)
                self.current_mode = mode_name
            
            # Reapply the theme to apply any mode-specific color overrides
            self.applyTheme()
            
            # Update window title to reflect mode
            mode_display = "Standard Mode" if mode_name is None else mode_name
            file_name = "Untitled" if self.current_file is None else os.path.basename(self.current_file)
            theme_name = ThemeManager.get_current_theme()
            self.setWindowTitle(f'{self.app_name} - {file_name} ({mode_display}) [{theme_name}]')
            
            # Update info label
            self.updateInfoLabel()
            
            # Call post_mode_change hook for extensions
            extension_manager.call_hook_for_all('post_mode_change', self, mode_name)
            
        except Exception as e:
            self._show_error(f"Failed to switch to mode: {mode_name}", e)
            
    def undo(self):
        """Undo the last action in the active editor"""
        try:
            if self.current_mode is None:
                self.text_edit.undo()
            elif self.current_mode in self.mode_editors:
                self.mode_editors[self.current_mode].undo()
        except Exception as e:
            self._show_error("Undo operation failed", e)
            
    def redo(self):
        """Redo the last undone action in the active editor"""
        try:
            if self.current_mode is None:
                self.text_edit.redo()
            elif self.current_mode in self.mode_editors:
                self.mode_editors[self.current_mode].redo()
        except Exception as e:
            self._show_error("Redo operation failed", e)
            
    def cut(self):
        """Cut selected text in the active editor"""
        try:
            if self.current_mode is None:
                self.text_edit.cut()
            elif self.current_mode in self.mode_editors:
                self.mode_editors[self.current_mode].cut()
        except Exception as e:
            self._show_error("Cut operation failed", e)
            
    def copy(self):
        """Copy selected text in the active editor"""
        try:
            if self.current_mode is None:
                self.text_edit.copy()
            elif self.current_mode in self.mode_editors:
                self.mode_editors[self.current_mode].copy()
        except Exception as e:
            self._show_error("Copy operation failed", e)
            
    def paste(self):
        """Paste clipboard content in the active editor"""
        try:
            if self.current_mode is None:
                self.text_edit.paste()
            elif self.current_mode in self.mode_editors:
                self.mode_editors[self.current_mode].paste()
        except Exception as e:
            self._show_error("Paste operation failed", e)
        
    def getCurrentEditor(self):
        """Return the currently active editor widget"""
        if self.current_mode is None:
            return self.text_edit
        elif self.current_mode in self.mode_editors:
            return self.mode_editors[self.current_mode]
        return self.text_edit
        
    def applyTheme(self):
        """Apply theme settings to the application"""
        try:
            is_dark = ThemeManager.is_dark_mode()
            
            # Get the current theme module
            theme_module = ThemeManager._get_theme_module()
            theme_name = ThemeManager.get_current_theme()
            
            # Get the mode-specific color dictionary
            if is_dark:
                theme_colors = getattr(theme_module, 'DARK_MODE', {})
            else:
                theme_colors = getattr(theme_module, 'LIGHT_MODE', {})
                
            # Apply mode-specific color overrides if available
            if self.current_mode is not None:
                mode_overrides = mode_manager.get_theme_color_overrides(self.current_mode)
                if mode_overrides:
                    # Create a copy of theme_colors and update it with mode overrides
                    theme_colors = theme_colors.copy()
                    theme_colors.update(mode_overrides)
                    print(f"Applied color overrides for {self.current_mode} mode")
                
            # Check if theme wants transparency
            wants_transparency = getattr(theme_module, 'USE_TRANSPARENCY', True)
            
            # Apply transparency setting
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, wants_transparency)
            
            # Set the background color based on transparency
            if wants_transparency:
                # For transparent themes, use gradient from stylesheet
                bg_style = """
                    QWidget#backgroundWidget {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 %s,
                                      stop:1 %s);
                    }
                """ % (
                    theme_colors.get("window_bg_gradient_start", "rgba(0,0,0,0.9)"),
                    theme_colors.get("window_bg_gradient_end", "rgba(10,10,26,0.9)")
                )
            else:
                # For solid themes, use a solid color
                solid_bg = theme_colors.get("background", "#000000" if is_dark else "#FFFFFF")
                bg_style = f"""
                    QWidget#backgroundWidget {{
                        background-color: {solid_bg};
                    }}
                """
            
            # Set object name for the background widget so we can target it with CSS
            self.background_widget.setObjectName("backgroundWidget")
            
            # Apply style directly to background widget
            self.background_widget.setStyleSheet(bg_style)
            
            # Get the general stylesheet for the application
            stylesheet = ThemeManager.get_stylesheet(is_dark)
            
            # Apply stylesheet to application
            QApplication.instance().setStyleSheet(stylesheet)
            
            # Update all UI elements
            self.updateUIElementsForTheme(theme_colors)
            
            print(f"Applied theme: {theme_name} (Transparency: {wants_transparency})")
            
        except Exception as e:
            self._show_error(f"Failed to apply theme: {str(e)}", e)
            import traceback
            traceback.print_exc()
    
    def updateUIElementsForTheme(self, colors):
        """Update UI elements to match the current theme"""
        try:
            # Update circular menu buttons
            self.file_button.updateStyle()
            self.edit_button.updateStyle()
            self.modes_button.updateStyle()
            self.themes_button.updateStyle()
            self.extensions_button.updateStyle()
            
            # Style the file label
            text_color = colors.get("text", "#ffffff")
            secondary_color = colors.get("accent", "#64ffda")
            
            self.file_label.setStyleSheet(f"""
                QLabel {{
                    color: {text_color};
                    font-weight: bold;
                    font-size: 12pt;
                    padding: 5px 5px 0px 5px;
                }}
            """)
            
            # Style the info label with faded text
            self.info_label.setStyleSheet(f"""
                QLabel {{
                    color: {secondary_color};
                    font-size: 9pt;
                    padding: 0px 5px 5px 5px;
                    opacity: 0.7;
                }}
            """)
            
            # Apply shadow effects
            ThemeManager.apply_shadow_effect(self.text_edit)
            for editor in self.mode_editors.values():
                ThemeManager.apply_shadow_effect(editor)
                
            ThemeManager.apply_shadow_effect(self.file_button)
            ThemeManager.apply_shadow_effect(self.edit_button)
            ThemeManager.apply_shadow_effect(self.modes_button)
            ThemeManager.apply_shadow_effect(self.themes_button)
            ThemeManager.apply_shadow_effect(self.extensions_button)
            ThemeManager.apply_shadow_effect(self.file_label)
            
        except Exception as e:
            self._show_error(f"Failed to update UI elements: {str(e)}", e)
    
    def newFile(self):
        """Create a new file"""
        try:
            # Clear all editors
            self.text_edit.clear()
            for editor in self.mode_editors.values():
                if hasattr(editor, 'clear'):
                    editor.clear()
                elif hasattr(editor, 'setPlainText'):
                    editor.setPlainText("")
            
            self.current_file = None
            mode_display = "Standard Mode" if self.current_mode is None else self.current_mode
            theme_name = ThemeManager.get_current_theme()
            self.setWindowTitle(f'{self.app_name} - Untitled ({mode_display}) [{theme_name}]')
            
            # Update the file label
            self.updateFileLabel()
            
            # Update the info label
            self.updateInfoLabel()
        except Exception as e:
            self._show_error("Failed to create new file", e)
        
    def openFile(self):
        """Open a file"""
        try:
            file_path = FileManager.get_open_file_path(self)
            if file_path:
                text = FileManager.read_file(file_path)
                
                # Update all editors
                self.text_edit.setText(text)
                for editor in self.mode_editors.values():
                    if hasattr(editor, 'setPlainText'):
                        editor.setPlainText(text)
                    elif hasattr(editor, 'setText'):
                        editor.setText(text)
                
                self.current_file = file_path
                mode_display = "Standard Mode" if self.current_mode is None else self.current_mode
                theme_name = ThemeManager.get_current_theme()
                self.setWindowTitle(f'{self.app_name} - {os.path.basename(file_path)} ({mode_display}) [{theme_name}]')
                
                # Update the file label
                self.updateFileLabel()
                
                # Update the info label
                self.updateInfoLabel()
                
                # Call post_load_file hook for extensions
                extension_manager.call_hook_for_all('post_load_file', self, file_path)
        except Exception as e:
            self._show_error("Failed to open file", e)
                
    def saveFile(self):
        """Save the current file"""
        try:
            current_editor = self.getCurrentEditor()
            
            if hasattr(current_editor, 'toPlainText'):
                content = current_editor.toPlainText()
            else:
                content = current_editor.toHtml() if hasattr(current_editor, 'toHtml') else ""
            
            # Call pre_save_file hook for extensions
            extension_manager.call_hook_for_all('pre_save_file', self, self.current_file, content)
            
            if not self.current_file:
                file_path = FileManager.get_save_file_path(self)
                if not file_path:
                    return
                self.current_file = file_path
            
            FileManager.write_file(self.current_file, content)
            mode_display = "Standard Mode" if self.current_mode is None else self.current_mode
            theme_name = ThemeManager.get_current_theme()
            self.setWindowTitle(f'{self.app_name} - {os.path.basename(self.current_file)} ({mode_display}) [{theme_name}]')
            
            # Update the file label
            self.updateFileLabel()
            
            # Update the info label
            self.updateInfoLabel()
        except Exception as e:
            self._show_error("Failed to save file", e)
                
    def loadSettings(self):
        """Load application settings"""
        try:
            settings = QSettings(self.app_name, self.app_name)
            geometry = settings.value('geometry')
            if geometry:
                self.restoreGeometry(geometry)
                
            # Always start in Standard Mode
            # Clear any previously saved mode
            self.current_mode = None
            self.switchToMode(None)
            
            # Update menu to reflect Standard Mode is active
            for action in self.mode_group.actions():
                if action.text() == "Standard Mode":
                    action.setChecked(True)
                    break
        except Exception as e:
            self._show_error("Failed to load settings", e)
            
    def checkForRecoveryFile(self):
        """Check for and load temporary recovery file if it exists"""
        try:
            tmp_file_path = os.path.join(os.getcwd(), "tmp.txt")
            if os.path.exists(tmp_file_path):
                # Ask user if they want to recover the unsaved content
                reply = QMessageBox.question(
                    self, 
                    'Recover Unsaved Content',
                    'HyprText found unsaved content from a previous session. Would you like to recover it?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # Load the content
                    content = FileManager.read_file(tmp_file_path)
                    
                    # Set the content in the current editor
                    if self.current_mode is None:
                        self.text_edit.setText(content)
                    elif self.current_mode in self.mode_editors:
                        self.mode_editors[self.current_mode].setPlainText(content)
                    
                    # Update window title to indicate recovered content
                    mode_display = "Standard Mode" if self.current_mode is None else self.current_mode
                    theme_name = ThemeManager.get_current_theme()
                    self.setWindowTitle(f'{self.app_name} - Recovered Content ({mode_display}) [{theme_name}]')
                    
                    # Update the file label
                    self.file_label.setText(f"Recovered Content -- Spike's HyprText")
                    
                    # Update the info label
                    self.updateInfoLabel()
                    
                    # Notify the user
                    QMessageBox.information(
                        self,
                        'Content Recovered',
                        'Unsaved content has been successfully recovered.'
                    )
                
                # Delete the temporary file regardless of choice
                os.remove(tmp_file_path)
        except Exception as e:
            self._show_error(f"Failed to check for recovery file: {str(e)}", e)

    def closeEvent(self, event):
        """Handle window close event"""
        try:
            # Call pre_close hook for active extensions
            extension_manager.call_hook_for_all('pre_close', self)
            
            # Save application settings
            settings = QSettings(self.app_name, self.app_name)
            settings.setValue('geometry', self.saveGeometry())
            settings.setValue('last_mode', self.current_mode)
            
            # Get content from current editor
            current_text = ""
            if self.current_mode is None:
                current_text = self.text_edit.toPlainText()
            elif self.current_mode in self.mode_editors:
                current_text = self.mode_editors[self.current_mode].toPlainText()
            
            # If there's unsaved content, save it to a temporary file
            if current_text.strip() and (self.current_file is None or self.isContentModified()):
                try:
                    tmp_file_path = os.path.join(os.getcwd(), "tmp.txt")
                    FileManager.write_file(tmp_file_path, current_text)
                    print(f"Unsaved content saved to {tmp_file_path}")
                except Exception as save_error:
                    print(f"Failed to save temporary content: {str(save_error)}")
            
            event.accept()
        except Exception as e:
            self._show_error("Failed to save settings", e)
            event.accept()  # Accept anyway to allow closing
    
    def isContentModified(self):
        """Check if the content has been modified since last save"""
        try:
            if self.current_file is None:
                return False
            
            # Get current content
            current_text = ""
            if self.current_mode is None:
                current_text = self.text_edit.toPlainText()
            elif self.current_mode in self.mode_editors:
                current_text = self.mode_editors[self.current_mode].toPlainText()
            
            # Compare with saved file
            saved_text = FileManager.read_file(self.current_file)
            return current_text != saved_text
        except Exception:
            # If any error occurs, assume content is modified
            return True

    def _show_error(self, message, exception=None):
        """Display an error message dialog"""
        error_details = str(exception) if exception else ""
        if exception:
            traceback.print_exc()
        QMessageBox.critical(self, 'Error', f"{message}: {error_details}")

    def topBarMousePressEvent(self, event):
        """Handle mouse press on the top bar to enable window dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def topBarMouseMoveEvent(self, event):
        """Handle mouse move on the top bar to move the window"""
        if event.buttons() & Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def updateFileLabel(self):
        """Update the file name label in the center of the top bar"""
        if self.current_file is None:
            self.file_label.setText("New File -- Spike's HyprText")
        else:
            file_name = os.path.basename(self.current_file)
            self.file_label.setText(f"{file_name} -- Spike's HyprText")
        
        # Also update the info label
        self.updateInfoLabel()

    def updateInfoLabel(self):
        """Update the info label with current mode and theme"""
        try:
            mode_display = "Standard Mode" if self.current_mode is None else self.current_mode
            theme_name = ThemeManager.get_current_theme()
            self.info_label.setText(f"{mode_display} -- in {theme_name}")
        except Exception as e:
            print(f"Failed to update info label: {str(e)}")

    def applyExtensionLayouts(self):
        """Apply layout modifications from active extensions"""
        try:
            extension_manager.call_hook_for_all('modify_layout', self)
        except Exception as e:
            print(f"Error applying extension layouts: {str(e)}")
            traceback.print_exc()

    def toggleExtension(self, extension_name, checked):
        """Toggle an extension on or off"""
        try:
            # Check current states before toggling
            was_active = extension_manager.is_extension_active(extension_name)
            
            # Toggle the extension individually - this calls cleanup for this specific extension
            is_active = extension_manager.toggle_extension(extension_name, self)
            
            # Don't refresh all extensions, only handle the one that changed
            if is_active:
                # Extension was activated - apply its layout modifications only
                print(f"Applying layout for newly activated extension: {extension_name}")
                extension_manager._call_hook(extension_name, 'modify_layout', self)
            else:
                # Extension was deactivated - we don't need to do anything else 
                # since the cleanup hook should have restored its changes
                pass
            
            # Show message
            QMessageBox.information(self, 
                'Extension ' + ('Activated' if is_active else 'Deactivated'), 
                f'The "{extension_name}" extension has been {"activated" if is_active else "deactivated"}.')
            
            # Ensure menu item reflects current state 
            for action in self.extensions_menu.actions():
                if action.text() == extension_name:
                    action.setChecked(is_active)
                    break
                    
        except Exception as e:
            self._show_error(f"Failed to toggle extension: {extension_name}", e)
    
    def refreshExtensionLayouts(self):
        """Refresh and reapply all active extension layouts"""
        try:
            # Get the main layout (needed for potential layout changes)
            main_layout = self.background_widget.layout()
            
            # Make a local copy of active extensions to avoid issues if the list changes during iteration
            active_extensions = list(extension_manager._active_extensions.keys())
            
            print(f"Refreshing layouts for {len(active_extensions)} active extensions")
            
            # Call modify_layout for all active extensions in sequence
            for ext_name in active_extensions:
                # Skip extensions that aren't actually active (might have been disabled)
                if not extension_manager.is_extension_active(ext_name):
                    continue
                    
                print(f"Applying layout for extension: {ext_name}")
                extension_manager._call_hook(ext_name, 'modify_layout', self)
            
            # Force layout update
            if main_layout:
                main_layout.update()
                self.background_widget.updateGeometry()
                
        except Exception as e:
            print(f"Error refreshing extension layouts: {str(e)}")
            traceback.print_exc()

    def resetButtonState(self, button):
        """Reset the hover state of a button"""
        # Force button to update its style
        button.setAttribute(Qt.WidgetAttribute.WA_UnderMouse, False)
        button.update()

def main():
    """Application entry point"""
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')  # Use Fusion style for better theming support
        app.setApplicationName(APP_NAME)
        app.setApplicationDisplayName(APP_NAME)
        
        # Apply stylesheet to the entire application
        is_dark = ThemeManager.is_dark_mode()
        app.setStyleSheet(ThemeManager.get_stylesheet(is_dark))
        
        ex = HyprText()
        # Initialize the file label at startup
        ex.updateFileLabel()
        ex.show()
        
        sys.exit(app.exec())
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main() 