sudo apt-get update
sudo apt-get upgrade
if command -v python3 &>/dev/null; then
    echo Python 3 is installed
else
    cd /opt
    sudo wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tar.xz
    sudo tar xf Python-3.6.6.tar.xz
    cd Python-3.6.6/
    sudo ./configure
    sudo make
    sudo make altinstall
fi
sudo apt-get install python3-pip
sudo apt-get install python-dev
sudo apt-get install python-lxml
sudo python3.6 -m pip install --upgrade pip
sudo python3.6 -m pip install -U discord.py
sudo python3.6 -m pip install requests-xml
sudo python3.6 -m pip install wikipedia
sudo python3.6 -m pip install wiktionaryparser
sudo python3.6 -m pip install praw
sudo python3.6 -m pip install pytz
sudo python3.6 -m pip install youtube-dl
cd ~
sudo mkdir projects
cd projects
sudo mkdir logs
sudo wget https://github.com/x3l51/discord_bot/archive/master.zip
sudo unzip master.zip
sudo chmod 777 config.json
python3 setup.py