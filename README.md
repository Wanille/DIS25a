# Clippy: Your friendly neighborhood chatbot 📎

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

## Todo implementation
- [x] add regex
- [ ] add recommendations
- [x] update requirements.txt
- [ ] add installation script
- [ ] upload models to sciebo
- [ ] add check for sentiment without ":"
- [ ] rewrite the help message with new regex conv for sentiment matching


## 🚀 Features
- Predict sentiment of Movie Reviews with:
  - naive bayes
  - logistic regression
- Tell you jokes
- Give movie recommendations based on
  - Actors
  - Runtime
  - ...
- Is a great companion


## 🔌 Installation instructions 

Create new folder `Pickles/`.
```
mkdir Pickles
```
To use first download models/vectorizer and move into folder `Pickles`.  
Create environment and install all needed requirements  
```
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

Run chatbot with `python chatbot.py`