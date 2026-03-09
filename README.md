# 🚨 Live Fall Detection System

A real-time fall detection system using computer vision and machine learning. The system detects human falls through a live camera feed and automatically sends SMS alerts to registered contacts.

## 📌 Features

- 🎥 **Live Fall Detection** — Real-time detection using webcam/camera feed
- 🦴 **Human Skeleton Tracking** — MediaPipe-based pose estimation
- 🤖 **ML Classification** — Trained Random Forest model for fall vs. non-fall classification
- 🔐 **Face Authentication** — Secure login using facial recognition
- 📱 **SMS Alerts** — Automatic SMS notification via Fast2SMS API when a fall is detected
- 📊 **Evaluation & Graph** — Visual performance graph of the detection model
- 🖥️ **Tkinter GUI** — User-friendly graphical interface

## 🗂️ Project Structure

```
fall-detection/
│
├── GUI_main.py              # Main GUI launcher
├── GUI_Master.py            # Master GUI controller
├── Home.py                  # Home screen
├── login.py                 # Login screen
├── registration.py          # User registration
├── Face_Auth.py             # Face authentication module
├── human_skeleten.py        # Pose/skeleton detection
├── coordinate_in_CSV.py     # Landmark coordinate extraction to CSV
├── training.py              # Model training script
├── graph.py                 # Performance graph visualization
├── sms.py                   # SMS alert via Fast2SMS API
├── untitled2.py             # Utility script
│
├── body_language.pkl        # Trained ML model (Logistic Regression)
├── body_language_rf.pkl     # Trained ML model (Random Forest)
├── haarcascade_frontalface_default.xml  # Face detection XML
├── trainingdata.yml         # Training data config
├── coords.csv / coords1.csv # Pose landmark datasets
├── evaluation.db            # Evaluation results database
├── face.db                  # Face recognition database
│
└── assets/                  # Images and audio used in GUI
```

## 🛠️ Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

### Main Dependencies

- Python 3.8+
- OpenCV (`opencv-python`)
- MediaPipe
- scikit-learn
- Pillow
- NumPy
- requests
- tkinter (built-in with Python)

## ⚙️ Setup & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/fall-detection.git
   cd fall-detection
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure SMS API:**
   - Open `sms.py`
   - Replace `YOUR_FAST2SMS_API_KEY_HERE` with your actual [Fast2SMS](https://www.fast2sms.com) API key

4. **Run the application:**
   ```bash
   python GUI_main.py
   ```

## 🔑 SMS Alert Configuration

This project uses the [Fast2SMS](https://www.fast2sms.com) API for sending alerts.  
**Never commit your real API key to GitHub.**  
Store it in an environment variable or config file and add that file to `.gitignore`.

## 📷 How It Works

1. User logs in via face authentication
2. Live camera feed is processed frame-by-frame
3. MediaPipe extracts 33 body landmark coordinates
4. A trained Random Forest classifier predicts if the pose is a "fall"
5. On fall detection, an SMS is sent to the registered phone number

## 📄 License

This project is for educational purposes.
