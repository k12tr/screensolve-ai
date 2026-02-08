import os
import time
import pyautogui
from google.genai import types
import numpy as np
from PIL import Image, ImageChops, ImageFilter
from google import genai
from flask import Flask, render_template_string
from threading import Thread
import shutil
import traceback
from datetime import datetime # Added for timestamp
import csv

# --- SETTINGS ---
GEMINI_API_KEY = "YOUR_API_KEY"
client = genai.Client(api_key=GEMINI_API_KEY)
LOG_FILE = "question_answer_log.csv"
SAVE_DIR = "question_records"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

last_answer = "The system is ready. Change is expected..."
app = Flask(__name__)

base_path = os.path.dirname(os.path.abspath(__file__))
new_img = os.path.join(base_path, "new_screen.png")
old_img = os.path.join(base_path, "old_screen.png")

def save_results(time, question_file, answer):
    # Save to CSV File (can be opened with Excel)
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Time', 'Filename', 'Answer'])
        writer.writerow([time, question_file, answer])

def now_time():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def screen_is_changed(img_new, img_old, threshold_percentage=5.0):
    if not os.path.exists(img_old):
        return True
    
    # Comparison optimization
    i1 = Image.open(img_new).convert('L').resize((300, 300))
    i2 = Image.open(img_old).convert('L').resize((300, 300))
    
    fark = ImageChops.difference(i1, i2)
    change = (np.count_nonzero(fark) / (300 * 300)) * 100
    return change > threshold_percentage

# --- WEB UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="20">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; padding: 30px; }
        .card { background: #1e293b; border-radius: 12px; padding: 25px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); border-left: 5px solid #38bdf8; }
        .status { font-size: 14px; color: #94a3b8; margin-bottom: 15px; font-weight: bold; border-bottom: 1px solid #334155; pb: 10px; }
        .content { font-size: 20px; color: #f1f5f9; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="card">
        <div class="status">{{ status_message }}</div>
        <div class="content">{{ answer }}</div>
    </div>
</body>
</html>
"""

status_log = "System started..."

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, status_message=status_log, answer=last_answer)

def assistant_loop():
    global last_answer, status_log
    
    if not os.path.exists(old_img):
        pic = pyautogui.screenshot(old_img)
        pic.save(old_img)

    while True:
        try:
            pic = pyautogui.screenshot(new_img)
            pic.save(new_img)
            time_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
            time_readable = now_time()

            if screen_is_changed(new_img, old_img):
                status_log = f"🔄 New content detected, prompting Gemini: {time_readable}"
                print(status_log)
                
                #1. Save screenshot permanently
                saved_image_name = f"question_{time_tag}.png"
                saved_image_path = os.path.join(SAVE_DIR, saved_image_name)
                shutil.copy2(new_img, saved_image_path)

                # Gemini Proccess
                with open(new_img, "rb") as f:
                    image_data = f.read()
                response = client.models.generate_content(
                    #model="gemini-2.0-flash",
                    model="gemini-flash-latest",
                    contents=[
                        types.Part.from_text(text="Solve this question, just write the answer and a brief reason."),
                        types.Part.from_bytes(data=image_data, mime_type="image/png")
                    ]
                )
                print(response.text)
                last_answer = response.text
                save_results(time_readable, saved_image_name, last_answer)
                shutil.copy2(new_img, old_img)
                status_log = f"✅ Answer saved: {time_readable}"
            else:
                status_log = f"😴 Screen fixed (No change): {time_readable}"
                print(status_log)

        except Exception as e:
            status_log = f"⚠️ ERROR: {str(e)} | {now_time()}"
            error_details = traceback.format_exc() # Tells the exact location of the error
            print(f"CRITICAL ERROR:\n{error_details}")
            status_log = f"⚠️ ERROR: {str(e)} | {now_time()}"
            
        time.sleep(20) # Check frequency

if __name__ == '__main__':
    # Start Thread to clear Flask logs
    t = Thread(target=assistant_loop)
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', port=5005, debug=False, use_reloader=False)