import spacy
nlp = spacy.load('en_core_web_sm')


def get_nouns(doc):  
    doc = nlp(str(doc))
    current_noun = ''
    nouns = []
    for idx, token in enumerate (doc):
        if token.tag_ in ["NNP","NN","NNPS","NNS","FW","POS"] and (current_noun != []):
            if token.tag_ == 'POS':
                nouns.append(token.text)
            else:
                nouns.append(token.text)
        elif token.tag_ in ["NNP","NN","NNPS","NNS","FW"] and (current_noun == []) :
            current_noun = ''
            for pre in range(idx,0,-1):
                if doc[pre-1:pre] :
                    if doc[pre-1].tag_ in ["JJ","DT","PRP$"]:
                        current_noun= doc[pre-1].text + current_noun
                    else :
                        break
            current_noun = token.text       
            if current_noun:
                nouns.append(current_noun)
    return nouns