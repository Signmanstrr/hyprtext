from PyQt6.QtWidgets import QTextEdit, QPlainTextEdit
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt, pyqtProperty, QTimer, QObject
from PyQt6.QtGui import QColor, QTextCharFormat, QTextCursor
import traceback

class AnimationManager(QObject):
    """Manages animations and cleans up completed or stalled animations"""
    
    def __init__(self):
        super().__init__()
        self.active_animations = []
    
    def add_animation(self, animation):
        """Add an animation to the tracking list"""
        try:
            if animation not in self.active_animations:
                self.active_animations.append(animation)
                
                # Set up a finished signal to remove the animation when done
                if hasattr(animation, 'finished'):
                    animation.finished.connect(lambda: self.remove_animation(animation))
        except Exception as e:
            print(f"Error adding animation: {str(e)}")
            traceback.print_exc()
    
    def remove_animation(self, animation):
        """Remove an animation from the tracking list"""
        try:
            if animation in self.active_animations:
                self.active_animations.remove(animation)
        except Exception as e:
            print(f"Error removing animation: {str(e)}")
            traceback.print_exc()
    
    def manual_cleanup(self):
        """Manually clean up animations - to be called at specific points"""
        try:
            for animation in list(self.active_animations):
                try:
                    # Check if animation is still valid or if it's completed
                    if hasattr(animation, 'state') and animation.state() == QPropertyAnimation.State.Stopped:
                        self.active_animations.remove(animation)
                    elif not hasattr(animation, 'state'):
                        # Invalid animation object
                        self.active_animations.remove(animation)
                except RuntimeError:
                    # Object may have been deleted
                    self.active_animations.remove(animation)
                except Exception as e:
                    print(f"Error cleaning up animation: {str(e)}")
                    traceback.print_exc()
                    self.active_animations.remove(animation)
        except Exception as e:
            print(f"Error in animation cleanup: {str(e)}")
            traceback.print_exc()

# Create a global animation manager instance
animation_manager = AnimationManager()

