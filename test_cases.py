# This is to store some of the example sentences at the bottom of 
# the fortune_cookie.py file and create a type of test structure
# to see if the functions produce the correct output.

EXAMPLE_SENTENCES = [
'An RAF squadron is assigned to knock out a German rocket fuel factory in Norway.'
, 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.'
, 'The ninja find themselves trapped in a pyramid and must escape encroaching lava to warn Ninjago City of a new Serpentine invasion.'
, 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.'
, 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.'
, "A cowboy doll is profoundly threatened and jealous when a new spaceman action figure supplants him as top toy in a boy's bedroom."
, 'A man raised by gorillas must decide where he really belongs when he discovers he is a human.'
, "To save her father from death in the army, a young maiden secretly goes in his place and becomes one of China's greatest heroines in the process."
, 'An English soldier and the daughter of an Algonquin chief share a romance when English colonists invade seventeenth century Virginia.'
, "A poor but hopeful boy seeks one of the five coveted golden tickets that will send him on a tour of Willy Wonka's mysterious chocolate factory."
]

EXPECTED_OUTPUT = [
"You will be assigned to knock out a German rocket fuel factory in Norway."
, "You from the Shire and eight companions will set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron."
, "You will find yourself trapped in a pyramid and must escape encroaching lava to warn Ninjago City of a new Serpentine invasion."
, "When you known as the Joker will wreak havoc and chaos on the people of Gotham, Batman will accept one of the greatest psychological and physical tests of his ability to fight injustice."
, "You will bond over a number of years, finding solace and eventual redemption through acts of common decency."
, "You will be profoundly threatened and jealous when a new spaceman action figure supplants him as top"

# The following output is a tricky case as the model verb 'must' 
# effectively shows "future" via a currently unfulfilled obligation.  
# The model will likely mislabel or decide that "must decide" will become
# "must will decide" which is incorrect
, "You raised by gorillas must decide where you really will belong when you discover you are a human."
, "To save your father from death in the army, you secretly will go in his place and become one of China's greatest heroines in the process."
, "You will share a romance when English colonists invade seventeenth century Virginia."

# This one is also slightly awkward to convert to "you" + future tense.
# The following removes the clause that modifies the original NP
, "You will seek one of the five coveted golden tickets that will send you on a tour of Willy Wonka's mysterious chocolate factory."
]
