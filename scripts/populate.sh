#!/bin/bash

populate_script=$(cat scripts/populate.py)

echo "$populate_script" | ./manage.py shell