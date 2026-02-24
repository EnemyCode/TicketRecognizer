#To create the virtual enviroment: python3 -m venv venv
#To activate the virtual enviroment: source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

sudo apt update
sudo apt install -y \
    tesseract-ocr \
    libtesseract-dev \
    libgl1 \
    libglib2.0-0 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    libxkbcommon-x11-0 \
    libsm6 \
    libice6 \
    fontconfig \
    fonts-dejavu-core \
    fonts-dejavu-extra \
    tesseract-ocr-spa \
    tesseract-ocr-eng

sudo apt install fontconfig fonts-dejavu-core

export QT_QPA_PLATFORM=wayland
export QT_QPA_FONTDIR=/usr/share/fonts
export FONTCONFIG_PATH=/etc/fonts
