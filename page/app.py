from flask import Flask,render_template, request
from werkzeug.utils import secure_filename
import cv2
# import Extraction_Keyword

app = Flask(__name__)

@app.route('/')
def fileupload():
    return render_template('index.html');

@app.route('/fileUpload', methods = ['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('c:' + secure_filename(f.filename))
        image = cv2.imread("Image/result.jpg", cv2.IMREAD_ANYCOLOR)
        cv2.imshow("Result",image)
        cv2.namedWindow('Result')
        cv2.waitKey(0)
        return '파일 업로드 성공'
        # return Extraction_Keyword.tes_ocr(f)
    
if __name__ == "__main__":
		app.run(debug=True)


