mig:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

super:
	python manage.py createsuperuser