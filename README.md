# ⌨️ Virtual Keyboard with MediaPipe

This project implements a **real-time virtual keyboard** using **MediaPipe Hand Tracking** and OpenCV.  
It detects hand gestures to simulate key presses on a virtual keyboard and sends them to your system in real time.

---

## 🚀 Features
- Real-time hand tracking with MediaPipe.
- Virtual keyboard UI rendered directly on webcam feed.
- Hover detection for highlighting keys.
- Pinch gesture to simulate key press.
- Keyboard input sent to the system via `pyautogui`.

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/faisal-ajao/virtual-keyboard-mediapipe.git
cd virtual-keyboard-mediapipe

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\\Scripts\\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the main script:
```bash
python main.py
```

### Controls
- **ESC** → Exit program  
- Hover over a button to highlight it.  
- Pinch (index & middle finger tips close) → Press selected key.  

---

## 📊 Output Example (Video)  
[![Watch the output](https://img.youtube.com/vi/klg4ghm8R7g/hqdefault.jpg)](https://youtu.be/klg4ghm8R7g?feature=shared)

---

## 📂 Project Structure
```
virtual-keyboard-mediapipe/
├── HandTrackingModule.py   # Custom wrapper around MediaPipe Hands
├── utils.py                # Utility functions (e.g., corner rectangle)
├── main.py                 # Main application script
├── README.md
└── requirements.txt
```

---

## 🧠 Tech Stack
- Python 3.11.5
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

---

## 📜 License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
