wget -O - http://sgjp.pl/apt/sgjp.gpg.key|sudo apt-key add -
sudo add-apt-repository 'deb http://sgjp.pl/apt/ubuntu trusty main'
sudo apt-get update
sudo apt-get install libmorfeusz2 morfeusz2 morfeusz2-dictionary-sgjp python-morfeusz2