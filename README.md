# 3sc

# for dumping data into json file
python manage.py dumpdata > filename.json
# For specific app
python manage.py dumpdata appname > filename.json


# for loading dumped data into db

python manage.py loaddata filename.json