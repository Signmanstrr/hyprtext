# HyprText

A simple and modular text editor environment made with Hyprland tiling windows in mind.

## Features
- Clean smooth interface with easy themeing capabilities
- Basic text editing, ala Notepad
- Automatic unsaved file backup on app close
- Fully modular system allowing easy creation and installation of custom Text Editing Modes, Application Themes, and Extensions (base app modifiers)

## Requirements

- Python 3.8 or higher
- PyQt6
- darkdetect

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/hyprtext.git
cd hyprtext
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Make the script executable:
```bash
chmod +x src/main.py
```

## Usage

Run the editor:
```bash
./src/main.py
```

### Keyboard Shortcuts

- `Ctrl+N`: New file
- `Ctrl+O`: Open file
- `Ctrl+S`: Save file
- `Ctrl+Q`: Quit
- `Ctrl+Z`: Undo
- `Ctrl+Y`: Redo
- `Ctrl+X`: Cut
- `Ctrl+C`: Copy
- `Ctrl+V`: Paste

## Contributing

Feel free to submit issues and enhancement requests! 