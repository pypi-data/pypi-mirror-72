#imports
import pandas as pd
import numpy as np

import plotly.graph_objs as go
# from scipy import stats

import plotly.io as pio


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
# hover template - do define what to show on tooltip
plotly_template = pio.templates["ZS_theme"]

def zs_bubble(x_data_list,y_data_list, z_data_list):
    '''
    This method is used to plot bubblechart
    :param x_data_list: x data values of type list<int>
    :param y_data_list: y data values of type list<int>
    :param z_data_list: this decides the marker size. Data type expected: list<int>
    :return: None
    '''
    #ToDo: Right now, marker size can only be between 0-100, if we give exact size as in the case of high charts, the
    # bubbles are covering the chart, right now, we are scaling the values using z-score and cdf and displaying the marker
    # 1) we need to figure out if there is a better way
    # 2) figure out how to display actual values while hovering over the bubble
    fig = go.Figure(data=[go.Scatter(
        x=x_data_list, y=y_data_list,
        mode='markers',
        marker_size=z_data_list)
    ])
    fig.update_layout(template='ZS_theme')
    fig.show()

def zs_heatmap(x_data_list, y_data_list, z_data_list):
    '''
    This method is used to plot heatmap
    :param x_data_list: x data values of type list<String>
    :param y_data_list: y data values of type list<string>
    :param z_data_list: z data values of type list<list<int>>
    :return:
    '''
    #ToDo: Add x-title, y-title and chart title
    fig = go.Figure(data=go.Heatmap(
        z=z_data_list,
        x=x_data_list,
        y=y_data_list,
        # hoverongaps=False
        ))
    fig.update_layout(template='ZS_theme')
    fig.show()

def _z_score(values):
    '''function that converts values in z-scores'''
    # calculate mean and std
    mean, std = np.mean(values), np.std(values)
    if std != 0:
        return [(x - mean) / std for x in values]
    else:
        return [1 / len(values) for x in values]

####################bubble chart##########################
# df = pd.read_csv('dummy_Data.csv')
df = {'Months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
   'Product': ['A', 'B', 'C'],
   'z': [[4878.33, 5085.508, 4707.289000000001, 4900.915, 4575.376,
          4460.7609999999995, 4984.863, 4908.686, 4370.1359999999995, 4587.643,
          4545.523, 4440.393], [1234.0, 3245.0, 654.0, 2346.0, 1234.0, 7653.0,
                                8975.0, 3456.0, 123.0, 4568.0, 1234.0, 6543.0], [1234.0, 987.0, 4589.0,
                                                                                 3246.0, 728.0, 35921.0, 1389.0, 3257.0,
                                                                                 1493.0, 9614.0, 2692.0, 1379.0],
         [4878.33, 5085.508, 4707.289000000001, 4900.915, 4575.376,
          4460.7609999999995, 4984.863, 4908.686, 4370.1359999999995, 4587.643,
          4545.523, 4440.393], [1234.0, 3245.0, 654.0, 2346.0, 1234.0, 7653.0,
                                8975.0, 3456.0, 123.0, 4568.0, 1234.0, 6543.0], [1234.0, 987.0, 4589.0,
                                                                                 3246.0, 728.0, 35921.0, 1389.0, 3257.0,
                                                                                 1493.0, 9614.0, 2692.0, 1379.0],
         [4878.33, 5085.508, 4707.289000000001, 4900.915, 4575.376,
          4460.7609999999995, 4984.863, 4908.686, 4370.1359999999995, 4587.643,
          4545.523, 4440.393], [1234.0, 3245.0, 654.0, 2346.0, 1234.0, 7653.0,
                                8975.0, 3456.0, 123.0, 4568.0, 1234.0, 6543.0], [1234.0, 987.0, 4589.0,
                                                                                 3246.0, 728.0, 35921.0, 1389.0, 3257.0,
                                                                                 1493.0, 9614.0, 2692.0, 1379.0]]
   }
# df = pd.DataFrame.from_dict(df2)
# zs_bubble(x_data_list=[60,20,30], y_data_list=[20,12,15],z_data_list=stats.norm.cdf(_z_score(df.groupby(['Product']).sum().Trx.to_list()))*100)
##########################################################


####################heatmap###############################
# heat_data_list = []
# data_temp = df.groupby(['Product'])
# for name, group in data_temp:
#     heat_data_list.append(group['Trx'].to_list())

# zs_heatmap(x_data_list=list(df.Months.unique()),y_data_list=list(df.Product.unique()),z_data_list=heat_data_list)
zs_heatmap(x_data_list=list(df['Months']),y_data_list=list(df['Product']),z_data_list=df['z'])
#########################################################




