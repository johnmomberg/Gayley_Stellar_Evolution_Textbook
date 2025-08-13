# Define all available options in all dropdown/radio selectors 

import marimo as mo 
import utils.plotting as plotting 
from dataclasses import dataclass
from typing import Callable





# Base class: each class will need a "display" keyword so no need to copy it many times 
# Each instance of this class or a child class corresponds to one option in a particular dropdown or radio selector 
# Using a class allows me to hold all info relevant to that option, such as the plotting function that it uses 
@dataclass
class OptionBase:
    display: str # The string that is displayed next to this option in the dropdown 





# Comparison mode: No select, select mass first and compare stages, or select stage first and compare masses 
@dataclass 
class CompareModeOption(OptionBase): 
    pass 

COMPAREMODE_NOSELECTION = CompareModeOption(display="No selection") 
COMPAREMODE_MASSFIRST = CompareModeOption(display="Select mass first") 
COMPAREMODE_STAGEFIRST = CompareModeOption(display="Select stage first") 

COMPAREMODE_OPTIONS = [COMPAREMODE_NOSELECTION, COMPAREMODE_MASSFIRST, COMPAREMODE_STAGEFIRST]





# Plot mode: HR diagram, history vs time at fixed location in star, or profile vs interior at fixed point in time 
@dataclass 
class PlotModeOption(OptionBase): 
    pass 

# Empty because the strings include dropdowns and are displayed separately  
PLOTMODE_HRDIAGRAM = PlotModeOption(display="")
PLOTMODE_HISTORY = PlotModeOption(display=" ")
PLOTMODE_PROFILE = PlotModeOption(display="  ")

PLOTMODE_OPTIONS = [PLOTMODE_HRDIAGRAM, PLOTMODE_HISTORY, PLOTMODE_PROFILE]





# History plots: Composition, radius, or fusion vs time 
@dataclass 
class HistoryPlotOption(OptionBase): 
    plot_func: Callable  

HISTORYPLOT_COMPOSITION = HistoryPlotOption(
    display="Center composition", 
    plot_func=plotting.plot_history_centercomposition) 

HISTORYPLOT_RADIUS = HistoryPlotOption(
    display="Radius", 
    plot_func=plotting.plot_history_radius) 

HISTORYPLOT_FUSION = HistoryPlotOption(
    display="Fusion rate", 
    plot_func=plotting.plot_history_fusion)

HISTORYPLOT_OPTIONS = [HISTORYPLOT_COMPOSITION, HISTORYPLOT_RADIUS, HISTORYPLOT_FUSION]





# Profile plots: composition, convection, etc vs interior coordinate at a fixed point in time 
@dataclass
class ProfilePlotOption(OptionBase):
    plot_func: Callable
    title_str: str

PROFILEPLOT_COMPOSITION = ProfilePlotOption(
    display="Composition", 
    plot_func=plotting.plot_profile_composition, 
    title_str="Compostion in interior of a")

PROFILEPLOT_CONVECTION = ProfilePlotOption(
    display="Convection", 
    plot_func=plotting.plot_profile_convection, 
    title_str="Convective regions in interior of a")

PROFILEPLOT_TEMP = ProfilePlotOption(
    display="Temperature (degeneracy)", 
    plot_func=plotting.plot_profile_temp, 
    title_str="Temperature in interior of a")

PROFILEPLOT_TEMPGRAD = ProfilePlotOption(
    display="Temperature gradient (heat transport)", 
    plot_func=plotting.plot_profile_tempgrad, 
    title_str="Temperature gradient in interior of a")

PROFILEPLOT_FUSION = ProfilePlotOption(
    display="Fusion rate", 
    plot_func=plotting.plot_profile_fusion, 
    title_str="Fusion in interior of a")

PROFILEPLOT_OPTIONS = [PROFILEPLOT_COMPOSITION, PROFILEPLOT_CONVECTION, PROFILEPLOT_TEMP, PROFILEPLOT_TEMPGRAD, PROFILEPLOT_FUSION]





# Profile plot x-axis: either use mass coordinate or radius coordinate to represent the location within the interior 
@dataclass
class ProfileXAxisOption(OptionBase):
    get_values: Callable  # function that takes profile and returns the array 
    xlabel_units: str 

PROFILEXAXIS_MASS = ProfileXAxisOption(
    display="mass coordinate", 
    get_values=lambda profile: profile.mass, 
    xlabel_units="(mass coordinate ($M_{{sun}}$))" ) 

PROFILEXAXIS_RADIUS = ProfileXAxisOption(
    display="radius coordinate", 
    get_values=lambda profile: profile.radius, 
    xlabel_units="(radius coordinate ($R_{{sun}}$))" )

PROFILEXAXIS_OPTIONS = [PROFILEXAXIS_MASS, PROFILEXAXIS_RADIUS]





# Using a list of options defined above, create a Marimo dropdown or radio selector 
def create_dropdown(options_list, default_index=0):
    options_dict = {opt.display: opt for opt in options_list} 
    dropdown = mo.ui.dropdown(options=options_dict, value=list(options_dict.keys())[default_index]) 
    return dropdown 

def create_radio(options_list, default_index=0):
    options_dict = {opt.display: opt for opt in options_list}
    radio = mo.ui.radio(options=options_dict, value=list(options_dict.keys())[default_index]) 
    return radio 

    



