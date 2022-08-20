from base_app import app

try:
    from dash import dcc
    from dash import html
except ModuleNotFoundError:
    import dash_core_components as dcc
    import dash_html_components as html


layout = html.Div([
            html.Div(id='center_content_container', children=[
                html.P("...but we'll tell you about it anyway.", style={'text-align':'center'}),
                html.Br(),
                dcc.Markdown("**What if fortune cookies were filled with movie plots?**"),
                html.Br(),
                # html.P("You've probably wondered that many times. Or maybe you haven't - that's fine too."),
                # html.Br(),
                dcc.Markdown("""
                
                        Grab some extra buttery popcorn and test your movie knowledge with a [fortune cookie movie quiz](/quiz) or tempt fate with a [random movie fortune](/random).
                        
                        """),
                html.Br(),
                html.P("Thanks for visiting!"),  # Adventure awaits! 
                html.Br(),
                dcc.Markdown("""Got feedback? Give us a shout!
                            Create an issue in the [GitHub repo](https://github.com/EricPostMaster/fortune-cookie-movies), or even better - submit a Pull Request!
                            """
                            # This project uses spaCy to transform brief movie summaries into fortune cookie messages that will almost certainly come true...
                            ),
                html.Br(),
                
                # html.P("Idea and NLP code from")

            ],
                    className='eight columns',
                    style={'margin-left': '2.5rem'},
            ),
            html.Div(id='right_container', children=[
                html.Div([
                    html.Img(
                        src=app.get_asset_url('Fumeo9250.jpg'),
                        style={
                            'height': '100%',
                            'width': '100%',
                            'float': 'left',
                            'margin-top': '1.5rem',
                            'margin-bottom': '1.5rem',
                            'margin-right': '1.5rem'
                        },
                    ),
                ],
                    className="row"
                ),
                html.Div([
                    html.Figcaption("Fumeo 9250 projector, taken from Wikimedia Commons",
                    style={
                            'font-style': 'italic',
                            'text-align': 'center',
                            'font-size': '1.0 rem',
                            'line-height': '1.0 rem',
                        },
                    ),
                ],
                    className="row",
                ),
            ],
                className="three columns"),
        ], )
