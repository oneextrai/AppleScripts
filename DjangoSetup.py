import argparse

# create parser
parser = argparse.ArgumentParser()

# add arguments
parser.add_argument("ProjectName")
parser.add_argument("AppName")
parser.add_argument("ProjectDirectory")

# parse the arguments
args = parser.parse_args()

# SETTINGS
def update_settings():
	with open("{}/{}/settings.py".format(args.ProjectDirectory, args.ProjectName), 'r') as f:
		lines = f.readlines()

	message = ""

	for line in lines:
		if "INSTALLED_APPS = [" in line:
			line += ("\t'{}.apps.{}Config',\n".format(args.AppName, args.AppName.capitalize()))
		if "ALLOWED_HOSTS = []" in line:
			line = "ALLOWED_HOSTS = ['192.168.1.103']"
		message += line

	with open("{}/{}/settings.py".format(args.ProjectDirectory, args.ProjectName), 'w') as f:
		f.write(message)

# URLS
def update_app_urls():
	filename = "{}/{}/urls.py".format(args.ProjectDirectory, args.AppName)

	contents = """from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home),
]"""

	with open(filename, 'w') as f:
		f.write(contents)

def update_project_urls():
	filename = "{}/{}/urls.py".format(args.ProjectDirectory, args.ProjectName)

	contents = """from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('{}.urls'))
]""".format(args.AppName)

	with open(filename, 'w') as f:
		f.write(contents)

def base_html():
	filename = "{}/{}/templates/{}/base.html".format(args.ProjectDirectory, args.AppName, args.AppName)

	contents = """{% load static %}
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
	filename = "{}/{}/views.py".format(args.ProjectDirectory, args.AppName)

	contents = """from django.shortcuts import render

def home(request):
    return render(request, '{}/base.html')""".format(args.AppName)

	with open(filename, 'w') as f:
		f.write(contents)

update_settings()
update_app_urls()
update_project_urls()
base_html()
add_home()