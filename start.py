import subprocess
import os.path

db_create = None
if not os.path.isfile('/var/www/pyeconomics/db/db.sqlite3'):
    db_create = True

subprocess.check_output(['python3.6','/var/www/pyeconomics/manage.py','makemigrations'])
subprocess.check_output(['python3.6','/var/www/pyeconomics/manage.py','migrate'])

if db_create:
    subprocess.check_output(['python3.6','/var/www/pyeconomics/manage.py','load','/var/www/pyeconomics/auth.json'])
    subprocess.check_output(['python3.6','/var/www/pyeconomics/manage.py','load','/var/www/pyeconomics/app.json'])
 