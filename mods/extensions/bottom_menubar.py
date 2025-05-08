"""
Bottom Menubar Extension for HyprText
====================================

This extension moves the menubar from the top to the bottom of the window.
It demonstrates how to modify the application's UI layout without changing the core code.
"""

# Extension metadata
EXTENSION_NAME = "Bottom Menubar"
EXTENSION_DESCRIPTION = "Moves the menubar from the top to the bottom of the window"
EXTENSION_AUTHOR = "HyprText Extensions"
EXTENSION_VERSION = "1.0"

# Store original UI elements
_original_layout = None
_app_instance = None
_top_bar = None
_is_at_bottom = False
_original_show_menu = None  # Store the original _showMenu method

def initialize(app=None):
    """Initialize the extension when activated"""
    global _app_instance, _top_bar, _is_at_bottom, _original_show_menu
    
    if app:
        _app_instance = app
        # Find the top bar if it's not already stored
        if not _top_bar and app.background_widget and app.background_widget.layout():
            # The top bar is typically the first widget in the main layout
            main_layout = app.background_widget.layout()
            if main_layout.count() > 0:
                _top_bar = main_layout.itemAt(0).widget()
        
        # Store the original _showMenu method
        if not _original_show_menu:
            _original_show_menu = app._showMenu
            
        _is_at_bottom = False
        print("Bottom Menubar extension initialized")

def cleanup(app=None):
    """Clean up when the extension is deactivated"""
    global _app_instance, _top_bar, _is_at_bottom, _original_show_menu
    
    if app and _top_bar and _is_at_bottom:
        # Restore original layout
        try:
            # Get the main layout
            main_layout = app.background_widget.layout()
            
            # Remove the top bar from its current position (at the bottom)
            main_layout.removeWidget(_top_bar)
            
            # Add it back to the top (index 0)
            main_layout.insertWidget(0, _top_bar)
            
            _is_at_bottom = False
            print("Restored menubar to top position")
        except Exception as e:
            print(f"Error restoring layout: {str(e)}")
    
    # Restore the original _showMenu method
    if app and _original_show_menu:
        app._showMenu = _original_show_menu
        print("Restored original menu positioning")
    
    # Reset stored variables
    _app_instance = None
    _original_show_menu = None
    
    print("Bottom Menubar extension cleaned up")

def _bottom_show_menu(app, button, menu):
    """Custom menu display function for bottom menubar"""
    from PyQt6.QtCore import QPoint
    
    # Position the menu above the button instead of below
    pos = button.mapToGlobal(QPoint(0, -menu.sizeHint().height()))
    menu.popup(pos)
    # Connect aboutToHide signal to reset button state
    menu.aboutToHide.connect(lambda: app.resetButtonState(button))

def modify_layout(app):
    """Move the menubar from top to bottom"""
    global _app_instance, _top_bar, _is_at_bottom, _original_show_menu
    
    if not app:
        return
    
    try:
        # Store the app instance for later
        _app_instance = app
        
        # Get the main layout
        main_layout = app.background_widget.layout()
        
        # Find the top bar (first widget in the layout)
        _top_bar = main_layout.itemAt(0).widget()
        
        # Remove the top bar from the layout
        main_layout.removeWidget(_top_bar)
        
        # Add it to the bottom
        main_layout.addWidget(_top_bar)
        
        # Save the original _showMenu method if not already saved
        if not _original_show_menu:
            _original_show_menu = app._showMenu
        
        # Override the _showMenu method to position menus above the buttons
        app._showMenu = lambda button, menu: _bottom_show_menu(app, button, menu)
        
        _is_at_bottom = True
        print("Moved menubar to bottom position")
        print("Modified menu positioning to open above buttons")
        
        return True
    except Exception as e:
        print(f"Error modifying layout: {str(e)}")
        import traceback
        traceback.print_exc()
        return False 