Character Prompt Generator

A local-first, offline tool for generating and managing realistic, dynamic video game characters with richly detailed system prompts. Designed for integration with tools like LM Studio or as a standalone creative assistant. Characters have living qualities: traits, backstory, goals, needs, and emotions that influence each other.

Demo Overview

The application allows you to:

Generate characters automatically in “Dumb Mode” (randomized) or “Smart Mode” (using an LLM via LM Studio).

Edit and save system prompts for each character.

Manage characters with multi-selection for deletion or copying.

Visualize each character’s “mind” with an embedded, dynamic mind map showing how backstory influences traits, goals, emotions, and needs.

Features
Character Generation

Smart Mode: Uses an LLM (GLM-4.6v-flash or other models in LM Studio) to generate coherent, complete characters.

Dumb Mode: Quickly generates characters with randomized names, traits, and backstories.

Generates fields for:

Name (gender-specific)

Age

Gender

Traits (weighted, positive/negative, mutually exclusive)

Backstory

Goals

Needs

Emotions

Character Manager

View all generated characters in a scrollable list.

Multi-select support for batch deletion or copying.

Real-time updates when prompts are edited or saved.

Prompt Viewer

Edit system prompts for each character.

Save changes to the character manager directly.

Changes highlight until saved.

Supports undo/redo for prompt edits.

Mind Map Visualization

Embedded Plotly mind map showing relationships between backstory, traits, goals, needs, and emotions.

Updates dynamically when the system prompt changes.

Fully integrated into the GUI—no external browser required.

Color-coded sections for clarity.

Tools Panel

Generate Character (Dumb or Smart Mode)

Copy All Prompts

Delete Selected

Save Prompt

Model selection dropdown for Smart Mode (automatically detects LM Studio models)

Debugging messages print to terminal for LLM issues

Tech Stack

Python 3.10+

Tkinter for GUI

Plotly for dynamic visualization

Requests for communicating with LM Studio

JSON for persistent character storage

Modular design for easy integration with other programs

Installation & Setup

Clone the repository:

git clone https://github.com/OurShamanJax/character-prompt-generator.git


Navigate to the project directory:

cd CharacterGenerator


Install dependencies:

pip install -r requirements.txt


requirements.txt contents:

plotly
requests
tkwebview2


Optional: If using Smart Mode with LM Studio, ensure LM Studio is installed and running.

Launch the application:

python main.py


In Smart Mode, select your LM Studio model from the dropdown to generate characters with the LLM.

Usage Tips

Multi-select characters in the list to delete or copy them in batches.

Save prompt edits frequently; unsaved changes are highlighted.

Mind map colors correspond to:

Backstory → Traits → Goals → Needs → Emotions

Check the terminal for debug messages if Smart Mode fails to generate characters.

License

Open source and fully editable for integration into your own projects.
