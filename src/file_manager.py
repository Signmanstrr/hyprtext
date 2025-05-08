import os
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from theme_manager import ThemeManager

class FileManager:
    """Handles file operations such as open, save, and new files"""
    
    @staticmethod
    def _get_themed_dialog_stylesheet():
        """Generate a stylesheet for file dialogs based on the current theme"""
        # Get current theme colors
        theme_module = ThemeManager._get_theme_module()
        is_dark = ThemeManager.is_dark_mode()
        
        # Get the theme's colors
        if is_dark:
            theme_colors = getattr(theme_module, 'DARK_MODE', {})
        else:
            theme_colors = getattr(theme_module, 'LIGHT_MODE', {})
            
        # Get specific colors from the theme
        bg_color = theme_colors.get("background")
        menu_bg = theme_colors.get("menu_bg")
        text_color = theme_colors.get("text")
        accent_color = theme_colors.get("accent")
        hover_color = theme_colors.get("menu_hover")
        active_color = theme_colors.get("menu_active")
        
        # Generate a stylesheet that matches the theme aesthetics
        return f"""
            QFileDialog {{
                background-color: {menu_bg};
                color: {text_color};
                border: 1px solid {accent_color};
                border-radius: 8px;
            }}
            QDialog, QFileDialog QWidget {{
                background-color: {menu_bg};
                color: {text_color};
            }}
            QListView, QTreeView {{
                background-color: {bg_color};
                color: {text_color};
                font-size: 12pt;
                border: 1px solid {accent_color};
                border-radius: 6px;
                padding: 4px;
                selection-background-color: {hover_color};
                selection-color: {accent_color};
            }}
            QHeaderView::section {{
                background-color: {menu_bg};
                color: {text_color};
                border: 1px solid {accent_color};
                padding: 4px;
            }}
            QPushButton {{
                background-color: {menu_bg};
                color: {text_color};
                border: 1px solid {accent_color};
                border-radius: 6px;
                padding: 6px 12px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                color: {accent_color};
                border: 1px solid {accent_color};
            }}
            QPushButton:pressed {{
                background-color: {active_color};
            }}
            QLineEdit {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {accent_color};
                border-radius: 6px;
                padding: 5px;
                font-size: 12pt;
            }}
            QLineEdit:focus {{
                border: 2px solid {accent_color};
            }}
            QComboBox {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {accent_color};
                border-radius: 6px;
                padding: 5px;
                font-size: 12pt;
            }}
            QComboBox:hover {{
                background-color: {hover_color};
                color: {accent_color};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 24px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {menu_bg};
                color: {text_color};
                border: 1px solid {accent_color};
                selection-background-color: {hover_color};
                selection-color: {accent_color};
            }}
            QToolButton {{
                background-color: {menu_bg};
                color: {text_color};
                border: 1px solid {accent_color};
                border-radius: 4px;
            }}
            QToolButton:hover {{
                background-color: {hover_color};
                color: {accent_color};
            }}
            QToolButton:pressed {{
                background-color: {active_color};
            }}
            QLabel {{
                color: {text_color};
            }}
            QScrollBar:vertical {{
                border: none;
                background-color: transparent;
                width: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {accent_color};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                border: none;
                background-color: transparent;
                height: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {accent_color};
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """
    
    @staticmethod
    def get_open_file_path(parent):
        """Open a file dialog and return the selected file path"""
        try:
            dialog = QFileDialog(parent, 'Open File')
            dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
            dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            dialog.setNameFilter('Text Files (*.txt);;All Files (*)')
            
            # Apply themed stylesheet
            dialog.setStyleSheet(FileManager._get_themed_dialog_stylesheet())
            
            # Set a reasonable minimum size
            dialog.setMinimumSize(700, 500)
            
            # Center dialog relative to parent
            if parent:
                dialog_size = dialog.sizeHint()
                parent_center = parent.geometry().center()
                dialog.setGeometry(
                    parent_center.x() - dialog_size.width() // 2,
                    parent_center.y() - dialog_size.height() // 2,
                    dialog_size.width(),
                    dialog_size.height()
                )
            
            if dialog.exec() == 1:  # QDialog.Accepted
                filename = dialog.selectedFiles()[0]
                return filename
            return None
        except Exception as e:
            QMessageBox.critical(parent, 'Error', f'Could not open file dialog: {str(e)}')
            return None
    
    @staticmethod
    def get_save_file_path(parent):
        """Open a save file dialog and return the selected file path"""
        try:
            dialog = QFileDialog(parent, 'Save File')
            dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
            dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            dialog.setNameFilter('Text Files (*.txt);;All Files (*)')
            
            # Apply themed stylesheet
            dialog.setStyleSheet(FileManager._get_themed_dialog_stylesheet())
            
            # Set a reasonable minimum size
            dialog.setMinimumSize(700, 500)
            
            # Center dialog relative to parent
            if parent:
                dialog_size = dialog.sizeHint()
                parent_center = parent.geometry().center()
                dialog.setGeometry(
                    parent_center.x() - dialog_size.width() // 2,
                    parent_center.y() - dialog_size.height() // 2,
                    dialog_size.width(),
                    dialog_size.height()
                )
            
            if dialog.exec() == 1:  # QDialog.Accepted
                filename = dialog.selectedFiles()[0]
                return filename
            return None
        except Exception as e:
            QMessageBox.critical(parent, 'Error', f'Could not open save dialog: {str(e)}')
            return None
    
    @staticmethod
    def read_file(file_path):
        """Read content from a file and return it as a string"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}")
    
    @staticmethod
    def write_file(file_path, content):
        """Write content to a file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"Error writing to file {file_path}: {str(e)}")
    
    # Keep backward compatibility with the old methods
    @staticmethod
    def new_file(parent, text_edit, config_text_edit):
        """Create a new file, prompting to save the current one if needed"""
        if text_edit.toPlainText():
            reply = QMessageBox.question(
                parent, 
                'New File',
                'Do you want to save the current file?',
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                FileManager.save_file(parent, text_edit, config_text_edit, parent.config_mode)
            elif reply == QMessageBox.StandardButton.Cancel:
                return False
                
        text_edit.clear()
        config_text_edit.clear()
        parent.setWindowTitle(f'{parent.app_name} - Untitled')
        return True
        
    @staticmethod
    def open_file(parent, text_edit, config_text_edit):
        """Open a file using Qt dialogs with custom styling"""
        try:
            file_path = FileManager.get_open_file_path(parent)
            if file_path:
                FileManager._load_file_content(parent, file_path, text_edit, config_text_edit)
        except Exception as e:
            QMessageBox.critical(parent, 'Error', f'Could not open file: {str(e)}')
    
    @staticmethod
    def _load_file_content(parent, filename, text_edit, config_text_edit):
        """Load content from a file into text editors"""
        try:
            content = FileManager.read_file(filename)
            text_edit.setText(content)
            config_text_edit.setPlainText(content)
            parent.setWindowTitle(f'{parent.app_name} - {os.path.basename(filename)}')
        except Exception as e:
            QMessageBox.critical(parent, 'Error', f'Could not open file: {str(e)}')
                
    @staticmethod
    def save_file(parent, text_edit, config_text_edit, config_mode=False):
        """Save the current file"""
        try:
            file_path = FileManager.get_save_file_path(parent)
            if file_path:
                FileManager._save_file_content(parent, file_path, text_edit, config_text_edit, config_mode)
        except Exception as e:
            QMessageBox.critical(parent, 'Error', f'Could not save file: {str(e)}')
    
    @staticmethod
    def _save_file_content(parent, filename, text_edit, config_text_edit, config_mode=False):
        """Save content to a file"""
        try:
            content = config_text_edit.toPlainText() if config_mode else text_edit.toPlainText()
            FileManager.write_file(filename, content)
            parent.setWindowTitle(f'{parent.app_name} - {os.path.basename(filename)}')
        except Exception as e:
            QMessageBox.critical(parent, 'Error', f'Could not save file: {str(e)}') 