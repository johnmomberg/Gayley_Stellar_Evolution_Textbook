import numpy as np 
from fractions import Fraction 

import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 

import utils.config.plot_options as plot_options 





class MajorLogLocator(mticker.Locator):
    def __init__(self):
        pass 

    def __call__(self):
        left, right = self.axis.get_view_interval() 
        return calc_log_ticks(left, right)



class MinorLogLocator(mticker.Locator):
    def __init__(self):
        pass 

    def __call__(self):
        left, right = self.axis.get_view_interval() 
        return calc_log_ticks(left, right, remove_overlaps=False)





# Do not ask me how this works. Too lazy to add comments right now 
def calc_log_ticks(left, right, remove_overlaps=True):
    xmin = np.min([left, right])
    xmax = np.max([left, right])



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
        


    def calc_gaps(input_array, minmax_func=np.min): 

        # Get sorting indices
        sort_idx = np.argsort(input_array)
        sorted_array = input_array[sort_idx]

        # Calculate gaps 
        gaps = [] 
        for i in range(len(sorted_array)): 
            if i==0: 
                gap = np.log10(sorted_array[1]/sorted_array[0])
            elif i==len(sorted_array)-1: 
                gap = np.log10(sorted_array[i]/sorted_array[i-1])
            else: 
                next_gap = np.log10(sorted_array[i+1] / sorted_array[i])
                prev_gap = np.log10(sorted_array[i] / sorted_array[i-1])
                gap = minmax_func([next_gap, prev_gap])
            gaps.append(gap)
        gaps = np.array(gaps)

        # Invert the sorting to get back to original order
        inverse_idx = np.argsort(sort_idx)
        unsorted_gaps = gaps[inverse_idx]

        return unsorted_gaps 



    start_exp = int(np.floor(np.log10(xmin)))
    stop_exp = int(np.floor(np.log10(xmax)))
    depth = 0 
    f_max = 0.5  
    f_min = 0.1
    length = np.log10(xmax / xmin) 
    array = np.array([]) 
    gaps = np.array([length]) 



    # Keep subdividing until the largest gap between ticks is smaller than f_max 
    # This will mean the smallest gaps are way too small, but we will remove those points in the next step 
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

        gaps = calc_gaps(array, minmax_func=np.max) 



    # First, check if we even want to remove overlapping points. 
    # If this is for minor tick LINES, leave overlapping points in so the gridline spacing 
    # matches what you would expect for a log plot, but for major tick LABELS, we don't want any text to overlap. 
    # When removing overlapping points, prioritize keeping "nicer" numbers. 
    # Example: If 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60 etc were the initial labels: 
    # First get rid of 0.1 numbers (what's left: 6, 8, 10, 20, 40, etc)
    # Then get rid of 0.2 numbers (what's left: 5, 10, 15, 20, 25)
    # Then get rid of 0.5 numbers (what's left: 10, 100, 1000) 
    # Prioritize keeping 0.0
    # Keep removing points until no remaining labels are overlapping/too close 
    while remove_overlaps==True:

        gaps = calc_gaps(array) 

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








class SpectralTypeBorderLocator(mticker.Locator):
    def __init__(self):
        pass 

    def __call__(self):
        tick_positions = [st.temp_range[0] for st in plot_options.SPECTRAL_TYPES]
        return tick_positions 





class SpectralTypeLabelLocator(mticker.Locator):
    def __init__(self):
        pass 

    def __call__(self):
        
        window_left, window_right = self.axis.get_view_interval() 

        label_positions = [] 

        for spectral_type in plot_options.SPECTRAL_TYPES: 

            st_mid = spectral_type.temp_midpoint 
            st_right, st_left = spectral_type.temp_range 

            if window_left > st_left and st_right > window_right: 
                label_positions.append(st_mid)
            elif window_left > st_left and st_left > window_right > st_right: 
                label_positions.append(np.sqrt(st_left*window_right))
            elif st_right > window_right and st_left > window_left > st_right: 
                label_positions.append(np.sqrt(window_left*st_right))
            elif st_left > window_left and window_right > st_right: 
                label_positions.append(np.sqrt(window_left*window_right))
            else: 
                label_positions.append(2*window_left) 

        return label_positions 






class SpectralTypeLabelFormatter(mticker.Formatter):
    def __init__(self):
        pass 

    def __call__(self, x, pos):
        return plot_options.SPECTRAL_TYPES[pos].letter 










