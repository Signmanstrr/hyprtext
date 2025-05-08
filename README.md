# HyprText

<div align="center">

![GitHub repo size](https://img.shields.io/github/repo-size/Signmanstrr/hyprtext)
![GitHub last commit](https://img.shields.io/github/last-commit/Signmanstrr/hyprtext)
![GitHub license](https://img.shields.io/github/license/Signmanstrr/hyprtext?color=blue)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**A sleek, modular text editor designed with Hyprland tiling windows in mind.**

<p align="center">
  <img src="https://github.com/user-attachments/assets/a6b48e3b-5065-4ac3-a877-f2d262ffcc7a" width="400" />
  <img src="https://github.com/user-attachments/assets/d4abf0cd-f7bf-4e49-8d30-2f18d521c8ac" width="400" />
</p>

</div>

## ✨ Features

- 🎨 Simple sleek UI with easily customizable theme system
- 🌙 Autodetects if you're in Dark Mode and changes to match
- 🧩 Modular system allowing for easy user modification of almost all elements
- 💾 Automagically saves a backup for unsaved files on program close
- 🔄 Easy-to-read scripting for custom extensions
- 🪟 Made with frameless WMs like Hyprland in mind

## 📦 Installation

### Prerequisites

- Python 3.8+
- PyQt6
- darkdetect

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Signmanstrr/hyprtext.git
cd hyprtext

# Install dependencies
pip install -r requirements.txt

# Make the script executable
chmod +x src/main.py

# Run HyprText
./src/main.py
```

## 🎮 Usage

### Keyboard Shortcuts

| Category | Action | Shortcut |
|----------|--------|----------|
| **File** | New File | <kbd>Ctrl</kbd> + <kbd>N</kbd> |
|          | Open File | <kbd>Ctrl</kbd> + <kbd>O</kbd> |
|          | Save File | <kbd>Ctrl</kbd> + <kbd>S</kbd> |
|          | Exit | <kbd>Ctrl</kbd> + <kbd>Q</kbd> |
| **Edit** | Undo | <kbd>Ctrl</kbd> + <kbd>Z</kbd> |
|          | Redo | <kbd>Ctrl</kbd> + <kbd>Y</kbd> |
|          | Cut | <kbd>Ctrl</kbd> + <kbd>X</kbd> |
|          | Copy | <kbd>Ctrl</kbd> + <kbd>C</kbd> |
|          | Paste | <kbd>Ctrl</kbd> + <kbd>V</kbd> |
| **Other** | Refresh Modes | <kbd>Ctrl</kbd> + <kbd>R</kbd> |
|           | Refresh Themes | <kbd>Ctrl</kbd> + <kbd>T</kbd> |
|           | Refresh Extensions | <kbd>Ctrl</kbd> + <kbd>E</kbd> |

## 🧩 Mods

HyprText was built with a focus on modular design. In the mods folder, you can:

- Create custom text editing modes for specific environments
- Easily design your own themes, with support for transparency and glow effects
- Make extensions that modify main app functionality without overriding any main code

### Themeing Quickstart

Create a new Python file in `mods/themes/` with the following structure:

```python
# Theme metadata
THEME_NAME = "My Custom Theme"
THEME_DESCRIPTION = "A beautiful custom theme"
THEME_AUTHOR = "Your Name"
THEME_VERSION = "1.0"

# Theme Colors
DARK_MODE = {
    "background": "rgba(10, 10, 10, 0.85)",
    "text": "#ffffff",
    "accent": "#64ffda",
    # Add more colors as needed
}

LIGHT_MODE = {
    "background": "rgba(255, 255, 255, 0.85)",
    "text": "#0a192f",
    "accent": "#64ffda",
    # Add more colors as needed
}
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest features
- Submit pull requests

---

<div align="center">
  <i>Made with ❤️ by <a href="https://github.com/Signmanstrr">Signmanstrr</a></i>
</div> 
