"""
Left-Aligned Header Extension for HyprText
=========================================

This extension changes the header text (file name and mode/theme info) from 
center-aligned to left-aligned. It demonstrates how to modify UI elements 
without changing core code.
"""

# Import Qt for alignment flags
from PyQt6.QtCore import Qt

# Extension metadata - these are required for any extension
EXTENSION_NAME = "Left-Aligned Header"
EXTENSION_DESCRIPTION = "Changes header text from center-aligned to left-aligned"
EXTENSION_AUTHOR = "HyprText Extensions"
EXTENSION_VERSION = "1.0"

# Store state to track changes and ensure proper cleanup
_app_instance = None
_file_label = None
_info_label = None
_original_file_alignment = None
_original_info_alignment = None
_original_file_stylesheet = None
_original_info_stylesheet = None
_is_left_aligned = False

def initialize(app=None):
    """
    Initialize the extension when activated
    
    This hook is called when the extension is first enabled.
    It's a good place to:
    - Store references to the app instance
    - Initialize any extension state
    - Set up event handlers or connections
    - Store original values of things you'll modify
    
    Args:
        app: The main application instance (HyprText)
    """
    global _app_instance
    
    if app:
        _app_instance = app
        print("Left-Aligned Header extension initialized")

def cleanup(app=None):
    """
    Clean up when the extension is deactivated
    
    This hook is called when the extension is disabled.
    Always restore the original application state by:
    - Removing any UI elements you've added
    - Restoring original values of modified properties
    - Disconnecting any signals you've connected
    
    Args:
        app: The main application instance (HyprText)
    """
    global _app_instance, _file_label, _info_label, _is_left_aligned
    global _original_file_alignment, _original_info_alignment
    global _original_file_stylesheet, _original_info_stylesheet
    
    if app and _is_left_aligned and _file_label and _info_label:
        # Restore original alignments if we have them
        if _original_file_alignment is not None:
            _file_label.setAlignment(_original_file_alignment)
        
        if _original_info_alignment is not None:
            _info_label.setAlignment(_original_info_alignment)
        
        # Restore original stylesheets if we have them
        if _original_file_stylesheet is not None:
            _file_label.setStyleSheet(_original_file_stylesheet)
        
        if _original_info_stylesheet is not None:
            _info_label.setStyleSheet(_original_info_stylesheet)
        
        _is_left_aligned = False
        print("Restored centered header alignment")
    
    # Reset stored variables for good practice
    _app_instance = None
    
    print("Left-Aligned Header extension cleaned up")

def modify_layout(app):
    """
    Modify the application's UI layout
    
    This hook is called when:
    1. The extension is activated
    2. The extension manager refreshes all extensions
    
    It should apply whatever layout changes your extension makes.
    Keep a reference to anything you'll need to restore during cleanup.
    
    Args:
        app: The main application instance (HyprText)
        
    Returns:
        bool: True if modification was successful, False otherwise
    """
    global _app_instance, _file_label, _info_label, _is_left_aligned
    global _original_file_alignment, _original_info_alignment
    global _original_file_stylesheet, _original_info_stylesheet
    
    if not app:
        return False
    
    try:
        # Store the app instance for later
        _app_instance = app
        
        # Get references to the labels we want to modify
        _file_label = app.file_label
        _info_label = app.info_label
        
        # Store the original alignment and stylesheet for later restoration
        if not _is_left_aligned:
            _original_file_alignment = _file_label.alignment()
            _original_info_alignment = _info_label.alignment()
            _original_file_stylesheet = _file_label.styleSheet()
            _original_info_stylesheet = _info_label.styleSheet()
        
        # Change alignment from center to left
        _file_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        _info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Also modify the stylesheet to ensure alignment
        # Get the current stylesheet and modify it
        file_style = _file_label.styleSheet()
        info_style = _info_label.styleSheet()
        
        # Add or replace text-align property in the stylesheet
        from PyQt6.QtGui import QColor
        
        # Append text-align property to existing stylesheet
        file_style = file_style.replace("text-align: center;", "")
        info_style = info_style.replace("text-align: center;", "")
        
        file_style += "\nQLabel { text-align: left; padding-left: 15px; }"
        info_style += "\nQLabel { text-align: left; padding-left: 15px; }"
        
        _file_label.setStyleSheet(file_style)
        _info_label.setStyleSheet(info_style)
        
        # Update our state tracking
        _is_left_aligned = True
        print("Applied left-aligned header text")
        
        return True
    except Exception as e:
        print(f"Error modifying layout: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def post_theme_change(app, theme_name):
    """
    Handle theme changes
    
    This optional hook is called after a theme is changed.
    Use it to adjust your extension to match the new theme colors,
    or reapply modifications that might be affected by theme changes.
    
    Args:
        app: The main application instance (HyprText)
        theme_name: The name of the new theme
    """
    if _is_left_aligned:
        # Re-apply our modifications if needed
        # This ensures they persist through theme changes
        if _file_label and _info_label:
            _file_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            _info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            
            # Get the current stylesheet and modify it
            file_style = _file_label.styleSheet()
            info_style = _info_label.styleSheet()
            
            # Add or replace text-align property
            file_style = file_style.replace("text-align: center;", "")
            info_style = info_style.replace("text-align: center;", "")
            
            file_style += "\nQLabel { text-align: left; padding-left: 15px; }"
            info_style += "\nQLabel { text-align: left; padding-left: 15px; }"
            
            _file_label.setStyleSheet(file_style)
            _info_label.setStyleSheet(info_style)
            
            print(f"Reapplied left-aligned header after theme change to {theme_name}") 