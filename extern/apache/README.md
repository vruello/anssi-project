# Apache2

## /etc/apache2/apache.conf

Ajouter à la fin :

```
WSGIScriptAlias / /var/www/walhid/anssi/wsgi.py
WSGIPythonPath /var/www/walhid
WSGIDaemonProcess anssi-project-web python-path=/var/www/walhid/
WSGIProcessGroup anssi-project-web

<Directory /var/www/walhid/anssi/>
<Files wsgi.py>
Require all granted
</Files>
</Directory>

```  

## /etc/apache2/envvars

```
26:export LANG=C.UTF-8
```  
