import os
import getpass

def main():
	deploy()

def deploy():
	os.system("sudo apt update && sudo apt upgrade -y")
	os.system("sudo apt install nginx supervisor python3 git")
	os.system("sudo apt install python3-venv -y")
	os.system("cd ~/ && python3 -m venv djangoEnv")



	username = input("Enter your github username/Email id : ")
	password = getpass.getpass(prompt = "Enter your github password : ")
	gitlink = input("Enter your .git link : ")
	gitlink = gitlink[8:]

	li =gitlink.rindex("/")
	pdir = "~/"+gitlink[li+1:].replace(".git","")


	os.system("cd ~/ && git clone https://"+username+":"+password+"@"+gitlink)

	projectDir = input("project sub path :")

	pdir+="/"+projectDir

	os.system(". ~/djangoEnv/bin/activate && pip install -r "+pdir+"/requirements.txt && deactivate")

	os.system('echo "\n[program:gunicorn]\ndirectory='+pdir+'\ncommand=/home/ubuntu/djangoEnv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/'+pdir+'/app.sock '+projectDir+'.wsgi:application\nautostart=true\nautorestart=true\n\n[group:guni]\nprograms:gunicorn" | sudo tee -a /etc/supervisor/conf.d/gunicorn.conf')

	os.system( "echo '\nserver\n{listen 80;\nlocation /\n{\ninclude proxy_params;\nproxy_pass http://unix:"+pdir+"/app.sock;\n}\nlocation /static/ \n{\nautoindex on;\nalias "+pdir+"/static/;}\nlocation /media/ {\nautoindex on;\nalias "+pdir+"/media/;  \n}\n}' | sudo tee -a /etc/nginx/sites-available/django.conf")
	
	os.system("sudo ln /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled && sudo rm default.conf")

	os.system("sudo supervisorctl reread && sudo supervisorctl update && sudo service nginx restart")

if __name__ == "__main__":
	main()

