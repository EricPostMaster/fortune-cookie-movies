import time
from numpy import dtype
import spacy
from spacy import displacy
from spacy.matcher import Matcher
import textacy
from textacy import extract
import language_tool_python
import pickle
import re
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



def count_pronoun_types(original_document):
    nlp_doc = nlp(original_document)

    ######################
    # First chunk is seeing how many different types of pronouns are present
    pronoun_types_present = []

    for token in nlp(nlp_doc):
        if token.pos_ == "PRON":
            # this structure is great for possible debugging, but the below code block could be shortened to:
            # pronoun_types_present.extend(key for key, val in pronouns_dict.items() if str(token) in val)
            # print(token)
            for key, val in pronouns_dict.items():
                # print(key)
                # print(val)
                if str(token) in val:
                    pronoun_types_present.append(key)

    unique_pronoun_types_present = set(pronoun_types_present)

    # if len(unique_pronoun_types_present)>1:
    #     return original_document

    return len(unique_pronoun_types_present)

def pronoun_replace(original_document, i=0):
    """Replace a single family of pronouns with second-person pronouns.

    Note: This function currently only replaces pronouns in sentences containing
        a single family of pronouns, such as feminine singular (she/her) or
        third-person plural/neutral singular (they/them). If you'd like to
        improve the function, please create an issue and share your ideas!

    Parameters
    ----------
    original_document : str
        Document that needs pronouns replaced.
    
    """

    nlp_doc = nlp(original_document)

    # more concise, but possibly less readable depending on the reader's python experience:
    # pronoun_count = sum(spacy.explain(token.tag_) in ["pronoun, possessive", "pronoun, personal"] for token in nlp_doc)
    pronoun_count = 0
    for token in nlp_doc:
        if spacy.explain(token.tag_) in ["pronoun, possessive", "pronoun, personal"]:
            pronoun_count +=1

    if i == pronoun_count:
        return original_document

    # Loop replaces diff types of pronouns, similar to verb_replace
    for token in nlp_doc:
        token_tag = spacy.explain(token.tag_)

        if (token_tag == "pronoun, possessive"
            and str(token) != "your"):
            working_doc = re.sub(r'\b' + str(token) + r'\b', "your", original_document)
            i += 1
            return pronoun_replace(working_doc, i)
        
        if (token_tag == "pronoun, personal"
            and str(token) != "yourself"):
            # working_doc = original_document.replace(str(token), "yourself")
            working_doc = re.sub(r'\b' + str(token) + r'\b', "you", original_document)
            i += 1
            return pronoun_replace(working_doc, i)

    return original_document


def noun_replace(original_document):
    """Returns a list of documents. Noun chunks that meet the specified
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

    """

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

def verb_replace(original_document, i=0):
    """Returns a document replacing verbs meeting specified criteria with the
    structure "will {lemmatized verb}"
    
    Parameters
    ----------
    original_document : str
        Document in which you would like to replace verbs
    i : int
        Counter set to 0. I should put it in the function instead. I'll do that
        later because right now it's working, and changing that will probably
        magically break it... haha (sort of)
    """
    nlp_doc = nlp(original_document)

    # same as above. more concise, but possibly less readable depending on the reader's python experience:
    # verb_count = sum(token.pos_ in ['VERB', 'AUX'] for token in nlp_doc)
    verb_count = 0
    for token in nlp_doc:
        if token.pos_ in ['VERB', 'AUX']:
            verb_count +=1
    # print("vc:",verb_count)
    # print("i:",i)

    if i == verb_count:
        return original_document

    for token in nlp_doc:
        # print(token)
        # print(spacy.explain(token.tag_), '\n')
        token_tag = spacy.explain(token.tag_)

        if (token.pos_ in ['VERB', 'AUX']
            and token_tag in ["verb, 3rd person singular present"
                             ,"verb, non-3rd person singular present"]
            and token.dep_ != 'advcl'):
            # This will not work for adverbial clauses, so add that logic in later
            # working_doc = original_document.replace(str(token),f"will {token.lemma_}")
            working_doc = re.sub(r'\b' + str(token) + r'\b', f"will {token.lemma_}", original_document)
            # print("Working Doc:",working_doc)
            i += 1
            return verb_replace(working_doc, i)

    return original_document

def verb_replace_advcl(original_document):
    nlp_doc = nlp(original_document)

    # same as above. more concise, but possibly less readable depending on the reader's python experience:
    # verb_count = sum(token.pos_ in ['VERB', 'AUX'] for token in nlp_doc)
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

    return language_tool_python.utils.correct(text, matches)


if __name__ == "__main__":

    print("Testing all outputs...")

    all_outputs = []

    for k in movie_data:
        plot = movie_data[k]['plot']
    # for plot in test_cases.EXAMPLE_SENTENCES:
        unique_pronoun_types = count_pronoun_types(plot)
        if unique_pronoun_types <= 1:
            pronouns_replaced = pronoun_replace(plot)
            nouns_replaced = noun_replace(pronouns_replaced)

            current_plot_outputs = []
            for noun_plots in nouns_replaced:
                verbs_replaced = verb_replace(noun_plots)
                verbs_replaced = verb_replace_advcl(verbs_replaced)
                current_plot_outputs.append(verbs_replaced)
                print(verbs_replaced,"\n----------")

            all_outputs.append(current_plot_outputs)

    # for i in all_outputs:
    #     for j in i:
    #         print(j,"\n----------")


# plot = 'Gru meets his long-lost, charming, cheerful, and more successful twin brother Dru, who wants to team up with him for one last criminal heist.'

# unique_pronoun_types = count_pronoun_types(plot)
# if unique_pronoun_types <= 1:
#     pronouns_replaced = pronoun_replace(plot)
# nouns_replaced = noun_replace(pronouns_replaced)


# # current_plot_outputs = []
# for noun_plots in nouns_replaced:
#     verbs_replaced = verb_replace(noun_plots)
#     verbs_replaced = verb_replace_advcl(verbs_replaced)
#     print(verbs_replaced)
#     # current_plot_outputs.append(verbs_replaced)

        





# for token in nlp(plot):
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