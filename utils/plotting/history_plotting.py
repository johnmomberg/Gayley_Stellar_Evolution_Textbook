import numpy as np 

import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 

import utils.helpers as helpers 
import utils.config.plot_options as plot_options 
















def add_model_labels_time(ax, history):
    """
    Adds a secondary x-axis with major (labeled) and 
    minor (unlabeled) ticks showing where models are available.
    """

    # X locations of ticks = ages, labels above ticks = model numbers 
    all_models = history.model_numbers_available
    all_ages = history.star_age[all_models - 1]

    def update_secondary_axis(event_ax):
        if hasattr(ax, "_model_label_ax2"):
            ax._model_label_ax2.remove()

        # Calculate which ages and modelnums are actually in view of the current plot window 
        xmin, xmax = ax.get_xlim()
        indices_in_view = np.where((all_ages >= xmin) & (all_ages <= xmax))
        ages_in_view = all_ages[indices_in_view]
        models_in_view = all_models[indices_in_view]

        if len(ages_in_view) == 0:
            ax.figure.canvas.draw_idle()
            return

        ax2 = ax.secondary_xaxis('top') 

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


        # --- Final cleanup ---
        ax._model_label_ax2 = ax2
        ax.figure.canvas.draw_idle()

    ax.callbacks.connect('xlim_changed', update_secondary_axis)
    update_secondary_axis(ax)





def add_substage_highlight(fig, model_selected, history):
    ax = fig.axes[0] 
    if model_selected.model_start is not None: 
        ax.axvspan(
            history.star_age[model_selected.model_start-1], 
            history.star_age[model_selected.model_end-1], 
            color=model_selected.parent_substage.flowchart_color, alpha=0.1, 
            label=model_selected.parent_substage.flowchart_text) 
        ax.legend() 





# Reuse the same boilerplate for all history plots 
def create_history_plot(history, plot_func, ylabel, ylim, yscale, title, modelnum_now=None): 

    # Initialize figure 
    fig, ax = plt.subplots(figsize=(10.7, 5))
    fig.subplots_adjust(top=0.80, bottom=0.16, left=0.10, right=0.95)

    # The specific plotting logic (radius, fusion rate, center composition, etc)
    plot_func(ax, history) 

    # Add dashed line to signify current time 
    if modelnum_now is not None: 
        ax.axvline(history.star_age[modelnum_now-1], color="black", ls="dotted", label="Current time") 

    # xlabel, xlim, xaxis formatter
    ax.set_xlabel("Age (years)", fontsize=18, labelpad=14)
    ax.xaxis.set_major_formatter(mticker.EngFormatter())
    ax.set_xlim(0, np.nanmax(history.star_age))

    # ylabel, ylim, yscale 
    ax.set_ylabel(ylabel, fontsize=18, labelpad=14) 
    if ylim is not None: 
        ax.set_ylim(ylim)
    ax.set_yscale(yscale) 
    
    # Title, subtitle 
    ax.set_title(title, fontsize=20, pad=50)
    ax.text(0.5, 1.14, f"{history.star_mass[0]:.1f} $M_{{sun}}$ star", 
             transform=ax.transAxes, 
             fontsize=12, ha='center')

    # Grid, legend, ticks 
    ax.grid(alpha=0.5) 
    ax.legend(fontsize=14) 
    ax.tick_params(labelsize=14) 
    add_model_labels_time(ax, history) 

    return fig 
    




def plot_history_centercomposition(history, modelnum_now=None): 

    def plot_func(ax, history): 

        # Loop through list of Isotope objects
        for isotope in plot_options.ISOTOPES:
            # Use getattr() to dynamically access the correct attribute from the profile
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


    return create_history_plot(
        history=history, 
        plot_func=plot_func, 
        ylabel="Composition (by mass) at center", 
        ylim=(0,1), 
        yscale="linear", 
        title="Composition at center vs age", 
        modelnum_now=modelnum_now)





def plot_history_radius(history, modelnum_now=None): 

    def plot_func(ax, history): 
        ax.plot(history.star_age, 10**history.log_R, lw=2) 


    return create_history_plot(
        history=history, 
        plot_func=plot_func, 
        ylabel="Radius ($R_{{sun}}$)", 
        ylim=None, 
        yscale="log", 
        title="Overall radius vs age", 
        modelnum_now=modelnum_now)





def plot_history_fusion(history, modelnum_now=None): 

    def plot_func(ax, history): 

        ax.plot(history.star_age, 10**history.log_LH, lw=2, label="Hydrogen")
        ax.plot(history.star_age, 10**history.log_LHe, lw=2, label="Helium")
        ax.plot(history.star_age, 10**history.log_LZ, lw=2, label="Metals")

    # Use ML relation on the MS to predict the range of fusion rates 
    L_guess = helpers.mass_luminosity_relation(history.star_mass[0]) 
    ylim = (   10**(np.log10(L_guess)-1),    10**(np.log10(L_guess)+4)   ) 

    return create_history_plot(
        history=history, 
        plot_func=plot_func, 
        ylabel=f"Fusion rate ($L_{{sun}}$)", 
        ylim=ylim,  
        yscale="log", 
        title="Fusion rate vs age", 
        modelnum_now=modelnum_now)
