class HRDiagram: 

    def __init__(self): 

        self.fig, self.ax = plt.subplots(figsize=(10.7, 7))
        self.fig.subplots_adjust(top=0.87, bottom=0.15, left=0.12, right=0.96)


        # X axis: Temperature 
        self.ax.set_xlabel("Effective Temperature (K)", fontsize=18, labelpad=14)
        self.ax.set_xscale("log")
        self.ax.set_xlim((70000, 2000)) 
        
        self.ax.xaxis.set_major_locator(MajorLogLocator()) 
        self.ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}")) 

        self.ax.xaxis.set_minor_locator(MinorLogLocator()) 
        self.ax.xaxis.set_minor_formatter(mticker.NullFormatter())         


        # Y axis: Luminosity 
        self.ax.set_ylabel("Luminosity ($L_{{sun}}$)", fontsize=18, labelpad=14)
        self.ax.set_yscale("log")
        self.ax.set_ylim((1e-3, 1e7))

        # Grid, ticks, title 
        self.ax.tick_params(labelsize=14, length=10, which="major") 
        # self.ax.tick_params(length=0, which="minor") 
        self.ax.grid(alpha=0.5, which="both")
        self.ax.set_title("Evolutionary Path on HR Diagram", fontsize=20, pad=15) 



    def add_path(self, history, color="tab:blue", label=None, lw=2, alpha=1): 
        self.ax.plot(
            10**history.log_Teff, 
            10**history.log_L, 
            color=color, 
            label=label, 
            lw=lw, 
            alpha=alpha)



    def legend(self): 
        self.ax.legend(fontsize=14) 



    def label_spectraltypes(self): 

        ax_labels = self.ax.secondary_xaxis(location="top") 

        # Major ticks = borders (long lines, no labels)
        ax_labels.xaxis.set_major_locator(SpectralTypeBorderLocator())
        ax_labels.xaxis.set_major_formatter(mticker.NullFormatter())
        ax_labels.tick_params(length=20, which="major")

        # Minor ticks = labels (no lines, but show text)
        ax_labels.xaxis.set_minor_locator(SpectralTypeLabelLocator())
        ax_labels.xaxis.set_minor_formatter(SpectralTypeLabelFormatter())
        ax_labels.tick_params(length=0, which="minor", labelsize=14)  

        for spectral_type in plot_options.SPECTRAL_TYPES: 
            plt.axvspan(spectral_type.temp_range[1], spectral_type.temp_range[0], color=spectral_type.color, alpha=0.05)



































# # Add model labels to points on an HR diagram, skipping some models to avoid overlapping labels 
# def add_model_labels_hr_diagram(history): 

#     current_xlim = plt.gca().get_xlim()
#     current_ylim = plt.gca().get_ylim()
#     current_xrange = np.abs(current_xlim[0] - current_xlim[1])
#     current_yrange = np.abs(current_ylim[0] - current_ylim[1]) 

#     # Sub-function: Add white dot + text box for model at one point 
#     def add_model_point(log_Teff_current, log_L_current, modelnum_current): 
#         plt.scatter(log_Teff_current, log_L_current, zorder=100, color="white", ec="black", s=10) 
#         xrange_fraction_offset = 300 
#         yrange_fraction_offset = 300 
#         plt.text(
#             log_Teff_current-current_xrange/xrange_fraction_offset, 
#             log_L_current+current_yrange/yrange_fraction_offset, 
#             str(modelnum_current), 
#             fontsize=6, ha='left', va='bottom', zorder=100, clip_on=True, 
#             bbox=dict(facecolor='white', edgecolor='black', alpha=0.7, boxstyle='round,pad=0.2'))

#     def is_too_close(log_Teff, log_L, log_Teff_list, log_L_list): 
#         xrange_fraction_min_spacing = 200 
#         yrange_fraction_min_spacing = 100 
#         for x, y in zip(log_Teff_list, log_L_list): 
#             if (np.abs(x-log_Teff) < current_xrange/xrange_fraction_min_spacing) or (np.abs(y-log_L) < current_yrange/yrange_fraction_min_spacing): 
#                 return True 
#         return False
    
#     # Add label for the first model available  
#     modelnum = history.model_numbers_available[0]
#     index = modelnum-1 
#     log_Teff = history.log_Teff[index]
#     log_L = history.log_L[index]
#     add_model_point(log_Teff, log_L, modelnum) 
#     log_Teff_list = [log_Teff]
#     log_L_list = [log_L]

#     # Attempt to plot the next point 
#     for modelnum in history.model_numbers_available[1:]: 
#         index = modelnum-1 
#         log_Teff = history.log_Teff[index]
#         log_L = history.log_L[index]
        
#         # Check distance from all previously labeled points
#         if is_too_close(log_Teff, log_L, log_Teff_list, log_L_list):
#             continue  # Skip this point

#         # Otherwise, label this point
#         add_model_point(log_Teff, log_L, modelnum)
#         log_Teff_list.append(log_Teff)
#         log_L_list.append(log_L)




