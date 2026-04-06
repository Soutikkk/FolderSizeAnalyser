# Folder Size Analyzer PRO

A premium, modern, web-based tool for analyzing local directory sizes quickly and visually.

## Features
- **Deep Scanning:** Recursively calculates the exact space your folders take up.
- **Top 10 Largest Files Tab:** Identifies space hogs anywhere in the deep directory tree.
- **Extension Chart:** Visualizes with a modern doughnut chart which file types consume the most space.
- **Beautiful UI:** Developed with modern dark aesthetics, dynamic glassmorphism, and real-time processing indicators.

## Running Locally

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and go to `http://127.0.0.1:5000`
5. Type any absolute directory path into the text field (e.g. `C:\Users\USER\Desktop`) and hit **Analyze**.

*Note: Access to system-restricted directories or heavily protected files might bypass files you cannot read. The UI will alert you if the top folder cannot be accessed. For scanning full drives like `C:\`, try running your command prompt terminal as Administrator.*
