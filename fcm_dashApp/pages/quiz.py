from base_app import app

try:
    from dash import dcc
    from dash import html
except ModuleNotFoundError:
    import dash_core_components as dcc
    import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from fcm_code import fortune_cookie as fc

import random
import json

# get a list of all available films/dictionary keys here to randomly select from list of films
test_cases = json.load(open("./fcm_code/test_cases.json"))
films = list(test_cases.keys())

colors = {
'background': 'rgba(255, 245, 245, 0.85)',
'title': 'rgb(26, 26, 26)',
'text': 'rgb(38, 38, 38)',
}


layout = html.Div(
            id='center_content_container', children=[

                html.P("Those who don't remember the past are destined to repeat it... "
                       "Do you remember the past? Which movie is this future from? "),

                # clicker div
                html.Div([
                    html.P('Click here to decipher your fortune...'),
                    html.Button('Quiz Me', id='clicker_quiz'),

                    html.Div(id='fortune_output',
                            #  children='Find out what your future has in store...',
                             style={'color': colors['text'],
                                    'margin-left': '10px',
                                    'padding-top': '10px',
                                    'padding-bottom': '10px'}
                             ),

                ],
                    className="five columns",
                    style={'text-align': 'center',
                           'padding-top': '3rem'}
                ),

                html.Div([
                    html.Div(id='quiz_output',
                            #  children='Find out what your future has in store...',
                             style={'color': colors['text'],
                                    'margin-left': '10px',
                                    'padding-top': '10px',
                                    'padding-bottom': '10px'}
                             ),
                        html.Div(id='answer_container',
                             children=[
                                html.P(id='movieName',
                                       style={"display": "none"}), # invisible html element that will store the correct answer to the quiz
                                html.Div(id='answer_output')
                             ],
                             style={'color': colors['text'],
                                    'margin-left': '10px',
                                    'padding-top': '10px',
                                    'padding-bottom': '10px'}
                             )
                ],
                    className="six columns offset-by-one",
                    style={'text-align': 'center',
                           'padding-top': '3rem'}
                ),

                # text below the clicker

                html.Br(),
            ],
         )


# function to generate fortune + quiz question

@app.callback(
    [Output('fortune_output', 'children'),
     Output('quiz_output', 'children'),
     Output('movieName', 'children')],
    [Input('clicker_quiz', 'n_clicks')]
)
def update_clicker_output(n_clicks_click):

    if n_clicks_click is None:
        raise PreventUpdate
    elif n_clicks_click > 0:

        print("There are this many examples to choose from:")
        print(len(films))

        film = films[random.randint(0, len(films) -1)]

        plot = test_cases[film]["originalText"]
        pronouns_replaced = fc.pronoun_replace(plot)
        nouns_replaced = fc.noun_replace(pronouns_replaced)

        current_plot_outputs = []
        for noun_plots in nouns_replaced:
            verbs_replaced = fc.verb_replace(noun_plots)
            verbs_replaced = fc.verb_replace_advcl(verbs_replaced)
            current_plot_outputs.append(verbs_replaced)

        print(len(current_plot_outputs))

        if len(current_plot_outputs) > 1:
            output = current_plot_outputs[random.randint(0, len(current_plot_outputs) -1)]
        else:
            output = current_plot_outputs[0]

        if n_clicks_click < 50:
            counter = 'By the way, you have now clicked me {} times.'.format(n_clicks_click)
        elif 49 < n_clicks_click < 100:
            counter = "By the way, you have now clicked me {} times. Easy there!".format(n_clicks_click),              
        else:
            counter = "By the way, you have now clicked me {} times. It may be time for you to move on, friend".format(n_clicks_click),

        # get list of 5 random films for the quiz options
        quiz_choices = [film]

        for i in range(len(films)):
            sel = films[random.randint(0, len(films) -1)]
            if sel in quiz_choices:
                pass 
            else: 
                quiz_choices.append(sel)
            if len(quiz_choices) == 4:
                break
    
    return (
                html.Div([
                    html.H4(output),
                    html.P(counter), 
                    html.Br(),
                ]),
                html.Div([
                    html.P("Which film should you watch in order to see how your destiny will play out?"),
                    dcc.RadioItems(id="quiz_options", options=[ {"label": i, "value": i} for i in quiz_choices], value=None )
                ]),
                film
            )
                


# function to show answer to quiz question

@app.callback(
    Output('answer_output', 'children'),
    [Input('quiz_options', 'value')],
    [State('movieName', 'children')]
)
def update_clicker_output(answer, right_answer):
    print(answer, right_answer)

    if answer is None:
        response = ""
    elif answer == right_answer:
        response = "Hurrah! You are correct! Nice job, movie buff!"
    else:
        response = "Not quite... Maybe spend some more time on Netflix and Disney+ and then try again."

    return html.H6(response)