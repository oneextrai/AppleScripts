import os
import requests
import argparse

# create parser
parser = argparse.ArgumentParser()

# add arguments
parser.add_argument("ProjectName")
parser.add_argument("AppName")
parser.add_argument("ProjectDirectory")

# parse the arguments
args = parser.parse_args()

def add_files():
	os.system(f'mkdir {args.ProjectDirectory}/{args.ProjectName}/{args.AppName}/static/')
	os.system(f'mkdir {args.ProjectDirectory}/{args.ProjectName}/{args.AppName}/static/css {args.ProjectDirectory}/{args.ProjectName}/{args.AppName}/static/js')
	os.system(f'mkdir {args.AppName}/templates/')
	os.system(f'mkdir {args.AppName}/templates/{args.AppName}')
	
	os.system(f'touch {args.ProjectDirectory}/{args.ProjectName}/{args.AppName}/static/js/scripts.js {args.ProjectDirectory}/{args.ProjectName}/{args.AppName}/static/css/style.css')

# SETTINGS
def update_settings():
	filename = f"{args.ProjectDirectory}/{args.ProjectName}/{args.ProjectName}/settings.py"
	with open(filename, 'r') as f:
		lines = f.readlines()

	message = ""

	for line in lines:
		if "INSTALLED_APPS = [" in line:
			line += (f"\t'{args.AppName}.apps.{args.AppName.capitalize()}Config',\n")
		message += line

	with open(filename, 'w') as f:
		f.write(message)	

# URLS
def update_app_urls():
	filename = f"{args.ProjectDirectory}/{args.ProjectName}/{args.AppName}/urls.py"

	contents = """from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home),
]"""

	with open(filename, 'w') as f:
		f.write(contents)

def update_project_urls():
	filename = f"{args.ProjectDirectory}/{args.ProjectName}/{args.ProjectName}/urls.py"
	with open(filename, 'r') as f:
		contents = f.readlines()

	message = ""
	for line in contents:	
		if "urlpatterns = [" in line:
			line += f"""\tpath('{args.AppName.lower()}/', include('{args.AppName}.urls')),\n"""
		message += line

	with open(filename, 'w') as f:
		f.write(message)

def base_html():
	filename = f"{args.ProjectDirectory}/{args.ProjectName}/{args.AppName}/templates/{args.AppName}/base.html"

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
	filename = f"{args.ProjectDirectory}/{args.ProjectName}/{args.AppName}/views.py"

	contents = f"""from django.shortcuts import render

def home(request):
    return render(request, '{args.AppName}/base.html')"""

	with open(filename, 'w') as f:
		f.write(contents)

add_files()
update_settings()
update_app_urls()
update_project_urls()
base_html()
add_home()