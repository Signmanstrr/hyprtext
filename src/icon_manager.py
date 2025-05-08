"""
HyprText Icon Manager
=====================

This module manages SVG icons for the HyprText editor.
It provides functions to load and retrieve icons by name.
"""

import os
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtSvg import QSvgRenderer

# Path to the icons directory
ICONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons')

# Icon cache to avoid loading the same icon multiple times
_icon_cache = {}

def ensure_icons_dir_exists():
    """
    Ensure the icons directory exists, creating it if needed
    """
    if not os.path.exists(ICONS_DIR):
        os.makedirs(ICONS_DIR)
        print(f"Created icons directory at {ICONS_DIR}")

def get_icon(name, fallback=None, textColor=None):
    """
    Get an icon by name from the icon set
    
    Args:
        name (str): The name of the icon (without extension)
        fallback: A fallback icon or StandardPixmap to use if the icon isn't found
        textColor (str): Optional color to apply to the SVG icon (for theming)
        
    Returns:
        QIcon: The requested icon
    """
    # Ensure the icons directory exists
    ensure_icons_dir_exists()
    
    # Create a cache key that includes the color if provided
    cache_key = f"{name}_{textColor}" if textColor else name
    
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]
        
    # Try to load the icon from the icon directory
    svg_path = os.path.join(ICONS_DIR, f'{name}.svg')
    if os.path.exists(svg_path):
        # If textColor is provided, use colorize function
        if textColor:
            try:
                # Read SVG content
                with open(svg_path, 'r') as f:
                    svg_content = f.read()
                
                # Create colorized icon
                icon = create_colorized_icon(svg_content, textColor)
                _icon_cache[cache_key] = icon
                return icon
            except Exception as e:
                print(f"Error colorizing icon: {e}")
                # Fall back to standard icon loading
        
        # Standard icon loading (no color override)
        icon = QIcon(svg_path)
        _icon_cache[cache_key] = icon
        return icon
    
    # If we can't find the SVG, use the fallback
    if fallback is not None:
        return fallback
        
    # Return a blank icon if no fallback is provided
    return QIcon()

def create_colorized_icon(svg_content, color="#FFFFFF", size=QSize(24, 24)):
    """
    Create a colorized icon from SVG content string
    
    Args:
        svg_content (str): The SVG content string
        color (str): The color to apply to the SVG
        size (QSize): The size of the icon
        
    Returns:
        QIcon: The colorized icon
    """
    # Replace the color in the SVG content
    colorized_svg = svg_content.replace('fill="currentColor"', f'fill="{color}"')
    
    # Create a QPixmap from the SVG content
    renderer = QSvgRenderer(bytes(colorized_svg, encoding='utf-8'))
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    # Render the SVG onto the pixmap
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    # Create a QIcon from the pixmap
    return QIcon(pixmap)

def register_custom_icon(name, icon):
    """
    Register a custom icon in the icon cache
    
    Args:
        name (str): The name to give the icon
        icon (QIcon): The icon to register
    """
    _icon_cache[name] = icon

# Standard icon names for the application
ICON_FILE = "file"            # File operations icon
ICON_EDIT = "edit"            # Edit operations icon
ICON_MODE = "mode"            # Mode switching icon
ICON_THEME = "theme"          # Theme switching icon
ICON_EXTENSION = "extension"  # Extensions icon
ICON_NEW = "new"              # New file icon
ICON_OPEN = "open"            # Open file icon
ICON_SAVE = "save"            # Save file icon
ICON_UNDO = "undo"            # Undo icon
ICON_REDO = "redo"            # Redo icon
ICON_CUT = "cut"              # Cut icon
ICON_COPY = "copy"            # Copy icon
ICON_PASTE = "paste"          # Paste icon
ICON_EXIT = "exit"            # Exit application icon
ICON_REFRESH = "refresh"      # Refresh icon

# Ensure the icons directory exists when the module is imported
ensure_icons_dir_exists() 