# HyprText Modes

This directory contains custom editing modes for the HyprText editor. Each mode provides a specialized editing experience with unique behaviors, styling, and functionality.

## What is a Mode?

In HyprText, a mode is a specialized editing environment that transforms how users interact with their text. Modes can change:
- Visual appearance (colors, fonts, styling)
- Text editing behavior and animations
- Key binding functionality
- Special features specific to certain content types

## Creating a Custom Mode

### Basic Structure

Every mode must be defined as a Python module with the following components:

#### Required Components:

1. **Mode Metadata**:
   ```python
   MODE_NAME = "My Custom Mode"
   MODE_DESCRIPTION = "Short description of what this mode does"
   MODE_ICON = None  # Optional path to an icon
   ```

2. **Editor Creation Function**:
   ```python
   def create_editor(parent=None):
       """Create and return the editor widget for this mode"""
       return MyCustomTextEdit(parent)
   ```

3. **Custom Editor Widget**:
   Most modes define their own editor widget by extending `QTextEdit`, `QPlainTextEdit`, or `SmoothTextEdit`.

### Optional Components

#### Theme Override System

Modes can override theme colors by defining `THEME_COLOR_OVERRIDES`:

```python
THEME_COLOR_OVERRIDES = {
    "text": "#000000",
    "background": "#f8f4e3",
    "accent": "#8B4513",
    # ... other color keys
}
```

These overrides will be applied whenever the mode is activated, regardless of the current theme.

#### Hook Functions

Modes can define hook functions that are called during specific events:

1. **post_theme_change(app, theme_name)**:
   Called after a theme change to ensure mode-specific styling remains consistent.
   
   ```python
   def post_theme_change(app, theme_name):
       """Handle theme changes by ensuring mode colors are preserved"""
       if app.current_mode == MODE_NAME and app.current_mode in app.mode_editors:
           editor = app.mode_editors[app.current_mode]
           # Re-apply mode-specific styling
   ```

2. **on_mode_activate(app, previous_mode)**:
   Called when the mode is activated.

3. **on_mode_deactivate(app, next_mode)**:
   Called when switching away from this mode.

## Animation Support

For modes with special animation effects, use the `SmoothTextEdit` base class instead of standard `QTextEdit`:

```python
from animation import SmoothTextEdit

class MyAnimatedEditor(SmoothTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animations_enabled = True
        self.animation_duration = 150  # milliseconds
```

## Example Modes

The repository includes several example modes:

- **Example Mode**: A template demonstrating basic mode structure (example_mode.py)
- **Zen Mode**: Distraction-free writing experience (zen_mode.py)
- **Typewriter Mode**: Simulates typing on an old-style typewriter (typewriter_mode.py)
- **Config Mode**: Specialized mode for editing configuration files (config_mode.py)

You can examine these modes to understand how to implement various features in your own custom modes.

## How Modes Are Loaded

HyprText automatically loads modes from this directory at startup. To add a new mode:

1. Create a new Python file in this directory
2. Implement the required components described above
3. Restart HyprText or use the reload function if available

Each mode appears in the mode selector menu, allowing users to switch between different editing experiences.

## Mode Extension Points

Beyond the basic requirements, your mode can customize:

- **Key Bindings**: Override `keyPressEvent` to handle keys differently
- **Context Menus**: Create custom right-click menus
- **File Handling**: Add special handling for specific file types
- **UI Elements**: Add custom UI components to the editor
- **Animations**: Create custom transitions and effects
- **Styling**: Implement specialized visual styling 