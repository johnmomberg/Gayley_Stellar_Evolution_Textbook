import numpy as np 

import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 

import utils.config.plot_options as plot_options 




class HRDiagram: 

    def __init__(self): 

        self.fig, self.ax = plt.subplots(figsize=(10.7, 10.7))
        
        # X axis: Temperature 
        self.ax.invert_xaxis() 
        self.ax.set_xlabel("Effective Temperature (K)", fontsize=18, labelpad=14)
        self.ax.set_xscale("log")
        self.ax.set_xlim((70000, 2000))        
        self.ax.xaxis.set_major_locator(mticker.LogLocator(base=10.0, subs=np.array([0.1, 0.2, 0.3, 0.5, 0.7]), numticks=10))
        self.ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

        # Y axis: Luminosity 
        self.ax.set_ylabel("Luminosity ($L_{{sun}}$)", fontsize=18, labelpad=14)
        self.ax.set_yscale("log")
        self.ax.set_ylim((1e-3, 1e7))

        # Grid, ticks, title 
        self.ax.tick_params(labelsize=14, length=8) 
        self.ax.grid(alpha=0.5, which="both")
        self.ax.set_title("Evolutionary Path on HR Diagram", fontsize=20, pad=15) 



    def add_path(self, history, color="tab:blue", label=None, lw=2): 
        self.ax.plot(
            10**history.log_Teff, 
            10**history.log_L, 
            color=color, 
            label=label, 
            lw=lw)



    def legend(self): 
        self.ax.legend(fontsize=14) 














# Set up the HR diagram axis with labels, limits, and spectral types labeled 
def ax_setup_hr_diagram(ax): 
    
    # X axis: Temperature 
    ax.set_xlabel('Effective Temperature (K)')
    ax.set_xlim((np.log10(2000), np.log10(70000)))
    ax.invert_xaxis() 
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda val, _: f"{10**val:.0f}"))

    # Y axis: Luminosity 
    ax.set_ylabel("Luminosity ($L_{{sun}}$)")
    ax.set_ylim((-3, 7))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda val, _: f"$10^{{{val}}}$"))

    # Add colored regions representing each spectral type 
    for spectral_type in plot_options.SPECTRAL_TYPES: 
        
        # For O spectral type, plotting to np.infty doesn't work, so replace it with the maximum value visible in the plot 
        left_side = np.log10(spectral_type.temperature_range[1])
        if left_side == np.infty: 
            left_side = ax.get_xlim()[0] 
            
        ax.axvspan(
            left_side, np.log10(spectral_type.temperature_range[0]), 
            color=spectral_type.color, alpha=0.1, label=spectral_type.letter)
        
    ax.grid(alpha=0.5)





# Add evolutionary path for a given star to the HR diagram 
def ax_plot_hr_path(ax, history, color): 

    ax.plot(history.log_Teff, history.log_L, lw=2, color=color)

    # Add point on path corresponding to Zero Age Main Sequence (ZAMS)
    try: 
        log_Teff_ZAMS = history.log_Teff[history.index_ZAMS]
        log_L_ZAMS = history.log_L[history.index_ZAMS]
        ax.scatter([log_Teff_ZAMS], [log_L_ZAMS], s=60, zorder=2, color="tab:blue", ec="black", label=f"ZAMS ({history.modelnum_ZAMS})")
    except IndexError: 
        pass 

    # Same for Terminal Age Main Sequence (TAMS)
    try: 
        log_Teff_TAMS = history.log_Teff[history.index_TAMS]
        log_L_TAMS = history.log_L[history.index_TAMS]
        ax.scatter(log_Teff_TAMS, log_L_TAMS, s=60, zorder=3, color="tab:orange", ec="black", label=f"TAMS ({history.modelnum_TAMS})")
    except IndexError: 
        pass 

    # Same for Helium ignition 
    try: 
        log_Teff_He_fusion = history.log_Teff[history.index_He_fusion]
        log_L_He_fusion = history.log_L[history.index_He_fusion]
        ax.scatter(log_Teff_He_fusion, log_L_He_fusion, s=60, zorder=4, color="tab:green", ec="black", label=f"He ignition ({history.modelnum_He_fusion})")
    except IndexError: 
        pass 





# Add model labels to points on an HR diagram, skipping some models to avoid overlapping labels 
def add_model_labels_hr_diagram(history): 

    current_xlim = plt.gca().get_xlim()
    current_ylim = plt.gca().get_ylim()
    current_xrange = np.abs(current_xlim[0] - current_xlim[1])
    current_yrange = np.abs(current_ylim[0] - current_ylim[1]) 

    # Sub-function: Add white dot + text box for model at one point 
    def add_model_point(log_Teff_current, log_L_current, modelnum_current): 
        plt.scatter(log_Teff_current, log_L_current, zorder=100, color="white", ec="black", s=10) 
        xrange_fraction_offset = 300 
        yrange_fraction_offset = 300 
        plt.text(
            log_Teff_current-current_xrange/xrange_fraction_offset, 
            log_L_current+current_yrange/yrange_fraction_offset, 
            str(modelnum_current), 
            fontsize=6, ha='left', va='bottom', zorder=100, clip_on=True, 
            bbox=dict(facecolor='white', edgecolor='black', alpha=0.7, boxstyle='round,pad=0.2'))

    def is_too_close(log_Teff, log_L, log_Teff_list, log_L_list): 
        xrange_fraction_min_spacing = 200 
        yrange_fraction_min_spacing = 100 
        for x, y in zip(log_Teff_list, log_L_list): 
            if (np.abs(x-log_Teff) < current_xrange/xrange_fraction_min_spacing) or (np.abs(y-log_L) < current_yrange/yrange_fraction_min_spacing): 
                return True 
        return False
    
    # Add label for the first model available  
    modelnum = history.model_numbers_available[0]
    index = modelnum-1 
    log_Teff = history.log_Teff[index]
    log_L = history.log_L[index]
    add_model_point(log_Teff, log_L, modelnum) 
    log_Teff_list = [log_Teff]
    log_L_list = [log_L]

    # Attempt to plot the next point 
    for modelnum in history.model_numbers_available[1:]: 
        index = modelnum-1 
        log_Teff = history.log_Teff[index]
        log_L = history.log_L[index]
        
        # Check distance from all previously labeled points
        if is_too_close(log_Teff, log_L, log_Teff_list, log_L_list):
            continue  # Skip this point

        # Otherwise, label this point
        add_model_point(log_Teff, log_L, modelnum)
        log_Teff_list.append(log_Teff)
        log_L_list.append(log_L)





def plot_HR_diagram(history, modelnum=-1, T_max=-1, T_min=-1, logL_min=-1, logL_max=-1): 

    fig = plt.figure(figsize=(15,12))
    ax = fig.add_subplot() 
    ax_setup_hr_diagram(ax) 

    if T_max != -1: 
        ax.set_xlim(np.log10(T_max), np.log10(T_min)) 
        ax.set_ylim(logL_min, logL_max) 

    ax_plot_hr_path(ax, history, "red") 
    add_model_labels_hr_diagram(history) 

    if modelnum != -1: 
        ax.scatter(
            history.log_Teff[modelnum-1], history.log_L[modelnum-1], 
            facecolors='none', edgecolors='mediumblue', s=200, linewidths=2, zorder=1000, label=f"Current pos ({modelnum})")
    
    ax.legend() 


