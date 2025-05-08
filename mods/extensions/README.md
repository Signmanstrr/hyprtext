# HyprText Extensions System

The extensions system in HyprText allows you to modify the editor's behavior and appearance without changing the core code. Extensions can be toggled on and off independently through the Extensions menu.

## How Extensions Work

Extensions are Python modules that implement specific hooks (functions) that are called by the extension manager at different points during the application lifecycle. The extension manager discovers extensions in the `mods/extensions` directory and makes them available to the user.

### Extension Lifecycle

1. **Discovery**: Extensions are discovered in the `mods/extensions` directory.
2. **Registration**: Extensions are registered with metadata (name, description, etc.).
3. **Activation**: Extensions can be activated by the user through the Extensions menu.
4. **Hook Execution**: Active extensions' hooks are called at specific points in the application.
5. **Deactivation**: Extensions can be deactivated, which calls the cleanup hook.

## Creating an Extension

To create an extension:

1. Create a new Python file in the `mods/extensions` directory.
2. Define the required metadata constants.
3. Implement the desired hooks.

### Required Metadata

Every extension must define these constants:

```python
EXTENSION_NAME = "My Extension"
EXTENSION_DESCRIPTION = "What my extension does"
EXTENSION_AUTHOR = "Your Name"
EXTENSION_VERSION = "1.0"
```

### Available Hooks

| Hook Name | Description | Parameters |
|-----------|-------------|------------|
| `initialize` | Called when the extension is activated | `app` |
| `cleanup` | Called when the extension is deactivated | `app` |
| `modify_layout` | Called to apply layout changes | `app` |
| `pre_close` | Called before the application closes | `app` |
| `post_load_file` | Called after a file is loaded | `app`, `file_path` |
| `pre_save_file` | Called before a file is saved | `app`, `file_path`, `content` |
| `post_theme_change` | Called after the theme is changed | `app`, `theme_name` |
| `post_mode_change` | Called after the mode is changed | `app`, `mode_name` |
| `process_keystroke` | Called to process keystrokes | `app`, `event` |
| `extend_menus` | Called to add items to menus | `app` |

## Best Practices

1. **Store Original State**: Always store original values of UI elements you modify.
2. **Clean Up Changes**: In the cleanup hook, restore the application to its original state.
3. **Use Flags for Tracking**: Track what changes you've made with boolean flags.
4. **Error Handling**: Wrap modifications in try/except blocks to prevent crashes.
5. **Descriptive Comments**: Document your extension thoroughly.

## Extension Examples

### Bottom Menubar

Moves the menubar from top to bottom, demonstrates layout modification:

```python
def modify_layout(app):
    # Remove menubar from top
    main_layout = app.background_widget.layout()
    top_bar = main_layout.itemAt(0).widget()
    main_layout.removeWidget(top_bar)
    
    # Add to bottom
    main_layout.addWidget(top_bar)
```

### Left-Aligned Header

Changes header text alignment from center to left:

```python
def modify_layout(app):
    # Store original alignment
    _original_alignment = app.file_label.alignment()
    
    # Change to left alignment
    app.file_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    app.info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
```

## Debugging Extensions

- Enable an extension to see debug output in the console.
- If an extension causes issues, you can disable it from the Extensions menu.
- Use `print()` statements for debugging (they appear in the terminal).
- Extension errors are caught by the extension manager to prevent application crashes.

## Contributing Extensions

If you create a useful extension, consider sharing it with the community by:

1. Ensuring it follows the best practices outlined above
2. Adding thorough documentation
3. Creating a pull request to the HyprText repository 