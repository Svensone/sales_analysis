import dash_html_components as html
from utils import Header

def create_layout(app, df):
    return html.Div(
        [
            Header(app),
            # page 6
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Findings", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.P(
                                                "Dummy Text"
                                            ),
                                            html.P(
                                                "Dummy text"
                                            ),
                                        ],
                                        style={"color": "#7a7a7a"},
                                    ),
                                ],
                                className="row",
                            ),
                            html.Div(
                                [
                                    html.H6("Further Analysis", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.Li("effects of weather on sales"),
                                            html.Li("reason why Promo2 not effective or by coincidence occur with other events"),
                                            html.Li("add socio_economic data, stores in richer regions (Munich, Schwabing) might display different sales than drugstore in rural places"),
                                        ],
                                        id="reviews-bullet-pts",
                                    ),
                                    html.Div(
                                        [
                                            html.P(
                                                "dummy text"
                                            ),
                                        ],
                                        style={"color": "#7a7a7a"},
                                    ),
                                ],
                                className="row",
                            ),
                        ],
                        className="row ",
                    )
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
