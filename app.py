from flask import Flask, send_from_directory, jsonify, request
import os
from image_process import nd2_read,tif_read,sum_z,one_to_png,save_png
from generate_values import calculate
import hashlib
from math import sqrt, pi, cos, sin
import numpy as np
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path == '':
        return send_from_directory('client/', 'index.html')
    else:
        if os.path.exists('client/' + path):
            return send_from_directory('client/', path)
        else:
            return send_from_directory('client/', 'index.html')

@app.route('/uploader_nd2', methods = ['POST'])
def upload_nd2():
    if not os.path.isdir('data'):
        os.mkdir('data')
    if not os.path.isdir('client/img'):
        os.mkdir('client/img')
    hasher = hashlib.md5()
    f = request.files['file']
    buf = f.read()
    hasher.update(buf)
    hex = hasher.hexdigest()[0:7]
    filename = hex+".nd2"
    exists = os.path.isfile('data/'+filename)
    if not exists:
        print("Saving new file...")
        with open('data/'+filename,"wb+") as f:
            f.write(buf)
    img = tif_read("data/{}".format(filename))
    gfp = img[:,:,:,2]
    vals,chosens,_ = calculate(gfp)
    # chosens = np.repeat(np.array(chosens)[None,:],72,0)
    print(vals)
    ret = {
        "vals":vals,
        "hex":hex,
    }
    if not os.path.isdir("client/img/"+hex):
        print("Generating new Image...")
        new_png = []
        os.mkdir("client/img/"+hex)
        time = 0
        for img in gfp:
            y,x,r = chosens[time]
            show = img/np.max(img)
            show[y,x] = 1
            points = []
            for t in range(100):
                points.append((y + int(r * sin(2 * pi * t / 100)),x + int(r * cos(2 * pi * t / 100))))
            for dot in points:
                show[dot] = 1
            show = (show * 255).astype(np.uint8)
            new_png.append(show)
            # plt.imshow(show)
            # plt.show()
            time+=1
        save_png(new_png,'client/img/'+hex)
    return jsonify(ret)

@app.route('/uploader_tif', methods = ['POST'])
def upload_tif():
    if not os.path.isdir('data'):
        os.mkdir('data')
    if not os.path.isdir('client/img'):
        os.mkdir('client/img')
    hasher = hashlib.md5()
    f = request.files.getlist("file")
    buf1 = f[0].read()
    buf2 = f[1].read()
    hasher.update(buf1)
    hasher.update(buf2)
    hex = hasher.hexdigest()[0:7]
    filename1 = hex+".dic"
    filename2 = hex+".gfp"
    exists = os.path.isfile('data/'+filename1) and os.path.isfile('data/'+filename2)
    if not exists:
        print("Saving new file...")
        with open('data/'+filename1,"wb+") as f:
            f.write(buf1)
        with open('data/'+filename2,"wb+") as f:
            f.write(buf2)
    dic = sum_z(tif_read("data/{}".format(filename1)))
    gfp = sum_z(tif_read("data/{}".format(filename2)))
    vals = calculate(gfp)
    ret = {
        "vals":vals,
        "hex":hex,
    }
    if not os.path.isdir("client/img/"+hex):
        print("Generating new Image...")
        os.mkdir("client/img/"+hex)
        new_png = one_to_png(gfp)
        save_png(new_png,'client/img/'+hex)
    return jsonify(ret)