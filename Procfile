web: sh -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn caresense_project.wsgi --log-file -"
