import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import easyocr
from utils import gen_regx_matches

reader = easyocr.Reader(['id', 'en'])

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FILE_DIR = 'files'

app = Flask(__name__)

if not os.path.exists(FILE_DIR):
    os.makedirs(FILE_DIR)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = FILE_DIR + '/' + secure_filename(file.filename)
            file.save(filename)
            parsed = result = reader.readtext(filename, decoder = 'wordbeamsearch', beamWidth= 4, batch_size = 1,\
                 workers = 0, allowlist = None, blocklist = None, detail = 0,\
                 rotation_info = None, paragraph = False, min_size = 20,\
                 contrast_ths = 0.5,adjust_contrast = 0.5, filter_ths = 0.003,\
                 text_threshold = 0.65, low_text = 0.4, link_threshold = 0.4,\
                 canvas_size = 2560, mag_ratio = 1.,\
                 slope_ths = 0.1, ycenter_ths = 0.5, height_ths = 0.5,\
                 width_ths = 0.5, y_ths = 0.5, x_ths = 1.0, add_margin = 0.1, output_format='standard') 
            req = gen_regx_matches(parsed)
            # text = '<br/>\n'.join(map(lambda x: x[1], parsed))
            # handle file upload
            return (req)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)