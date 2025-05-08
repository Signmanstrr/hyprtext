"""
Extension Manager for HyprText
==============================

This module manages extensions that can modify the behavior of HyprText without editing core files.
Extensions can be toggled on and off independently of each other.
"""

import os
import sys
import importlib.util
import traceback
from PyQt6.QtCore import QSettings

# Standard extension hooks that can be implemented
EXTENSION_HOOKS = [
    'initialize',          # Called when the extension is first loaded
    'cleanup',             # Called when the extension is unloaded/disabled
    'modify_layout',       # Hook to modify the application layout
    'pre_close',           # Called before the application closes
    'post_load_file',      # Called after a file is loaded
    'pre_save_file',       # Called before a file is saved
    'post_theme_change',   # Called after the theme is changed
    'post_mode_change',    # Called after the mode is changed
    'process_keystroke',   # Hook to process keystrokes
    'extend_menus'         # Hook to add items to menus
]

class ExtensionManager:
    """Manages HyprText extensions that modify application behavior"""
    
    _instance = None  # Singleton instance
    _available_extensions = {}  # Dictionary of available extensions
    _active_extensions = {}  # Dictionary of currently active extensions
    _extension_states = {}  # Track individual extension states
    
    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance"""
        if cls._instance is None:
            cls._instance = ExtensionManager()
        return cls._instance
    
    def __init__(self):
        """Initialize the extension manager"""
        if ExtensionManager._instance is not None:
            raise RuntimeError("ExtensionManager is a singleton. Use get_instance() instead.")
        
        ExtensionManager._instance = self
        self._discover_extensions()
        self._load_active_extensions()
    
    def _discover_extensions(self):
        """Discover available extensions in the mods/extensions directory"""
        try:
            # Get the absolute path to the app directory
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Calculate the extensions directory path
            extensions_dir = os.path.join(app_dir, "mods", "extensions")
            
            # Print debug info
            print(f"Looking for extensions in: {extensions_dir}")
            
            # Ensure the directory exists
            if not os.path.exists(extensions_dir):
                print(f"Creating extensions directory: {extensions_dir}")
                os.makedirs(extensions_dir, exist_ok=True)
                return
            
            # Find all Python files in the directory
            for filename in os.listdir(extensions_dir):
                if filename.endswith(".py") and filename != "__init__.py":
                    extension_name = filename[:-3]  # Remove .py extension
                    module_path = os.path.join(extensions_dir, filename)
                    
                    try:
                        # Load the module
                        spec = importlib.util.spec_from_file_location(extension_name, module_path)
                        module = importlib.util.module_from_spec(spec)
                        sys.modules[extension_name] = module
                        spec.loader.exec_module(module)
                        
                        # Check for required attributes
                        if hasattr(module, 'EXTENSION_NAME') and hasattr(module, 'EXTENSION_DESCRIPTION'):
                            extension_name = module.EXTENSION_NAME
                            self._available_extensions[extension_name] = {
                                "module_path": module_path,
                                "name": extension_name,
                                "description": module.EXTENSION_DESCRIPTION,
                                "author": getattr(module, 'EXTENSION_AUTHOR', "Unknown"),
                                "version": getattr(module, 'EXTENSION_VERSION', "1.0"),
                                "module": module,
                                "hooks": self._get_extension_hooks(module)
                            }
                            # Initialize state tracking for this extension
                            self._extension_states[extension_name] = {
                                "active": False,
                                "has_modified_layout": False
                            }
                            print(f"Loaded extension: {extension_name}")
                        else:
                            print(f"Skipping {filename}: Missing required attributes")
                    except Exception as e:
                        print(f"Error loading extension {filename}: {str(e)}")
                        traceback.print_exc()
        except Exception as e:
            print(f"Error discovering extensions: {str(e)}")
            traceback.print_exc()
    
    def _get_extension_hooks(self, module):
        """Get available hooks from an extension module"""
        hooks = {}
        for hook_name in EXTENSION_HOOKS:
            if hasattr(module, hook_name):
                hooks[hook_name] = getattr(module, hook_name)
        return hooks
    
    def _load_active_extensions(self):
        """Load previously active extensions from settings"""
        settings = QSettings("HyprText", "HyprText")
        active_extensions = settings.value('active_extensions', [])
        
        if active_extensions:
            for ext_name in active_extensions:
                if ext_name in self._available_extensions:
                    self._active_extensions[ext_name] = self._available_extensions[ext_name]
                    # Update state tracking
                    if ext_name in self._extension_states:
                        self._extension_states[ext_name]["active"] = True
                    self._call_hook(ext_name, 'initialize')
                    print(f"Activated extension: {ext_name}")
    
    def _save_active_extensions(self):
        """Save active extensions to settings"""
        settings = QSettings("HyprText", "HyprText")
        settings.setValue('active_extensions', list(self._active_extensions.keys()))
    
    def get_available_extensions(self):
        """Return a list of available extension names"""
        return list(self._available_extensions.keys())
    
    def get_extension_description(self, extension_name):
        """Return the description for an extension"""
        if extension_name in self._available_extensions:
            return self._available_extensions[extension_name].get("description", "No description available")
        return "Extension not found"
    
    def is_extension_active(self, extension_name):
        """Check if an extension is currently active"""
        return extension_name in self._active_extensions
    
    def toggle_extension(self, extension_name, app_instance=None):
        """Toggle an extension on or off"""
        if extension_name not in self._available_extensions:
            print(f"Extension not found: {extension_name}")
            return False
        
        if self.is_extension_active(extension_name):
            # Deactivate the extension - only call cleanup for this specific extension
            print(f"Cleaning up extension: {extension_name}")
            self._call_hook(extension_name, 'cleanup', app_instance)
            self._active_extensions.pop(extension_name)
            
            # Update state tracking
            if extension_name in self._extension_states:
                self._extension_states[extension_name]["active"] = False
                self._extension_states[extension_name]["has_modified_layout"] = False
            
            self._save_active_extensions()
            print(f"Deactivated extension: {extension_name}")
            return False
        else:
            # Activate the extension
            self._active_extensions[extension_name] = self._available_extensions[extension_name]
            
            # Update state tracking
            if extension_name in self._extension_states:
                self._extension_states[extension_name]["active"] = True
            
            self._call_hook(extension_name, 'initialize', app_instance)
            self._save_active_extensions()
            print(f"Activated extension: {extension_name}")
            return True
    
    def _call_hook(self, extension_name, hook_name, *args, **kwargs):
        """Call a hook function for an extension if it exists"""
        if extension_name in self._active_extensions:
            extension = self._active_extensions[extension_name]
            if hook_name in extension["hooks"]:
                try:
                    result = extension["hooks"][hook_name](*args, **kwargs)
                    
                    # Track layout modifications for better cleanup
                    if hook_name == 'modify_layout' and extension_name in self._extension_states:
                        self._extension_states[extension_name]["has_modified_layout"] = True
                        
                    return result
                except Exception as e:
                    print(f"Error calling {hook_name} hook in {extension_name}: {str(e)}")
                    traceback.print_exc()
        return False
    
    def call_hook_for_all(self, hook_name, *args, **kwargs):
        """Call a hook function for all active extensions"""
        results = []
        # Make a copy of the keys to avoid modification during iteration
        active_extension_names = list(self._active_extensions.keys())
        for ext_name in active_extension_names:
            result = self._call_hook(ext_name, hook_name, *args, **kwargs)
            results.append((ext_name, result))
        return results
    
    def get_extension_state(self, extension_name):
        """Get the current state of an extension"""
        if extension_name in self._extension_states:
            return self._extension_states[extension_name]
        return {"active": False, "has_modified_layout": False}
    
    def reset_layout_state(self, extension_name):
        """Reset the layout modification state for an extension"""
        if extension_name in self._extension_states:
            self._extension_states[extension_name]["has_modified_layout"] = False
            return True
        return False

# Initialize the singleton instance
extension_manager = ExtensionManager.get_instance() 