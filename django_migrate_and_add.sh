#!/bin/bash

source ./venv/bin/activate

python manage.py makemigrations
python manage.py migrate

# Add objects to Django models (replace 'YourModel' with the actual model name)
python manage.py shell <<EOF
from accounts.models import Permission

# Create and save objects
obj1 = Permission(title="salom")
obj1.save()

EOF
