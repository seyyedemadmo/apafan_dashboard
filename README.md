
# Apafan Dashboard Backend

backend of apafan dashboard for download in every company

![Logo](https://www.atibinco.ir/wp-content/uploads/2020/09/ati-bin-logo2.png)


## Deployment

To deploy this project run

```bash
  git clone https://github.com/seyyedemadmo/apafan_dashboard.git
  cd apafan_dashboard
```
after that we need to create some venv for run project
```bash
  python -m venv venv
```
then we need active venv 
```bash
  sh ./venv/bin/activate
  # Or
  ./venv/bin/activate
```
after that we need install the requirement of project

```bash
  pip install -r requirement.txt
```
notice: youo should install postgis and gdal-bin because this project using geometry information

now we can run the project

```bash
  python manage.py runserver 0.0.0.0:8000
```
## Authors

- [@Emad_Modaresi](https://www.github.com/seyyedemadmo)


## Badges


[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

