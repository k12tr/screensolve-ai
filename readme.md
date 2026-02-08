# ScreenSolve AI 👁️🤖

> **Your screen blinks.** 
> **The AI understands.** 
> **The test loses.**


**ScreenSolve AI** is a specialized Python-based agent designed to bridge the gap between complex online assessments and AI reasoning. It monitors your screen in real-time, detects content changes using Computer Vision, and delivers expert-level solutions to a **private local web server** accessible from any device (like your smartphone).

---

## 🧠 Key Features

* **⚡ Smart Delta Detection:** Uses pixel-level hashing and comparison to trigger the AI only when the screen content changes by more than 5%. This saves your API quota and prevents redundant requests.
* **📱 Stealth Mobile UI:** Answers are served on a clean, dark-mode web dashboard at `localhost:5005`.  
  Designed to keep your main screen clean and free from browser-based monitoring tools.
* **📊 Automatic Archiving:** 
    * **Image Logs:** Every detected question is saved in the `/question_records` folder.
    * **Data Logs:** All solutions are recorded in `question_answer_log.csv` with timestamps for later review.
* **🤖 Multi-Modal Intelligence:** Powered by **Gemini**, providing high-speed reasoning for math, coding, and logical questions.
* **🛡️ Zero Footprint:** No browser extensions, no JS injection, and no DOM manipulation. It watches your screen just like a human eye.

---

## 🛠️ How It Works

1. **Observation:** The script captures high-resolution screenshots of your primary monitor.
2. **Comparison:** It compares the current frame with the previous one. If a significant change (new question) is detected, it proceeds.
3. **Analysis:** The frame is sent to the Gemini AI API with a specialized "Assessment Expert" prompt.
4. **Broadcast:** The solution is instantly pushed to the Flask-based web interface and logged into the CSV file.

---

## 🚀 Installation

### 1. Prerequisites

* Python 3.9+
* A Gemini API Key (Get it from Google AI Studio)

### 2. Setup

```bash
# Clone the repository
git clone https://github.com/k12tr/screensolve-ai.git
cd screensolve-ai

# Install dependencies
pip install -r requirements.txt

```

### 3. Configuration

Open `main.py` and insert your API key:

```python
GEMINI_API_KEY = "your_api_key_here"

```

### 4. Run

```bash
python main.py

```

---

## 📱 Mobile Companion Access

1. Ensure your phone and PC are on the same Wi-Fi network.
2. Find your Local IP (e.g., `192.168.1.XX`).
3. Navigate to `http://192.168.1.XX:5005` on your phone's browser.
4. Sit back and watch the answers roll in as you navigate through your test.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Vision:** PyAutoGUI & Pillow (PIL)
* **Brain:** Google Gen AI 
* **Server:** Flask
* **Storage:** CSV & Local Filesystem

---

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**. The developer is not responsible for any misuse, academic integrity violations, or account bans. Use it to understand how AI interprets visual data, not to bypass legitimate testing protocols.

---

**Developed with ⚡ and Python.** *If this project helped you, don't forget to give it a ⭐!*