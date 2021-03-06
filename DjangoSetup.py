import requests
import argparse

# create parser
parser = argparse.ArgumentParser()

# add arguments
parser.add_argument("ProjectName")
parser.add_argument("AppName")
parser.add_argument("ProjectDirectory")
parser.add_argument("IPAddress")

# parse the arguments
args = parser.parse_args()

# SETTINGS
def update_settings():
	with open(f"{args.ProjectDirectory}/{args.ProjectName}/settings.py", 'r') as f:
		lines = f.readlines()

	message = ""

	for line in lines:
		if "INSTALLED_APPS = [" in line:
			line += (f"\t'{args.AppName}.apps.{args.AppName.capitalize()}Config',\n")
		if "ALLOWED_HOSTS = [" in line:
			line = f"""ALLOWED_HOSTS = ['192.168.1.103', '{args.IPAddress}']"""
		message += line

	with open(f"{args.ProjectDirectory}/{args.ProjectName}/settings.py", 'w') as f:
		f.write(message)	

# URLS
def update_app_urls():
	filename = f"{args.ProjectDirectory}/{args.AppName}/urls.py"

	contents = """from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home),
]"""

	with open(filename, 'w') as f:
		f.write(contents)

def update_project_urls():
	filename = f"{args.ProjectDirectory}/{args.ProjectName}/urls.py"

	contents = f"""from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('{args.AppName}.urls'))
]"""

	with open(filename, 'w') as f:
		f.write(contents)

def base_html():
	filename = f"{args.ProjectDirectory}/{args.AppName}/templates/{args.AppName}/base.html"

	contents = """{% load static %}
	<!DOCTYPE html>
	<html lang="en">
	<head>
		<meta charset="UTF-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

	    <title>Hello</title>
  
	    <link rel="stylesheet" href="{% static 'css/style.css' %}">
	</head>
	<body>
	    <h1>Hello, World</h1>
	</body>
	</html>"""

	with open(filename, 'w') as f:
		f.write(contents)

def add_home():
	filename = f"{args.ProjectDirectory}/{args.AppName}/views.py"

	contents = f"""from django.shortcuts import render

def home(request):
    return render(request, '{args.AppName}/base.html')"""

	with open(filename, 'w') as f:
		f.write(contents)

update_settings()
update_app_urls()
update_project_urls()
base_html()
add_home()