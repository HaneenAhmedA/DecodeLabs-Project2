# ============================================================
#  Basic Encryption & Decryption — Enhanced GUI
#  DecodeLabs Industrial Training Kit — Project 2
#  Features: Caesar, Vigenère, Brute Force, Frequency Analysis
# ============================================================

import sys
from collections import Counter
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QSpinBox,
    QTextEdit, QTabWidget, QScrollArea, QGridLayout,
    QSizePolicy
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# ── Cipher Logic ─────────────────────────────────────────────

def caesar_encrypt(text: str, shift: int) -> str:
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)

def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)

def vigenere_encrypt(text: str, key: str) -> str:
    if not key.isalpha():
        return text
    key = key.upper()
    result = []
    k = 0
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[k % len(key)]) - ord('A')
            result.append(chr((ord(char) - base + shift) % 26 + base))
            k += 1
        else:
            result.append(char)
    return ''.join(result)

def vigenere_decrypt(text: str, key: str) -> str:
    if not key.isalpha():
        return text
    key = key.upper()
    result = []
    k = 0
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[k % len(key)]) - ord('A')
            result.append(chr((ord(char) - base - shift) % 26 + base))
            k += 1
        else:
            result.append(char)
    return ''.join(result)

def brute_force(text: str) -> list:
    return [(shift, caesar_decrypt(text, shift)) for shift in range(1, 26)]

def get_letter_freq(text: str) -> dict:
    letters = [c.upper() for c in text if c.isalpha()]
    total = len(letters) if letters else 1
    counts = Counter(letters)
    return {chr(65+i): round(counts.get(chr(65+i), 0) / total * 100, 1) for i in range(26)}


# ── Styles ────────────────────────────────────────────────────

DARK   = "#1e1e2e"
DARKER = "#181825"
CARD   = "#313244"
BORDER = "#45475a"
MUTED  = "#6c7086"
TEXT   = "#cdd6f4"
BLUE   = "#89b4fa"
GREEN  = "#a6e3a1"
ORANGE = "#fab387"
RED    = "#f38ba8"
PURPLE = "#cba6f7"

STYLE = f"""
QWidget {{ background-color: {DARK}; color: {TEXT}; font-family: 'Segoe UI'; }}
QTabWidget::pane {{ border: 1px solid {BORDER}; border-radius: 8px; background: {DARK}; }}
QTabBar::tab {{
    background: {CARD}; color: {MUTED}; border-radius: 6px;
    padding: 8px 20px; margin-right: 4px; font-size: 12px;
}}
QTabBar::tab:selected {{ background: {BLUE}; color: {DARKER}; font-weight: bold; }}
QTabBar::tab:hover {{ background: {BORDER}; color: {TEXT}; }}
QLineEdit, QTextEdit {{
    background-color: {CARD}; color: {TEXT};
    border: 1px solid {BORDER}; border-radius: 8px;
    padding: 10px 14px; font-size: 13px;
}}
QLineEdit:focus, QTextEdit:focus {{ border: 1px solid {BLUE}; }}
QSpinBox {{
    background-color: {CARD}; color: {TEXT};
    border: 1px solid {BORDER}; border-radius: 8px;
    padding: 8px 14px; font-size: 13px;
}}
QPushButton#encBtn {{
    background-color: {BLUE}; color: {DARKER}; border: none;
    border-radius: 8px; padding: 10px; font-size: 13px; font-weight: bold;
}}
QPushButton#encBtn:hover {{ background-color: #74c7ec; }}
QPushButton#decBtn {{
    background-color: {GREEN}; color: {DARKER}; border: none;
    border-radius: 8px; padding: 10px; font-size: 13px; font-weight: bold;
}}
QPushButton#decBtn:hover {{ background-color: #94e2d5; }}
QPushButton#bfBtn {{
    background-color: {ORANGE}; color: {DARKER}; border: none;
    border-radius: 8px; padding: 10px; font-size: 13px; font-weight: bold;
}}
QPushButton#bfBtn:hover {{ background-color: #f9e2af; }}
QPushButton#clearBtn {{
    background-color: {BORDER}; color: {TEXT}; border: none;
    border-radius: 8px; padding: 10px; font-size: 13px;
}}
QPushButton#clearBtn:hover {{ background-color: #585b70; }}
QPushButton#copyBtn {{
    background-color: {CARD}; color: {MUTED}; border: 1px solid {BORDER};
    border-radius: 6px; padding: 4px 10px; font-size: 11px;
}}
QPushButton#copyBtn:hover {{ color: {TEXT}; }}
QScrollArea {{ border: none; background: transparent; }}
QLabel#title {{ font-size: 20px; font-weight: bold; color: {TEXT}; }}
QLabel#sublabel {{ font-size: 11px; color: {MUTED}; }}
QLabel#sectionLabel {{ font-size: 11px; font-weight: bold; color: {BLUE}; }}
QLabel#tag {{
    background: {CARD}; color: {MUTED}; border-radius: 4px;
    padding: 2px 8px; font-size: 11px;
}}
"""


