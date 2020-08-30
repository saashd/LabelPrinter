import os
import sys

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time
import json
from flask import Flask, request, jsonify, Response

# install brother_ql, pyusb and libusb-win32
# type ipconfig in cmd to check ur IP adress

# .py to .exe : install pyinstaller and write in cmd: pyinstaller --onefile print_label_via_brother.py
# server to communicate with label printer


app = Flask(__name__)

#  http://127.0.0.1:5000/print?number=2&quantity=2 -this is how it works
@app.route("/print",methods=['get'])
def do_print():
    print_str = request.args.get('string', None)  # use default value replace 'None'
    quantity = request.args.get('quantity', None)
    create_label(print_str)

    if print_label('print.png',quantity)==0:
        return jsonify( {'status': 'success'} ),200
    return jsonify({'status': 'fail'}),500





#add serial number to template to create new label
def create_label(print):
    in_file = 'template.png'
    out_file = 'print.png'
    year_last_2_digits = time.strftime("%y", time.localtime())
    print_string = print
    text =   print_string+ '/' + year_last_2_digits
    img = Image.open(in_file)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("C:\Windows\Fonts\Calibri.ttf", 100)
    draw.text((125, 125), text, fill="black", font=font, align='center')
    img.save(out_file)

# print label using brother_ql library
def print_label(img,quantity):
    quantity=int(quantity)
    data = parse_json()
    brother_cmd=data['brother_cmd']
    status=None
    for i in range(0,quantity):
        status=(os.system(brother_cmd + img))
    return status

def parse_json():
    with open('config.json') as f:
        data = json.load(f)
        return data

def main():
    data=parse_json()
    host=data['localhost']
    port=data['port']
    if host==True:
        app.run(port=port)
    else:
        app.run(host='0.0.0.0', port=port)
    # this line should prevent exe file from closing.it allows server to keep running until the exe file is open
    if input() == 'quit':
        sys.exit(0)



    return


if __name__ == '__main__':
    main()
