# Apache2

## /etc/apache2/apache.conf

Ajouter à la fin : 

``̀ 
WSGIScriptAlias / /var/www/anssi-project/anssi/wsgi.py
WSGIPythonPath /var/www/anssi-project
WSGIDaemonProcess anssi-project-web python-path=/var/www/anssi-project/ 
WSGIProcessGroup anssi-project-web

<Directory /var/www/anssi-project/anssi/>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
```  

## /etc/apache2/envvars

```
26:export LANG=C.UTF-8
``̀   
