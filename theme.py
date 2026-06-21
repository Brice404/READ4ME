LIGHT_STYLE = """
QWidget {
    background-color: #f5f5f5;
    color: #1a1a1a;
    font-size: 14px;
}

QTextEdit {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 3px;
    padding: 8px;
}

QPushButton {
    background-color: #e4e4e7;   /* same family as #f5f5f5 bg, slightly darker */
    color: #1a1a1a;              /* dark text — bg is light, so white won't read */
    border: 1px solid #d0d0d0;   /* subtle border keeps the button visible */
    border-radius: 3px;
    padding: 8px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #d4d4d8;   /* one shade darker on hover */
}

QPushButton:disabled {
    background-color: #ededee;
    color: #a0a0a0;
}

QComboBox, QDoubleSpinBox {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 3px;
    padding: 4px;
}
"""

DARK_STYLE = """
QWidget {
    background-color: #2b2b2b;
    color: #e0e0e0;
    font-size: 14px;
}

QTextEdit {
    background-color: #1e1e1e;
    border: 1px solid #444444;
    border-radius: 3px;
    padding: 8px;
}

QPushButton {
    background-color: #3a3a3a;   /* same family as #2b2b2b bg, slightly lighter */
    color: #e0e0e0;              /* light text on a dark button */
    border: 1px solid #444444;   /* subtle border keeps the button visible */
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #4a4a4a;   /* one shade lighter on hover */
}

QPushButton:disabled {
    background-color: #323232;
    color: #5a5a5a;
}

QComboBox, QDoubleSpinBox {
    background-color: #1e1e1e;
    border: 1px solid #444444;
    border-radius: 4px;
    padding: 4px;
}
"""