#!/bin/python

import os, random
from flask import Flask, Response, request, abort, render_template_string, send_from_directory, send_file
from PIL import Image, ImageOps
from io import StringIO, BytesIO

print("\n\n\n\n current working directory", os.getcwd(),"\n\n\n\n")


app = Flask(__name__)

WIDTH = 300
HEIGHT = 200

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <meta charset="utf-8" />
    <style>
        body {
            background-color:#333;
            text-align:center;
            display: grid;
            justify-content: center;
            align-items: center;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            grid-auto-rows: minmax(200px, auto);
            grid-gap: 20px;
            grid-auto-flow: dense;
        }
        .image {
            margin: 0 auto;
            display:block;
            border: 5px solid #666;
        }
    </style>
    <script src="https://code.jquery.com/jquery-1.10.2.min.js" charset="utf-8"></script>
    <script src="http://luis-almeida.github.io/unveil/jquery.unveil.min.js" charset="utf-8"></script>
    <script>
$(document).ready(function() {
    $('img').unveil(1000);
});
    </script>
</head>
<body>
    {% for image in images %}
        <a class="image" href="{{ image.src }}" style="width: {{ image.width }}px; height: {{ image.height }}px">
            <img src="{{ image.src }}" 
			data-src="{{ image.src }}?w={{ image.width }}&amp;h={{ image.height }}" 
			width="{{ image.width }}" 
			height="{{ image.height }}" />
        </a>
    {% endfor %}
</body>
'''

path = './data/'
files = os.listdir(path)


print("files ", files) 

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')







@app.route('/<path:filename>')
def image(filename):
    try:
        w = int(request.args['w'])
        h = int(request.args['h'])
    except (KeyError, ValueError):
        return send_from_directory('.', filename)

    try:
        im = Image.open(filename)
        im.thumbnail((w, h), Image.ANTIALIAS)
        io = BytedIOIO()
        im.save(io, format='JPEG')
        return Response(io.getvalue(), mimetype='image/jpeg')

    except IOError:
        abort(404)

    return send_from_directory('.', filename)

@app.route('/list')
def index():
    images = []
    for root, dirs, files in os.walk('/data/'):
        
        for filename in [os.path.join(root, name) for name in files]:
            if not filename.endswith('.jpg'):
                continue

            im = Image.open(filename)
            w, h = im.size
            aspect = 1.0*w/h
            if aspect > 1.0*WIDTH/HEIGHT:
                width = min(w, WIDTH)
                height = width/aspect
            else:
                height = min(h, HEIGHT)
                width = height*aspect

            images.append({
                'width': int(width),
                'height': int(height),
                'src': filename
            })

    return render_template_string(TEMPLATE, **{
        'images': images
    })

@app.route('/<int:width>/<int:height>')
def download(width=600, height=400):
    width=int(width)
    height = int(height)
    file = random.choice(files)
    img = Image.open(os.path.join(path, file))
    img  = ImageOps.fit(img, (width,height), Image.ANTIALIAS)
    
    return serve_pil_image(img)

if __name__ == '__main__':
    app.run(debug=True, host='::', port=80)
