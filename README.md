# Character Prompt Generator

A local-first tool for creating and managing realistic, "living" video game characters with detailed system prompts. Designed for offline use and integration with other programs such as LLM Studio.

---

## **Features**

### Character Generation
- Generates characters with:
  - Name (gender-specific)
  - Age
  - Backstory
  - Traits (positive/negative, weighted)
  - Goals
  - Needs
  - Emotions
- Respects mutually exclusive traits (e.g., "brave" vs "shy").

### Character Manager
- View all generated characters in a scrollable list
- Add or delete characters
- Multi-purpose clipboard copy for all character prompts

### Prompt Viewer
- Editable system prompt text for each character
- Changes detected automatically
- Save updates directly to the character manager
- Updates reflected in the list and visualization

### Mind Map Visualization
- Dynamic, embedded Plotly visualization of each character’s "mind":
  - Backstory → Traits → Goals → Emotions → Needs
- Updates automatically with prompt changes
- Fully embedded within the GUI, no external browser needed

### Tools Panel
- Buttons for:
  - Generate Character
  - Copy All Prompts
  - Delete Selected
  - Save Prompt
- Modern, clean layout
- Save button disabled until changes are made

---

## **Tech Stack**
- Python 3.10+
- PySide6 for GUI and embedded web views
- Plotly for interactive visualization
- JSON for persistent storage
- Fully modular, easy to extend

---

## **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/OurShamanJax/character-prompt-generator.git


  Launch CMD, cd to Character Generator\CharacterGenerator, then run "python main.py"
