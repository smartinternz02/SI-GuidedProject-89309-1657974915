import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
global graph
graph = tf.compat.v1.get_default_graph()
from flask import Flask , request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import cv2

app = Flask(__name__)
model = load_model("Lungcancer.h5")

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/predict',methods = ['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['image']
        print("current path")
        basepath = os.path.dirname(__file__)
        print("current path", basepath)
        filepath = os.path.join(basepath,'uploads',f.filename)
        print("upload folder is ", filepath)
        f.save(filepath)
        
        img = image.load_img(filepath,target_size = (64,64))
        gray = cv2.cvtColor(np.float32(img), cv2.COLOR_BGR2GRAY)
        print(gray.shape)
        x = image.img_to_array(gray)
        x = np.expand_dims(x,axis =0)
        
    
        preds = np.argmax(model.predict(x))
            
        print("prediction",preds)
            
        index = ['Cancer','NonCancer']
        text = str(index[preds])
        
        if (text == "Cancer"):
            text = "Cancer is seen. We recommend you to get in touch with an oncologist at the earliest."
        else:
            text = "Cancer not seen. Stay safe and healthy."
        
    return render_template("result.html",predict_text=text)
if __name__ == '__main__':
    app.run(debug = False, threaded = False)
        
        
        
    
    
    