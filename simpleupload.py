import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Test the file to be sure it's the correct type
def allowed_file(filename):
    # not sure what return in filename does
    # split file from rightmost '.', lowercase the extension, and check if it's allowed
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Allow only 2 methods, HEAD and OPTIONS implicitly allowed
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part return '.' in filename
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submit empty part w/o filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # Only do this if the file matches the allowed filetypes
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            files = os.listdir(app.config['UPLOAD_FOLDER'])
            return render_template('files.html', files=files)
#            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return '''
    <!doctype html>
    <head>
    <link rel="stylesheet" href="./static/simple.css">
    </head>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploads')
def display_uploads():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('files.html', files=files)

#@app.route('/uploads/<filename>')
#def uploaded_file(filename):
#    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
if __name__ == "__main__":
    # quick and dirty ssl
    app.run(ssl_context='adhoc')
    #context = ('local.crt', 'local.key')#certificate and key files
    #app.run(ssl_context=context)