import os
from MyTools import MyTools as tools
from selenium.common.exceptions import WebDriverException
from time import sleep
from getpass import getpass

def get_info():
	people = []

	try:
		with open('../secret.txt', 'r') as f:
			lines = f.readlines()
		username = lines[0].strip()
		password = lines[1].strip()
	except:
		username = input("Enter linkedin username: ")
		password = getpass("Enter password: ")
	

	with tools.driver(headless=False) as driver:
		print('Logging in, please wait.')

		url = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
		driver.get(url)
		driver.execute_script('document.getElementById("username").click()')
		driver.execute_script(f'document.getElementById("username").value = "{username}"')
		driver.execute_script('document.getElementById("password").click()')
		driver.execute_script(f'document.getElementById("password").value = "{password}"')
		driver.execute_script('document.getElementsByClassName("btn__primary--large from__button--floating")[0].click()')

		driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')

		contacts = driver.execute_script('return document.getElementsByClassName("mn-connection-card__link ember-view").length')

		profile_links = [driver.execute_script(f'return document.getElementsByClassName("mn-connection-card__link ember-view")[{i}].href') for i in range(contacts)]

		for link in profile_links:
			newrl = link + 'detail/contact-info/'
			driver.get(newrl)

			name = driver.execute_script('return document.getElementById("pv-contact-info").innerText')
			print(f'Found: {name}')

			try:
				email = driver.execute_script('return document.getElementsByClassName("pv-contact-info__contact-type ci-email")[0].children[2].firstElementChild.innerText')
			except WebDriverException:
				email = 'none'

			try:
				phone = driver.execute_script('return document.getElementsByClassName("pv-contact-info__contact-type ci-phone")[0].children[2].firstElementChild.innerText')
			except WebDriverException:
				phone = 'none'

			profile_link = link

			people.append({
				'firstname':name.split(' ')[0],
				'lastname':name.split(' ')[1],
				'mobile':phone.split(' ')[0],
				'email':email
				})

	return people

def add_contacts():
	people = get_info()
	x = 1
	for i in people:
		firstname = i['firstname'][::-1]
		lastname = i['lastname'][::-1]
		mobile = i['mobile']
		email = i['email']

		os.system(f"osascript ~/Desktop/AppleScripts/AddContact.scpt \"{x}\" \"{x}\" \"{mobile}\" \"{email}\"")
		x += 1

get_info()




