from PyQt6.QtWidgets import QPlainTextEdit, QWidget
from PyQt6.QtGui import QPainter, QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt6.QtCore import Qt, QRect, QSize, QRegularExpression
import sys
import os

# Add the src directory to the path if needed
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from theme_manager import ThemeManager, ACCENT_COLOR

# Mode metadata
MODE_NAME = "Config Mode"
MODE_DESCRIPTION = "Editor mode with syntax highlighting and line numbers"
MODE_ICON = None  # Could be a path to an icon

class LineNumberArea(QWidget):
    """Widget for displaying line numbers in a code editor"""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

class SyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for programming languages"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        self._setup_highlighting_rules()
    
    def _setup_highlighting_rules(self):
        # Define formats
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#ff79c6"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#f1fa8c"))
        
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6272a4"))
        
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#bd93f9"))
        
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#50fa7b"))
        
        # Add rules
        keywords = [
            "\\bif\\b", "\\belse\\b", "\\bfor\\b", "\\bwhile\\b",
            "\\bdef\\b", "\\bclass\\b", "\\breturn\\b", "\\bimport\\b",
            "\\bfrom\\b", "\\bas\\b", "\\btry\\b", "\\bexcept\\b",
            "\\bfinally\\b", "\\bwith\\b", "\\bpass\\b", "\\bbreak\\b",
            "\\bcontinue\\b", "\\bTrue\\b", "\\bFalse\\b", "\\bNone\\b"
        ]
        
        for pattern in keywords:
            self.highlighting_rules.append((
                QRegularExpression(pattern),
                keyword_format
            ))
            
        # String literals
        self.highlighting_rules.append((
            QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'),
            string_format
        ))
        self.highlighting_rules.append((
            QRegularExpression("'[^'\\\\]*(\\\\.[^'\\\\]*)*'"),
            string_format
        ))
        
        # Comments
        self.highlighting_rules.append((
            QRegularExpression("#[^\n]*"),
            comment_format
        ))
        
        # Numbers
        self.highlighting_rules.append((
            QRegularExpression("\\b[0-9]+\\b"),
            number_format
        ))
        
        # Function calls
        self.highlighting_rules.append((
            QRegularExpression("\\b[A-Za-z0-9_]+(?=\\()"),
            function_format
        ))
        
    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class ConfigTextEdit(QPlainTextEdit):
    """Config text editor with line numbers and syntax highlighting"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set a background color to show it's working
        self.setStyleSheet("background-color: #282a36; color: #f8f8f2;")
        
        # Set monospace font
        monospace_font = ThemeManager.get_monospace_font()
        self.setFont(monospace_font)
        self.document().setDefaultFont(monospace_font)
        
        # Create line number area
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.update_line_number_area_width(0)
        
        # Apply syntax highlighting
        self.highlighter = SyntaxHighlighter(self.document())
    
    def line_number_area_width(self):
        """Calculate width needed for line number area"""
        digits = max(1, len(str(self.blockCount())))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def update_line_number_area_width(self, _):
        """Update line number area width"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        """Update line number area on scroll"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
    
    def resizeEvent(self, event):
        """Handle resize event"""
        super().resizeEvent(event)
        
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))
    
    def line_number_area_paint_event(self, event):
        """Paint event for line number area"""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#21222c"))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#6272a4"))  # Line number color
                painter.drawText(0, top, self.line_number_area.width() - 5, self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1

# Mode interface functions
def create_editor(parent=None):
    """Create and return an editor widget for this mode"""
    return ConfigTextEdit(parent) 