import numpy as np 
from dataclasses import dataclass

import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

import utils.load_data as load_data
import utils.constants as constants 
import utils.helpers as helpers 




# Define all isotopes (hydrogen, helium, etc) for use with composition plots (both profile data and history data)

@dataclass
class Isotope:
    """Represents an isotope with its plotting properties."""
    profile_key: str                        # The attribute name in the MESA profile (e.g., "profile.h1") 
    history_key: str                        # The attribute name in the MESA history (e.g., "history.center_h1")
    label: str                              # The label for the plot legend (e.g., 'Hydrogen')
    color: str                              # The color for the plot line 
    show_initial_abundance: bool = False    # Include a horizontal dashed line to profile plots to indicate the initial abundance of this element? 

ISOTOPES = [ 
    Isotope(profile_key="h1",   history_key="center_h1",   label="Hydrogen",     color="tab:blue", show_initial_abundance=True), 
    Isotope(profile_key="he3",  history_key="center_he3",  label="Helium 3",     color="tab:orange"), 
    Isotope(profile_key="he4",  history_key="center_he4",  label="Helium 4",     color="tab:green", show_initial_abundance=True), 
    Isotope(profile_key="c12",  history_key="center_c12",  label="Carbon 12",    color="tab:red"), 
    Isotope(profile_key="n14",  history_key="center_n14",  label="Nitrogen 14",  color="tab:purple"), 
    Isotope(profile_key="o16",  history_key="center_o16",  label="Oxygen 16",    color="tab:brown"), 
    Isotope(profile_key="ne20", history_key="center_ne20", label="Neon 20",      color="tab:pink"), 
    Isotope(profile_key="mg24", history_key="center_mg24", label="Magnesium 24", color="tab:grey"), 
    Isotope(profile_key="si28", history_key="center_si28", label="Silicon 28",   color="tab:olive"), 
    Isotope(profile_key="s32",  history_key="center_s32",  label="Sulfur 32",    color="tab:cyan"), 
    Isotope(profile_key="ar36", history_key="center_ar36", label="Argon 36",     color="mediumblue"), 
    Isotope(profile_key="ca40", history_key="center_ca40", label="Calcium 40",   color="orange"), 
    Isotope(profile_key="ti44", history_key="center_ti44", label="Titanium 44",  color="mediumspringgreen"), 
    Isotope(profile_key="cr48", history_key="center_cr48", label="Chromium 48",  color="maroon"), 
    Isotope(profile_key="fe52", history_key="center_fe52", label="Iron 52",      color="mediumslateblue"), 
    Isotope(profile_key="fe54", history_key="center_fe54", label="Iron 54",      color="saddlebrown"), 
    Isotope(profile_key="fe56", history_key="center_fe56", label="Iron 56",      color="magenta"), 
    Isotope(profile_key="ni56", history_key="center_ni56", label="Nickel 56",    color="black"), 
]  



# Define all spectral types for use with HR diagram plots 

@dataclass 
class SpectralType: 
    """Represents a Spectral Type (O, B, etc) with its plotting properties.""" 
    letter: str                     # "O", "B", "A" "F", "G", "K", or "M" 
    temperature_range: tuple        # (lower bound, upper bound)    # From: https://en.wikipedia.org/wiki/Stellar_classification#Harvard_spectral_classification 
    MS_mass_range: tuple            # (lower bound, upper bound)    # From: https://en.wikipedia.org/wiki/Stellar_classification#Harvard_spectral_classification 
    color: str                      # Color used to represent this region on HR diagram 

SPECTRAL_TYPES = [ 
    SpectralType(letter="O", temperature_range=(33_000, np.infty), MS_mass_range=(16, np.infty), color="blue"), 
    SpectralType(letter="B", temperature_range=(10_000, 33_000),   MS_mass_range=(2.1, 16),      color="dodgerblue"), 
    SpectralType(letter="A", temperature_range=(7_300, 10_000),    MS_mass_range=(1.4, 2.1),     color="lightskyblue"), 
    SpectralType(letter="F", temperature_range=(6_000, 7_300),     MS_mass_range=(1.04, 1.4),    color="silver"), 
    SpectralType(letter="G", temperature_range=(5_300, 6_000),     MS_mass_range=(0.8, 1.04),    color="yellow"), 
    SpectralType(letter="K", temperature_range=(3_900, 5_300),     MS_mass_range=(0.45, 0.8),    color="orange"), 
    SpectralType(letter="M", temperature_range=(2_300, 3_900),     MS_mass_range=(0.08, 0.45),   color="red"), 
]


















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
    for spectral_type in SPECTRAL_TYPES: 
        
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
        ax.scatter(history.log_Teff[modelnum-1], history.log_L[modelnum-1], 
                   facecolors='none', edgecolors='mediumblue', s=200, linewidths=2, zorder=1000, label=f"Current pos ({modelnum})")
    
    ax.legend() 
























