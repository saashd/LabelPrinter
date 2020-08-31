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


@app.route("/api", methods=['get'])
def check_status():
    return jsonify({"Message": "Running"})


@app.route("/label_printer", methods=['post'])
def get_keys():
    data = request.json
    content = data['Content']
    quantity = data['Quantity']
    template = data['WithLogo']
    text = reverse_and_flip(content)
    try:
        if template:
            create_label(text, 'template.png')
        else:
            create_label(text, 'template1.png')
            status_code = print_label('print.png', quantity)
            if status_code == 0:
                return jsonify({'Message': 'success'}), 200
            return jsonify({'Message': 'failed with status code: {}'.format(status_code)}), 500
    except Exception as e:
        return jsonify({'Message': str(e)}), 500


def is_hebrew_char(c):
    return 1424 <= ord(c) <= 1514


def reverse_and_flip(text):
    s = text.split(' ')
    builder = []
    buffer = []
    for w in reversed(s):
        if (len(w) == 0):
            continue
        flag = is_hebrew_char(w[0])
        if flag:
            if len(buffer) > 0:
                for b in reversed(buffer):
                    builder.append(b)
                buffer = list()
            builder.append(''.join(reversed(w)))
        else:
            buffer.append(w)

    if len(buffer) > 0:
        for b in reversed(buffer):
            builder.append(b)

    return ' '.join(builder)


def create_label(content_print, file):
    length = len(content_print)
    if 0 <= length <= 9:
        size = 100
        W = (720 - length * 55) / 2
    elif 10 <= length <= 19:
        size = 75
        W = (720 - length * 39) / 2
    elif 20 <= length <= 29:
        size = 50
        W = (720 - length * 26) / 2
    else:
        raise Exception("Max length allowed is 29 characters")

    W = max(0, W)
    img = Image.open(file)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("C:\Windows\Fonts\Calibri.ttf", size)
    draw.text((W, 150), content_print, fill="black", font=font, align='center')
    img.save('print.png')


# print label using brother_ql library
def print_label(img, quantity):
    quantity = int(quantity)
    data = parse_json()
    brother_cmd = data['brother_cmd']
    status = None
    for i in range(0, quantity):
        status = (os.system(brother_cmd + img))
    return status


def parse_json():
    with open('config.json') as f:
        data = json.load(f)
        return data


def main():
    data = parse_json()
    host = data['localhost']
    port = data['port']
    if host == True:
        app.run(port=port)
    else:
        app.run(host='0.0.0.0', port=port)
    # this line should prevent exe file from closing.it allows server to keep running until the exe file is open
    if input() == 'quit':
        sys.exit(0)

    return


if __name__ == '__main__':
    main()
