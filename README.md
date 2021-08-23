<h1>Recognition of Dog Breeds</h1>


1. git clone https://github.com/SasaMMS/CoralDog_api.git
2. Download - https://drive.google.com/file/d/1GDux7Nto7da314SMAB-RQWZAkAuT9Otz/view?usp=sharing or skip it if exist "EFN.pth"
3. Move EFN.pth to ./Web_App/models/

4. python -m venv env (Make environment in Web_App folder)

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
- http://192.168.2.92:5000/send-image/https://i.pinimg.com/564x/39/0f/f5/390ff5f5469dbd1b759521a8b8822553.jpg

data:image/jpeg;base64

data:image/png;base64

--------------------------
Output:
```
{
  "f_id": 59, 
  "first": "DOBERMAN", 
  "first_prediction_procent": "91%", 
  "others_breeds": "6%", 
  "s_id": 98, 
  "second": "MEXICAN_HAIRLESS", 
  "second_prediction_procent": "3%"
}
```
--------------------------