# ── Output Box helper ─────────────────────────────────────────

def make_output_box(color: str) -> QTextEdit:
    box = QTextEdit()
    box.setReadOnly(True)
    box.setFixedHeight(75)
    box.setStyleSheet(f"""
        QTextEdit {{
            background-color: {DARKER};
            color: {color};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 8px 12px;
            font-family: 'Consolas', monospace;
            font-size: 13px;
        }}
    """)
    return box


# ── Caesar Tab ────────────────────────────────────────────────

class CaesarTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Input
        lbl = QLabel("Input Text"); lbl.setObjectName("sectionLabel")
        layout.addWidget(lbl)
        self.input = QTextEdit()
        self.input.setPlaceholderText("Enter your message...")
        self.input.setFixedHeight(80)
        layout.addWidget(self.input)

        # Shift row
        row = QHBoxLayout()
        sl = QLabel("Shift Key (1–25):"); sl.setObjectName("sectionLabel"); sl.setFixedWidth(130)
        self.shift = QSpinBox(); self.shift.setRange(1, 25); self.shift.setValue(3); self.shift.setFixedWidth(75)
        formula = QLabel("  E(x) = (x + n) % 26"); formula.setObjectName("tag")
        row.addWidget(sl); row.addWidget(self.shift); row.addWidget(formula); row.addStretch()
        layout.addLayout(row)

        # Buttons
        btns = QHBoxLayout(); btns.setSpacing(10)
        enc = QPushButton("🔒  Encrypt"); enc.setObjectName("encBtn"); enc.setCursor(Qt.PointingHandCursor); enc.clicked.connect(self._encrypt)
        dec = QPushButton("🔓  Decrypt"); dec.setObjectName("decBtn"); dec.setCursor(Qt.PointingHandCursor); dec.clicked.connect(self._decrypt)
        clr = QPushButton("✕  Clear");   clr.setObjectName("clearBtn"); clr.setCursor(Qt.PointingHandCursor); clr.clicked.connect(self._clear)
        btns.addWidget(enc); btns.addWidget(dec); btns.addWidget(clr)
        layout.addLayout(btns)

        line = QFrame(); line.setFrameShape(QFrame.HLine); line.setStyleSheet(f"color:{BORDER};")
        layout.addWidget(line)

        # Outputs
        el = QLabel("Encrypted"); el.setObjectName("sectionLabel"); layout.addWidget(el)
        self.enc_out = make_output_box(ORANGE); layout.addWidget(self.enc_out)
        dl = QLabel("Decrypted"); dl.setObjectName("sectionLabel"); layout.addWidget(dl)
        self.dec_out = make_output_box(GREEN); layout.addWidget(self.dec_out)

        self.info = QLabel(""); self.info.setStyleSheet(f"color:{MUTED}; font-size:11px;")
        self.info.setAlignment(Qt.AlignCenter); layout.addWidget(self.info)
        layout.addStretch()

    def _encrypt(self):
        text = self.input.toPlainText(); shift = self.shift.value()
        if not text.strip(): self.info.setText("⚠ Enter some text first."); return
        enc = caesar_encrypt(text, shift); dec = caesar_decrypt(enc, shift)
        self.enc_out.setPlainText(enc); self.dec_out.setPlainText(dec)
        self.info.setText(f"Shift: {shift}  |  '{text[:20]}...' → '{enc[:20]}...'")

    def _decrypt(self):
        text = self.input.toPlainText(); shift = self.shift.value()
        if not text.strip(): self.info.setText("⚠ Enter some text first."); return
        dec = caesar_decrypt(text, shift)
        self.enc_out.setPlainText(text); self.dec_out.setPlainText(dec)
        self.info.setText(f"Treating input as ciphertext. Shift: {shift}")

    def _clear(self):
        self.input.clear(); self.enc_out.clear(); self.dec_out.clear(); self.info.setText("")


# ── Vigenère Tab ─────────────────────────────────────────────

class VigenereTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        lbl = QLabel("Input Text"); lbl.setObjectName("sectionLabel"); layout.addWidget(lbl)
        self.input = QTextEdit(); self.input.setPlaceholderText("Enter your message..."); self.input.setFixedHeight(80)
        layout.addWidget(self.input)

        row = QHBoxLayout()
        kl = QLabel("Keyword:"); kl.setObjectName("sectionLabel"); kl.setFixedWidth(70)
        self.key = QLineEdit(); self.key.setPlaceholderText("e.g. SECRET"); self.key.setFixedWidth(160)
        tag = QLabel("  Uses repeating keyword instead of fixed shift"); tag.setObjectName("tag")
        row.addWidget(kl); row.addWidget(self.key); row.addWidget(tag); row.addStretch()
        layout.addLayout(row)

        btns = QHBoxLayout(); btns.setSpacing(10)
        enc = QPushButton("🔒  Encrypt"); enc.setObjectName("encBtn"); enc.setCursor(Qt.PointingHandCursor); enc.clicked.connect(self._encrypt)
        dec = QPushButton("🔓  Decrypt"); dec.setObjectName("decBtn"); dec.setCursor(Qt.PointingHandCursor); dec.clicked.connect(self._decrypt)
        clr = QPushButton("✕  Clear");   clr.setObjectName("clearBtn"); clr.setCursor(Qt.PointingHandCursor); clr.clicked.connect(self._clear)
        btns.addWidget(enc); btns.addWidget(dec); btns.addWidget(clr)
        layout.addLayout(btns)

        line = QFrame(); line.setFrameShape(QFrame.HLine); line.setStyleSheet(f"color:{BORDER};")
        layout.addWidget(line)

        el = QLabel("Encrypted"); el.setObjectName("sectionLabel"); layout.addWidget(el)
        self.enc_out = make_output_box(PURPLE); layout.addWidget(self.enc_out)
        dl = QLabel("Decrypted"); dl.setObjectName("sectionLabel"); layout.addWidget(dl)
        self.dec_out = make_output_box(GREEN); layout.addWidget(self.dec_out)

        self.info = QLabel(""); self.info.setStyleSheet(f"color:{MUTED}; font-size:11px;")
        self.info.setAlignment(Qt.AlignCenter); layout.addWidget(self.info)
        layout.addStretch()

    def _encrypt(self):
        text = self.input.toPlainText(); key = self.key.text().strip()
        if not text.strip(): self.info.setText("⚠ Enter some text first."); return
        if not key or not key.isalpha(): self.info.setText("⚠ Keyword must be letters only."); return
        enc = vigenere_encrypt(text, key); dec = vigenere_decrypt(enc, key)
        self.enc_out.setPlainText(enc); self.dec_out.setPlainText(dec)
        self.info.setText(f"Keyword: '{key.upper()}'  |  Encrypted successfully")

    def _decrypt(self):
        text = self.input.toPlainText(); key = self.key.text().strip()
        if not text.strip(): self.info.setText("⚠ Enter some text first."); return
        if not key or not key.isalpha(): self.info.setText("⚠ Keyword must be letters only."); return
        dec = vigenere_decrypt(text, key)
        self.enc_out.setPlainText(text); self.dec_out.setPlainText(dec)
        self.info.setText(f"Treating input as ciphertext. Keyword: '{key.upper()}'")

    def _clear(self):
        self.input.clear(); self.key.clear(); self.enc_out.clear(); self.dec_out.clear(); self.info.setText("")


# ── Brute Force Tab ──────────────────────────────────────────

class BruteForceTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        lbl = QLabel("Ciphertext to Crack"); lbl.setObjectName("sectionLabel"); layout.addWidget(lbl)
        self.input = QTextEdit(); self.input.setPlaceholderText("Paste encrypted text here..."); self.input.setFixedHeight(70)
        layout.addWidget(self.input)

        note = QLabel("⚠  Caesar cipher only has 25 possible keys — all attempts shown below")
        note.setStyleSheet(f"color:{ORANGE}; font-size:11px;")
        layout.addWidget(note)

        btn = QPushButton("💥  Run Brute Force"); btn.setObjectName("bfBtn")
        btn.setCursor(Qt.PointingHandCursor); btn.clicked.connect(self._run)
        btn.setFixedHeight(40); layout.addWidget(btn)

        line = QFrame(); line.setFrameShape(QFrame.HLine); line.setStyleSheet(f"color:{BORDER};")
        layout.addWidget(line)

        rl = QLabel("All 25 Possible Decryptions"); rl.setObjectName("sectionLabel"); layout.addWidget(rl)

        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; }}")
        container = QWidget(); container.setStyleSheet(f"background:{DARKER}; border-radius:8px;")
        self.grid = QVBoxLayout(container)
        self.grid.setContentsMargins(12, 12, 12, 12); self.grid.setSpacing(4)
        scroll.setWidget(container); layout.addWidget(scroll)

    def _run(self):
        text = self.input.toPlainText()
        if not text.strip(): return

        # clear
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        results = brute_force(text)
        for shift, decrypted in results:
            row = QHBoxLayout()
            tag = QLabel(f"Shift {shift:02d}")
            tag.setFixedWidth(58)
            tag.setStyleSheet(f"color:{BLUE}; font-size:11px; font-family:Consolas;")
            sep = QLabel("│"); sep.setStyleSheet(f"color:{BORDER};"); sep.setFixedWidth(12)
            val = QLabel(decrypted[:80])
            val.setStyleSheet(f"color:{TEXT}; font-size:12px; font-family:Consolas;")
            val.setTextInteractionFlags(Qt.TextSelectableByMouse)
            row.addWidget(tag); row.addWidget(sep); row.addWidget(val); row.addStretch()
            w = QWidget(); w.setLayout(row)
            self.grid.addWidget(w)

        self.grid.addStretch()


