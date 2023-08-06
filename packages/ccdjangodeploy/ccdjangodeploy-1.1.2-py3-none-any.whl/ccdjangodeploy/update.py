import os

def update():
    username = input("Enter your github username/Email id : ")
	password = getpass.getpass(prompt = "Enter your github password : ")
	gitlink = input("Enter your .git link : ")
	gitlink = gitlink[8:]

	li =gitlink.rindex("/")
	pdir = "/home/ubuntu/"+gitlink[li+1:].replace(".git","")
	os.system("cd "+pdir+" && git pull https://"+username+":"+password+"@"+gitlink)
    os.system("sudo supervisorctl reload")
	os.system("sudo service nginx restart")

if __name__ == 'main':
    update()
	
	
