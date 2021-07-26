from  flask import Flask,render_template, request, url_for ,jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import run 
from xlrd import open_workbook
from xlutils.copy import copy
from PIL import Image
import PIL
import piexif
import shutil
import random
from flask_restful import Resource, Api, reqparse
import base64
from io import BytesIO
import requests
import json


f = open("./files/breed.txt", "r")
breeds=[]
for x in f:
 breeds.append(x.strip())

app = Flask(__name__,template_folder="templates")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
UPLOAD_FOLDER = './static/uploadIMG'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

 
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
def rasa_unos(unos):

    file = open("./files/rasa.txt","a+") 
    rasa_pasa=unos      
    # Reading from file
    file.write(rasa_pasa+"\n")
    file.close()

def rasa_citac():
    with open('./files/rasa.txt') as myfile:
        return(list(myfile)[-1])


def index():
    path_to_image=os.path.basename(str(rasa_citac()))
    full_path= str(rasa_citac())
    file = path_to_image
    try:
        if file: 
            filename = secure_filename(file)
            exten=filename.split(".")
            exten=exten[-1]
            datetime_object = datetime.now()
            #name = str(int(datetime_object.timestamp())-1586289491)
            name = str(random.randint(0, 1000000))

            while(name in os.listdir(app.config['UPLOAD_FOLDER'])):
                    name = str(random.randint(0, 1000000))
            dirr = os.path.join(app.config['UPLOAD_FOLDER'], name)
            os.mkdir(dirr)
            dirr = os.path.join(dirr, name)
            os.mkdir(dirr)
            #file.resize((400, 350))

            os.replace(full_path.replace("\n", ""), os.path.join(dirr, name + "." +exten ))

            try:
                imgMain = Image.open(os.path.join(dirr, name + "." +exten))
                
                img = piexif.load(os.path.join(dirr, name + "." +exten))
                #Get the orientation if it exists
                orientation = img["0th"].pop(piexif.ImageIFD.Orientation)
                exif_bytes = piexif.dump(img)

                if orientation == 2:
                    imgMain = imgMain.transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 3:
                    imgMain = imgMain.rotate(180)
                elif orientation == 4:
                    imgMain = imgMain.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 5:
                    imgMain = imgMain.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 6:
                    imgMain = imgMain.rotate(-90, expand=True)
                elif orientation == 7:
                    imgMain = imgMain.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 8:
                    imgMain = imgMain.rotate(90, expand=True)

                imgMain.save(os.path.join(dirr, name + "." +exten),exif=exif_bytes)
                print(" Work ")
            except:
                print('Go ahead')             
     
            p=os.path.join(dirr, name + "." +exten).replace('\\','/')
            width, height = Image.open(os.path.join(dirr, name + "." +exten)).size
            dat = {'img':p ,'w':width,'h':height}
            resp= jsonify(dat)
            print("File uploaded")

            imgsrc = p
            idx = imgsrc.index("/static/")
            
            #Ulaz slike
            o1,p1,o2,p2=run.r(imgsrc[idx:])
            
            with open('./files/labels.json') as f:
                data = json.load(f)

            name_by_id = dict([(str(p['id']), p['breed']) for p in data])
            id_by_name = dict([(p['breed'], p['id']) for p in data])

            f = open("./files/log.txt", "a")
            f.write( "\n" + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "," +o1 +"," +str(p1))
            f.close()
            others_breeds=str(100-(int(p1*100)+int(p2*100))) + "%"

            return jsonify(
              f_id=id_by_name[o1],
              first=o1.upper(),
              first_prediction_procent=str(int(p1*100))+"%",
              s_id=id_by_name[o2],
              second=o2.upper(),
              second_prediction_procent=str(int(p2*100))+"%",
              others_breeds=others_breeds
              )
    except:
        print('Please try with different URL !!!')
        return jsonify(
              f_id=None,
              first=None,
              first_prediction_procent=None,
              s_id=None,
              second=None,
              second_prediction_procent=None,
              others_breeds=None
              )
        # print("First prediction: "+o1.upper()+" > "+str(int(p1*100))+"%")
        # print("Second prediction: "+o2.upper()+" > "+str(int(p2*100))+"%")
        # print("Other breeds:"+others_breeds)
        # print(get_breeds_index(o1))
        # o1 = o1.split("_")
        # o1 = [word.capitalize() for word in o1]
        # o1=" ".join(o1)
        # o2 = o2.split("_")
        # o2 = [word.capitalize() for word in o2]
        # o2=" ".join(o2)       

        # data = {'o1':o1 ,'p1':p1,'o2':o2,'p2':p2}
        # print(data)


@app.route("/send-image/<path:url>", methods=['GET', 'POST'])
def image_check(url):
    # ----- SECTION 1 -----  
    #File naming process for nameless base64 data.
    #We are using the timestamp as a file_name.
    from datetime import datetime
    dateTimeObj = datetime.now()
    file_name_for_base64_data = dateTimeObj.strftime("%d-%b-%Y--(%H-%M-%S)")
    
    #File naming process for directory form <file_name.jpg> data.
    #We are taken the last 8 characters from the url string.
    file_name_for_regular_data = url[-10:-4]
    
    # ----- SECTION 2 -----
    try:
        # Base64 DATA
        if "data:image/jpeg;base64," in url:
            base_string = url.replace("data:image/jpeg;base64,", "")
            decoded_img = base64.b64decode(base_string)
            img = Image.open(BytesIO(decoded_img))

            file_name = file_name_for_base64_data + ".jpg"
            rasa_unos(os.path.abspath(file_name))

            img.save(file_name, "jpeg")

        # Base64 DATA
        elif "data:image/png;base64," in url:
            base_string = url.replace("data:image/png;base64,", "")
            decoded_img = base64.b64decode(base_string)
            img = Image.open(BytesIO(decoded_img))

            file_name = file_name_for_base64_data + ".png"
            img.save(file_name, "png")
            rasa_unos(os.path.abspath(file_name))

        # Regular URL Form DATA
        else:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            file_name = file_name_for_regular_data + ".jpg"
            img.save(file_name, "jpeg")
            rasa_unos(os.path.abspath(file_name))

    # ----- SECTION 3 -----    
        status = "Image has been succesfully sent to the server."
    except Exception as e:
        status = "Error! = " + str(e)

    #rasa_unos(os.path.abspath(file_name))
    return index()
    #return os.path.abspath(file_name)     



app.run(debug=True)
#app.run(host="0.0.0.0", port=5555)
