from base_app import app

try:
    from dash import dcc
    from dash import html
except ModuleNotFoundError:
    import dash_core_components as dcc
    import dash_html_components as html
from dash.dependencies import Input, Output

import random
import pandas as pd
import os

# get a list of all available films/dictionary keys here to randomly select from later
movie_plots = pd.read_csv(".\\data\\good_only_titles_and_plots.csv"
                         ,usecols=['movie_id','movie_title','plot'])


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
                            #  children='Find out what your future has in store...',
                             style={'color': colors['text'],
                                    'margin-left': '10px',
                                    'padding-top': '20px',
                                    'padding-bottom': '20px',
                                    # 'background-color': 'white'
                                    
                                    }
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
        return '' #'Find out what your future has in store...'
    elif n_clicks_click > 0:

        movie_index = random.randint(0, len(movie_plots) -1)
        plot_display = movie_plots['plot'].loc[movie_index]
        plot_movie = movie_plots['movie_title'].loc[movie_index]

        lucky_numbers = [random.randint(1, 99) for _ in range(6)]

        num_output = f"Lucky Numbers: {' '.join(map(str, lucky_numbers))}"

        output = plot_display

        # output = plot_display
        print("Fortune: ", plot_display)
        print("Movie: ", plot_movie)

        if n_clicks_click < 50:
            counter = 'By the way, you have now clicked me {} times.'.format(n_clicks_click)
        elif 49 < n_clicks_click < 100:
            counter = "By the way, you have now clicked me {} times. Easy there!".format(n_clicks_click),              
        else:
            counter = "By the way, you have now clicked me {} times. It may be time for you to move on, friend".format(n_clicks_click),
    
    return html.Div(
                    [
                    # html.H4(current_plot_outputs),
                    html.P(output, style={'font-family': 'serif'}),
                    html.P(num_output, style={'font-family': 'serif'}), 
                    # html.Br(),
                    ],
                    className='fc-fortune'
    )
                
