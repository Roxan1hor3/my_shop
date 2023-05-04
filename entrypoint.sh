python manage.py makemigrations --noinput
python manage.py migrate --noinput
gunicorn my_shop.wsgi:application --bind 0.0.0.0:8000
