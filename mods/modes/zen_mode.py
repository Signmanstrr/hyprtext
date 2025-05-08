from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtCore import Qt
import sys
import os

# Add the src directory to the path if needed
src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src")
if src_dir not in sys.path:
    sys.path.append(src_dir)

from theme_manager import ThemeManager
from animation import SmoothTextEdit  # Import our new SmoothTextEdit

# Mode metadata
MODE_NAME = "Zen Mode"
MODE_DESCRIPTION = "Distraction-free writing mode with smooth animations and minimalist interface"
MODE_ICON = None  # Could be a path to an icon

class ZenTextEdit(SmoothTextEdit):  # Change parent class to SmoothTextEdit
    """Distraction-free writing environment with smooth animations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)  # Initialize SmoothTextEdit parent class
        
        # Set custom font for zen mode
        zen_font = ThemeManager.get_editor_font()
        zen_font.setPointSize(14)  # Larger font for better readability
        self.setFont(zen_font)
        
        # Center text
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        # Configure for distraction-free writing
        self.setFrameStyle(QTextEdit.Shape.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Set a calm color scheme
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#232733"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#EEEEEE"))
        self.setPalette(palette)
        
        # Set custom margins
        self.setViewportMargins(120, 60, 120, 60)  # Left, Top, Right, Bottom
        
        # Make the text edit read-only while not focused to prevent accidental edits
        self.setReadOnly(True)
        self.focusInEvent = self._focus_in
        self.focusOutEvent = self._focus_out
        
        # Enable smooth animations with a longer duration for a more zen-like experience
        self.animations_enabled = True
        self.animation_duration = 400  # Longer for a more calm, zen-like feel
        
        # Add a typewriter sound effect option (disabled by default)
        self.set_typing_sound(False)
    
    def _focus_in(self, event):
        """Handle focus in event - make editable"""
        self.setReadOnly(False)
        super().focusInEvent(event)
    
    def _focus_out(self, event):
        """Handle focus out event - make read-only"""
        self.setReadOnly(True)
        super().focusOutEvent(event)

# Mode interface functions
def create_editor(parent=None):
    """Create and return an editor widget for this mode"""
    return ZenTextEdit(parent) 