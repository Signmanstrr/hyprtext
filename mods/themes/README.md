# HyprText Theme System

This directory contains custom themes for the HyprText editor. You can create your own themes by following the instructions below.

## Creating a Custom Theme

1. Copy the default theme file from `hyprtext/src/theme_default.py` to this directory with a new name, e.g., `my_theme.py`.
2. Modify the values in the file to customize the appearance.
3. Restart HyprText or use the "Refresh Themes" option in the Themes menu.

## Theme File Structure

A theme file must contain the following components:

### Required Constants

```python
# Theme metadata
THEME_NAME = "My Theme"  # Display name in the UI
THEME_DESCRIPTION = "A description of my custom theme"
THEME_AUTHOR = "Your Name"
THEME_VERSION = "1.0"

# Application settings
APP_NAME = "HyprText"  # Should not be changed
```

### Color Schemes

Define color schemes for both dark and light modes:

```python
# Dark mode colors
DARK_MODE = {
    "background": "#1E1E2E",  # Editor background
    "text": "#CDD6F4",        # Text color
    "accent": "#89B4FA",      # Accent color for highlights
    "menu_bg": "rgba(30, 30, 46, 0.95)",  # Menu background
    "menu_hover": "rgba(137, 180, 250, 0.15)",  # Hover effect
    "menu_active": "rgba(137, 180, 250, 0.3)",  # Active/selected item
    "window_bg_gradient_start": "rgba(24, 24, 37, 0.95)",  # Window gradient start
    "window_bg_gradient_end": "rgba(30, 30, 46, 0.95)",    # Window gradient end
    "editor_border": "#89B4FA",  # Border color for editor
    "scrollbar_handle": "#89B4FA"  # Scrollbar color
}

# Light mode colors (similar structure)
LIGHT_MODE = { ... }
```

### Shadow Effects

Configure the shadow effect for widgets:

```python
SHADOW_EFFECT = {
    "blur_radius": 20,
    "color": "#89B4FA",
    "offset_x": 0,
    "offset_y": 0
}
```

### Stylesheet Templates

The stylesheet templates should be kept as is unless you want to add custom styling for specific widgets. The templates use the color values from the color schemes.

## Example

Check out the default theme in `hyprtext/src/theme_default.py` for a complete example.

## Tips for Creating Great Themes

1. Use complementary colors for background and text to ensure readability
2. Choose an accent color that stands out against your background
3. Use rgba colors for semi-transparent elements (menus, overlays)
4. Test both dark and light modes to ensure good contrast
5. Consider accessibility - ensure text is readable and contrast is sufficient 