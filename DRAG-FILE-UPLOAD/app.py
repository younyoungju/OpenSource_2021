from flask import Flask,render_template, request
from werkzeug.utils import secure_filename
import OCR_final

app = Flask(__name__)

@app.route('/')
def fileupload():
    return render_template('index.html');

@app.route('/fileUpload', methods = ['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('c:' + secure_filename(f.filename))
        return OCR_final.tes_ocr(f)
    
if __name__ == "__main__":
		app.run(debug=True)


