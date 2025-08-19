# from . import mqtt_mysql
# from .mqtt_mysql import client
import pymysql

# Start the Django project "python.exe .\manage.py runserver 0.0.0.0:8080"
# and init module "mqtt_mysql" from __init__.py from package "diango_mqtt_mysql".
# It will init module "mqtt_mysql" twice.

# one solution is using "python.exe .\manage.py runserver 0.0.0.0:8080 --noreload"

# another solution is import from views.py in package "myapp"

pymysql.install_as_MySQLdb()
