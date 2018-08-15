sudo apt-get update
sudo apt-get upgrade
cd /opt
sudo wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tar.xz
sudo tar xf Python-3.6.6.tar.xz
cd Python-3.6.6/
sudo ./configure
sudo make
sudo make altinstall
sudo apt-get install python-dev
sudo apt-get install python-lxml
sudo python3.6 -m pip install --upgrade pip
sudo python3.6 -m pip install -U discord.py
sudo python3.6 -m pip install requests-xml
sudo python3.6 -m pip install wikipedia
sudo python3.6 -m pip install wiktionaryparser
sudo python3.6 -m pip install praw
sudo python -m pip install pytz
cd ~
sudo mkdir projects
cd projects
sudo wget https://github.com/x3l51/discord_bot/archive/master.zip
sudo unzip master.zip
sudo chmod 777 credentials.log
sudo chmod 777 members.log
python3.6 setup.py
python3.6 bcad_bot_3.6.py
