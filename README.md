# logger_video
## Install & Run
```PowerShell
#PowerShell
git clone https://github.com/shiba0627/logger_video.git
cd logger_video
python -m venv venv_log
./venv_log/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## パッケージリストの更新
```PowerShell
python -m pip freeze > requirements.txt 
```

## ディレクトリ構成の出力
```
tree /F /A > tree.txt
```