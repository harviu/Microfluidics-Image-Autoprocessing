pip install -r .\requirements.txt
pip install .\JPype1-0.7.0-cp37-cp37m-win_amd64.whl
$Env:FLASK_APP="./app.py"
flask run