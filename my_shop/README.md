my_shop

launch the project

docker-compose up --build

to launch the project, you need to make migrations

docker-compose exec web python manage.py migrate --noinput

collect static

docker-compose exec web python manage.py collectstatic --noinput
