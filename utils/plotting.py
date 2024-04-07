
import pandas as pd
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import HoverTool, ColumnDataSource, CategoricalColorMapper
# from bokeh.palettes import Spectral10
output_notebook()

def plot_interactive(data_df: pd.DataFrame, title: str, color_by: str='primary'):
    
    primary_palette = ('#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000')
    common_palette = ('#e6194b', '#3cb44b')
    gender_palette = ('#e6194b', '#3cb44b')
    batch_palette = ('#ffe119', '#4363d8', '#f58231')

    if color_by == 'primary':
        if 'primary' not in data_df.columns:
            raise ValueError("No 'primary' column in data_df")
        the_mapper = CategoricalColorMapper(factors=data_df['primary'].unique(), palette=primary_palette)
    elif color_by == 'common':
        if 'common' not in data_df.columns:
            raise ValueError("No 'common' column in data_df")
        the_mapper = CategoricalColorMapper(factors=data_df['common'].unique(), palette=common_palette)
    elif color_by == 'gender':
        if 'gender' not in data_df.columns:
            raise ValueError("No 'gender' column in data_df")
        the_mapper = CategoricalColorMapper(factors=data_df['gender'].unique(), palette=gender_palette)
    elif color_by == 'batch':
        if 'batch' not in data_df.columns:
            raise ValueError("No 'batch' column in data_df")
        the_mapper = CategoricalColorMapper(factors=data_df['batch'].unique(), palette=batch_palette)
    else:
        raise ValueError("Invalid color_by value")
    
    plot_figure = figure(
        title=title,
        width=1000,
        height=600,
        tools=('pan, wheel_zoom, reset')
    )
    
    plot_figure.add_tools(HoverTool(tooltips="""
    <div>
        <div>
            <span style='font-size: 16px; color: #224499'>Primary:</span>
            <span style='font-size: 16px'>@primary</span>
        </div>
        <div>
            <span style='font-size: 16px; color: #224499'>Sample:</span>
            <span style='font-size: 16px'>@ident</span>
        </div>
    </div>
    """))

    datasource = ColumnDataSource(data_df)
    plot_figure.circle(
        'x',
        'y',
        source=datasource,
        color=dict(field=color_by, transform=the_mapper),
        line_alpha=0.6,
        fill_alpha=0.6,
        size=8,
        legend_label=color_by
    )
    show(plot_figure)