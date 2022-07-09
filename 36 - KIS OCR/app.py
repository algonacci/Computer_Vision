from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import easyocr
import os
import module as md
from PIL import Image
import pandas as pd

app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = 'static/'
app.config['DOWNLOAD_FOLDER'] = 'downloads/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/kis-ocr', methods=['GET', 'POST'])
def ocr():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        upload_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        reader = easyocr.Reader(['id'], gpu=True)
        result = reader.readtext(img)
        data = []
        for detection in result:
            text = detection[1]
            data.append(text)
        nomor_kartu, nama, alamat, tanggal_lahir, nik, faskes = md.extract_data(
            data=data)
        df = pd.DataFrame({
                          'Nomor Kartu': nomor_kartu,
                          'Nama': nama,
                          'Alamat': alamat,
                          'Tanggal Lahir': tanggal_lahir,
                          'NIK': nik,
                          'Faskes': faskes})
        table = df.to_html(index=False)
        return render_template('result.html', image=upload_file, table=table)


@app.route('/download_excel')
def download_file():
    md.download_excel()
    excel = md.download_excel.filename_excel
    return send_file(excel, as_attachment=True, mimetype='application/vnd.ms-excel')
