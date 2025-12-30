import sys
import re
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
                               QTextEdit, QPushButton, QLabel, QMessageBox)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt
import plotly.graph_objects as go
import tempfile
import os

from character import Character
from manager import CharacterManager

class CharacterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Character Prompt Generator")
        self.resize(1200, 600)

        self.manager = CharacterManager()
        self.current_character_index = None

        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)

        # -------- Left panel --------
        left_panel = QVBoxLayout()
        main_layout.addLayout(left_panel, 2)

        # Characters Header
        char_header = QLabel("Characters")
        char_header.setAlignment(Qt.AlignCenter)
        left_panel.addWidget(char_header)

        # Character list
        self.listbox = QListWidget()
        self.listbox.currentRowChanged.connect(self.view_prompt)
        left_panel.addWidget(self.listbox)

        # Prompt Viewer Header
        prompt_header = QLabel("Prompt Viewer")
        prompt_header.setAlignment(Qt.AlignCenter)
        left_panel.addWidget(prompt_header)

        # Editable prompt text
        self.prompt_text = QTextEdit()
        self.prompt_text.textChanged.connect(self.on_prompt_modified)
        left_panel.addWidget(self.prompt_text)

        # -------- Right panel --------
        right_panel = QVBoxLayout()
        main_layout.addLayout(right_panel, 3)

        # Tools Header
        tools_header = QLabel("Tools")
        tools_header.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(tools_header)

        # Buttons
        self.btn_generate = QPushButton("Generate Character")
        self.btn_generate.clicked.connect(self.generate_character)
        right_panel.addWidget(self.btn_generate)

        self.btn_copy_all = QPushButton("Copy All Prompts")
        self.btn_copy_all.clicked.connect(self.copy_all_prompts)
        right_panel.addWidget(self.btn_copy_all)

        self.btn_delete = QPushButton("Delete Selected")
        self.btn_delete.clicked.connect(self.delete_selected)
        right_panel.addWidget(self.btn_delete)

        self.btn_save = QPushButton("Save Prompt")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self.save_prompt)
        right_panel.addWidget(self.btn_save)

        # Visualization Header
        visual_header = QLabel("Mind Map")
        visual_header.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(visual_header)

        # Embedded Plotly WebEngine
        self.web_view = QWebEngineView()
        right_panel.addWidget(self.web_view, 1)

    # ---------------- Character Management ----------------
    def refresh_list(self):
        self.listbox.clear()
        for c in self.manager.characters:
            self.listbox.addItem(f"{c.name} ({c.gender})")

    def generate_character(self):
        char = Character()
        self.manager.add_character(char)
        self.refresh_list()

    def view_prompt(self, index):
        if index < 0 or index >= len(self.manager.characters):
            self.prompt_text.setPlainText("Select a character to view its prompt.")
            self.web_view.setHtml("<h3>Select a character to visualize</h3>")
            return

        self.current_character_index = index
        char = self.manager.characters[index]
        self.prompt_text.setPlainText(char.format_prompt())
        self.btn_save.setEnabled(False)
        self.update_visualization(char)

    def on_prompt_modified(self):
        self.btn_save.setEnabled(True)

    def save_prompt(self):
        if self.current_character_index is None:
            return

        char = self.manager.characters[self.current_character_index]
        updated_text = self.prompt_text.toPlainText().strip()
        lines = updated_text.splitlines()

        for line in lines:
            line = line.strip()
            if line.startswith("You are"):
                match = re.match(r"You are (\w+), a (\d+)-year-old (\w+)\.", line)
                if match:
                    char.name = match.group(1)
                    char.age = int(match.group(2))
                    char.gender = match.group(3)
            elif line.startswith("Personality traits:"):
                traits_str = line.replace("Personality traits:", "").strip()
                char.traits = [t.strip() for t in traits_str.split(",") if t.strip()]
            elif line.startswith("Backstory:"):
                char.backstory = line.replace("Backstory:", "").strip()
            elif line.startswith("Goals:"):
                char.goals = line.replace("Goals:", "").strip()
            elif line.startswith("Current feelings:"):
                char.emotions = line.replace("Current feelings:", "").strip()
            elif line.startswith("Needs:"):
                char.needs = line.replace("Needs:", "").strip()

        self.manager.save()
        self.refresh_list()
        self.btn_save.setEnabled(False)
        self.update_visualization(char)

    def delete_selected(self):
        index = self.listbox.currentRow()
        if index < 0:
            return
        char = self.manager.characters[index]
        self.manager.remove_character(char.id)
        self.refresh_list()
        self.prompt_text.clear()
        self.web_view.setHtml("<h3>Select a character to visualize</h3>")
        self.btn_save.setEnabled(False)

    def copy_all_prompts(self):
        prompts = self.manager.get_all_prompts()
        QApplication.clipboard().setText(prompts)
        QMessageBox.information(self, "Copied", "All prompts copied to clipboard!")

    # ---------------- Visualization ----------------
    def update_visualization(self, char):
        fig = go.Figure()

        nodes = ["Backstory", "Traits", "Goals", "Emotions", "Needs"]
        values = [char.backstory, ", ".join(char.traits), char.goals, char.emotions, char.needs]

        for i, (n, v) in enumerate(zip(nodes, values)):
            fig.add_trace(go.Scatter(
                x=[i*2], y=[0],
                text=[f"<b>{n}</b><br>{v}"],
                mode="markers+text",
                marker=dict(size=60, color=i*40+50, colorscale="Viridis"),
                textposition="bottom center"
            ))

        fig.update_layout(showlegend=False, margin=dict(l=10,r=10,t=10,b=10))

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        fig.write_html(tmp_file.name)
        self.web_view.load(f"file:///{tmp_file.name.replace(os.sep, '/')}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CharacterApp()
    window.show()
    sys.exit(app.exec())