# ── Frequency Analysis Tab ────────────────────────────────────

class FreqTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        lbl = QLabel("Text to Analyze"); lbl.setObjectName("sectionLabel"); layout.addWidget(lbl)
        self.input = QTextEdit(); self.input.setPlaceholderText("Paste any text (plaintext or ciphertext)...")
        self.input.setFixedHeight(70); layout.addWidget(self.input)

        btn = QPushButton("📊  Analyze Frequency"); btn.setObjectName("encBtn")
        btn.setCursor(Qt.PointingHandCursor); btn.clicked.connect(self._analyze)
        btn.setFixedHeight(40); layout.addWidget(btn)

        note = QLabel("Identical frequency shapes between plaintext and ciphertext expose the Caesar cipher to frequency analysis attacks.")
        note.setStyleSheet(f"color:{MUTED}; font-size:11px;")
        note.setWordWrap(True); layout.addWidget(note)

        # Chart
        self.fig, self.ax = plt.subplots(figsize=(7, 3))
        self.fig.patch.set_facecolor(DARKER)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setStyleSheet(f"background:{DARKER}; border-radius:8px;")
        layout.addWidget(self.canvas)

    def _analyze(self):
        text = self.input.toPlainText()
        if not text.strip(): return
        freq = get_letter_freq(text)

        self.ax.clear()
        self.ax.set_facecolor(DARKER)
        letters = list(freq.keys())
        values  = list(freq.values())
        colors  = [BLUE if v == max(values) else CARD for v in values]

        bars = self.ax.bar(letters, values, color=colors, edgecolor=BORDER, linewidth=0.5)
        self.ax.set_xlabel("Letter", color=MUTED, fontsize=9)
        self.ax.set_ylabel("Frequency (%)", color=MUTED, fontsize=9)
        self.ax.set_title("Letter Frequency Analysis", color=TEXT, fontsize=11, pad=10)
        self.ax.tick_params(colors=MUTED, labelsize=8)
        for spine in self.ax.spines.values():
            spine.set_edgecolor(BORDER)
        self.ax.set_ylim(0, max(values) * 1.2 if max(values) > 0 else 10)

        # highlight max
        max_letter = letters[values.index(max(values))]
        self.ax.set_title(
            f"Letter Frequency Analysis  |  Most common: '{max_letter}' ({max(values):.1f}%)",
            color=TEXT, fontsize=10, pad=10
        )

        self.fig.tight_layout()
        self.canvas.draw()


# ── Main Window ───────────────────────────────────────────────

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cipher Tool — DecodeLabs Project 2")
        self.setMinimumSize(600, 680)
        self.setStyleSheet(STYLE)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        # Header
        title = QLabel("🔐 Encryption & Decryption Tool")
        title.setObjectName("title"); root.addWidget(title)
        sub = QLabel("DecodeLabs Industrial Training Kit — Project 2  |  Caesar · Vigenère · Brute Force · Frequency Analysis")
        sub.setObjectName("sublabel"); root.addWidget(sub)

        line = QFrame(); line.setFrameShape(QFrame.HLine); line.setStyleSheet(f"color:{BORDER};")
        root.addWidget(line)

        # Tabs
        tabs = QTabWidget()
        tabs.addTab(CaesarTab(),     "🔒  Caesar Cipher")
        tabs.addTab(VigenereTab(),   "🗝  Vigenère Cipher")
        tabs.addTab(BruteForceTab(), "💥  Brute Force")
        tabs.addTab(FreqTab(),       "📊  Frequency Analysis")
        root.addWidget(tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())