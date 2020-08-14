#!/bin/bash

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

set -e

site=zcam

mkdir /var/www/$site

chown -R $USER /var/www

ln -s /var/www/$site/ ./fileserver

echo "Options +Indexes" > /var/www/$site/.htaccess
echo "Alias /$site \"/var/www/$site/\"" > /etc/apache2/sites-available/$site.conf

a2ensite $site.conf
service apache2 restart