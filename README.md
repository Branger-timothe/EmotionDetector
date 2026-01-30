# numbersWithFingers
Detetction of numbers on camera with AI 

# Hand Detector
ouvrir un terminal powershell
: 


install python 3.10.X

`winget install Python.Python.3.10`

verify

`py -3.10 --version`

should return :

`Python 3.10.x`

ouvrir un terminal sous linux
: 

create venv : 


`cd C:\Your\Path\To\The\Project`

create your env : 


`python -m venv handDetectorEnv`


activate your env :

`yoloenv\Scripts\activate`

Install version of packages : 


`python -m pip install --upgrade pip
pip install numpy==1.26.4
pip install torch torchvision torchaudio
pip install ultralytics>=8.1.0
pip install opencv-python
pip install pygame`

To throw the game : 
`python -m src.game.game`

