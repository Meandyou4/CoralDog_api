<h1>Recognition of Dog Breeds</h1>


1. git clone https://github.com/SasaMMS/dog_app.git
2. Download - https://drive.google.com/file/d/1GDux7Nto7da314SMAB-RQWZAkAuT9Otz/view?usp=sharing
3. Fajl prebaci ga u ./Web_App/models/

4. python -m venv env (Napravi env u Web_App folderu)

- cd to env 

- activate env

5. pip install -r requirements.txt


6. Make .flaskenv file with:
------------------------
FLASK_APP=app.py 

FLASK_ENV=development

------------------------
- flask run

- #flask run --host IP_ADDRESS

--------------------------
Testing api: app.py
--------------------------
API:

- localhost:5000/send-image/<path:url>

data:image/jpeg;base64

data:image/png;base64

--------------------------
Output:
```
{
    "f_id": 39,
    "first": "BULL_TERRIER",
    "first_prediction_procent": "99%",
    "others_breeds": "1%",
    "s_id": 132,
    "second": "SOFT-COATED_WHEATEN_TERRIER",
    "second_prediction_procent": "0%"
}
```
--------------------------
