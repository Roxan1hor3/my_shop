Проект інтернет магазин. Написаний на Python фреймворк Django, bd Postgres.
Фронтенд позичений і підправлений під написаний бекенд. Проект можна запустити в контейнері за допомогою докер файлів.
Є налаштована джанго админка.
Є функціонал Wishlist, Cart, налаштована авторизація з підтвердженням пошти,
можна створити замовлення і отримати повідомлення на пошту з деталями замовлення,
копони зі знижками,
фільтри за оцінкою, за тегом та за ціною для пошуку товарів,
теги,
можливість редагувати свій профіль,
пагінація сторінок товарів,
можливість добавляти коментарі під товари і ставаити їм оцінки.


my_shop

launch the project

docker-compose up --build

to launch the project, you need to make migrations

docker-compose exec web python manage.py migrate --noinput

collect static

docker-compose exec web python manage.py collectstatic --noinput
