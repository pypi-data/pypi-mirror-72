import plotly.graph_objs as go
import plotly.io as pio

pio.templates["z43_base"] = go.layout.Template(
    layout=dict(
        font=dict(
            size=14,
            family="Roboto"
        ),
        title=dict(
            x=0.5,
            font=dict(
                size=22,
                family="Roboto"
            ),
        ),
        xaxis=dict(
            title=dict(
                font=dict(
                    size=16,
                    family="Roboto"
                )
            ),
            ticks="outside"
        ),
        yaxis=dict(
            title=dict(
                font=dict(
                    size=16,
                    family="Roboto"
                )
            ),
            ticks="outside"
        ),
        images=[dict(
            x=1,
            y=0,
            sizex=0.1,
            sizey=0.1,
            source="https://github.com/odeimaiz/z43_plot_styles/blob/master/imgs/z43_logo.png?raw=true",
            opacity=0.5,
            visible=True
        )]
    )
)

pio.templates["z43_poster"] = go.layout.Template(
    layout=dict(
        font=dict(
            size=22,
            family="Roboto"
        ),
        title=dict(
            x=0.5,
            font=dict(
                size=40,
                family="Roboto"
            ),
        ),
        xaxis=dict(
            title=dict(
                font=dict(
                    size=24,
                    family="Roboto"
                )
            ),
            ticks="outside"
        ),
        yaxis=dict(
            title=dict(
                font=dict(
                    size=24,
                    family="Roboto"
                )
            ),
            ticks="outside"
        ),
        images=[dict(
            x=1,
            y=0,
            sizex=0.2,
            sizey=0.2,
            source="https://github.com/odeimaiz/z43_plot_styles/blob/master/imgs/z43_logo.png?raw=true",
            opacity=0.5,
            visible=True
        )]
    )
)


text_dark = "#FFFFFF"
text_axes_dark = "#BFBFBF"
bg_dark = "#202020"
grid_dark = "#373737"

pio.templates["z43_dark"] = go.layout.Template(
    layout=dict(
        font=dict(
            color=text_dark
        ),
        plot_bgcolor=bg_dark,
        paper_bgcolor=bg_dark,
        xaxis=dict(
            title=dict(
                font=dict(
                    color=text_axes_dark
                )
            ),
            tickfont=dict(
                color=text_axes_dark
            ),
            tickcolor=text_axes_dark,
            gridcolor=grid_dark,
            linecolor=grid_dark,
            zerolinecolor=grid_dark
        ),
        yaxis=dict(
            title=dict(
                font=dict(
                    color=text_axes_dark
                )
            ),
            tickfont=dict(
                color=text_axes_dark
            ),
            tickcolor=text_axes_dark,
            gridcolor=grid_dark,
            linecolor=grid_dark,
            zerolinecolor=grid_dark
        )
    )
)


text_light = "#000000"
text_axes_light = "#404040"
bg_light = "#DFDFDF"
grid_light = "#C8C8C8"

pio.templates["z43_light"] = go.layout.Template(
    layout=dict(
        font=dict(
            color=text_light
        ),
        plot_bgcolor=bg_light,
        paper_bgcolor=bg_light,
        xaxis=dict(
            title=dict(
                font=dict(
                    color=text_axes_light
                )
            ),
            tickfont=dict(
                color=text_axes_light
            ),
            tickcolor=text_axes_light,
            gridcolor=grid_light,
            linecolor=grid_light,
            zerolinecolor=grid_light
        ),
        yaxis=dict(
            title=dict(
                font=dict(
                    color=text_axes_light
                )
            ),
            tickfont=dict(
                color=text_axes_light
            ),
            tickcolor=text_axes_light,
            gridcolor=grid_light,
            linecolor=grid_light,
            zerolinecolor=grid_light
        )
    )
)
