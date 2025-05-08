import os
import importlib.util
import sys
from PyQt6.QtWidgets import QTextEdit

class ModeManager:
    """Manager for dynamically loading and handling editor modes"""
    
    def __init__(self):
        self.modes = {}  # Dictionary of mode_name: mode_module
        self.current_mode = None
        
    def discover_modes(self):
        """Scan the mods/modes directory for mode modules"""
        # Get the absolute path to the app directory
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Print current working directory and app directory for debugging
        print(f"Current working directory: {os.getcwd()}")
        print(f"App directory: {app_dir}")
        
        # Calculate the modes directory path
        modes_dir = os.path.join(app_dir, "mods", "modes")
        
        # Also try the path relative to the current working directory
        if not os.path.exists(modes_dir):
            modes_dir = os.path.join(os.getcwd(), "mods", "modes")
            
        print(f"Looking for modes in: {modes_dir}")
        
        # Clear existing modes before rescanning
        self.modes.clear()
        
        # Ensure the directory exists
        if not os.path.exists(modes_dir):
            print(f"Creating modes directory: {modes_dir}")
            os.makedirs(modes_dir, exist_ok=True)
            return
        
        # Find all Python files in the directory
        for filename in os.listdir(modes_dir):
            if filename.endswith(".py"):
                module_name = filename[:-3]  # Remove .py extension
                module_path = os.path.join(modes_dir, filename)
                
                try:
                    # Load the module
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    
                    # Check for required attributes and functions
                    if hasattr(module, 'MODE_NAME') and hasattr(module, 'create_editor'):
                        mode_name = module.MODE_NAME
                        self.modes[mode_name] = module
                        print(f"Loaded mode: {mode_name}")
                    else:
                        print(f"Skipping {filename}: Missing required attributes")
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")
    
    def get_mode_names(self):
        """Return a list of available mode names"""
        return list(self.modes.keys())
    
    def get_mode_description(self, mode_name):
        """Return the description for a mode"""
        if mode_name in self.modes and hasattr(self.modes[mode_name], 'MODE_DESCRIPTION'):
            return self.modes[mode_name].MODE_DESCRIPTION
        return "No description available"
    
    def create_editor_for_mode(self, mode_name, parent=None):
        """Create and return an editor instance for the specified mode"""
        if mode_name in self.modes:
            try:
                return self.modes[mode_name].create_editor(parent)
            except Exception as e:
                print(f"Error creating editor for {mode_name}: {str(e)}")
        
        # Fallback to a basic editor if mode not found or error occurred
        print(f"Using fallback editor for mode: {mode_name}")
        return QTextEdit(parent)
    
    def get_default_mode(self):
        """Return the default mode name (None for Standard Mode)"""
        # Always return None to ensure Standard Mode is the default
        return None
        
    def get_theme_color_overrides(self, mode_name):
        """Get theme color overrides for the specified mode
        
        Some modes may need to override theme colors to ensure readability.
        This method checks if a mode provides THEME_COLOR_OVERRIDES and returns them.
        
        Returns:
            dict: A dictionary of color keys and values to override the current theme's colors
                 or None if no overrides are specified
        """
        if mode_name in self.modes:
            try:
                if hasattr(self.modes[mode_name], 'THEME_COLOR_OVERRIDES'):
                    return self.modes[mode_name].THEME_COLOR_OVERRIDES
            except Exception as e:
                print(f"Error getting theme color overrides for {mode_name}: {str(e)}")
        return None

# Create a global instance
mode_manager = ModeManager() 