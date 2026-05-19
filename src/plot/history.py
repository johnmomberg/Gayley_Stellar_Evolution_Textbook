import numpy as np 
from dataclasses import dataclass 

import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 
import matplotlib.patches as mpatches 
import matplotlib.transforms as mtransforms 

from ..data import isotopes 
from .. import misc 





# Dataclass that holds plot parameters that need to be passed to HistoryPlot._setup() when initializing a plot 
@dataclass
class HistoryPlotConfigParams:
    ylabel: str
    ylim: tuple | None
    yscale: str
    title: str 





# Class that holds all history plots so that the shared code can be held in a setup() function 
class HistoryPlot:



    # Code shared by all history plots 
    @staticmethod
    def _setup(history, config): 

        # Initialize figure 
        fig, ax = plt.subplots(figsize=(12.8, 5))
        fig.subplots_adjust(top=0.80, bottom=0.16, left=0.10, right=0.81)

        # xlabel, xlim, xaxis formatter
        ax.set_xlabel("Age (years)", fontsize=18, labelpad=14)
        ax.xaxis.set_major_formatter(mticker.EngFormatter())
        ax.set_xlim(0, np.nanmax(history.star_age))

        # ylabel and yscale 
        ax.set_ylabel(config.ylabel, fontsize=18, labelpad=14) 
        ax.set_yscale(config.yscale) 
    
        # Set ylim 
        # If ylim is None, do nothing because setting the ylims is handled by the individual plotting function 
        # Useful when ylims need to be calculated rather than being a known constant value 
        if config.ylim is not None: 
            ax.set_ylim(config.ylim)
            
        # Title, subtitle 
        ax.set_title(config.title, fontsize=20, pad=50)
        ax.text(0.5, 1.14, f"{history.initial_mass_string} $M_{{sun}}$ star", 
                transform=ax.transAxes, 
                fontsize=12, ha='center')

        # Grid, ticks 
        ax.grid(alpha=0.5) 
        ax.tick_params(labelsize=14) 
        return fig, ax 
    


    # History plot: center composition vs time 
    @classmethod
    def composition(cls, history): 

        # Setup 
        config = HistoryPlotConfigParams(
            ylabel="Composition (mass fraction)",
            ylim=(0, 1),
            yscale="linear",
            title="Composition at center vs age")
        fig, ax = cls._setup(history, config)
        
        # Loop through list of Isotope objects
        for isotope in isotopes.ISOTOPES:
            composition_history = getattr(history, isotope.history_key)

            # Only plot profiles that are significant
            if np.nanmax(composition_history) > 0.01:
                ax.plot(
                    history.star_age,
                    composition_history,
                    label=isotope.label,
                    color=isotope.color,
                    lw=3
                )  

        # Legend 
        ax.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5)) 

        return fig 
    


    # History plot: fusion rate vs time 
    @classmethod
    def fusion(cls, history): 

        # Setup 
        config = HistoryPlotConfigParams(
            ylabel=f"Fusion rate ($L_{{sun}}$)",
            ylim=None,
            yscale="log",
            title="Fusion rate vs age")
        fig, ax = cls._setup(history, config)
        
        # 3 fusion rates: Hydrogen, helium, and everything else (aka metals) 
        ax.plot(
            history.star_age, 10**history.log_L, 
            lw=3, color="cyan", 
            label="Total luminosity \nof star")
        ax.plot(
            history.star_age, 10**history.log_LH, 
            lw=2, color="tab:blue", 
            label=f"Hydrogen \u2192 Helium")
        ax.plot(
            history.star_age, 10**history.log_LHe, 
            lw=2, color="tab:green", 
            label=f"Helium \u2192 Carbon")
        ax.plot(
            history.star_age, 10**history.log_LZ, 
            lw=2, color="tab:red", 
            label=f"Heavier elements") 

        # Use mass-luminosity relation on the MS to predict the range of fusion rates to use for y limits 
        L_guess = misc.mass_luminosity_relation(history.star_mass[0]) 
        ax.set_ylim(
            10**( np.log10(L_guess)-1 ), 
            10**( np.log10(L_guess)+4 ) ) 
        
        # Legend 
        ax.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5)) 

        return fig 



    # History plot: radius vs time 
    @classmethod
    def radius(cls, history): 

        # Setup 
        config = HistoryPlotConfigParams(
            ylabel="Radius ($R_{{sun}}$)",
            ylim=None,
            yscale="log",
            title="Radius vs age")
        fig, ax = cls._setup(history, config)

        # Plot radius vs age         
        ax.plot(history.star_age, 10**history.log_R, lw=2) 

        return fig 



    # History plot: mass vs time 
    @classmethod
    def mass(cls, history): 

        # Setup 
        config = HistoryPlotConfigParams(
            ylabel="Mass ($M_{{sun}}$)",
            ylim=None,
            yscale="linear",
            title="Mass vs age")
        fig, ax = cls._setup(history, config)

        # Plot mass vs age         
        ax.plot(history.star_age, history.star_mass, lw=2) 

        ax.set_ylim(0, 1.05*np.nanmax(history.star_mass))

        return fig 





