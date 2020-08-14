#!/bin/bash

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

set -e

mkdir /var/www/zcam

chown -R $USER /var/www

ln -s /var/www/zcam/ ./fileserver

echo "Options +Indexes" > /var/www/zcam/.htaccess
echo "Alias /site \"/var/www/site/\"" > /etc/apache2/sites-available/zcam.conf

a2ensite zcam.conf
service apache2 restart