def add_colored_title(fig, strings, colors, fontsize, y=0.95, spacing_pts=10):

    ax = fig.axes[0]  
    ax.set_title("") 
    fontprops = FontProperties(family='DejaVu Sans', size=fontsize)

    def get_text_width(text, fontprops):
        tp = TextPath((0, 0), text, prop=fontprops)
        return tp.get_extents().width
    
    tp_widths = [get_text_width(p, fontprops) for p in strings]
    total_width_pts = sum(tp_widths) + spacing_pts * (len(strings) - 1)

    fig_width_in = fig.get_figwidth()
    pts_to_fig_frac = 1 / (fig_width_in * 72)

    x = 0.5 - total_width_pts * pts_to_fig_frac / 2
    for part, color, width in zip(strings, colors, tp_widths):
        fig.text(x, y, part, fontproperties=fontprops,
                 color=color, ha='left', va='center')
        x += width * pts_to_fig_frac + spacing_pts * pts_to_fig_frac





# Reuse the same boilerplate for all profile plots 
def create_profile_plot(profile, history, plot_func, ylabel, ylim, yscale, title): 

    # Initialize figure 
    fig, ax = plt.subplots(figsize=(10.7, 5))
    fig.subplots_adjust(top=0.86, bottom=0.16, left=0.10, right=0.95)

    # The specific plotting logic (composition, fusion, convection, etc)
    plot_func(ax, profile, history) 

    x_arr = profile.mass 
    x_units_str = "(mass coordinate ($M_{{sun}}$))"

    # Set xlabel (mass or radius) and xlim  
    ax.set_xlabel(f"Location inside star {x_units_str}", fontsize=18, labelpad=0)
    ax.set_xlim(0, 1.001*np.max(x_arr))

    # Add extra labels to left side (core) and right side (surface) of plot 
    xticks = ax.get_xticks() 
    xticks = np.append(xticks, np.max(x_arr))
    xtick_labels = [
        "0\n(Core)" if round(xticks[i], 2) == 0 else
        f"\n(Surface)" if i == len(xticks)-1 else
        str(round(xticks[i], 2))
        for i in range(len(xticks)) 
    ]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)
    ax.set_xlim(0, 1.001*np.max(x_arr))

    # Set ylabel yscale  
    ax.set_ylabel(ylabel, fontsize=18, labelpad=14) 
    if ylim is not None: 
        ax.set_ylim(ylim[0], ylim[1]) 
    ax.set_yscale(yscale) 

    # Set title and subtitle 
    ax.set_title(title, fontsize=20, pad=25) 
    ax.text(0.5, 1.025, f"{profile.total_mass:.1f} $M_{{sun}}$ star at {mticker.EngFormatter(places=2)(profile.age)} years old", 
             transform=ax.transAxes, 
             fontsize=12, ha='center')

    # Grid, legend, ticks 
    ax.grid(alpha=0.5) 
    ax.legend(fontsize=14) 
    ax.tick_params(labelsize=14) 

    return fig





def plot_profile_convection(profile, history):

    def plot_func(ax, profile, history):

        ax.plot(profile.mass, 10**profile.log_D_conv, label="Convective", lw=3) 
        ax.plot(profile.mass, 10**profile.log_D_semi, label="Semiconvective", lw=3) 
        ax.plot(profile.mass, 10**profile.log_D_ovr, label="Overshoot", lw=3) 
        ax.plot(profile.mass, 10**profile.log_D_thrm, label="Thermohaline", lw=3) 



    return create_profile_plot(
        profile=profile, 
        history=history, 
        plot_func=plot_func, 
        ylabel="Strength of convection", 
        ylim=(1e0, 1e20), 
        yscale="log", 
        title="Heat transport regions inside star")





def plot_profile_tempgrad(profile, history):

    def plot_func(ax, profile, history): 

        ax.plot(profile.mass, profile.gradT, lw=5, color="black", label="Actual") 
        ax.plot(profile.mass, profile.grada, lw=2, color="red", label="Theoretical, adiabatic")
        ax.plot(profile.mass, profile.gradr, lw=2, color="limegreen", label="Theoretical, radiative")



    return create_profile_plot(
        profile=profile, 
        history=history, 
        plot_func=plot_func, 
        ylabel="Temperature gradient", 
        ylim=(min(profile.gradT)/2, max(profile.gradT)*2), 
        yscale="log", 
        title="Interior temperature gradient")





