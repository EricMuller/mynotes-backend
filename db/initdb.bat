
cd ..

del  /s .\apps\webmarks_bookmarks\migrations
del  /s .\apps\webmarks_crawler\migrations
del  /s .\apps\webmarks_directory\migrations
del  /s .\apps\webmarks_notes\migrations
del  /s .\apps\webmarks_storage\migrations
del  /s .\apps\webmarks_upload\migrations
del  /s .\apps\webmarks_social\migrations


python manage.py makemigrations webmarks_social webmarks_django_contrib webmarks_directory webmarks_bookmarks webmarks_notes webmarks_upload webmarks_storage
python manage.py migrate
python manage.py loaddata initial_data
