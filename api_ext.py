import os
from flask import Flask, request, redirect, url_for,jsonify,Response
from werkzeug import secure_filename
import gintool
UPLOAD_FOLDER = '/home/cnsc/ExtracterRomToFrameworkAndroid/rom'
ALLOWED_EXTENSIONS = set(['rar', 'zip', 'tar', 'ftf'])
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/rom", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = gintool.extractRom(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return Response(response=result, status=200, mimetype='application/json')
    return {"message":"File Not Support"}

if __name__ == '__main__':
     app.run(port=5002)