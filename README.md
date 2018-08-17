# library

## Dev Quickstart

```
conda create -n library
source activate library
conda install pip
pip install -r requirements/local.txt
createdb qiime2-library
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