class CharacterAnimation:
    """Handles animation of a single character with fade in/out effects"""
    
    FADE_IN = 0
    FADE_OUT = 1
    
    def __init__(self, text_widget, position, animation_type=FADE_IN, duration=200):
        self.text_widget = text_widget
        self.position = position
        self.animation_type = animation_type
        self.duration = duration
        self.steps = 5
        self.current_step = 0
        self.completed = False
        
        # Create a dedicated timer for this animation
        self.timer = QTimer(text_widget)
        self.timer.setInterval(duration // self.steps)
        self.timer.timeout.connect(self.animation_step)
    
    def start(self):
        """Start the animation"""
        try:
            # Set initial values
            if self.animation_type == self.FADE_IN:
                self.current_step = 0
            else:  # FADE_OUT
                self.current_step = self.steps
                
            # Start the timer
            self.timer.start()
            return True
        except Exception as e:
            print(f"Error starting character animation: {str(e)}")
            traceback.print_exc()
            return False
    
    def stop(self):
        """Stop the animation and clean up"""
        try:
            self.timer.stop()
            self.completed = True
        except Exception as e:
            print(f"Error stopping character animation: {str(e)}")
            traceback.print_exc()
    
    def animation_step(self):
        """Process one step of the animation"""
        try:
            # Update step counter
            if self.animation_type == self.FADE_IN:
                self.current_step += 1
                opacity = self.current_step / self.steps
                done = self.current_step >= self.steps
            else:  # FADE_OUT
                self.current_step -= 1
                opacity = self.current_step / self.steps
                done = self.current_step <= 0
            
            # Check if text still exists and position is valid
            document = self.text_widget.document()
            if self.position >= len(self.text_widget.toPlainText()):
                self.stop()
                return
                
            # Apply the opacity to the character
            cursor = QTextCursor(document)
            cursor_position = self.text_widget.textCursor().position()  # Save current position
            
            # Get text format - different widgets have different methods
            if hasattr(self.text_widget, 'textColor'):
                # For QTextEdit
                format = QTextCharFormat()
                color = self.text_widget.textColor()
                color.setAlphaF(opacity)
                format.setForeground(color)
            elif isinstance(self.text_widget, QPlainTextEdit):
                # For any QPlainTextEdit (including custom editors)
                # Try to get format from cursor to preserve syntax highlighting if available
                try:
                    # Select the character at the position
                    cursor.setPosition(self.position)
                    cursor.setPosition(self.position + 1, QTextCursor.MoveMode.KeepAnchor)
                    format = cursor.charFormat()
                    color = format.foreground().color()
                    # If color is not valid, use a default
                    if not color.isValid():
                        color = QColor(Qt.GlobalColor.white)
                except:
                    # If we can't get valid format, create a new one with default color
                    format = QTextCharFormat()
                    color = QColor(Qt.GlobalColor.black if self.text_widget.palette().text().color().lightness() > 128 else Qt.GlobalColor.white)
                color.setAlphaF(opacity)
                format.setForeground(color)
            else:
                # For other widget types
                format = QTextCharFormat()
                color = QColor(Qt.GlobalColor.black if self.text_widget.palette().text().color().lightness() > 128 else Qt.GlobalColor.white)
                color.setAlphaF(opacity)
                format.setForeground(color)
            
            # Try to apply the format to the character at position
            try:
                # Select the character at the position
                cursor.setPosition(self.position)
                cursor.setPosition(self.position + 1, QTextCursor.MoveMode.KeepAnchor)
                
                # Apply the format
                cursor.mergeCharFormat(format)
                
                # Restore cursor position
                cursor.setPosition(cursor_position)
                self.text_widget.setTextCursor(cursor)
            except Exception as e:
                print(f"Error updating format at position {self.position}: {str(e)}")
                self.stop()
                return
            
            # Check if animation is complete
            if done:
                if self.animation_type == self.FADE_OUT:
                    # For fade out, we want the character to be fully invisible before stopping
                    color.setAlphaF(0)
                    format.setForeground(color)
                    cursor.mergeCharFormat(format)
                self.stop()
                if hasattr(self.text_widget, 'animation_completed'):
                    self.text_widget.animation_completed(self)
                
        except Exception as e:
            print(f"Error in animation step: {str(e)}")
            traceback.print_exc()
            self.stop()

class AnimatedTextEdit(QTextEdit):
    """TextEdit with text fade-in animations when typing"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animations_enabled = False  # Disabled by default for snappier standard mode
        self.active_animations = {}  # Maps positions to animation objects
        self.animation_duration = 200  # ms
        self.prev_text = ""
        
        # Connect text change signal
        self.textChanged.connect(self.handle_text_changed)
    
    def handle_text_changed(self):
        """Handle text changes and animate characters accordingly"""
        if not self.animations_enabled:
            return
            
        try:
            current_text = self.toPlainText()
            
            # If no previous text, just set it and return
            if not self.prev_text:
                self.prev_text = current_text
                return
            
            # Handle two cases: text insertion and text deletion
            if len(current_text) > len(self.prev_text):
                # Text insertion case
                # Find the first position where texts differ
                diff_pos = self.find_first_difference(self.prev_text, current_text)
                # Calculate how many characters were inserted
                inserted_chars = len(current_text) - len(self.prev_text)
                
                # Animate each new character
                for i in range(inserted_chars):
                    position = diff_pos + i
                    self.start_animation(position, CharacterAnimation.FADE_IN)
                
            elif len(current_text) < len(self.prev_text):
                # Text deletion case
                # Find where deletion occurred
                diff_pos = self.find_first_difference(current_text, self.prev_text)
                # Calculate how many characters were deleted
                deleted_chars = len(self.prev_text) - len(current_text)
                
                # Shift existing animations after deletion point
                self.shift_animations(diff_pos, -deleted_chars)
                
            # Update previous text
            self.prev_text = current_text
            
        except Exception as e:
            print(f"Error handling text change: {str(e)}")
            traceback.print_exc()
    
    def find_first_difference(self, str1, str2):
        """Find the position of the first different character between two strings"""
        min_len = min(len(str1), len(str2))
        for i in range(min_len):
            if str1[i] != str2[i]:
                return i
        return min_len
    
    def shift_animations(self, from_pos, offset):
        """Shift animation positions after text modifications"""
        try:
            # Create a new dictionary with updated positions
            new_animations = {}
            
            for pos, animation in self.active_animations.items():
                if pos >= from_pos:
                    # This animation is after the modification point
                    new_pos = pos + offset
                    if new_pos >= 0:  # Ensure we don't get negative positions
                        animation.position = new_pos
                        new_animations[new_pos] = animation
                else:
                    # This animation is before the modification point, no change needed
                    new_animations[pos] = animation
                    
            # Update the animations dictionary
            self.active_animations = new_animations
        except Exception as e:
            print(f"Error shifting animations: {str(e)}")
            traceback.print_exc()
    
    def start_animation(self, position, animation_type):
        """Start a character animation at the given position"""
        try:
            # Stop any existing animation at this position
            if position in self.active_animations:
                self.active_animations[position].stop()
                
            # Create and start new animation
            animation = CharacterAnimation(self, position, animation_type, self.animation_duration)
            self.active_animations[position] = animation
            animation.start()
            
        except Exception as e:
            print(f"Error starting animation: {str(e)}")
            traceback.print_exc()
    
    def animation_completed(self, animation):
        """Called when an animation completes"""
        try:
            # Find and remove the animation from our tracking dictionary
            for pos, anim in list(self.active_animations.items()):
                if anim == animation:
                    del self.active_animations[pos]
                    break
        except Exception as e:
            print(f"Error handling animation completion: {str(e)}")
            traceback.print_exc()
    
    def set_animations_enabled(self, enabled=True):
        """Enable or disable text animations"""
        self.animations_enabled = enabled
        # Clear any active animations
        if not enabled:
            for animation in list(self.active_animations.values()):
                animation.stop()
            self.active_animations.clear()
            
    def clear(self):
        """Override clear to clean up animations"""
        super().clear()
        # Reset animations and text tracking
        self.active_animations.clear()
        self.prev_text = ""

class MenuFader:
    """Handles fade animations for menus"""
    
    @staticmethod
    def fade_in(widget, duration=200):
        """Create a fade-in animation for a widget"""
        try:
            # Set widget opacity to 0
            widget.setWindowOpacity(0.0)
            
            # Create animation
            animation = QPropertyAnimation(widget, b"windowOpacity")
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            animation.setDuration(duration)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            # Start animation
            animation.start()
            
            # Register with the animation manager
            animation_manager.add_animation(animation)
            
            # Return the animation object for reference
            return animation
        except Exception as e:
            print(f"Error creating fade-in animation: {str(e)}")
            traceback.print_exc()
            return None
    
    @staticmethod
    def fade_out(widget, duration=200, on_finished=None):
        """Create a fade-out animation for a widget"""
        try:
            # Create animation
            animation = QPropertyAnimation(widget, b"windowOpacity")
            animation.setStartValue(widget.windowOpacity())
            animation.setEndValue(0.0)
            animation.setDuration(duration)
            animation.setEasingCurve(QEasingCurve.Type.InCubic)
            
            # Connect finished signal if callback provided
            if on_finished:
                animation.finished.connect(on_finished)
            
            # Start animation
            animation.start()
            
            # Register with the animation manager
            animation_manager.add_animation(animation)
            
            # Return the animation object for reference
            return animation
        except Exception as e:
            print(f"Error creating fade-out animation: {str(e)}")
            traceback.print_exc()
            if on_finished:
                on_finished()
            return None 

class SmoothTextEdit(QTextEdit):
    """Enhanced text editor with smooth typing animations for Zen mode"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animations_enabled = True
        self.active_animations = {}
        self.animation_duration = 300  # Longer for smoother fade
        self.fade_steps = 10  # More steps for smoother animation
        self.prev_text = ""
        self.typing_sound_enabled = False
        
        # Connect text change signal
        self.textChanged.connect(self.handle_text_changed)
        
        # Apply shadow effect for depth
        self.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: transparent;
            }
        """)
    
    def handle_text_changed(self):
        """Handle text changes with smooth animations"""
        if not self.animations_enabled:
            return
            
        try:
            current_text = self.toPlainText()
            
            # If no previous text, just set it and return
            if not self.prev_text:
                self.prev_text = current_text
                return
            
            # Handle two cases: text insertion and text deletion
            if len(current_text) > len(self.prev_text):
                # Text insertion case
                # Find the first position where texts differ
                diff_pos = self.find_first_difference(self.prev_text, current_text)
                # Calculate how many characters were inserted
                inserted_chars = len(current_text) - len(self.prev_text)
                
                # Create a smooth word fade-in effect when typing
                # If multiple characters were inserted at once, animate them as a group
                if inserted_chars > 1:
                    # Word or paste insertion - use a single animation for the group
                    self.start_smooth_animation(diff_pos, inserted_chars, fade_in=True)
                else:
                    # Single character - use character animation
                    self.start_character_animation(diff_pos, fade_in=True)
                
            elif len(current_text) < len(self.prev_text):
                # Text deletion case - no animation for deleted text
                # Just update tracking of characters
                diff_pos = self.find_first_difference(current_text, self.prev_text)
                deleted_chars = len(self.prev_text) - len(current_text)
                
                # Clean up any animations in the deleted range
                self.cleanup_animations_in_range(diff_pos, diff_pos + deleted_chars)
                
                # Shift remaining animations
                self.shift_animations(diff_pos, -deleted_chars)
            
            # Update previous text
            self.prev_text = current_text
            
        except Exception as e:
            print(f"Error handling text change: {str(e)}")
            traceback.print_exc()
    
    def find_first_difference(self, str1, str2):
        """Find the position of the first different character between two strings"""
        min_len = min(len(str1), len(str2))
        for i in range(min_len):
            if str1[i] != str2[i]:
                return i
        return min_len
    
    def start_character_animation(self, position, fade_in=True):
        """Start a simple character animation at the given position"""
        try:
            # Stop any existing animation at this position
            if position in self.active_animations:
                animation = self.active_animations[position]
                if hasattr(animation, 'stop'):
                    animation.stop()
            
            # Create character animation
            animation = CharacterAnimation(
                self, 
                position, 
                CharacterAnimation.FADE_IN if fade_in else CharacterAnimation.FADE_OUT,
                self.animation_duration
            )
            
            # Track and start
            self.active_animations[position] = animation
            animation.start()
            
        except Exception as e:
            print(f"Error starting character animation: {str(e)}")
            traceback.print_exc()
    
    def start_smooth_animation(self, start_position, length, fade_in=True):
        """Start a smooth animation for multiple characters (like a word)"""
        try:
            # Create animations for each character, staggered for a flowing effect
            for i in range(length):
                pos = start_position + i
                delay = min(i * 15, 150)  # Stagger with max 150ms delay
                
                # Use a timer to delay the start of each character's animation
                timer = QTimer(self)
                timer.setSingleShot(True)
                timer.timeout.connect(lambda p=pos, fi=fade_in: self.start_character_animation(p, fi))
                timer.start(delay)
                
                # Store the timer in active_animations for tracking
                self.active_animations[f"timer_{pos}"] = timer
                
        except Exception as e:
            print(f"Error starting smooth animation: {str(e)}")
            traceback.print_exc()
    
    def cleanup_animations_in_range(self, start, end):
        """Clean up animations in a specific range"""
        try:
            for pos in list(self.active_animations.keys()):
                if isinstance(pos, int) and start <= pos < end:
                    animation = self.active_animations[pos]
                    if hasattr(animation, 'stop'):
                        animation.stop()
                    del self.active_animations[pos]
        except Exception as e:
            print(f"Error cleaning up animations: {str(e)}")
            traceback.print_exc()
    
    def shift_animations(self, from_pos, offset):
        """Shift animation positions after text modifications"""
        try:
            # Create a new dictionary with updated positions
            new_animations = {}
            
            for pos, animation in self.active_animations.items():
                # Only process integer keys (position-based animations)
                if isinstance(pos, int) and pos >= from_pos:
                    # This animation is after the modification point
                    new_pos = pos + offset
                    if new_pos >= 0:  # Ensure we don't get negative positions
                        if hasattr(animation, 'position'):
                            animation.position = new_pos
                        new_animations[new_pos] = animation
                elif isinstance(pos, int):
                    # This animation is before the modification point, no change needed
                    new_animations[pos] = animation
                else:
                    # Non-integer keys (like timers) are preserved as-is
                    new_animations[pos] = animation
                    
            # Update the animations dictionary
            self.active_animations = new_animations
        except Exception as e:
            print(f"Error shifting animations: {str(e)}")
            traceback.print_exc()
    
    def animation_completed(self, animation):
        """Called when an animation completes"""
        try:
            # Find and remove the animation from our tracking dictionary
            for pos, anim in list(self.active_animations.items()):
                if anim == animation:
                    del self.active_animations[pos]
                    break
        except Exception as e:
            print(f"Error handling animation completion: {str(e)}")
            traceback.print_exc()
    
    def set_animations_enabled(self, enabled=True):
        """Enable or disable text animations"""
        self.animations_enabled = enabled
        # Clear any active animations
        if not enabled:
            self.clear_all_animations()
    
    def clear_all_animations(self):
        """Clear all active animations"""
        try:
            for key, animation in list(self.active_animations.items()):
                if hasattr(animation, 'stop'):
                    animation.stop()
                elif hasattr(animation, 'deleteLater'):
                    animation.deleteLater()
            self.active_animations.clear()
        except Exception as e:
            print(f"Error clearing animations: {str(e)}")
            traceback.print_exc()
    
    def clear(self):
        """Override clear to clean up animations"""
        super().clear()
        # Reset animations and text tracking
        self.clear_all_animations()
        self.prev_text = ""
        
    def set_typing_sound(self, enabled=True):
        """Enable or disable typing sound effects"""
        self.typing_sound_enabled = enabled 