# Define all available options in all dropdown/radio selectors 

import marimo as mo 
from dataclasses import dataclass
from typing import Callable, Optional 
from . import base_option 
from ..plot.profile import profile as profile_plotting
from ..plot import history as history_plotting 
from ..plot.profile import circle as circle_plotting 





# Plot mode: HR diagram, history vs time at fixed location in star, or profile vs interior at fixed point in time 
@dataclass 
class PlotModeOption(base_option.BaseOption): 
    pass 

# Empty because the strings include dropdowns and are displayed separately  
PLOTMODE_HRDIAGRAM = PlotModeOption(display="")
PLOTMODE_HISTORY = PlotModeOption(display=" ")
PLOTMODE_PROFILE = PlotModeOption(display="  ")

PLOTMODE_OPTIONS = [PLOTMODE_HRDIAGRAM, PLOTMODE_HISTORY, PLOTMODE_PROFILE]





# History plots: Composition, radius, or fusion vs time 
@dataclass 
class HistoryPlotOption(base_option.BaseOption): 
    plot_func: Callable  

HISTORYPLOT_COMPOSITION = HistoryPlotOption(
    display="Center composition", 
    plot_func=history_plotting.HistoryPlot.composition) 

HISTORYPLOT_RADIUS = HistoryPlotOption(
    display="Radius", 
    plot_func=history_plotting.HistoryPlot.radius) 

HISTORYPLOT_MASS = HistoryPlotOption( 
    display="Mass", 
    plot_func=history_plotting.HistoryPlot.mass)

HISTORYPLOT_FUSION = HistoryPlotOption(
    display="Fusion rate", 
    plot_func=history_plotting.HistoryPlot.fusion)

HISTORYPLOT_OPTIONS = [HISTORYPLOT_COMPOSITION, HISTORYPLOT_RADIUS, HISTORYPLOT_MASS, HISTORYPLOT_FUSION]





# Profile plots: composition, convection, etc vs interior coordinate at a fixed point in time 
@dataclass
class ProfilePlotOption(base_option.BaseOption):
    plot_func: Callable
    title_str: str 
    line_or_circle: Optional[str] = "line" 
    include: Optional[bool] = True # True = standard plots, False = experimental/extra plots 



PROFILEPLOT_COMPOSITION_CIRCLE = ProfilePlotOption(
    display="Composition (circle plot)", 
    plot_func = circle_plotting.circle_composition, 
    title_str="Compostion inside", 
    line_or_circle = "circle"
) 

PROFILEPLOT_COMPOSITION_LINE = ProfilePlotOption(
    display="Composition (line plot)", 
    plot_func=profile_plotting.ProfilePlot.composition, 
    title_str="Compostion in interior of a", 
    include = False 
) 

PROFILEPLOT_COMPOSITION_LINE_LOG = ProfilePlotOption( 
    display="Composition (line plot) (log scale)", 
    plot_func=profile_plotting.ProfilePlot.composition_log, 
    title_str="Composition in interior of a", 
    include = False 
) 



PROFILEPLOT_CONVECTION_CIRCLE = ProfilePlotOption(
    display="Convection (circle plot)", 
    plot_func = circle_plotting.circle_convection, 
    title_str="Convection inside", 
    line_or_circle="circle"
)

PROFILEPLOT_CONVECTION_CIRCLE_LOG = ProfilePlotOption( 
    display="Convection (circle plot) (log scale)", 
    plot_func = circle_plotting.circle_convection_log, 
    title_str="Convection inside", 
    line_or_circle="circle", 
    include = False 
)

PROFILEPLOT_CONVECTION_LINE = ProfilePlotOption(
    display="Convection (line plot)", 
    plot_func=profile_plotting.ProfilePlot.convection, 
    title_str="Convective regions in interior of a", 
    include = False 
)



PROFILEPLOT_FUSION_CIRCLE = ProfilePlotOption(
    display="Fusion rate (circle plot)", 
    plot_func = circle_plotting.circle_fusion, 
    title_str="Fusion inside", 
    line_or_circle="circle"
) 

PROFILEPLOT_FUSION_LINE = ProfilePlotOption(
    display="Fusion rate (line plot) (log scale)", 
    plot_func=profile_plotting.ProfilePlot.fusion, 
    title_str="Fusion in interior of a", 
    include = False 
) 



PROFILEPLOT_TEMP_CIRCLE = ProfilePlotOption(
    display="Temperature (circle plot)", 
    plot_func = circle_plotting.circle_temp, 
    title_str="Temperature inside", 
    line_or_circle="circle", 
    include = False 
)

PROFILEPLOT_TEMP_LINE = ProfilePlotOption(
    display="Temperature (line plot)", 
    plot_func=profile_plotting.ProfilePlot.temp, 
    title_str="Temperature in interior of a", 
    include = False 
)



PROFILEPLOT_MU_LINE = ProfilePlotOption( 
    display="Mass/particle (line plot)", 
    plot_func=profile_plotting.ProfilePlot.mu, 
    title_str=f"Mass/particle ($\mu$) in interior of a", 
    include = False 
)

PROFILEPLOT_TEMPGRAD_LINE = ProfilePlotOption(
    display="Temp grad (line plot)", 
    plot_func=profile_plotting.ProfilePlot.tempgrad, 
    title_str="Temperature gradient in interior of a", 
    include = False 
)

PROFILEPLOT_DEGENERACY_LINE = ProfilePlotOption( 
    display="Degeneracy (line plot)", 
    plot_func=profile_plotting.ProfilePlot.degeneracy, 
    title_str="Degeneracy of electrons and baryons inside a", 
    include = False 
) 




PROFILEPLOT_OPTIONS = [
    PROFILEPLOT_COMPOSITION_CIRCLE, 
    PROFILEPLOT_COMPOSITION_LINE, 
    PROFILEPLOT_COMPOSITION_LINE_LOG, 
    PROFILEPLOT_CONVECTION_CIRCLE, 
    PROFILEPLOT_CONVECTION_CIRCLE_LOG, 
    PROFILEPLOT_CONVECTION_LINE, 
    PROFILEPLOT_FUSION_CIRCLE, 
    PROFILEPLOT_FUSION_LINE, 
    PROFILEPLOT_TEMP_CIRCLE, 
    PROFILEPLOT_TEMP_LINE, 
    PROFILEPLOT_MU_LINE, 
    PROFILEPLOT_TEMPGRAD_LINE, 
    PROFILEPLOT_DEGENERACY_LINE, 
]









# Available model numbers dropdown, used when loading your own MESA file 
@dataclass 
class AvailableModelnumsOption(base_option.BaseOption): 
    modelnum: int 
    age: float 





# Using a list of options defined above, create a Marimo dropdown or radio selector 
def create_dropdown(options_list, default_index=0, label=""):
    options_dict = {opt.display: opt for opt in options_list} 
    dropdown = mo.ui.dropdown(options=options_dict, value=list(options_dict.keys())[default_index], label=label) 
    return dropdown 

def create_radio(options_list, default_index=0):
    options_dict = {opt.display: opt for opt in options_list}
    radio = mo.ui.radio(options=options_dict, value=list(options_dict.keys())[default_index]) 
    return radio 

    