def add_model_labels_time(ax, history, modelnum_now):
    """
    Adds a secondary x-axis with major (labeled) and 
    minor (unlabeled) ticks showing where models are available.
    """

    # X locations of ticks = ages, labels above ticks = model numbers 
    all_models = history.model_numbers_available
    all_ages = history.star_age[all_models - 1]

    def update_secondary_axis(event_ax): 

        # Remove current versions so it doesn't duplicate every time you move the xlim 
        if hasattr(ax, "_model_label_ax2"):
            ax._model_label_ax2.remove()



        ax2 = ax.secondary_xaxis('top') 

        # Calculate which ages and modelnums are actually in view of the current plot window 
        xmin, xmax = ax.get_xlim()
        indices_in_view = np.where((all_ages >= xmin) & (all_ages <= xmax))
        ages_in_view = all_ages[indices_in_view]
        models_in_view = all_models[indices_in_view]

        # Previously, I found a bug where if I zoomed the window to a region with no models and then zoomed back out, 
        # the model numbers that should re-appear in frame were gone, and this function was broken until you reloaded the plot entirely. 
        # This if statement fixes that bug by running the important stuff even if there's no models visible in the current window  
        if len(ages_in_view) == 0:
            ax._model_label_ax2 = ax2  
            ax2.set_xticks([])
            ax.figure.canvas.draw_idle()
            return



        # Calculate location and labels of ticks 
        current_xmin, current_xmax = ax.get_xlim() 
        min_labeled_spacing = 0.02 # Fraction of the axis that major ticks must be spaced out
        min_unlabeled_spacing = min_labeled_spacing/5 # Fraction of the axis that minor ticks must be spaced out 
        tick_ages = [ages_in_view[0]] 
        tick_labels = [models_in_view[0]] 
        ages_with_labels = [ages_in_view[0]]

        for i in np.arange(1, len(ages_in_view)): 
            age = ages_in_view[i] 
            model = models_in_view[i] 

            # 1. MAJOR TICKS: If next tick is far enough away for labels to not overlap  
            if age > ages_with_labels[-1] + (current_xmax - current_xmin)*min_labeled_spacing: 
                tick_ages.append(age) 
                tick_labels.append(model) 
                ages_with_labels.append(age)

            # 2. MINOR TICKS: If next tick is not far enough away to be labeled but is far enough away to add a minor tick 
            elif age > tick_ages[-1] + (current_xmax - current_xmin)*min_unlabeled_spacing: 
                tick_ages.append(age) 
                tick_labels.append("")

        ax2.set_xticks(tick_ages)
        ax2.set_xticklabels(tick_labels, fontsize=6, rotation=90)
        ax2.tick_params(which='major', length=4)

        ax._model_label_ax2 = ax2 
        ax.figure.canvas.draw_idle()



        # Add vertical line to currently selected model number 
        if modelnum_now is not None: 
            xpos = history.star_age[modelnum_now-1] 
            ax.axvline(xpos, color="black", ls="dashed")  
            


    ax.callbacks.connect('xlim_changed', update_secondary_axis)
    update_secondary_axis(ax)





def add_substage_highlight(
        fig, selected_row, history, 
        lower_alpha=0.05, lower_border_linewidth=0, lower_border_color="none", 
        upper_alpha=0.5, upper_border_linewidth=0, upper_border_color="none", 
        include_label=False): 

    if int(selected_row["model_start"]) is None: 
        return 

    ax = fig.axes[0] 
    trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)

    xmin = history.star_age[selected_row["model_start"]-1] 
    xmax = history.star_age[selected_row["model_end"]-1] 
    color = selected_row["Color"]
    label = selected_row["Short Name"]

    # Highlight inside plot 
    ax.axvspan(
        xmin, xmax, 
        facecolor = color, 
        alpha = lower_alpha, 
        linewidth = lower_border_linewidth, 
        edgecolor = lower_border_color, 
        label=label) 
    
    # Add a vertical line at the example plot 
    ax.axvline(history.star_age[selected_row["model_example"]-1], color=color, ls="dashed", lw=0.8)

    # Add colored rectangle above plot
    rect = mpatches.Rectangle(
        xy = (xmin, 1.00), 
        width = xmax-xmin, 
        height = 0.1, 
        transform = trans, 
        facecolor = color, 
        alpha = upper_alpha, 
        linewidth=upper_border_linewidth, 
        edgecolor=upper_border_color, 
        clip_on = True ) 
    ax.add_patch(rect) 

    # Set clip boundary of rectangle 
    clip_fig_rect = mpatches.Rectangle( 
        xy = (fig.subplotpars.left, 0), 
        width = fig.subplotpars.right - fig.subplotpars.left, 
        height = 1.0, 
        transform=fig.transFigure, 
        facecolor="none", 
        edgecolor="none")
    rect.set_clip_path(clip_fig_rect) 

    # Left and right sides of box (either the actual position, or the position where it gets cropped to)
    x_left = np.max([xmin, ax.get_xlim()[0]]) 
    x_right = np.min([xmax, ax.get_xlim()[1]]) 

    # Check if wide enough for a label
    data_to_fig = (ax.transData + fig.transFigure.inverted())
    x0_fig, _ = data_to_fig.transform((x_left, 0))
    x1_fig, _ = data_to_fig.transform((x_right, 0))
    fig_width_fraction = x1_fig - x0_fig 
    if fig_width_fraction >= 0.05:
        include_label = True

    # Add text in the middle of the rectangle 
    if include_label == True: 
        xmid = (x_left + x_right) / 2
        ymid = rect.get_xy()[1] + rect.get_height()/2 - 0.005
        ax.text(
            xmid,
            ymid,
            label,
            ha="center",
            va="center",
            color="white", 
            # weight="bold", 
            fontsize=12, 
            transform=trans )
    

