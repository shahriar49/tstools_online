# Classes for individual projects

import tstools.utils as utils
import tstools.leaflet_tools as lft
import tstools.ccd as ccd_tools
import ipyleaflet
import datetime
import pandas as pd
import tstools.plots as plots
import ipywidgets as widgets


class ts_explorer(object):

    def __init__(self):
        ts_explorer.band_index2 = 4
        ts_explorer.pyccd_flag2 = False
        ts_explorer.minv = 0
        ts_explorer.maxv = 6000
        ts_explorer.b1 = 'SWIR1'
        ts_explorer.b2 = 'NIR'
        ts_explorer.b3 = 'RED'

    # Starting variables
    pyccd_flag2 = False
    current_band = ''
    band_index2 = 4
    click_col = ''
    point_color = ['#43a2ca']
    click_df = pd.DataFrame()
    PyCCDdf = pd.DataFrame()
    band_list = ['BLUE', 'GREEN', 'RED', 'NIR', 'SWIR1', 'SWIR2', 'BRIGHTNESS',
                 'GREENNESS', 'WETNESS']
    year_range = [1986, 2018]
    doy_range = [1, 365]

    ylim2 = plots.make_range_slider([0, 4000], -10000, 10000, 500, 'YLim:')
    xlim2 = plots.make_range_slider([2000, 2018], 1984, 2019, 1, 'XLim:')

    band_selector2 = plots.make_drop('SWIR1', band_list, 'Select band')
    image_band_1 = plots.make_drop('RED', band_list, 'Red:')
    image_band_2 = plots.make_drop('GREEN', band_list, 'Green:')
    image_band_3 = plots.make_drop('BLUE', band_list, 'Blue:')

    color_check = plots.make_checkbox(False, 'Color DOY', False)

    stretch_min = plots.make_text_float(0, 0, 'Min:')
    stretch_max = plots.make_text_float(1450, 0, 'Max:')

    pyccd_button2 = plots.make_button(False, 'Run PyCCD 2', icon='')
    clear_layers = plots.make_button(False, 'Clear Map', icon='')

    # HTML
    time_label = plots.make_html('')
    hover_label = plots.make_html('Test Value')
    text_brush = plots.make_html('Selected year range:')

    # Set axes
    # Dates
    lc1_x2 = plots.make_bq_scale('date', datetime.date(xlim2.value[0], 2, 1),
                                 datetime.date(xlim2.value[1], 1, 1))
    # DOY
    lc1_x3 = plots.make_bq_scale('linear', 0, 365)

    # Reflectance
    lc2_y2 = plots.make_bq_scale('linear', ylim2.value[0], ylim2.value[1])

    # Set plots
    lc3 = plots.make_bq_plot('scatter', [], [], {'x': lc1_x2, 'y': lc2_y2},
                             [1, 1], {'click': 'select', 'hover': 'tooltip'},
                             {'opacity': 1.0,
                              'fill': 'DarkOrange',
                              'stroke': 'Red'},
                             {'opacity': 0.5},
                             display_legend=True, labels=['Clicked point'])

    lc6 = plots.make_bq_plot('lines', [], [], {'x': lc1_x2, 'y': lc2_y2},
                             [1, 1],
                             {}, {}, {}, colors=['black'], stroke_width=3)

    lc7 = plots.make_bq_plot('scatter', [], [], {'x': lc1_x2, 'y': lc2_y2},
                             [1, 1], {}, {},
                             {}, labels=['Model Endpoint'], colors=['red'],
                             marker='triangle-up')

    lc8 = plots.make_bq_plot('scatter', [], [], {'x': lc1_x3, 'y': lc2_y2},
                             [1, 1], {'click': 'select', 'hover': 'tooltip'},
                             {'opacity': 1.0,
                              'fill': 'DarkOrange',
                              'stroke': 'Red'},
                             {'opacity': 0.5},
                             display_legend=True, labels=['Clicked point'])

    x_ax2 = plots.make_bq_axis('Date', lc1_x2, num_ticks=6, tick_format='%Y',
                               orientation='horizontal')
    x_ax3 = plots.make_bq_axis('DOY', lc1_x3, num_ticks=6,
                               orientation='horizontal')
    y_ay2 = plots.make_bq_axis('SWIR1', lc2_y2, orientation='vertical')

    # Set figures
    fig2 = plots.make_bq_figure([lc3, lc6, lc7], [x_ax2, y_ay2],
                                {'height': '300px', 'width': '100%'},
                                'Clicked TS')
    fig3 = plots.make_bq_figure([lc8], [x_ax3, y_ay2],
                                {'height': '300px', 'width': '100%'},
                                'Clicked TS')

    # Functions to interact with figures and map
    def change_yaxis2(value):
        ts_explorer.lc2_y2.min = ts_explorer.ylim2.value[0]
        ts_explorer.lc2_y2.max = ts_explorer.ylim2.value[1]

    def change_xaxis2(value):
        ts_explorer.lc1_x2.min = datetime.date(ts_explorer.xlim2.value[0], 2, 1)
        ts_explorer.lc1_x2.max = datetime.date(ts_explorer.xlim2.value[1], 2, 1)

    def hover_event(self, target):
        ts_explorer.hover_label.value = str(target['data']['x'])

    # Functions for changing image stretch
    def change_image_band1(change):
        new_band = change['new']
        ts_explorer.b1 = new_band

    def change_image_band2(change):
        new_band = change['new']
        ts_explorer.b2 = new_band

    def change_image_band3(change):
        new_band = change['new']
        ts_explorer.b3 = new_band

    # Band selection for clicked point
    def on_band_selection2(change):
        ts_explorer.plot_ts(ts_explorer.click_df, ts_explorer.lc3, 'ts')
        ts_explorer.plot_ts(ts_explorer.click_df, ts_explorer.lc8, 'doy')
        ts_explorer.y_ay2.label = ts_explorer.band_selector2.value

        if ts_explorer.pyccd_flag2:
            ts_explorer.do_pyccd2(0)

    def clear_map(b):
        lft.clear_map(ts_explorer.m, streets=True)
        ts_explorer.map_point()

    def add_image2(self, target):
        m = ts_explorer.m
        df = ts_explorer.click_df
        current_band = ts_explorer.band_list[ts_explorer.band_index2]
        click_col = ts_explorer.click_col
        stretch_min = ts_explorer.minv
        stretch_max = ts_explorer.maxv
        b1 = ts_explorer.b1
        b2 = ts_explorer.b2
        b3 = ts_explorer.b3
        lft.click_event(target, m, current_band, df, click_col, stretch_min, 
                        stretch_max, b1, b2, b3)

    def plot_ts(df, plot, plottype):
        if ts_explorer.color_check.value is True:
            color_marks = list(ts_explorer.click_df['color'].values)
        else:
            color_marks = None

        band = ts_explorer.band_selector2.value

        if plottype == 'ts':
            plots.add_plot_ts(df, plot, band=band, color_marks=color_marks)
        else:
            plots.add_plot_doy(df, plot, band=band, color_marks=color_marks)

        if ts_explorer.pyccd_flag2:
            ts_explorer.do_pyccd2(0)

    def do_draw(self, action, geo_json):
        current_band = ts_explorer.band_list[ts_explorer.band_index2]
        year_range = ts_explorer.year_range
        doy_range = ts_explorer.doy_range
        _col, _df = utils.handle_draw(action, geo_json, current_band,
                                      year_range, doy_range)
        ts_explorer.click_df = _df
        ts_explorer.click_col = _col
        ts_explorer.lc6.x = []
        ts_explorer.lc6.y = []
        ts_explorer.lc7.x = []
        ts_explorer.lc7.y = []

        ts_explorer.plot_ts(ts_explorer.click_df, ts_explorer.lc3, 'ts')
        ts_explorer.plot_ts(ts_explorer.click_df, ts_explorer.lc8, 'doy')

        if ts_explorer.color_check.value is False:
            ts_explorer.lc3.colors = list(ts_explorer.point_color)
        else:
            ts_explorer.lc3.colors = list(ts_explorer.click_df['color'].values)

    def do_pyccd2(b):
        ts_explorer.pyccd_flag2 = True
        display_legend = ts_explorer.lc7.display_legend
        dfPyCCD = ts_explorer.click_df
        band_index = ts_explorer.band_selector2.index
        results = ccd_tools.run_pyccd(display_legend, dfPyCCD, band_index)
        if band_index > 5:
            ts_explorer.lc6.y = []
            ts_explorer.lc6.x = []
            ts_explorer.lc7.y = []
            ts_explorer.lc7.x = []
            ts_explorer.lc7.display_legend = False
            return
        else:
            ccd_tools.plot_pyccd(dfPyCCD, results, band_index, (0, 4000),
                                 ts_explorer.lc6, ts_explorer.lc7)

    # Set map
    dc = ipyleaflet.DrawControl(marker={'shapeOptions': {'color': '#ff0000'}},
                                polygon={}, circle={}, circlemarker={},
                                polyline={})

    zoom = 5
    layout = widgets.Layout(width='50%')
    center = (3.3890701010382958, -67.32297252983098)
    m = lft.make_map(zoom, layout, center)
    lft.add_basemap(m, ipyleaflet.basemaps.Esri.WorldImagery)

    # Display controls interaction
    ylim2.observe(change_yaxis2)
    xlim2.observe(change_xaxis2)
    clear_layers.on_click(clear_map)
    band_selector2.observe(on_band_selection2, names='value')
    image_band_1.observe(change_image_band1, names='value')
    image_band_2.observe(change_image_band2, names='value')
    image_band_3.observe(change_image_band3, names='value')

    # PyCCD
    pyccd_button2.on_click(do_pyccd2)

    # Set plot interaction
    lc3.on_element_click(add_image2)
    lc3.tooltip = hover_label
    lc3.on_hover(hover_event)

    lc8.on_element_click(add_image2)
    lc8.tooltip = hover_label
    lc8.on_hover(hover_event)

    # Map click interaction
    dc.on_draw(do_draw)
    m.add_control(dc)
    m.add_control(ipyleaflet.LayersControl())
