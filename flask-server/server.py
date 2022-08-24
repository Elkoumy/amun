import os
import datetime
import subprocess
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS
import pandas as pd
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log.versions.to_dataframe import get_dataframe_from_event_stream
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
import json
from amun import amun_service

from flask import send_file



app = Flask(__name__, static_folder='../build', static_url_path='/')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]iasdfffsd/'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return app.send_static_file('index.html')



ALLOWED_EXTENSIONS = set(['csv', 'xes'])


# global UPLOAD_FOLDER
# UPLOAD_FOLDER= r'C:\Users\elkoumy\OneDrive - Tartu Ülikool\Differential Privacy\flask-react-app\uploads'

def CreateNewDir():
    print ("I am being called")
    # UPLOAD_FOLDER = r'C:\Users\elkoumy\OneDrive - Tartu Ülikool\Differential Privacy\flask-react-app\uploads'
    UPLOAD_FOLDER = '../uploads'
    print (UPLOAD_FOLDER)
    UPLOAD_FOLDER = UPLOAD_FOLDER+datetime.datetime.now().strftime("%d%m%y%H")
    cmd="mkdir -p %s && ls -lrt %s"%(UPLOAD_FOLDER,UPLOAD_FOLDER)
    output = subprocess.Popen([cmd], shell=True,  stdout = subprocess.PIPE).communicate()[0]

    if b'' == output:
        print ("Success: Created Directory %s"%(UPLOAD_FOLDER))
    else:
        print ("Failure: Failed to Create a Directory (or) Directory already Exists",UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadLog', methods=['GET', 'POST'])
def upload_file():
    new_filename=''
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
            filename = secure_filename(file.filename)
            filename = file.filename
            # UPLOAD_FOLDER= r'C:\Users\elkoumy\OneDrive - Tartu Ülikool\Differential Privacy\flask-react-app\uploads'
            UPLOAD_FOLDER = '../uploads'
            CreateNewDir()
            # global UPLOAD_FOLDER
            x=file.save(os.path.join(UPLOAD_FOLDER, filename))
            new_filename=filename
            x=url_for('uploaded_file',filename=filename)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return new_filename



@app.route('/uploaded', methods=['GET', 'POST'])
def uploaded_file():
    filename=request.args['filename']
    #perform validation here.
    if filename.split('.')[-1]=='csv':
        #validate csv here
        try:
            file=pd.read_csv(os.path.join( os.getcwd(),'..', 'uploads', filename))
        except:

            return '''error_csv'''

        try:
            file = file[['case:concept:name', 'concept:name', 'time:timestamp']]
        except KeyError as e:

            return '''error_column'''

        try:
            file['time:timestamp'] = pd.to_datetime(file['time:timestamp'], utc=True)
        except:

            return '''error_timestamp'''

        if file.isna().any().any()==True:

            return '''error_null'''

        file.to_csv( os.path.join( os.getcwd(),'..', 'uploads', filename), index=False)

    elif filename.split('.')[-1]=='xes':
        #validate xes
        try:
            file =xes_import_factory.apply(os.path.join( os.getcwd(), '..','uploads', filename))
            file = get_dataframe_from_event_stream(file)
        except:
            return '''xes_error'''

        try:
            file = file[['case:concept:name', 'concept:name', 'time:timestamp']]
        except KeyError as e:

            return '''error_column'''

        try:
            file['time:timestamp'] = pd.to_datetime(file['time:timestamp'], utc=True)
        except:

            return '''error_timestamp'''

        if file.isna().any().any()==True:

            return '''error_null'''

        log = conversion_factory.apply(file)
        xes_exporter.export_log(log, os.path.join( os.getcwd(), '..','uploads', filename))

    else:
        #raise an error
        return '''error'''


    return '''
	<!doctype html>
	<title>Uploaded the file</title>
	<h1> File has been Successfully Uploaded </h1>
	'''


@app.route('/anonymize', methods=['GET', 'POST'])
def anonymize():
    print("Starting Anonymization")
    filename = json.loads(request.data.decode('utf-8'))['filename']
    mode=json.loads(request.data.decode('utf-8'))['mode']
    dataset=os.path.join(os.getcwd(),'..','uploads',filename)

    #call amun here

    # mode = 'sampling'
    # modes=['oversampling','filtering','sampling']
    delta = 0.2

    data,risk_pert_event = amun_service.amun(dataset, mode, delta)
    org_file_name=filename.split('.')[0]
    if  filename.split('.')[-1]== 'csv':
        data.to_csv(os.path.join(os.getcwd(),'..','output','anonymized_'+filename),index=False,encoding='utf-8',sep=',')
        risk_pert_event.to_csv(os.path.join(os.getcwd(),'..','output',org_file_name+'_risk.csv'),index=False,encoding='utf-8',sep=',')

    else:
        log = conversion_factory.apply(data)
        xes_exporter.export_log(log, os.path.join(os.getcwd(),'..','output','anonymized_'+filename))
        risk_pert_event.to_csv(os.path.join(os.getcwd(), '..', 'output', org_file_name + '_risk.csv'),index=False,encoding='utf-8',sep=',')


    return 'success'





@app.route('/output/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    org_file_name = filename.split('.')[0]
    path = os.path.join(os.getcwd(),'..','output',filename)
    return send_file(path, as_attachment=True)





if __name__ == '__main__':
      app.secret_key = 'super secret key'
      app.config['SESSION_TYPE'] = 'filesystem'
      app.debug = True
      app.run()