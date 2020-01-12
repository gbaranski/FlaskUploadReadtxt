import os
from os import listdir
from os.path import isfile, join
from flask import *  

from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'txt'}
UPLOAD_FOLDER = './files'

app = Flask(__name__)  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

def get_files():
	return [f for f in listdir(app.config['UPLOAD_FOLDER']) if isfile(join(app.config['UPLOAD_FOLDER'], f))]

@app.route('/<filename>')
def view_file(filename):
	text = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r+')
	content = text.read()
	text.close()
	return render_template('content.html', text=content)

@app.route('/')
def upload_form():
	#text = open('textfile.txt', 'r+')
	#content = text.read()
	#text.close()
	#return render_template('content.html', text=content)

	files = get_files()
	return render_template('upload.html', files=files)

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			return render_template('error_nofile.html')
		if file and allowed_file(file.filename):
			text = request.form['text']
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], text))
			onlyfiles = get_files()
			print(onlyfiles)
			return render_template('success.html')
		else:
			return render_template('error_invalidformat.html')


if __name__ == "__main__":
    app.run(debug = True)  