import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB #Import Naive Bayes

class IntentClassifier:
    def __init__(self):
        self.data = pd.read_csv('intent_classification/data.csv') # Read the CSV file
        
        self.train()                                              # It will train whenever an instance is made

    def train(self):
        X_train, y_train= self.data['text'], self.data['intent']        # x is the training data and y is the target values
        self.count_vect = CountVectorizer()                             # name for countVectorizer func. CountVectorizer tokenizes the document and count word occurances
        X_train_counts = self.count_vect.fit_transform(X_train)         # fit_transform = fit() + transform() methods. fit collects all different terms from documents (phrases) present (alphabetical order). transform counts the nummber of terms in each phrase collected by fit and outputs a term frequency matrix. 
        tfidf_transformer = TfidfTransformer()                          # tf-idf (term frequency - inverse document frequency) transforms a matrix of term/token counts and returns vectors
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts) # Calculates tf-idf for the text. Calculates the importance / relevance of words as a fractional value in a phrase amongst a collection of phrases to place less emphasis on very common words
        self.clf = MultinomialNB().fit(X_train_tfidf, y_train)          # clf = classifer. classifier is a Naive Bayes model for a multinomial distribution (similar to binomial experiment but with multiple outcomes instead of 2)
    
    def predict(self, text):
        return self.clf.predict(self.count_vect.transform([text]))[0]   # tokenizes string of user input and counts word occurances, transform count matrix to tf representation (term frequency - non fractional) more emphasis on less common words, predicts intent (target value)
                                                                        # naive bayes assumes conditional independence meaning the relationship between all input features are indeoendent
# Test 
intent_classifier = IntentClassifier()                                  # create object of IntentClassifer class for instantiation in main


print(intent_classifier.predict("I want to laugh"))

print(intent_classifier.predict("how's the temperature"))


print(intent_classifier.predict("what's the weather"))
