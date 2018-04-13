import subprocess
import os.path

db_create = None
if not os.path.isfile('/opt/app-root/src/db/db.sqlite3'):
    db_create = True

subprocess.check_output(['pip3','install','-r','/opt/app-root/src/requirements.txt'])

subprocess.check_output(['python3','/opt/app-root/src/manage.py','makemigrations'])
subprocess.check_output(['python3','/opt/app-root/src/manage.py','migrate'])


if db_create:
    subprocess.check_output(['python3','/opt/app-root/src/manage.py','loaddata','/opt/app-root/src/auth.json'])    
    subprocess.check_output(['python3','/opt/app-root/src/manage.py','loaddata','/opt/app-root/src/app.json'])
 
 
#subprocess.check_output(['python3','/opt/app-root/src/manage.py','runserver'])
subprocess.check_output(['gunicorn','-b', '0.0.0.0:8080 ','pyeconomics.wsgi'])