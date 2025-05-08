import os
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from theme_manager import DARK_BG, LIGHT_BG, DARK_TEXT, LIGHT_TEXT, ThemeManager

class FileManager:
    """Handles file operations such as open, save, and new files"""
    
    @staticmethod
    def get_open_file_path(parent):
        """Open a file dialog and return the selected file path"""
        try:
            dialog = QFileDialog(parent, 'Open File')
            dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
            dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            dialog.setNameFilter('Text Files (*.txt);;All Files (*)')
            
            # Set dialog styling to match app theme
            is_dark = ThemeManager.is_dark_mode()
            bg_color = DARK_BG if is_dark else LIGHT_BG
            text_color = DARK_TEXT if is_dark else LIGHT_TEXT
            
            dialog.setStyleSheet(f"""
                QFileDialog {{
                    background-color: {bg_color};
                    color: {text_color};
                }}
                QListView, QTreeView {{
                    background-color: {bg_color};
                    color: {text_color};
                    font-size: 12pt;
                }}
                QPushButton {{
                    background-color: rgba(100, 255, 218, 0.2);
                    color: {text_color};
                    border: 1px solid #64ffda;
                    border-radius: 4px;
                    padding: 5px 15px;
                    font-size: 12pt;
                }}
                QPushButton:hover {{
                    background-color: rgba(100, 255, 218, 0.4);
                }}
                QLineEdit {{
                    background-color: {bg_color};
                    color: {text_color};
                    border: 1px solid #64ffda;
                    border-radius: 4px;
                    padding: 5px;
                    font-size: 12pt;
                }}
                QComboBox {{
                    background-color: {bg_color};
                    color: {text_color};
                    border: 1px solid #64ffda;
                    border-radius: 4px;
                    padding: 5px;
                    font-size: 12pt;
                }}
            """)
            
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
            
            # Set dialog styling to match app theme
            is_dark = ThemeManager.is_dark_mode()
            bg_color = DARK_BG if is_dark else LIGHT_BG
            text_color = DARK_TEXT if is_dark else LIGHT_TEXT
            
            dialog.setStyleSheet(f"""
                QFileDialog {{
                    background-color: {bg_color};
                    color: {text_color};
                }}
                QListView, QTreeView {{
                    background-color: {bg_color};
                    color: {text_color};
                    font-size: 12pt;
                }}
                QPushButton {{
                    background-color: rgba(100, 255, 218, 0.2);
                    color: {text_color};
                    border: 1px solid #64ffda;
                    border-radius: 4px;
                    padding: 5px 15px;
                    font-size: 12pt;
                }}
                QPushButton:hover {{
                    background-color: rgba(100, 255, 218, 0.4);
                }}
                QLineEdit {{
                    background-color: {bg_color};
                    color: {text_color};
                    border: 1px solid #64ffda;
                    border-radius: 4px;
                    padding: 5px;
                    font-size: 12pt;
                }}
                QComboBox {{
                    background-color: {bg_color};
                    color: {text_color};
                    border: 1px solid #64ffda;
                    border-radius: 4px;
                    padding: 5px;
                    font-size: 12pt;
                }}
            """)
            
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