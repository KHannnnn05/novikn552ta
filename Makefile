full_preparation:
	sudo apt-get update && sudo apt-get upgrade && sudo apt-get autoremove && sudo apt-get autoclean -y
	sudo apt-get install python3.11 -y
	sudo apt-get install python3-pip -y
	python3 -m pip install --upgrade pip
	python3 -m pip install --upgrade -r req.txt
	cd services && sudo mv * /etc/systemd/system/ && cd ..
	sudo systemctl daemon-reload
	sudo systemctl start parse.service
	sudo systemctl start parse.timer
	sudo systemctl start bot.service
	sudo systemctl start sys_update.service
	sudo systemctl start sys_update.timer
	sudo systemctl enable parse.service
	sudo systemctl enable sys_update.service
	sudo systemctl enable sys_update.timer
	sudo systemctl enable parse.timer
	sudo systemctl enable bot.service

system_update:
	sudo apt-get update && sudo apt-get upgrade && sudo apt-get autoremove && sudo apt-get autoclean -y
