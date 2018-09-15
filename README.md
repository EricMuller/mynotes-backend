# webmarks-backend

cd mywebmarks-backend
source ./env/bin/activate
python manage.py makemigrations users webmarks_base webmarks_bookmarks webmarks_notes upload storage 
python manage.py migrate 
python manage.py loaddata initial_data