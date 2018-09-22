# webmarks-backend

cd mywebmarks-backend
source ./env/bin/activate
python manage.py makemigrations users webmarks_base webmarks_bookmarks webmarks_notes upload storage 
python manage.py migrate 
python manage.py loaddata initial_data


#windows10

https://www.scivision.co/python-windows-visual-c++-14-required/
https://dimitri.janczak.net/2017/05/20/python-3-6-visual-studio-2017/

#"C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
#python -m pip install -U pip setuptools
#pip install pywin32

