#!/bin/bash

projectName=$1
appName=$2

cd ~/Desktop/Python/django/

django-admin startproject $projectName
cd $projectName

django-admin startapp $appName
cd $appName
	touch urls.py
	mkdir templates static
		cd templates
		mkdir $appName
		cd $appName
			touch base.html
		cd ../..
	cd static
		mkdir css js
		cd css
			touch style.css
		cd ..
		cd js
			touch scripts.js
			cd ../../..

open -a "Visual Studio Code" .
	