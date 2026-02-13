# Hand & Emotions detector
AI-powered detection hands & emotions detector using computer vision and hand tracking.

## Installation & Setup

### 1. Install Python 3.10
Open a PowerShell terminal and execute the following:

* **Install Python:**
  ```powershell
  winget install Python.Python.3.10
  ```

* **Verify Installation:**

   ```powershell
   py -3.10 --version
   ```
  <sup>(Expected output: Python 3.10.x)</sup>


### 2. Environment Configuration
Navigate to your project directory and set up the virtual environment:

* **Navigate to project folder:**

   ```bash
   cd C:\Your\Path\To\The\Project
   ```
* **Create virtual environment:**

   ```bash
   py -3.10 -m venv handDetectorEnv
   ```
*  **Activate the environment:**

   ```bash
   handDetectorEnv\Scripts\activate
   ```

### 3. Install Dependencies
With the environment activated, run these commands to install required packages:

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install packages :
```bash
pip install -r requirement.txt
```
<small>(This will automatically install NumPy, TensorFlow, DeepFace, and other dependencies)</small>

### 4. Download Model Weights
As the pre-trained model file is too large for GitHub, it must be downloaded manually:

* **Download `best.pt`:** [Click here to download](https://github.com/RionDsilvaCS/yolo-hand-pose/blob/main/model/best.pt)
* **Installation:** Move the `best.pt` file into the `model/` folder in the project root.
  *<small>(If the "model" folder does not exist, please create it manually)</small>*

### 5. Run the Application
Start the detection system by running the game module:

```bash
python -m src.mainWindow
```

### 6. Problems
This part of the project was intended to recognize and display certain hand gestures using the webcam, including:
	•	open hand
	•	two fingers
	•	thumbs up
	•	OK

At first, a YOLO-based model was used to detect the gestures, but it proved to be insufficiently trained for this level of precise recognition. It was able to detect a hand correctly when all fingers were lowered, but struggled as soon as a single finger was bent, making the detection unreliable.

An initial implementation was started with this model, but the recognition and gesture display issues led to a change of approach and a complete reimplementation.

The system now uses MediaPipe Hand models via OpenCV DNN — palm_detection_mediapipe for palm detection and handpose_estimation_mediapipe for estimating the 21 key points of the hand. This makes it possible to analyze finger orientation and correctly identify gestures.

The code is now functional: the webcam opens, the hand landmarks are detected, and the recognized gesture is displayed in the top-left corner of the screen.

Simply open the Python file and run it to test the real-time recognition.

We did not have time to integrate it into the main project, as it was resolved and completed only a few days before the final submission. However, we decided to include it here.


To run gestureRecognizer :
cd gesteDetector
python -m gestureRecognizer