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
Install PyTorch:
```bash
pip install torch torchvision torchaudio
```
Install remaining packages :
```bash
pip install -r requirements.txt
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