def plot_profile_fusion(profile, history):

    def plot_func(ax, profile, history):

        ax.plot(profile.mass, profile.eps_nuc, label = "Total fusion", lw=5, color="black")
        ax.plot(profile.mass, profile.pp, label = "Hydrogen (PP chain)", lw=2, color="tab:blue")
        ax.plot(profile.mass, profile.cno, label = "Hydrogen (CNO cycle)", lw=2, color="tab:orange")
        ax.plot(profile.mass, profile.tri_alfa, label = "Helium (triple alpha)", lw=2, color="tab:green")

        # Set ylim 
        specific_L = np.max(profile.luminosity)*constants.L_sun / (profile.total_mass*constants.M_sun) # Calculate the average ergs/sec/gram of the entire star's mass and luminosity 
        max_fusion = np.max(profile.eps_nuc) 
        if max_fusion>specific_L: 
            ax.set_ylim((specific_L/10, max_fusion)) 
        else: 
            ax.set_ylim((specific_L/10, specific_L*1000))



    return create_profile_plot(
        profile=profile, 
        history=history, 
        plot_func=plot_func, 
        ylabel="Fusion rate (ergs/sec/gram)", 
        ylim=None, 
        yscale="log", 
        title="Interior fusion rate")





def plot_profile_composition(profile, history): 

    def plot_func(ax, profile, history):

        # Loop through your list of Isotope objects
        for isotope in ISOTOPES:
            # Use getattr() to dynamically access the correct attribute from the profile
            composition_profile = getattr(profile, isotope.profile_key)

            # Only plot profiles that are significant
            if np.nanmax(composition_profile) > 0.01:
                ax.plot(
                    profile.mass,
                    composition_profile,
                    label=isotope.label,
                    color=isotope.color,
                    lw=3
                ) 

            # Add horizontal dashed lines showing the initial composition
            if isotope.show_initial_abundance: 
                composition_history = getattr(history, isotope.history_key)
                ax.axhline(composition_history[0], color=isotope.color, ls="dashed") 



    return create_profile_plot(
        profile=profile, 
        history=history, 
        plot_func=plot_func, 
        ylabel="Composition (by mass)", 
        ylim=(0,1), 
        yscale="linear", 
        title="Interior composition")





def plot_profile_mu(profile, history):

    def plot_func(ax, profile, history):

        # Plot mass/particle
        ax.plot(profile.mass, profile.mu, color="black", lw=3, label="Actual") 
            
        # Horizontal lines at 1.34 and 0.6 to represent mu of pure helium and mu of envelope 
        ax.axhline(0.62, color="dodgerblue", linestyle="dashed", lw=2, label="Theoretical: typical envelope")
        ax.axhline(1.34, color="tab:orange", linestyle="dashed", lw=2, label="Theoretical: Pure helium")
  
        # Set ylim 
        xmax = 0.95*np.max(profile.mass) 
        ind_within_xlim = np.where(profile.mass<xmax)
        mu_max = np.nanmax(profile.mu[ind_within_xlim]) 
        y_max = 1.44 
        if mu_max > 1.34: 
            y_max = 1.9 
        ax.set_ylim((0.5, y_max))



    return create_profile_plot(
        profile=profile, 
        history=history, 
        plot_func=plot_func, 
        ylabel="Mass/particle (AMU)", 
        ylim=None, 
        yscale="linear", 
        title=f"Interior $\mu$ profile",)





def plot_profile_temp(profile, history): 

    def plot_func(ax, profile, history): 

        KE_per_N_temp = 3/2*constants.k*10**profile.logT 
        KE_per_N_actual = 3/2 * profile.pressure * profile.mu*constants.m_p / (10**profile.logRho)

        ax.plot(profile.mass, KE_per_N_temp, lw=3, label="Temperature (in energy units)") 
        ax.plot(profile.mass, KE_per_N_actual, lw=3, label="Kinetic Energy / particle") 
      
        xmax = 0.95*np.max(profile.mass) 
        ind_within_xlim = np.where(profile.mass<xmax)
        
        ymin1 = np.min(KE_per_N_temp[ind_within_xlim]) 
        ymin2 = np.min(KE_per_N_actual[ind_within_xlim]) 
        ymin = np.min([ymin1, ymin2]) 
        
        ymax1 = np.max(KE_per_N_temp[ind_within_xlim]) 
        ymax2 = np.max(KE_per_N_actual[ind_within_xlim]) 
        ymax = np.max([ymax1, ymax2])
        
        ax.set_ylim(ymin, ymax) 



    return create_profile_plot(
        profile=profile, 
        history=history, 
        plot_func=plot_func, 
        ylabel="Energy (ergs)", 
        ylim=None, 
        yscale="log", 
        title="Interior temperature profile")





























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

        # Loop through your list of Isotope objects
        for isotope in ISOTOPES:
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





def label_substage(fig, model_selected, history):
    ax = fig.axes[0] 
    if model_selected.model_start is not None: 
        ax.axvspan(
            history.star_age[model_selected.model_start-1], 
            history.star_age[model_selected.model_end-1], 
            color=model_selected.parent_substage.flowchart_color, alpha=0.1, 
            label=model_selected.parent_substage.flowchart_text) 
        ax.legend() 
    return fig












