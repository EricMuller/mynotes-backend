
rm -R ./apps/webmarks_bookmarks/migrations
rm -R ./apps/webmarks_crawler/migrations
rm -R ./apps/webmarks_directory/migrations
rm -R ./apps/webmarks_notes/migrations
rm -R ./apps/webmarks_storage/migrations
rm -R ./apps/webmarks_upload/migrations
rm -R ./apps/webmarks_users/migrations


source ./env/bin/activate
python manage.py makemigrations webmarks_users webmarks_django_contrib webmarks_directory webmarks_bookmarks webmarks_notes webmarks_upload webmarks_storage 
python manage.py migrate
python manage.py loaddata initial_data