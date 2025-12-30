import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
from character import Character
from manager import CharacterManager
from lm_studio_client import LMStudioClient


class CharacterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Prompt Generator")
        self.root.geometry("1000x600")

        self.manager = CharacterManager()
        self.lm_client = LMStudioClient()

        self.smart_mode = tk.BooleanVar(value=False)
        self.selected_model = tk.StringVar()
        self.current_index = None

        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        # Frames
        self.frame_left = ttk.Frame(self.root, padding=10)
        self.frame_left.pack(side="left", fill="both", expand=True)
        self.frame_right = ttk.Frame(self.root, padding=10)
        self.frame_right.pack(side="right", fill="y")

        # Character Manager
        ttk.Label(self.frame_left, text="Characters").pack()
        self.listbox = tk.Listbox(self.frame_left, selectmode="extended")
        self.listbox.pack(fill="x")
        self.listbox.bind("<<ListboxSelect>>", self.show_prompt)

        # Prompt Viewer
        ttk.Label(self.frame_left, text="Prompt Viewer").pack(pady=(10, 0))
        self.prompt_text = tk.Text(self.frame_left, wrap="word", height=15)
        self.prompt_text.pack(fill="both", expand=True)
        self.prompt_text.bind("<<Modified>>", self.on_prompt_modified)

        # Tools
        ttk.Label(self.frame_right, text="Tools").pack(pady=(0, 5))

        ttk.Checkbutton(
            self.frame_right,
            text="Smart Mode (LM Studio)",
            variable=self.smart_mode,
            command=self.toggle_mode
        ).pack(fill="x", pady=5)

        self.model_combo = ttk.Combobox(
            self.frame_right,
            textvariable=self.selected_model,
            state="disabled"
        )
        self.model_combo.pack(fill="x")

        ttk.Button(
            self.frame_right,
            text="Generate Character",
            command=self.generate_character
        ).pack(fill="x", pady=10)

        ttk.Button(
            self.frame_right,
            text="Copy All Prompts",
            command=self.copy_all
        ).pack(fill="x", pady=5)

        ttk.Button(
            self.frame_right,
            text="Delete Selected",
            command=self.delete_selected
        ).pack(fill="x", pady=5)

        self.save_button = ttk.Button(
            self.frame_right,
            text="Save Prompt",
            command=self.save_prompt,
            state="disabled"
        )
        self.save_button.pack(fill="x", pady=(20, 5))

    # --- Event Handlers ---
    def toggle_mode(self):
        if self.smart_mode.get():
            models = self.lm_client.list_models()
            print(f"[DEBUG] /models response: {models}")
            if not models:
                messagebox.showerror("LM Studio", "No models found.")
                self.smart_mode.set(False)
                return
            self.model_combo["values"] = models
            self.selected_model.set(models[0])
            self.model_combo.config(state="readonly")
        else:
            self.model_combo.config(state="disabled")

    def on_prompt_modified(self, event):
        if self.prompt_text.edit_modified():
            self.save_button.config(state="normal")
        self.prompt_text.edit_modified(False)

    # --- Character Operations ---
    def generate_character(self):
        if self.smart_mode.get():
            self.generate_smart()
        else:
            self.generate_dumb()

    def generate_dumb(self):
        char = Character()
        self.manager.add_character(char)
        self.refresh_list()

    def generate_smart(self):
        try:
            with open("system_prompt.txt", encoding="utf-8") as f:
                system_prompt = f.read()

            char_data = self.lm_client.generate_character(
                self.selected_model.get(),
                system_prompt
            )
            print(f"[DEBUG] /chat/completions response: {char_data}")

            if not char_data:
                messagebox.showerror("Generation Failed", "No data returned from LM Studio")
                return

            char = Character.from_dict(char_data)
            self.manager.add_character(char)
            self.refresh_list()
            self.show_prompt_for_character(char)

        except Exception as e:
            messagebox.showerror("Generation Failed", str(e))
            print(f"[ERROR] Smart generation failed: {e}")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for c in self.manager.characters:
            self.listbox.insert(tk.END, f"{c.name} ({c.gender})")

    def show_prompt(self, _event=None):
        try:
            idx = self.listbox.curselection()
            if not idx:
                return
            self.current_index = idx[0]
            char = self.manager.characters[self.current_index]
            self.show_prompt_for_character(char)
        except IndexError:
            pass

    def show_prompt_for_character(self, char):
        self.prompt_text.config(state="normal")
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert(tk.END, char.format_prompt())
        self.prompt_text.edit_modified(False)
        self.save_button.config(state="disabled")

    def save_prompt(self):
        if self.current_index is None:
            return
        char = self.manager.characters[self.current_index]
        updated_text = self.prompt_text.get("1.0", tk.END)

        try:
            # Parse text lines
            for line in updated_text.splitlines():
                line = line.strip()
                if line.startswith("You are"):
                    match = re.match(r"You are (\w+(?: \w+)?), a (\d+)-year-old (\w+)\.", line)
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
            self.save_button.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Save Failed", str(e))
            print(f"[ERROR] Save failed: {e}")

    def delete_selected(self):
        selected = self.listbox.curselection()
        if not selected:
            return
        try:
            for idx in reversed(selected):
                char = self.manager.characters[idx]
                self.manager.remove_character(char.id)
            self.refresh_list()
            self.prompt_text.config(state="normal")
            self.prompt_text.delete("1.0", tk.END)
            self.save_button.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Deletion Failed", str(e))
            print(f"[ERROR] Deletion failed: {e}")

    def copy_all(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.manager.get_all_prompts())
        messagebox.showinfo("Copied", "All prompts copied.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterApp(root)
    root.mainloop()
