# 🎮 Bouncing Ball Game (Python + Pygame)

A fun and progressively challenging **Bouncing Ball Game** developed using **Python and Pygame**. The goal is simple: **guide the ball to the green goal while avoiding obstacles**, collecting power-ups, and surviving through increasing difficulty levels. This repository also represents my **learning journey**, from writing a simple Python game to handling real-world packaging and OS compatibility challenges.

---

## ✨ Features

- Smooth ball movement with keyboard & mouse control
- Progressive difficulty with increasing levels
- Obstacles and shrinking goals
- Power-ups:
  - ⚡ Speed Boost
  - ⏱️ Time Bonus
  - 🛡️ Shield Protection
- Particle effects & motion trail
- Sound effects (collision, goal, power-ups)
- High-score saving system
- Intro screen, pause mode, win & game-over screens

---

## 🗂️ Project Folder Structure
```text
Bouncing_Ball/
│
├── assets/                 # (Optional) assets folder
├── build/                  # PyInstaller build files
├── dist/                   # Executable (.exe) setup
│   └── BouncingBall.exe
│
├── BouncingBall.py         # Main game source code
├── BouncingBall.spec       # PyInstaller spec file
├── collision.wav           # Collision sound
├── goal.wav                # Goal sound
├── powerup.wav             # Power-up sound
├── highscore.txt           # Saved high score
└── README.md               # Project documentation
```

---

## 🚀 How to Run the Game

### ✅ Option 1: Run Using the Executable (Recommended)

If you face Python or library issues, use the pre-built executable:

1. Go to the `dist/` folder
2. Run:
```text
   BouncingBall.exe
```

✔ No Python installation required  
✔ Best option for Windows users

---

### 🐍 Option 2: Run Using Python Source Code

#### Prerequisites

- Python 3.8+
- Pygame library

#### Install Pygame
```bash
pip install pygame
```

#### Run the Game
```bash
python BouncingBall.py
```

⚠️ **Note:** If you encounter library or compatibility errors on Windows, use the EXE file instead.

---

## 🎮 Controls

| Action         | Control      |
|----------------|--------------|
| Move Ball      | Arrow Keys   |
| Aim & Launch   | Mouse Click  |
| Pause / Resume | P            |
| Restart        | ENTER        |

---

## 📖 Project Story & Learning Experience

This project is more than just a game. This article shares the full experience—from building a simple Python game, learning about packaging with tools like Buildozer, to eventually installing Ubuntu over Windows to overcome compatibility issues.

### Key Lessons Learned:

- Python game development using Pygame
- Handling collisions & physics
- Designing game states and UI screens
- Packaging Python apps using PyInstaller
- Understanding platform compatibility problems
- Exploring Linux (Ubuntu) as a better development environment

What started as a small experiment turned into a hands-on learning journey across software development, packaging, and operating systems.

---

## 🛠️ Tools & Technologies

- Python
- Pygame
- PyInstaller
- Windows & Ubuntu Linux

---

## 👤 Author

**Kasun Mahela**  
Electrical and Computer Engineering Undergraduate  
The Open University of Sri Lanka

📧 Email: kasunmahela@gmail.com  
📱 WhatsApp: +94 XX XXX XXXX

---

## 📜 License

This project is open for learning and personal use. Feel free to fork, explore, and improve it! 🚀

---

⭐ **If you like this project, don't forget to give it a star on GitHub!**
