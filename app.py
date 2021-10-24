#デコードされた画像の保存先パス
img_path = 'capture/img0000.jpg'

# ------------ save_img ------------
import base64
import numpy as np
import cv2

def save_img(img_base64):
    global img_path

    #binary <- string base64
    img_binary = base64.b64decode(img_base64)
    #jpg <- binary
    img_jpg=np.frombuffer(img_binary, dtype=np.uint8)
    #raw image <- jpg
    img = cv2.imdecode(img_jpg, cv2.IMREAD_COLOR)
    #画像を保存
    cv2.imwrite(img_path, img)
    return "SUCCESS"

# ------------ save_img ------------

# --------- ocr_translator ---------
from PIL import Image
import pytesseract
# tesseractコマンドのインストールパス
pytesseract.tesseract_cmd = './tesseract/4.1.1/bin/tesseract'

from googletrans import Translator
import io

def read_image_text():
    global img_path

    img = Image.open(img_path)
    txt = pytesseract.image_to_string(img, lang='eng').replace('.', '. ')
    print(txt)

    try:
        txt_translated = Translator().translate(txt, src = 'en' ,dest = 'ja').text
    except Exception as e:
        txt_translated = 'テキストがよく見えるようにしてね!!!'

    print(txt_translated)
    return txt_translated

# --------- ocr_translator ---------

# ------------- app -------------
from flask import Flask, request, make_response, render_template, url_for

api = Flask(__name__)

@api.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@api.route('/capture_img', methods=['POST'])
def capture_img():
    msg = save_img(request.form["img"])
    print(msg)

    txt = read_image_text()
    return make_response(txt)

# ------------- app -------------

if __name__ == "__main__":
    api.run(debug=True, threaded=True)
