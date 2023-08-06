import os
import getpass

def deploy():
	os.system("sudo apt update && sudo apt upgrade -y")
	os.system("sudo apt install nginx supervisor python3 git")
	os.system("sudo apt install python3-venv -y")
	os.system("cd ~/ && python3 -m venv djangoEnv")
	
	os.system(". ~/djangoEnv/bin/activate && pip install gunicorn && deactivate")

	username = input("Enter your github username/Email id : ")
	password = getpass.getpass(prompt = "Enter your github password : ")
	gitlink = input("Enter your .git link : ")
	gitlink = gitlink[8:]

	li =gitlink.rindex("/")
	pdir = "/home/ubuntu/"+gitlink[li+1:].replace(".git","")


	os.system("cd ~/ && git clone https://"+username+":"+password+"@"+gitlink)

	projectDir = input("project sub path :")
	
	if projectDir not in pdir:
		pdir+="/"+projectDir

	os.system(". ~/djangoEnv/bin/activate && pip install -r "+pdir+"/requirements.txt && deactivate")

	os.system('echo "\n[program:gunicorn]\ndirectory='+pdir+'\ncommand=/home/ubuntu/djangoEnv/bin/gunicorn --workers 3 --bind unix:'+pdir+'/app.sock '+projectDir+'.wsgi:application\nautostart=true\nautorestart=true\n\n[group:guni]\nprograms:gunicorn" | sudo tee -a /etc/supervisor/conf.d/gunicorn.conf')

	os.system( "'\nserver{\n\tlisten 80;\n\tlocation /{\n\t\tinclude proxy_params;\n\t\tproxy_pass http://unix:"+pdir+"/app.sock;\n\t}\n\tlocation /static/{\n\t\tautoindex on;\n\t\talias "+pdir+"/static/;}\n\tlocation /media/ {\n\t\tautoindex on;\n\t\talias "+pdir+"/media/;  \n\t}\n}'| sudo tee -a /etc/nginx/sites-available/django.conf")

	os.system("sudo ln /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled && sudo rm default")

	os.system("sudo supervisorctl reread && sudo supervisorctl update")
	
	os.system("sudo supervisorctl reload")
 
	os.system("sudo service nginx restart")
 
	print("Django site deployment successful")
	