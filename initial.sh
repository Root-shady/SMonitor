#! /bin/bash
rm -rf account/migrations 
rm -rf account/__pycache__

rm -rf rolepermission/migrations 
rm -rf rolepermission/__pycache__

rm -rf server/migrations 
rm -rf server/__pycache__

rm -rf projectlog/migrations 
rm -rf projectlog/__pycache__

rm -rf system/migrations 
rm -rf system/__pycache__

python3 manage.py migrate

python3 manage.py makemigrations account
python3 manage.py migrate account --fake


python3 manage.py makemigrations rolepermission
python3 manage.py migrate rolepermission --fake


python3 manage.py makemigrations server
python3 manage.py migrate server --fake

python3 manage.py makemigrations system
python3 manage.py migrate system --fake

python3 manage.py makemigrations projectlog
python3 manage.py migrate projectlog --fake
