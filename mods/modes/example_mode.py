"""
HyprText Example Mode
=====================

This file serves as a reference guide for creating custom editor modes for HyprText.
Follow this structure when creating your own modes.

REQUIREMENTS FOR A VALID MODE:
1. Each mode must define the following constants:
   - MODE_NAME: The display name for your mode
   - MODE_DESCRIPTION: A brief description of your mode's functionality
   
2. Each mode must implement the following function:
   - create_editor(parent=None): Returns a widget that will be used as the editor

3. Optional components:
   - MODE_ICON: Path to an icon for your mode (not currently used but reserved for future)
   - Custom widget classes with specialized editing functionality
"""

from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
import sys
import os

# Add the src directory to the path if needed
# This ensures your mode can import from the main application
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if src_dir not in sys.path:
    sys.path.append(src_dir)

# Import modules from the main application as needed
from theme_manager import ThemeManager

# ========== REQUIRED MODE METADATA ==========
# These constants are detected by the mode_manager and must be defined

# The name that will appear in the UI mode selector
MODE_NAME = "Example Mode"

# A short description that will appear as a tooltip
MODE_DESCRIPTION = "Example mode showing how to create custom editor modes"

# Optional: Path to an icon for your mode (for future use)
MODE_ICON = None


# ========== CUSTOM EDITOR WIDGET ==========
# Creating a custom editor widget gives you control over the editing experience
# You can inherit from QTextEdit, QPlainTextEdit, or any other suitable widget

class ExampleTextEdit(QTextEdit):
    """
    Example custom editor widget demonstrating mode creation
    
    Your editor widget can:
    - Customize appearance
    - Add custom functionality
    - Override standard behaviors
    - Implement special handling for different file types
    """
    
    def __init__(self, parent=None):
        """Initialize your editor with custom properties"""
        super().__init__(parent)
        
        # Example: Custom styling
        # You can define colors directly or use ThemeManager for consistency
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#3a506b"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#ffffff"))
        self.setPalette(palette)
        
        # Example: Custom formatting options
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        
        # Example: Set placeholder text
        self.setPlaceholderText("This is Example Mode - a template for creating your own modes!")
        
        # Example: You can connect to built-in signals
        # self.textChanged.connect(self.handle_text_changed)
    
    # Example: You can override methods from the parent class
    def keyPressEvent(self, event):
        """Example of handling key press events"""
        # Implement custom key behaviors here if needed
        # This is just a demonstration - we're calling the parent method
        super().keyPressEvent(event)
    
    # Example: Add custom methods for specialized functionality
    # def handle_text_changed(self):
    #     """Example method to handle text changes"""
    #     print("Text changed in Example Mode editor")


# ========== REQUIRED INTERFACE FUNCTION ==========
# This function is called by the mode_manager to create your editor

def create_editor(parent=None):
    """
    Create and return an editor widget for this mode
    
    This function MUST be defined in your mode file.
    It is the entry point for the mode_manager to create your editor.
    
    Args:
        parent: The parent widget (usually the main window)
        
    Returns:
        A widget that will serve as the editor for this mode
    """
    return ExampleTextEdit(parent)


# ========== OPTIONAL HELPER FUNCTIONS ==========
# You can add any additional functions needed by your mode

def get_example_file_extensions():
    """
    Example of a helper function specific to this mode
    
    You can define any additional functions needed by your mode.
    These won't be called by the mode_manager but can be used by your editor.
    """
    return [".example", ".demo", ".test"] 