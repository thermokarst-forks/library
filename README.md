# QIIME 2 Library

## Development Quickstart

A simple docker-compose recipe is available for development:

```bash
docker compose -f docker-compose.dev.yml up --remove-orphans --build
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
