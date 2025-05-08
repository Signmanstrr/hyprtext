"""
Typewriter Mode for HyprText
============================

A mode that simulates typing on an old-style typewriter, with sound effects 
and appropriate animations. Demonstrates custom animation implementation for modes.
"""

from PyQt6.QtWidgets import QTextEdit, QLabel
from PyQt6.QtGui import QPalette, QColor, QFont, QTextCursor
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
import sys
import os
import random

# Add the src directory to the path if needed
src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src")
if src_dir not in sys.path:
    sys.path.append(src_dir)

from theme_manager import ThemeManager
from animation import SmoothTextEdit

# Mode metadata
MODE_NAME = "Typewriter Mode"
MODE_DESCRIPTION = "Write with typewriter-style animations and effects"
MODE_ICON = None

# Theme color overrides to ensure readable text regardless of the current theme
THEME_COLOR_OVERRIDES = {
    "text": "#000000",                    # Pure black ink color for readability on paper
    "background": "#f8f4e3",              # Aged paper background
    "window_bg_gradient_start": "#f0ebda", # Lighter aged paper gradient start
    "window_bg_gradient_end": "#e8e0c8",   # Darker aged paper gradient end
    "accent": "#8B4513",                  # Brown accent color for typewriter feel
    "menu_bg": "#f0ebda",                 # Menu background matching paper
    "menu_hover": "#e8e0c8",              # Menu hover state matching paper
    "menu_active": "#d8ceb0",             # Menu active state matching paper
    "border": "#8B4513"                   # Brown border color for typewriter feel
}

