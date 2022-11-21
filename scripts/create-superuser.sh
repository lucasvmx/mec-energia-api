#!/bin/bash

create_script="
from users.models import CustomUser

password = 'admin'
email = 'admin@admin.com'

CustomUser.objects.create_superuser(email=email, password=password)"

echo "$create_script" | ./manage.py shell