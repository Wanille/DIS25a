# Clippy: Your friendly neighborhood chatbot

![clippy-idle](animations/originals/idle.gif)  

## To Do Liste 📑
* Anfrage-Set erstellen für Chatbot - Check
* Regex schreiben für Anfragen-Matching
* Anwort-Set schreiben für Chatbot - Check
* Sentiment-Classifier auswählen + trainieren (bspw. Naive Bayes, Logistic Regression) - Check
* Evaluation von Sentiment-Classifier (Precision, Recall, F1, Accuracy) - Check
* Overlay um Ausgabe schön zu machen (Smileys, Farbiger Output, Bilder/Grafiken einfügen)
* Additional Features
  * Spellchecker
  * recommendations - Check
  * too long message - Check
  * jokes - Check
  * Folgefragen - Check
  * Error message und neustart  - Check

* Dokumentation
  * Description of IMDB dataset
  * Description of the classifier process
  * Evaluation of classifier
  * Regular Expressions, explain procedure of chatbot, discuss regex used
  * Integration from sentiment analysis into chatbot
  * Discussion


## 🚀 Features
- Predict sentiment of Movie Reviews with:
  - naive bayes
  - logistic regression
- Tells you jokes
- Give movie recommendations based on
  - Actors
  - Runtime
- Is a great companion
- Nice overlay

Works best on unix system using a shell like zsh.
But also works on Windows Powershell.

## 🔌 Installation instructions 

### 🌀 Automatic installation
```
sh installer.sh
source .env/bin/activate
pip install -r requirements.txt
```
Run chatbot with `python chatbot.py`

### 📖 Manual installation
Download Sentiment Analysis models manually from sciebo via `https://th-koeln.sciebo.de/s/s11L3TLmur4Sogx`.  
Or use `wget https://th-koeln.sciebo.de/s/lb8Kqv5Hjoteh0T/download -O Pickles.tar.gz`  
Unzip using `gunzip Pickles.tar.gz`.  
Use tar to extract files from archive `tar -xf Pickles.tar`.

You should now have a folder called Pickles inside the root of this repository containing the following three files:
- LR_Model
- NB_Model
- Vectorizer
  
Create environment and install all needed requirements  
```
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

Run chatbot with `python chatbot.py`
