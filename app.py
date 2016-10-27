import os, sys
import webbrowser
import socket

from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
app = Flask(__name__, static_url_path='')


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("192.168.0.1",80))
ip = s.getsockname()[0]
UPLOAD_FOLDER = '/home/<user>/Desktop/uploads'                                    #change default folder
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','rar','docx']) #add more extensions to allow them
PORT = 8000                                                                        #change port if required

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def openbrowser():
	url="http://127.0.0.1:"+str(PORT)+"/home"
	webbrowser.open(url, new=0, autoraise=True)                                 

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
            return render_template('success.html',ip=ip,port=PORT)
    return render_template('index.html', ip=ip, port=PORT)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    #msg = filename + " uploaded succesfully!"
    #return msg
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/home')
def hello():	
	return render_template('dashboard.html', ip=ip,port=PORT)

@app.route('/files')
def files():
	path = '/home/<user>/Desktop/uploads'                                              #file directory
	dirs = os.listdir(path)
	return render_template('files.html', users = dirs, ip=ip, port=PORT, path=path)



if __name__ == "__main__":
	openbrowser()
	app.run(host = '0.0.0.0', port=PORT) 
    
