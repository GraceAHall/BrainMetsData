

import pandas as pd
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import HoverTool, ColumnDataSource, CategoricalColorMapper
# from bokeh.palettes import Spectral10
output_notebook()

def _annotate_sample_meta(data_df: pd.DataFrame, meta: dict[str, dict]) -> pd.DataFrame:
    samples = data_df.index.values.tolist()
    primaries = [meta['primary'][s.split('_')[0]] for s in samples]
    commons = [meta['common'][s.split('_')[0]] for s in samples]
    genders = [meta['gender'][s.split('_')[0]] for s in samples]
    batches = [meta['batch'][s.split('_')[0]] for s in samples]

    data_df["ident"] = pd.Series(samples, dtype=str)
    data_df["primary"] = pd.Series(primaries, dtype=str)
    data_df["common"] = pd.Series(commons, dtype=str)
    data_df["gender"] = pd.Series(genders, dtype=str)
    data_df["batch"] = pd.Series(batches, dtype=str)
    return data_df

def plot_interactive(data_df: pd.DataFrame, meta: dict[str, dict], title: str, color_by: str='primary'):
    data_df = _annotate_sample_meta(data_df, meta)
    
    primary_palette = ('#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000')
    common_palette = ('#e6194b', '#3cb44b')
    gender_palette = ('#e6194b', '#3cb44b')
    batch_palette = ('#ffe119', '#4363d8', '#f58231')

    primary_mapping = CategoricalColorMapper(factors=data_df['primary'].unique(), palette=primary_palette)
    common_mapping = CategoricalColorMapper(factors=data_df['common'].unique(), palette=common_palette)
    gender_mapping = CategoricalColorMapper(factors=data_df['gender'].unique(), palette=gender_palette)
    batch_mapping = CategoricalColorMapper(factors=data_df['batch'].unique(), palette=batch_palette)

    if color_by == 'primary':
        the_field = 'primary'
        the_mapper = primary_mapping
    elif color_by == 'common':
        the_field = 'common'
        the_mapper = common_mapping
    elif color_by == 'gender':
        the_field = 'gender'
        the_mapper = gender_mapping
    elif color_by == 'batch':
        the_field = 'batch'
        the_mapper = batch_mapping
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
        color=dict(field=the_field, transform=the_mapper),
        line_alpha=0.6,
        fill_alpha=0.6,
        size=8,
        legend_label=the_field
    )
    show(plot_figure)