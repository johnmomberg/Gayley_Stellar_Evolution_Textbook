import numpy as np 
from fractions import Fraction 

import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 

import utils.config.plot_options as plot_options 





class CustomLogLocator(mticker.Locator):
    def __init__(self, min_ticks=4):
        self.min_ticks = min_ticks

    def __call__(self):
        vmin, vmax = self.axis.get_view_interval()
        return calc_log_ticks(vmin, vmax)


def calc_log_ticks(xmin, xmax):

    def calc_next_depth(depth): 
        if depth == 0: 
            return 1 
        exp = int(np.floor(np.log10(depth)))
        mant = depth / (10**exp)  
        if mant == 1: 
            return int(depth*2) 
        if mant == 2: 
            return int(depth*2.5)
        if mant == 5: 
            return int(depth*2) 



    start_exp = int(np.floor(np.log10(xmin)))
    stop_exp = int(np.floor(np.log10(xmax)))
    depth = 0 
    f_max = 0.2   
    f_min = 0.1 
    length = np.log10(xmax / xmin) 
    array = np.array([]) 
    gaps = np.array([length]) 

    while len(array) < 4 or (np.max(gaps)>f_max*length):

        depth = calc_next_depth(depth) 

        arrs = []
        for k in range(start_exp, stop_exp+1):
            base = 10**k
            step = base / depth   # e.g. depth=2 → 500, depth=5 → 200
            arr = np.arange(base, 10*base + step, step)
            arrs.append(arr)

        array = np.unique(np.concatenate(arrs))
        array = array[(array >= xmin) & (array <= xmax)]
        array = np.append(array, xmin)
        array = np.append(array, xmax) 
        array = np.unique(array) 
        array = np.sort(array) 

        gaps = np.log10(array[1:] / array[:-1]) 

    while True:

        gaps = [] 
        for i in range(len(array)): 
            if i==0: 
                gap = np.log10(array[1]/array[0])
            elif i==len(array)-1: 
                gap = np.log10(array[i]/array[i-1])
            else: 
                next_gap = np.log10(array[i+1] / array[i])
                prev_gap = np.log10(array[i] / array[i-1])
                gap = np.min([next_gap, prev_gap])
            gaps.append(gap)

        if len(gaps) < 1 or np.min(gaps) >= f_min*length:
            break 

        array_too_close = array[np.where(gaps<f_min*length)]

        exp = np.floor(np.log10(array_too_close)) 
        mant = array_too_close / (10**exp) 
        dec = np.array([round(x%1, 10) for x in mant])
        denoms = np.array([Fraction(x).limit_denominator(100).denominator for x in dec])

        array_least_significant = array_too_close[np.where(denoms==np.max(denoms))] 
        ind_removal_candidates = np.array([np.where(array==x)[0][0] for x in array_least_significant]) 
        ind_remove = np.where(array == array[ind_removal_candidates][np.argmin(np.array(gaps)[ind_removal_candidates])])[0][0]

        array = np.delete(array, ind_remove)

    return array 





class HRDiagram: 

    def __init__(self): 

        self.fig, self.ax = plt.subplots(figsize=(10.7, 7))

        # X axis: Temperature 
        self.ax.set_xlabel("Effective Temperature (K)", fontsize=18, labelpad=14)
        self.ax.set_xscale("log")
        # self.ax.set_xlim((70000, 2000)) 
        self.ax.set_xlim((20000, 70000))
        self.ax.xaxis.set_major_locator(CustomLogLocator()) 
        self.ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}")) 
        self.ax.xaxis.set_minor_locator(mticker.NullLocator()) 
        # self.ax.invert_xaxis() 


        # Y axis: Luminosity 
        self.ax.set_ylabel("Luminosity ($L_{{sun}}$)", fontsize=18, labelpad=14)
        self.ax.set_yscale("log")
        self.ax.set_ylim((1e-3, 1e7))

        # Grid, ticks, title 
        self.ax.tick_params(labelsize=14, length=8, which="major") 
        # self.ax.tick_params(length=0, which="minor") 
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



    def label_spectraltypes(self): 

        label_positions = [st.temp_midpoint for st in plot_options.SPECTRAL_TYPES] 
        labels = [st.letter for st in plot_options.SPECTRAL_TYPES]
        tick_positions = [st.temp_range[0] for st in plot_options.SPECTRAL_TYPES]

        # Axis 1: ticks separating each spectral type
        ax_ticks = self.ax.secondary_xaxis(location="top")
        ax_ticks.set_xticks(tick_positions)
        ax_ticks.set_xticklabels([]) 
        ax_ticks.tick_params(axis="x", direction="out", length=15, which="major")  
        ax_ticks.tick_params(axis="x", direction="out", length=0, which="minor")  

        # Axis 2: labels ("O", "B", etc) in the gaps 
        ax_labels = self.ax.secondary_xaxis(location="top") 
        ax_labels.set_xticks(label_positions)
        ax_labels.set_xticklabels(labels)
        ax_labels.tick_params(axis="x", length=0, which="both")   















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


