# QIIME 2 Library

## Development Quickstart

You will need a pg database (set the connection info in `DATABASE_URL`), and
a rabbitmq message-broker (set the connection info in `RABBITMQ_URL`). The
`DJANGO_SETTINGS_MODULE` needs to be set to `config.settings.local`.

```bash
conda create -n library python=3.8
conda activate library
pip install -r requirements/local.txt
createdb qiime2-library
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver
```

A simple docker-compose recipe is available for development:

```bash
docker-compose up --build
```

## Production Environment Variables

- `ADMINS`
- `ALLOWED_HOSTS`
- `DATABASE_URL`
- `RABBITMQ_URL`
- `CElERY_BROKER_URL`
- `DISCOURSE_SSO_SECRET`
- `DJANGO_SETTINGS_MODULE`
- `GOOGLE_ANALYTICS_PROPERTY_ID`
- `SECRET_KEY`
- `AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY`
- `AWS_SES_REGION_NAME=YOUR_AWS_SES_REGION_NAME`
- `AWS_SES_REGION_ENDPOINT=YOUR_AWS_REGION_ENDPOINT`

## Misc

- `openssl rand -base64 66 | tr -d '\n'`
