import darkdetect
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtCore import QPointF, QSettings
import os
import importlib.util
import sys
import traceback

# Import default theme
from theme_default import (
    APP_NAME, DEFAULT_FONT, DEFAULT_FONT_SIZE, 
    DARK_MODE, LIGHT_MODE, SHADOW_EFFECT,
    DARK_STYLESHEET_TEMPLATE, LIGHT_STYLESHEET_TEMPLATE
)

# Shortcuts for commonly used constants (maintaining backwards compatibility)
ACCENT_COLOR = DARK_MODE["accent"]
DARK_BG = DARK_MODE["background"]
DARK_TEXT = DARK_MODE["text"]
LIGHT_BG = LIGHT_MODE["background"]
LIGHT_TEXT = LIGHT_MODE["text"]

class ThemeManager:
    """Manages theme settings and styling for the application"""
    
    _current_theme = None
    _available_themes = {}
    
    @classmethod
    def initialize(cls):
        """Initialize the theme manager by discovering available themes"""
        # Load default theme
        cls._available_themes = {
            "Default": {
                "module_path": None,
                "name": "Default",
                "description": "Default HyprText theme with Hyprland-inspired aesthetics",
                "author": "HyprText Team",
                "version": "1.0"
            }
        }
        
        # Discover custom themes
        cls.discover_themes()
        
        # Load theme from settings
        settings = QSettings(APP_NAME, APP_NAME)
        theme_name = settings.value('theme', "Default")
        
        # Default to "Default" if the saved theme is not available
        if theme_name not in cls._available_themes:
            theme_name = "Default"
            
        # Load the theme
        cls.load_theme(theme_name)
    
    @classmethod
    def discover_themes(cls):
        """Discover available themes in the mods/themes directory"""
        try:
            # Get the absolute path to the app directory
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Calculate the themes directory path
            themes_dir = os.path.join(app_dir, "mods", "themes")
            
            # Print debug info
            print(f"Looking for themes in: {themes_dir}")
            
            # Ensure the directory exists
            if not os.path.exists(themes_dir):
                print(f"Creating themes directory: {themes_dir}")
                os.makedirs(themes_dir, exist_ok=True)
                return
            
            # Find all Python files in the directory
            for filename in os.listdir(themes_dir):
                if filename.endswith(".py") and filename != "__init__.py":
                    module_name = filename[:-3]  # Remove .py extension
                    module_path = os.path.join(themes_dir, filename)
                    
                    try:
                        # Load the module
                        spec = importlib.util.spec_from_file_location(module_name, module_path)
                        module = importlib.util.module_from_spec(spec)
                        sys.modules[module_name] = module
                        spec.loader.exec_module(module)
                        
                        # Check for required attributes
                        if hasattr(module, 'THEME_NAME') and hasattr(module, 'THEME_DESCRIPTION'):
                            theme_name = module.THEME_NAME
                            cls._available_themes[theme_name] = {
                                "module_path": module_path,
                                "name": theme_name,
                                "description": module.THEME_DESCRIPTION,
                                "author": getattr(module, 'THEME_AUTHOR', "Unknown"),
                                "version": getattr(module, 'THEME_VERSION', "1.0"),
                                "module": module
                            }
                            print(f"Loaded theme: {theme_name}")
                        else:
                            print(f"Skipping {filename}: Missing required attributes")
                    except Exception as e:
                        print(f"Error loading theme {filename}: {str(e)}")
                        traceback.print_exc()
        except Exception as e:
            print(f"Error discovering themes: {str(e)}")
            traceback.print_exc()
    
    @classmethod
    def get_available_themes(cls):
        """Return a list of available theme names"""
        return list(cls._available_themes.keys())
    
    @classmethod
    def get_theme_description(cls, theme_name):
        """Return the description for a theme"""
        if theme_name in cls._available_themes:
            return cls._available_themes[theme_name].get("description", "No description available")
        return "Theme not found"
    
    @classmethod
    def load_theme(cls, theme_name):
        """Load a theme by name"""
        try:
            if theme_name not in cls._available_themes:
                print(f"Theme {theme_name} not found, using Default")
                theme_name = "Default"
                
            cls._current_theme = theme_name
            
            # Save the theme choice in settings
            settings = QSettings(APP_NAME, APP_NAME)
            settings.setValue('theme', theme_name)
            
            print(f"Loaded theme: {theme_name}")
            return True
        except Exception as e:
            print(f"Error loading theme {theme_name}: {str(e)}")
            traceback.print_exc()
            return False
    
    @classmethod
    def get_current_theme(cls):
        """Return the name of the current theme"""
        return cls._current_theme or "Default"
    
    @classmethod
    def is_dark_mode(cls):
        """Check if dark mode is enabled"""
        return darkdetect.isDark()
    
    @classmethod
    def get_editor_font(cls):
        """Get the editor font"""
        try:
            # Get the current theme module
            theme_module = cls._get_theme_module()
            
            # Get font from theme
            font_name = getattr(theme_module, 'DEFAULT_FONT', DEFAULT_FONT)
            font_size = getattr(theme_module, 'DEFAULT_FONT_SIZE', DEFAULT_FONT_SIZE)
            
            return QFont(font_name, font_size)
        except Exception as e:
            print(f"Error getting editor font: {str(e)}")
            traceback.print_exc()
            return QFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)
    
    @classmethod
    def get_monospace_font(cls):
        """Get a monospace font"""
        font = cls.get_editor_font()
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setFixedPitch(True)
        return font
    
    @classmethod
    def get_stylesheet(cls, is_dark=None):
        """Get the stylesheet for the current theme"""
        if is_dark is None:
            is_dark = cls.is_dark_mode()
            
        try:
            # Get the current theme module
            theme_module = cls._get_theme_module()
            
            # Get theme colors
            if is_dark:
                colors = getattr(theme_module, 'DARK_MODE', DARK_MODE)
                template = getattr(theme_module, 'DARK_STYLESHEET_TEMPLATE', DARK_STYLESHEET_TEMPLATE)
            else:
                colors = getattr(theme_module, 'LIGHT_MODE', LIGHT_MODE)
                template = getattr(theme_module, 'LIGHT_STYLESHEET_TEMPLATE', LIGHT_STYLESHEET_TEMPLATE)
            
            # Format the stylesheet template with the theme colors using % operator
            return template % colors
        except Exception as e:
            print(f"Error getting stylesheet: {str(e)}")
            traceback.print_exc()
            return cls.get_dark_stylesheet() if is_dark else cls.get_light_stylesheet()
    
    @classmethod
    def get_dark_stylesheet(cls):
        """Get the dark mode stylesheet from the default theme"""
        try:
            return DARK_STYLESHEET_TEMPLATE % DARK_MODE
        except Exception as e:
            print(f"Error formatting dark stylesheet: {str(e)}")
            traceback.print_exc()
            return ""
    
    @classmethod
    def get_light_stylesheet(cls):
        """Get the light mode stylesheet from the default theme"""
        try:
            return LIGHT_STYLESHEET_TEMPLATE % LIGHT_MODE
        except Exception as e:
            print(f"Error formatting light stylesheet: {str(e)}")
            traceback.print_exc()
            return ""
    
    @classmethod
    def apply_shadow_effect(cls, widget):
        """Apply a shadow effect to a widget"""
        try:
            # Get the current theme module
            theme_module = cls._get_theme_module()
            
            # Get shadow effect settings
            shadow_effect = getattr(theme_module, 'SHADOW_EFFECT', SHADOW_EFFECT)
            
            # Apply the shadow effect
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(shadow_effect.get("blur_radius", 15))
            shadow.setColor(QColor(shadow_effect.get("color", ACCENT_COLOR)))
            shadow.setOffset(QPointF(shadow_effect.get("offset_x", 0), shadow_effect.get("offset_y", 0)))
            widget.setGraphicsEffect(shadow)
            return shadow
        except Exception as e:
            print(f"Error applying shadow effect: {str(e)}")
            traceback.print_exc()
            
            # Fallback to default shadow
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setColor(QColor(ACCENT_COLOR))
            shadow.setOffset(QPointF(0, 0))
            widget.setGraphicsEffect(shadow)
            return shadow
    
    @classmethod
    def _get_theme_module(cls):
        """Get the module for the current theme"""
        theme_name = cls._current_theme or "Default"
        
        if theme_name == "Default":
            # Use imported default theme
            import theme_default
            return theme_default
        else:
            # Return the custom theme module
            theme_info = cls._available_themes.get(theme_name, {})
            return theme_info.get("module", None) or cls._load_theme_module(theme_name)
    
    @classmethod
    def _load_theme_module(cls, theme_name):
        """Load a theme module dynamically"""
        try:
            theme_info = cls._available_themes.get(theme_name, {})
            module_path = theme_info.get("module_path")
            
            if not module_path or not os.path.exists(module_path):
                print(f"Theme module not found: {theme_name}")
                return None
                
            # Load the module
            spec = importlib.util.spec_from_file_location(theme_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[theme_name] = module
            spec.loader.exec_module(module)
            
            # Cache the module
            cls._available_themes[theme_name]["module"] = module
            
            return module
        except Exception as e:
            print(f"Error loading theme module {theme_name}: {str(e)}")
            traceback.print_exc()
            return None

# Initialize the theme manager
ThemeManager.initialize() 