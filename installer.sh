echo "\033[92mDownloading models from sciebo..\033[0m."
wget https://th-koeln.sciebo.de/s/lb8Kqv5Hjoteh0T/download -O Pickles.tar.gz
gunzip Pickles.tar.gz
tar -xf Pickles.tar
rm Pickles.tar
echo "\033[92mCreating environment...\033[0m"
python3 -m venv .env
echo "\033[92mDone. Please run '\033[94msource .env/bin/activate\033[92m' to activate the environment. And run '\033[94mpip install -r requirements.txt\033[92m' to install the requirements."
echo "Then run '\031[94mpython3 chatbot.py\033[92m' to start the program :)\031[0m"
