from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp import tokenizers
from sumy.parsers.plaintext import PlaintextParser

class summarizer:
    def __init__(self,doc):
        self.toknizer = tokenizers
        self.agent = LsaSummarizer()
        self.doc = doc
    def run(self,no_sentence):
        doc_pars = PlaintextParser.from_string(self.doc,self.toknizer.Tokenizer("english"))
        summery = self.agent(doc_pars.document,no_sentence)
        return summery
