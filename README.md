# Foodgram - «Продуктовый помощник»
---
Cервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Пример развернутого проекта можно посмотреть [здесь](https://sinichka.ddns.net/)
---


## Технологии:
---
```
Django==3.2.15
djangorestframework==3.12.4
Python==3.9.10
PostgreSQL
Docker
```
 
## Особенности
---
Проект запускается в четырёх контейнерах docker-compose
IMAGES | NAMES | DESCRIPTIONS
:------|:-----:|:-----------:
nginx:latest | infra_nginx_1 | контейнер HTTP-сервера 
postgres:13.10 | infra_db_1 | контейнер базы данных на PostgreSQL
foodgram_backend | 	infra_backend_1 | 	контейнер backend-части Django приложения
foodgram_frontend | infra_frontend_1 | контейнер frontend-части проекта JS-React

*Примечание: При выполнении команды docker-compose up сервис frontend подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу и будет работать через nginx.

## Запуск и работа с проектом
---
Чтобы развернуть проект, вам потребуется:

1. Создать файл .env в папке проекта /infra/ и заполнить его всеми ключами:Форкнуть репозиторий и клонировать его (не забываем создать виртуальное окружение и установить зависимости):
```
git clone https://github.com/<Ваш username на GitHub>/foodgram-project-react

source venv/Scripts/activate

cd backend/
pip install -r requirements.txt 
```

2. Создать файл .env в папке проекта /infra/ и заполнить его всеми ключами:
```
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432
DEBUG=False
SECRET_KEY=<ваш_django_секретный_ключ>
IP=<ip вашего сервера>
DAEMON=<доменное имя вашего сервера>
```
Вы можете сгенерировать ```DJANGO_SECRET_KEY``` следующим образом. Из директории проекта /backend/ выполнить:
```
python manage.py shell
from django.core.management.utils import get_random_secret_key  
get_random_secret_key()
```
Полученный ключ скопировать в ```.env```.

3. Настройте конфигурацию Nginx так, чтобы все запросы шли в контейнеры на порт 8000

Пример конфигурация nginx в файле infra/nginx.conf:
```
server {
    listen 80;
    server_name <ваш ip> <ваш domain>;
    server_tokens off;
}
```

4. Собрать контейнеры:
```
cd foodgram-project-react/infra
docker-compose up -d --build
```
При успешном создании контейнеров в терминале должен быть статус:
```
✔ Container infra-db-1         Created                                                                                                                                                             
 ✔ Container infra-frontend-1  Created                                                                                                                                                           
 ✔ Container infra-backend-1   Created                                                                                                                                                           
 ✔ Container infra-nginx-1     Created
```

5. Сделать миграции, собрать статику и создать суперпользователя:
```
docker compose exec -T backend python manage.py makemigrations --noinput
docker compose exec -T backend python manage.py migrate --noinput
docker compose exec -T backend python manage.py collectstatic --no-input
docker compose exec backend python manage.py createsuperuser
```
Теперь можно зайти в админку http://<ваш ip или domain>/admin/ под вашим логином и паролем суперпользователя и заполнить базу данных Ingredients и tags.

---
С примерами запросов можно ознакомиться в спецификации API https://<ваш domain>/api/docs/

Автор проекта:
Синицын Иван
trololo2013.lo@mail.ru
Telegram: @sSinichka
