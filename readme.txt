first create a virtual enivironment with this python -m venv  europe_venv
then to activate the enivironment europe_venv\Scripts\activate
then pip install -r requirements.txt
then create a database with a name "ai_literacy_db"
then python manage.py makemigrations
then python manage.py migrate
then python manage.py populate_data  these creates data to test
then python manage.py collectstatic --noinput
then python manage.py createsuperuser   this for admin only
then python manage.py runserver

no need to create a superuser or admin
if you can login then there are two admin one is admin userid paswword admin use this as admin login
for student use the one it shows down of the page
if you want yo make a student administrator then you can do it in the Django which is http://127.0.0.1:8000/admin
