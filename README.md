# 📂 Folder Size Analyzer PRO

A modern, web-based folder analysis tool built with **Python** and **Flask** that helps you visualize disk usage, identify large files, and understand storage distribution through an elegant and responsive interface.

---

## ✨ Features

- 📁 **Deep Folder Scanning**
  - Recursively scans directories and calculates their total size.

- 📊 **File Type Distribution**
  - Displays storage usage by file extension using a beautiful doughnut chart.

- 📄 **Top 10 Largest Files**
  - Quickly identify the largest files occupying your storage.

- 📂 **Folder Size Breakdown**
  - View the size of immediate files and subfolders in descending order.

- ⚡ **Fast & Efficient**
  - Optimized recursive scanning with graceful handling of inaccessible files.

- 🛡 **Permission Error Handling**
  - Automatically skips restricted files and folders without crashing.

- 🎨 **Modern User Interface**
  - Dark theme with glassmorphism design, responsive layout, and loading animations.

---

## 🛠 Tech Stack

- **Backend**
  - Python 3
  - Flask

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript

- **Visualization**
  - Chart.js

---

## 📁 Project Structure

```
Folder-Size-Analyzer-PRO/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── screenshots/
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Folder-Size-Analyzer-PRO.git
```

### 2. Navigate to the project folder

```bash
cd Folder-Size-Analyzer-PRO
```

### 3. Create a virtual environment (Optional)

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

### 6. Open your browser

Visit:

```
http://127.0.0.1:5000
```

---

## 📷 Screenshots

Add screenshots of the application inside the **screenshots/** folder.

Example:

```
screenshots/
├── home.png
├── analysis.png
├── chart.png
└── largest-files.png
```

---

## 📈 What the Application Shows

- Total folder size
- Storage used by each file extension
- Top 10 largest files
- Size of each immediate child folder/file
- Interactive charts and visualizations

---

## 💡 Learning Objectives

This project helped me practice:

- Flask Web Development
- Python File System Operations
- Recursive Directory Traversal
- JSON APIs
- Error Handling
- Data Visualization
- Responsive Frontend Design

---

## 📦 Requirements

```
Flask
```

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Soutik Mandal**

AIML Student | Python Developer | Open Source Enthusiast

GitHub: https://github.com/<your-username>

---

⭐ If you found this project useful, consider giving it a **Star** on GitHub! to `http://127.0.0.1:5000`
5. Type any absolute directory path into the text field (e.g. `C:\Users\USER\Desktop`) and hit **Analyze**.

*Note: Access to system-restricted directories or heavily protected files might bypass files you cannot read. The UI will alert you if the top folder cannot be accessed. For scanning full drives like `C:\`, try running your command prompt terminal as Administrator.*
