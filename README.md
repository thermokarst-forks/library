# library

## Dev Quickstart

```
conda create -n library
source activate library
conda install pip
pip install -r requirements/local.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
