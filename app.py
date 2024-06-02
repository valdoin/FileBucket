from flask import Flask, request, render_template, url_for, send_file, make_response
import os
from zipfile import ZipFile
import io

app = Flask(__name__)

UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Aucun fichier trouvé'
        
        files = request.files.getlist('file')
        
        for file in files:
            if file.filename == '':
                return 'Aucun fichier sélectionné'

            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    
    return render_template('index.html', files=files)


@app.route('/download-all')
def download_all():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    memory_file = io.BytesIO()
    with ZipFile(memory_file, 'w') as zipf:
        for file in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            zipf.write(file_path, os.path.basename(file_path))
    
    memory_file.seek(0)
    response = make_response(memory_file.read())
    response.headers['Content-Disposition'] = 'attachment; filename=all_files.zip'
    response.headers['Content-Type'] = 'application/zip'
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
