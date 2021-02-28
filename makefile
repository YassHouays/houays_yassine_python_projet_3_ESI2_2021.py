# install environnement
create :
	python3 -m venv mon_projet

# active environnement
activation:
	source mon_projet/bin/activate

#install requirement.txt

requirement:
	pip install -r requirements.txt

#launch project

start:
	python3 main.py
