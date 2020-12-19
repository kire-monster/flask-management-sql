# Portal SQL_Serv

## prerequisitos para Ubuntur server 20.04
Primero, actualizaremos el índice de paquetes locales e instalaremos los paquetes que nos permitirán crear nuestro entorno de Python.
~~~
$ apt update
$ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-virtualenv
~~~
Hacemos la instalación del servidor web
~~~
$ sudo apt-get install apache2 libapache2-mod-wsgi-py3
~~~
### instalacion - Microsoft ODBC driver for SQL Server (Linux)
para mas informacion [ver](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15#ubuntu17)
~~~
sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

#Download appropriate package for the OS version
#Choose only ONE of the following, corresponding to your OS version

#Ubuntu 16.04
curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

#Ubuntu 18.04
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

#Ubuntu 20.04
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

exit
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install msodbcsql17
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo apt-get install unixodbc-dev
~~~

## Configuración
Clonamos el repositorio
~~~
$ cd ~
$ git clone https://github.com/kire-monster/pyweb-sql.git
~~~

Creamos un entorno virtual para nuestro proyecto
~~~
$ cd ~
$ virtualenv -p /usr/bin/python3 flask
$ source flask/bin/activate
(flask) $ sudo mv pyweb-sql /var/www/html/
(flask) $ pip install -r /var/www/html/pyweb-sql/requirements.txt
(flask) $ deactivate
~~~

En el directorio /var/www/html/pyweb-sql/ hemos creado nuestra aplicación WSGI en el fichero app.wsgi, donde activamos el entorno virtual que hemos creado:

~~~
import sys
sys.path.insert(0, '/var/www/html/pyweb-sql')
activate_this = '/home/<tu_suario>/flask/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))	

from portal import app as application
~~~

Por ultimo copia el archivo que se encutra en /var/www/html/pyweb-sql/pyweb-sql.conf a la siguiente ruta: /etc/apache2/sites-available/
~~~
$ sudo cp /var/www/html/pyweb-sql/pyweb-sql.conf /etc/apache2/sites-available/
~~~

Te recomiendo desactivar la configuracion de detault y habilitar el nuestro
~~~
$ sudo a2dissite 000-default
$ sudo a2ensite pyweb-sql
$ sudo systemctl reload apache2
~~~