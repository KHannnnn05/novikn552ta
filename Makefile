all_install:
	sudo apt-get update && sudo apt-get upgrade && sudo apt-get autoremove && sudo apt-get autoclean -y
	sudo apt-get install python3.11 -y
	sudo apt-get install python3-pip -y
	python3 -m pip install --upgrade pip
	python3 -m pip install --upgrade -r req.txt

