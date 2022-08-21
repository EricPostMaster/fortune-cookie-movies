from base_app import app
import random

try:
    from dash import dcc
    from dash import html
except ModuleNotFoundError:
    import dash_core_components as dcc
    import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd
import random

# get a list of all available films/dictionary keys here to randomly select from list of films
movie_plots = pd.read_csv(".\\data\\good_only_titles_and_plots.csv"
                         ,usecols=['movie_id','movie_title','plot'])



colors = {
'background': 'rgba(255, 245, 245, 0.85)',
'title': 'rgb(26, 26, 26)',
'text': 'rgb(38, 38, 38)',
}


layout = html.Div(
            id='center_content_container', children=[

                # html.P("Those who don't remember the past are destined to repeat it... "
                #        "Do you remember the past? Which movie is this future from? "),


                # clicker div
                html.Div([
                    html.P('Click here to test your knowledge...'), # decipher your fortune...'),
                    html.Button('Quiz Me', id='clicker_quiz'),

                    html.Div(id='fortune_output',
                            #  children='Find out what your future has in store...',
                             style={'color': colors['text'],
                                    'margin-left': '10px',
                                    'padding-top': '10px',
                                    'padding-bottom': '10px'}
                             ),

                ],
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

        # Subset dataset, remove duplicates, get 4 movies for quiz
        min_movies_needed = (movie_plots['movie_id'].value_counts()
                            [movie_plots['movie_id'].value_counts()>1]
                            .sum()+1)

        quiz_plots = movie_plots.sample(n=min_movies_needed, ignore_index=True)
        quiz_plots.drop_duplicates(subset='movie_id', inplace=True)
        quiz_plots = quiz_plots.head(4)

        # plot and movies list for multiple choice answers
        quiz_plot = quiz_plots.loc[0]['plot']
        quiz_answer = quiz_plots.loc[0]['movie_title']
        quiz_choices = list(quiz_plots['movie_title'])
        random.shuffle(quiz_choices)

        lucky_numbers = [random.randint(1, 99) for _ in range(6)]

        num_output = f"Lucky Numbers: {' '.join(map(str, lucky_numbers))}"

        # Message based on number of clicks
        if n_clicks_click == 1:
            counter = f"By the way, you have eaten {n_clicks_click} fortune cookie."
        elif 1 < n_clicks_click < 10:
            counter = f"By the way, you have eaten {n_clicks_click} fortune cookies."
        elif 9 < n_clicks_click < 25:
            counter = f"You've polished off {n_clicks_click} fortune cookies. Still going strong???"
        else:
            counter = f"Wow, {n_clicks_click} fortune cookies! You're the type that gets kicked out of buffets, am I right?"


    return (
                html.Div(
                        [
                        html.P(quiz_plot, style={'font-family': 'serif'}),
                        html.P(num_output, style={'font-family': 'serif'}), 
                        # html.P(counter),
                        # html.Br(),
                        ],
                        className='fc-fortune'
                ),
                html.Div([
                    html.P("Which film should you watch in order to see how your destiny will play out?"),
                    dcc.RadioItems(id="quiz_options", options=[ {"label": i, "value": i} for i in quiz_choices], value=None )
                ]),
                quiz_answer
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