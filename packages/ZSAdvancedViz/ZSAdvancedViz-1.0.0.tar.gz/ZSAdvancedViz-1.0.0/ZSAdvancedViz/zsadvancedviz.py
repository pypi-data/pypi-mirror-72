#imports
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout
import plotly.io as pio
import cufflinks as cf


def create_theme():
    pio.templates["ZS_theme"] = go.layout.Template(
		layout_colorway=[
			'#86C8BC', '#00629B', '#6E2B62', '#B8CC7B', '#01A6DC', '#A3B2AA', '#A0AFC6', '#B6E880', '#FF97FF', '#FECB52'
		],
		# layout_plot_bgcolor= '#86C8BC',
		# layout_paper_bgcolor= '#86C8BC',
		layout_font={'color': '#000000'},
		layout_xaxis={
			'automargin': True,
			'title': 'x axis title',
			# 'titlefont_size':20,
			'linecolor': '#0000cc',
			'ticks': '',
			'zerolinecolor': '#283442',
			'zerolinewidth': 0,
			# 'gridcolor': '#283442'
		},
		layout_yaxis={
			'automargin': True,
			'title': 'y axis title',
			# 'titlefont_size':20,
			'linecolor': '#0000cc',
			'ticks': '',
			'zerolinecolor': '#283442',
			'zerolinewidth': 0,
			# 'gridcolor': '#283442'
		},
		layout_coloraxis={
			'colorbar': {'outlinewidth': 0,
						 'ticks': ''}
		},
		layout_hovermode='closest',
		layout_hoverlabel={'align': 'left',
						   'bgcolor': 'white',
						   'font_size': 15,
						   'font_color': '#86C8BC',
						   'bordercolor': '#0000cc'
						   },

	)
    plotly_template = pio.templates["ZS_theme"]



def data_preparation(dataDF, x_data_cols, y_data_cols, y_data_names, chart_type):
    #array of cols, x-axis, name of metric
    data_list = []
    if chart_type == 'line':
        data_list.append(
            go.Scatter(
                x = dataDF[x_data_cols[0]],
                y = dataDF[y_data_cols[0]],
                mode = 'lines'
            )
        )
    elif chart_type == 'multiline':
        for i in range(len(y_data_cols)):
             data_list.append(
                go.Scatter(
                    x = dataDF[x_data_cols[0]],
                    y = dataDF[y_data_cols[i]],
                    name = y_data_names[i],
                    mode = 'lines+markers'
                )
            )
    elif chart_type == 'bar_single':
        data_list.append(
            go.Bar(
                x = dataDF[x_data_cols[0]],
                y = dataDF[y_data_cols[0]],
                name=y_data_names[0]
            )
        )
    elif (chart_type == 'bar_grp' or chart_type == 'bar_stack'):  
        for i in range(len(y_data_cols)):
            data_list.append(
                go.Bar(
                     x=dataDF[x_data_cols[0]].drop_duplicates(),
                     y=dataDF[y_data_cols[i]],
                     name=y_data_names[i]
                )
            ) 
    return data_list

def ZS_line(dataDF, chart_attr_dict, x_data_cols, y_data_cols):
    '''
        This method is used to plot line chart
        :param x_data_cols: columns for x data values of type list<String>
        :param y_data_cols: columns for y data values of type list<string>
        :param chart_attr_dict: chart attributes of type dict
        :return: chart
    '''
    create_theme()
    data = data_preparation(dataDF, x_data_cols, y_data_cols, None, 'line')
    layout = go.Layout(
                title=chart_attr_dict.chart_title,
                xaxis=dict(title=chart_attr_dict.chart_xAxis_title),
                yaxis=dict(title=chart_attr_dict.chart_yAxis_title)
            )
    fig = go.Figure(data = data, layout = layout)
    fig.update_layout(template = chart_attr_dict.chart_theme)
    fig.show()


def ZS_multiline(dataDF, chart_attr_dict, x_data_cols, y_data_cols, y_data_names):
    '''
        This method is used to plot group bar chart
        :param x_data_cols: columns for x data values of type list<String>
        :param y_data_cols: columns for y data values of type list<string>
        :param chart_attr_dict: chart attributes of type dict
        :return: chart
    '''
    create_theme()
    data = data_preparation(dataDF, x_data_cols, y_data_cols, y_data_names, 'multiline')
    layout = go.Layout(
                title=chart_attr_dict.chart_title,
                xaxis=dict(title=chart_attr_dict.chart_xAxis_title),
                yaxis=dict(title=chart_attr_dict.chart_yAxis_title)
            )
    fig = go.Figure(data = data, layout = layout)
    fig.update_layout(template = chart_attr_dict.chart_theme)
    return fig.show()


def ZS_bar(dataDF, chart_attr_dict, x_data_cols, y_data_cols, y_data_names, bar_type):
    '''
        This method is used to plot bar chart
        :param x_data_cols: columns for x data values of type list<String>
        :param y_data_cols: columns for y data values of type list<string>
        :param chart_attr_dict: chart attributes of type dict
        :return: chart
    '''
    create_theme()
    data = data_preparation(dataDF, x_data_cols, y_data_cols, y_data_names, bar_type)
    layout = go.Layout(
                title=chart_attr_dict['chart_title'],
                xaxis=dict(title=chart_attr_dict['chart_xAxis_title']),
                yaxis=dict(title=chart_attr_dict['chart_yAxis_title'])
            )
    fig = go.Figure(data = data, layout = layout)
    if bar_type == 'bar_stack':
            fig.update_layout(barmode='stack')
    fig.update_layout(template = chart_attr_dict['chart_theme'])
    fig.show()


def ZS_pie(dataDF, chart_attr_dict, data_labels, data_values):
    '''
        This method is used to plot pie chart
        :param data_labels: labels for sections of type list<String>
        :param data_values: data values for sections of type list<string>
        :param chart_attr_dict: chart attributes of type dict
        :return: chart
    '''
    create_theme()
    data = [go.Pie(
                labels=data_labels, 
                values=data_values, 
                textinfo='percent',
                insidetextorientation='radial'
                    )]
    layout = go.Layout(
        title=chart_attr_dict.chart_title,
    )
    fig = go.Figure(data = data, layout = layout)
    fig.update_layout(template = chart_attr_dict.chart_theme)
    fig.show()