class TypewriterEdit(SmoothTextEdit):
    """Text editor that simulates an old-style typewriter"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Use a monospace font for that typewriter feel
        typewriter_font = QFont("Courier New", 14)
        self.setFont(typewriter_font)
        
        # Set typewriter-like colors (old paper and dark ink)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#f8f4e3"))  # Aged paper color
        palette.setColor(QPalette.ColorRole.Text, QColor("#000000"))  # Pure black ink
        self.setPalette(palette)
        
        # Configure for typewriter experience
        self.setFrameStyle(QTextEdit.Shape.NoFrame)
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        
        # Enable cursor visibility
        self.setCursorWidth(2)
        
        # Set viewport margins for that old-typewriter page feel
        self.setViewportMargins(40, 30, 40, 30)
        
        # Enable typewriter animations
        self.animations_enabled = True
        self.animation_duration = 100  # Quick fades
        
        # Sound effects (simulated)
        self.typing_sound_enabled = True
        
        # Add slight cursor bounce effect
        self.cursor_pos_timer = QTimer(self)
        self.cursor_pos_timer.setInterval(100)
        self.cursor_pos_timer.timeout.connect(self.bounce_cursor)
        self.cursor_pos_timer.start()
        
        # Add typewriter carriage sound at end of line
        self.textChanged.connect(self.check_for_carriage_return)
        self.last_line_count = 1
        
        # Apply a vintage-looking style with paper texture
        self.setOldPaperBackground()
        
        # Create paper texture using a custom background widget
        self.createPaperTextureEffect()
        
        # Force text color
        self.setTextColor(QColor("#000000"))
        
        # Force text format to apply our color
        cursor = self.textCursor()
        fmt = cursor.charFormat()
        fmt.setForeground(QColor("#000000"))
        cursor.setCharFormat(fmt)
        self.setTextCursor(cursor)
    
    def createPaperTextureEffect(self):
        """Create a paper texture effect using a more PyQt-friendly approach"""
        # Instead of using complex CSS, we'll add subtle noise directly to the background
        try:
            # We'll use a QLabel with a background color as our paper
            self.paper_background = QLabel(self)
            self.paper_background.lower()  # Put it behind text
            self.paper_background.setAutoFillBackground(True)
            
            # Set basic paper color
            palette = self.paper_background.palette()
            palette.setColor(QPalette.ColorRole.Window, QColor("#f8f4e3"))
            self.paper_background.setPalette(palette)
            
            # Make it fill the viewport of the text edit
            self.paper_background.setGeometry(0, 0, self.width(), self.height())
            
            # Make sure it resizes with the editor
            self.resizeEvent = self.handleResize
            
            # Add a subtle grain texture using simple supported properties
            self.paper_background.setStyleSheet("""
                QLabel {
                    background-color: #f8f4e3;
                    border: none;
                }
            """)
            
            # Make the texture visible
            self.paper_background.show()
            
            # Start a timer to add some subtle "noise" variations
            self.grain_timer = QTimer(self)
            self.grain_timer.setInterval(1000)  # Update every second
            self.grain_timer.timeout.connect(self.updatePaperTexture)
            self.grain_timer.start()
            
        except Exception as e:
            print(f"Error creating paper texture: {str(e)}")
    
    def updatePaperTexture(self):
        """Update the paper texture with subtle variations"""
        try:
            # Create slight variations in the base color to simulate paper texture
            r = random.randint(-2, 2)  # Subtle color variations
            g = random.randint(-2, 2)
            b = random.randint(-2, 2)
            
            # Get the base color and apply the slight variation
            base = QColor("#f8f4e3")
            varied_color = QColor(
                max(0, min(255, base.red() + r)),
                max(0, min(255, base.green() + g)),
                max(0, min(255, base.blue() + b))
            )
            
            # Apply the varied color to the background
            palette = self.paper_background.palette()
            palette.setColor(QPalette.ColorRole.Window, varied_color)
            self.paper_background.setPalette(palette)
            
            # Draw a few random "noise" spots using opacity changes
            # This is a more PyQt-friendly approach for visual noise
            if random.random() < 0.3:  # Only sometimes (30% chance) to avoid overloading
                self.drawNoiseSpots()
                
        except Exception as e:
            print(f"Error updating paper texture: {str(e)}")
    
    def drawNoiseSpots(self):
        """Draw subtle noise spots on the paper background"""
        try:
            # We don't directly draw spots - instead we'll use the stylesheet
            # with slightly different background colors in different areas
            base_color = "#f8f4e3"
            lighter = QColor(base_color).lighter(102).name()  # Just 2% lighter
            darker = QColor(base_color).darker(102).name()    # Just 2% darker
            
            # Create a stylesheet with a simple gradient that changes slightly each time
            angle = random.randint(0, 359)  # Random gradient angle
            
            self.paper_background.setStyleSheet(f"""
                QLabel {{
                    background-color: {base_color};
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                              stop:0 {lighter}, 
                                              stop:0.4 {base_color},
                                              stop:0.6 {base_color},
                                              stop:1 {darker});
                }}
            """)
        except Exception as e:
            print(f"Error drawing noise spots: {str(e)}")
    
    def handleResize(self, event):
        """Handle resize events to keep the paper background sized correctly"""
        try:
            if hasattr(self, 'paper_background'):
                self.paper_background.setGeometry(0, 0, self.width(), self.height())
            # Call the original resizeEvent
            QTextEdit.resizeEvent(self, event)
        except Exception as e:
            print(f"Error in handleResize: {str(e)}")
            QTextEdit.resizeEvent(self, event)
    
    def setOldPaperBackground(self):
        """Apply a simple paper background using supported properties"""
        # Use a much simpler stylesheet without unsupported properties
        stylesheet = """
            QTextEdit {
                border: none;
                background-color: #f8f4e3;
                color: #000000 !important; /* Force black text color */
            }
        """
        self.setStyleSheet(stylesheet)
    
    def bounce_cursor(self):
        """Simulate slight mechanical cursor bounce"""
        try:
            if not self.hasFocus():
                return
                
            cursor = self.textCursor()
            # Only bounce when cursor is visible and text is being edited
            if cursor.hasSelection() or not self.isVisible():
                return
                
            # Add subtle visual feedback - briefly change cursor width
            old_width = self.cursorWidth()
            # Random slight variation in cursor width
            new_width = old_width + random.choice([-1, 0, 1])
            self.setCursorWidth(max(1, new_width))
            
            # Return to normal after a short delay
            QTimer.singleShot(50, lambda: self.setCursorWidth(old_width))
        except Exception as e:
            print(f"Error in bounce_cursor: {str(e)}")
    
    # Override setTextColor to ensure our color is always used
    def setTextColor(self, color):
        """Override to ensure our black ink color is always used"""
        super().setTextColor(QColor("#000000"))
    
    def check_for_carriage_return(self):
        """Check if we've added a new line and play 'carriage return' effect"""
        try:
            current_text = self.toPlainText()
            current_line_count = current_text.count('\n') + 1
            
            if current_line_count > self.last_line_count:
                # New line added - simulate carriage return sound and animation
                print("*DING* Carriage Return")
                # Here you would play a sound effect if audio was implemented
                
                # Visual carriage return effect - slight pause then continue
                cursor = self.textCursor()
                # Brief pause at start of new line to simulate carriage return
                self.setReadOnly(True)
                QTimer.singleShot(150, lambda: self.setReadOnly(False))
            
            self.last_line_count = current_line_count
        except Exception as e:
            print(f"Error in check_for_carriage_return: {str(e)}")
    
    def keyPressEvent(self, event):
        """Handle key press events with typewriter-like behavior"""
        try:
            # Add typewriter 'clack' sound effect simulation
            if self.typing_sound_enabled and event.text().strip():
                # Random slight variation in key sound (if audio was implemented)
                volume = random.uniform(0.8, 1.0)
                print(f"*CLACK* ({volume:.1f})")
            
            # Let parent handle the actual key press
            super().keyPressEvent(event)
            
            # Force black text for any newly added content
            self.setTextColor(QColor("#000000"))
            
            # Add slight delay after each keystroke for mechanical feel
            if event.text().strip():
                # Brief pause after keystroke (typewriters aren't instant)
                QTimer.singleShot(10, self.ensureCursorVisible)
        except Exception as e:
            print(f"Error in keyPressEvent: {str(e)}")
            super().keyPressEvent(event)
    
    def focusOutEvent(self, event):
        """Stop animation timers when losing focus"""
        super().focusOutEvent(event)
        # Slow down timers when not focused to save resources
        if hasattr(self, 'grain_timer'):
            self.grain_timer.setInterval(5000)  # Slow down to 5 seconds when not focused
    
    def focusInEvent(self, event):
        """Restart animation timers when gaining focus"""
        super().focusInEvent(event)
        # Reset to normal speed
        if hasattr(self, 'grain_timer'):
            self.grain_timer.setInterval(1000)  # Back to 1 second when focused

# Add post_theme_change hook at the module level to ensure our overrides are applied
def post_theme_change(app, theme_name):
    """Handle theme changes by ensuring typewriter colors are preserved"""
    if app.current_mode == MODE_NAME and app.current_mode in app.mode_editors:
        editor = app.mode_editors[app.current_mode]
        if isinstance(editor, TypewriterEdit):
            print(f"Re-applying typewriter colors after theme change to {theme_name}")
            
            # Re-apply our typewriter styling with the old paper background
            editor.setOldPaperBackground()
            
            # Refresh paper texture if needed
            if hasattr(editor, 'paper_background'):
                editor.drawNoiseSpots()
            
            # Ensure text is black for all content
            cursor = editor.textCursor()
            editor.selectAll()
            fmt = cursor.charFormat()
            fmt.setForeground(QColor("#000000"))
            editor.setCurrentCharFormat(fmt)
            editor.setTextColor(QColor("#000000"))
            
            # Reset cursor to prevent selection
            cursor.clearSelection()
            editor.setTextCursor(cursor)

# Mode interface functions
def create_editor(parent=None):
    """Create and return an editor widget for this mode"""
    return TypewriterEdit(parent) 