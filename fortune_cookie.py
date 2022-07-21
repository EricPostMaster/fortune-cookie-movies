import time
from numpy import dtype
import spacy
from spacy import displacy
from spacy.matcher import Matcher
import textacy
from textacy import extract
import language_tool_python

import test_cases

tool = language_tool_python.LanguageTool('en-US')


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


# nlp = spacy.load('en_core_web_sm')
nlp = spacy.load('en_core_web_trf')

# og_text = 'An RAF squadron is assigned to knock out a German rocket fuel factory in Norway.'
# og_text = 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.'
# og_text = 'The ninja find themselves trapped in a pyramid and must escape encroaching lava to warn Ninjago City of a new Serpentine invasion.'
# og_text ='When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.'
# og_text = 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.'
# og_text = "A cowboy doll is profoundly threatened and jealous when a new spaceman action figure supplants him as top toy in a boy's bedroom."
# og_text = 'A man raised by gorillas must decide where he really belongs when he discovers he is a human.'
og_text = "To save her father from death in the army, a young maiden secretly goes in his place and becomes one of China's greatest heroines in the process."
# og_text = 'An English soldier and the daughter of an Algonquin chief share a romance when English colonists invade seventeenth century Virginia.'
# og_text = "A poor but hopeful boy seeks one of the five coveted golden tickets that will send him on a tour of Willy Wonka's mysterious chocolate factory."


all_outputs = []

for plot in test_cases.EXAMPLE_SENTENCES:
    nlp_doc = nlp(plot)
    nouns_replaced = noun_replace(plot)

    current_plot_outputs = []
    for noun_plots in nouns_replaced:
        verbs_replaced = verb_replace(noun_plots)
        current_plot_outputs.append(verbs_replaced)
    
    all_outputs.append(current_plot_outputs)





nlp_doc = nlp(og_text)


nouns_replaced = noun_replace(og_text)


verbs_replaced = verb_replace(nouns_replaced[0])

# def pronoun_replace(original_document):







# for element in nouns_replaced:
#     print(verb_replace(element))






# transitive vs reflexive verbs - save her father vs save herself
# Not sure spaCy can tell if a verb is transitive vs reflexive
# possessive pronouns maybe






for token in nlp(verbs_replaced):
     print (token, token.lemma_, token.dep_, token.tag_, token.pos_, spacy.explain(token.tag_), token.head)

for token in nlp_doc:
     print (token, token.lemma_, token.dep_, token.tag_, token.pos_, spacy.explain(token.tag_))


for chunk in nlp(verbs_replaced).noun_chunks:
    print('noun chunk:',chunk
          ,'\nchunk root:', chunk.root.text
          ,'\nchunk dependency:', chunk.root.dep_
          ,'\nroot head text:', chunk.root.head.text
          ,'\nchunk part of speech',chunk.root.pos_
          ,'\n-------------------')





# print ([token.text for token in introduction_doc])

# for token in introduction_doc:
#      print (token, token.lemma_, token.dep_, token.tag_, token.pos_, spacy.explain(token.tag_))


displacy.serve(nlp_doc, style='dep')

# for chunk in introduction_doc.noun_chunks:
#     print('noun chunk:',chunk
#           ,'\nchunk root:', chunk.root.text
#           ,'\nchunk dependency:', chunk.root.dep_
#           ,'\nroot head text:', chunk.root.head.text
#           ,'\nchunk part of speech',chunk.root.pos_
#           ,'\n-------------------')




# Identify the subject of the sentence
# Find the noun chunk about the subject
# Change that noun chunk to "You"

# Find pronouns and change them to "yourself"

# Find the AUX verb to that noun chunk
# Lemmatize the verb
# Change that AUX verb to the future tense
# Make a rule that looks for ADV + VERB combo and adds "will" before the adverb,
## but only if the ADV+VERB combo is related to the subject.
## Exclude adverbial clauses ^^






# Expanding named entities and adding a component to the NLP pipeline object
# Example from https://spacy.io/usage/rule-based-matching#models-rules-ner
# import spacy
# from spacy.language import Language
# from spacy.tokens import Span

# nlp = spacy.load("en_core_web_sm")

# @Language.component("expand_person_entities")
# def expand_person_entities(doc):
#     new_ents = []
#     for ent in doc.ents:
#         if ent.label_ == "PERSON" and ent.start != 0:
#             prev_token = doc[ent.start - 1]
#             if prev_token.text in ("Dr", "Dr.", "Mr", "Mr.", "Ms", "Ms."):
#                 new_ent = Span(doc, ent.start - 1, ent.end, label=ent.label)
#                 new_ents.append(new_ent)
#         else:
#             new_ents.append(ent)
#     doc.ents = new_ents
#     return doc

# # Add the component after the named entity recognizer
# nlp.add_pipe("expand_person_entities", after="ner")

# doc = nlp("Dr. Alex Smith chaired first board meeting of Acme Corp Inc.")
# print([(ent.text, ent.label_) for ent in doc.ents])