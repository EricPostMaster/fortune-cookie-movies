import time
from numpy import dtype
import spacy
from spacy import displacy
from spacy.matcher import Matcher
import textacy
from textacy import extract
import language_tool_python
import pickle
# from fcm_code import test_cases

# Import the data
with open("..\\data\\movie_data.p", 'rb') as p:
    movie_data = pickle.load(p)

tool = language_tool_python.LanguageTool('en-US')

# nlp = spacy.load('en_core_web_sm')    # small spaCy English language model
nlp = spacy.load('en_core_web_trf')     # large spaCy English language model

#families of related pronouns:
pronouns_dict = {"third_male":["he", "him", "his", "himself"]
                ,"third_female":["she", "her", "hers", "herself"]
                ,"third_plural":["they", "them", "their", "theirs"
                                ,"themselves"]}


def pronoun_replace(original_document):
    '''Replace a single family of pronouns with second-person pronouns.

    Note: This function currently only replaces pronouns in sentences containing
        a single family of pronouns, such as feminine singular (she/her) or
        third-person plural/neutral singular (they/them). If you'd like to
        improve the function, please create an issue and share your ideas!

    Parameters
    ----------
    original_document : str
        Document that needs pronouns replaced.
    
    '''

    nlp_doc = nlp(original_document)

    pronoun_types_present = []

    for token in nlp(nlp_doc):
        if token.pos_ == "PRON":
            # print(token)
            for key, val in pronouns_dict.items():
                # print(key)
                # print(val)
                if str(token) in val:
                    pronoun_types_present.append(key)

    if len(pronoun_types_present)>1:
        return original_document

    # use loop to replace diff types of pronouns, similar to verb_replace
    working_doc = ""
    for token in nlp_doc:
        token_tag = spacy.explain(token.tag_)

        if token_tag == "pronoun, possessive":
            working_doc = original_document.replace(str(token), "your")
        
        # this may overwrite "you", so I'd need to put it before the
        # noun_replace function
        if token_tag == "pronoun, personal":
            working_doc = original_document.replace(str(token), "yourself")
                
    # Only return if replacements have been made
    if len(working_doc) > 0:
        return working_doc

    return original_document

def noun_replace(original_document):
    '''Returns a list of documents. Noun chunks that meet the specified
    dependency and POS criteria are replaced with 'you'.
    
    Parameters
    ----------
    original_document : string
        Document to be converted into a spacy nlp object.

    Example
    -------
    Original Document: "Bobby will cry when Alice takes the ball away."
    Returns:    ['you will cry when Alice takes the ball away.',
                'Bobby will cry when you takes the ball away.']

    '''

    labels = ["nsubj", "nsubjpass", "attr", "ROOT",
        # "pcomp","pobj","dative","appos","dobj",
    ]

    noun_mod_docs = []

    nlp_doc = nlp(original_document)

    for chunk in nlp_doc.noun_chunks:
        if chunk.root.dep_ in labels and chunk.root.pos_ in ('NOUN','PROPN'):
            second_person_doc = original_document.replace(str(chunk),'you')
            cap_second_person_doc = capitalize_first_letter(second_person_doc)
            noun_mod_docs.append(cap_second_person_doc)
    
    return noun_mod_docs

def verb_replace(original_document):
    '''Returns a document replacing verbs meeting specified criteria with the
    structure "will {lemmatized verb}"
    
    Parameters
    ----------
    original_document : str
        Document in which you would like to replace verbs
    '''

    nlp_doc = nlp(original_document)

    verb_count = 0
    for token in nlp_doc:
        if token.pos_ in ['VERB', 'AUX']:
            verb_count += 1

    if verb_count == 0:
        return original_document
    
    for token in nlp_doc:
        token_tag = spacy.explain(token.tag_)

        # Creating bail out statements (fail conditions) 

        # If the token in question isn't a verb or auxiliary verb
        # continue on to the next token in the document
        if token.pos_ not in ['VERB', 'AUX']:
            continue
        
        # If the token tag isn't a 3rd person singular present tense verb
        # or non-3rd person singular present tense verb, continue onward.
        if token_tag not in ["verb, 3rd person singular present"
                             , "verb, non-3rd person singular present"]:
            # print(f"Not a verb in 3P: Token =  \'{token}\'")
            continue

        # If the token dependency is an adverbial clause, we want to bail 
        # out early for now as this will not work for adverbial clauses; 
        # logic will be added in later
        if token.dep_ == 'advcl':
            continue

        # Now that the fail conditions are checked, 
        # we can directly use the original logic.
        # This logic will loop through the tokens in order
        # meaning we no longer need to increment i. 
        working_doc = original_document.replace(str(token),
                                                f"will {token.lemma_}")
                
        # Only return if replacements have been made
        if len(working_doc) > 0:
            return working_doc

    # Return the original if no replacements have been made.
    return original_document

def verb_replace_advcl(original_document):
    nlp_doc = nlp(original_document)

    verb_count = 0
    for token in nlp_doc:
        if token.pos_ in ['VERB', 'AUX']:
            verb_count += 1

    if verb_count == 0:
        return original_document
    
    for token in nlp_doc:
        token_tag = spacy.explain(token.tag_)

        # Bail-out statements
        if token.pos_ not in ['VERB', 'AUX']:
            continue

        if token_tag in ["verb, base form"]:
            continue

        if "you" not in [token.text for token in token.lefts]:
            continue

        working_doc = original_document.replace(str(token), token.lemma_)
                
        # Only return if replacements have been made
        if len(working_doc) > 0:
          return working_doc

    # Return the original if no replacements have been made.
    return original_document

def capitalize_first_letter(text):
    """Capitalizes the first letter of the input text if it is lowercase.
    
    Parameters
    ----------
    text : str
        The sentence that you want to check for capitalization.
    
    """
    matches = tool.check(text)

    cap_rule = lambda rule: rule.ruleId == 'UPPERCASE_SENTENCE_START'

    matches = [rule for rule in matches if cap_rule(rule)]

    new_text = language_tool_python.utils.correct(text, matches)
    
    return new_text


if __name__ == "__main__":

    print("Testing all outputs...")

    all_outputs = []

    for k in movie_data:
        plot = movie_data[k]['plot']
    # for plot in test_cases.EXAMPLE_SENTENCES:
        pronouns_replaced = pronoun_replace(plot)
        nouns_replaced = noun_replace(pronouns_replaced)

        current_plot_outputs = []
        for noun_plots in nouns_replaced:
            verbs_replaced = verb_replace(noun_plots)
            verbs_replaced = verb_replace_advcl(verbs_replaced)
            current_plot_outputs.append(verbs_replaced)

        all_outputs.append(current_plot_outputs)

    # tool.close()


    for i in all_outputs:
        for j in i:
            print(j,"\n----------")





        





# for token in nlp(all_outputs[2][0]):
#      print (token, token.lemma_, token.dep_, token.tag_, token.pos_
#             , spacy.explain(token.tag_), token.head)

# for chunk in nlp(verbs_replaced).noun_chunks:
#     print('noun chunk:',chunk
#           ,'\nchunk root:', chunk.root.text
#           ,'\nchunk dependency:', chunk.root.dep_
#           ,'\nroot head text:', chunk.root.head.text
#           ,'\nchunk part of speech',chunk.root.pos_
#           ,'\n-------------------')



# View dependency tree
# displacy.serve(nlp_doc, style='dep')