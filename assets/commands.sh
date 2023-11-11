# db to json
python manage.py dumpdata --output=test.json
# json to db
python manage.py loaddata test.json