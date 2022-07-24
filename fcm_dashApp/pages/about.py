from base_app import app

try:
    from dash import dcc
    from dash import html
except ModuleNotFoundError:
    import dash_core_components as dcc
    import dash_html_components as html


layout = html.Div([
            html.Div(id='center_content_container', children=[
                html.P("...but we'll tell you a bit about it anyway."),
                html.Br(),
                dcc.Markdown("""

                        **What if fortune cookies were filled with movie plots?**

                        You've probably wondered that many times. Or maybe you haven't - that's fine too.

                        This repo is a project currently in progress to create some sort of application using spaCy to transform brief movie synopses into fortune cookie statements and, hopefully, a web app that will be fun to use.

                        Thanks for visiting!
                        
                        """),
                html.Br(),
                html.P("This app is a work in progress, so let us know if anything isn't working or if you "
                       "have suggestions for additional features that could be added. "
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
