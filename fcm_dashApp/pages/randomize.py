from base_app import app

try:
    from dash import dcc
    from dash import html
except ModuleNotFoundError:
    import dash_core_components as dcc
    import dash_html_components as html
from dash.dependencies import Input, Output

from fcm_code import fortune_cookie as fc

import random
import json

# get a list of all available films/dictionary keys here to randomly select from later
test_cases = json.load(open("./fcm_code/test_cases.json"))
films = list(test_cases.keys())

colors = {
'background': 'rgba(255, 245, 245, 0.85)',
'title': 'rgb(26, 26, 26)',
'text': 'rgb(38, 38, 38)',
}

layout = html.Div(
            id='center_content_container', children=[

                html.P("Ever wished you could be in one of your favorite movies?"
                       " Well, now you can feel like you are! "),

                # clicker div
                html.Div([
                    html.P('Click here to discover your fortune...'),
                    html.Button('Click Me', id='clicker'),

                    html.Div(id='clicker_output',
                             children='Find out what your future has in store...',
                             style={'color': colors['text'],
                                    'margin-left': '10px',
                                    'padding-top': '10px',
                                    'padding-bottom': '10px'}
                             )
                ],
                    style={'text-align': 'center',
                           'padding-top': '3rem'}
                ),

                # text below the clicker
                html.Br(),
                # html.P("This app is a work in progress, so let us know if anything isn't working or if you "
                #        "have suggestions for additional features that could be added. "
                #        ),
                html.Br(),
            ],
         )


# click-me controller
@app.callback(
    Output('clicker_output', 'children'),
    [Input('clicker', 'n_clicks')]
)
def update_clicker_output(n_clicks_click):

    if n_clicks_click is None:
        return 'Find out what your future has in store...'
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
    
    return html.Div([
        # html.H4(current_plot_outputs),
        html.H4(output),
        html.P(counter), 
        html.Br(),
    ])
                
