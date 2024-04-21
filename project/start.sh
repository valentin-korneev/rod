#!/bin/sh

case ${SERVICE_TYPE} in
  "ASGI")
    pip install daphne
    ;;
  "WSGI")
    pip install uwsgi
    ;;
esac

python manage.py db_health_check
python manage.py migrate --no-input
python manage.py create_superuser --no-input

if [ ${DEBUG} = 1 ] && [ ${SERVICE_TYPE} != "CELERY" ]
then
  python manage.py runserver 0.0.0.0:${APP_ASGI_DEV_PORT}
else
  python manage.py collectstatic --no-input --clear

  case ${SERVICE_TYPE} in
    "ASGI")
      daphne -b 0.0.0.0 -p ${APP_ASGI_PORT} config.asgi:application
      ;;
    "WSGI")
      uwsgi --ini /opt/app/uwsgi/emperor.ini
      ;;
    "CELERY")
      celery -A config worker -l info
      ;;
  esac
fi