# importing modules
import os
import time
import click
import sys
from colorama import init
from termcolor import cprint
init(strip=not sys.stdout.isatty())
from pyfiglet import figlet_format


# main code
@click.command()
@click.option('--test', default=False, help="Create a test dir for your project") # option for test
@click.option('--add',  default=False, help='Write basic programs') # option to write code to programs
@click.option('--config',  default=False, help='Create a config file') # option to create a config file
@click.option('--mkenv', default=False, help='Create a virtual env for the project') # option to create a virtual env
def main(test, add, config, mkenv):
	"""flasker - Simple CLI tool to create flask project structures"""
	cprint(figlet_format('flasker'), 'green')

	# get user choice for project directory
	choice = input(f"Create the project in the current directory? : {os.getcwd()} (Y/N)")
	# set dir to current dir if choice is yes else allow user to input their own path
	curr_dir = os.getcwd() if choice.lower == 'y' else input("Enter full directory path: ")
	if choice.lower() == 'y' or choice == '':
		curr_dir = os.getcwd()

	# allow user to enter project name - name which will be given to the folder
	project_name = input("Enter a project name: ")
	cprint(f"Creating a project in {curr_dir}...", "green")
	time.sleep(1)
	try:
		os.mkdir(f"{curr_dir}/{project_name}")
		os.mkdir(f"{curr_dir}/{project_name}/app")
		if test:
			os.mkdir(f"{curr_dir}/{project_name}/app/test")
		os.mkdir(f"{curr_dir}/{project_name}/app/static")
		os.mkdir(f"{curr_dir}/{project_name}/app/{project_name}")
		os.mkdir(f"{curr_dir}/{project_name}/app/templates")
		with open(f"{curr_dir}/{project_name}/app/{project_name}/models.py", 'w') as models:
			models.write("""# your models go here""")
			models.close()
		with open(f"{curr_dir}/{project_name}/app/{project_name}/controllers.py", 'w') as controllers:
			controllers.write(f"""# your app controllers\nfrom flask import Blueprint, request, render_template, flash, g, session, redirect, url_for\nfrom flask_login import LoginManager, current_user, login_user, logout_user, login_required\nfrom app.module.models import *\n\ncontroller = Blueprint('{project_name}', __name__)\n\n@controller.route('/')\ndef index():\n\treturn "HELLO""""")
			controllers.close()
		with open(f"{curr_dir}/{project_name}/app/{project_name}/__init__.py", 'w') as init:
			init.close()
		if test:
			with open(f"{curr_dir}/{project_name}/app/test/test_config.py", "w") as write:
				write.write("# your testing configs")
				write.close()
		with open(f"{curr_dir}/{project_name}/main.py", 'w') as main_file:
			main_file.write("""from app import app\nif __name__ == "__main__":\n\tapp.run()""")
			main_file.close()
		with open(f"{curr_dir}/{project_name}/requirements.txt", 'w') as requirements:
			requirements.write("""Flask==1.1.1\nFlask-Bcrypt==0.7.1\nFlask-Login==0.5.0\nFlask-Migrate==2.5.2\nflask-restplus==0.13.0\nFlask-Script==2.0.6\nFlask-Session==0.3.1\nFlask-SQLAlchemy==2.4.1\nFlask-Testing==0.7.1""")
			requirements.close()

	except OSError as e:
		# catching folder creation error
		cprint(f"Creation of folder failed\nError: {e}", "red")
		sys.exit()
	except Exception as e:
		# catching any other error and printing it
		cprint(f"Error: {e}", 'red')
		sys.exit()
	else:
		cprint("Created project successfully", "green")

	if config:
		# if user chooses config option
		cprint("Creating config file", 'green')
		try:
			with open(f"{curr_dir}/{project_name}/config.py", 'w') as config:
				config.write("# your configs go here")
				config.close()
		except OSError as e:
			cprint(f"Creation of config failed\nError: {e}", "red")
			sys.exit()
		except Exception as e:
			cprint(f"Error: {e}", 'red')
			sys.exit()
		else:
			cprint("Created config file successfully", "green")

	if mkenv:
		# user chooses env option
		try:
			if sys.version[0] == '3':
				os.system("python3 -m venv env")
			else:
				os.system("python2 -m venv env")
		except:
			cprint("Making virtual environment failed", 'red')
			sys.exit()

if __name__ == '__main__':
	main()
