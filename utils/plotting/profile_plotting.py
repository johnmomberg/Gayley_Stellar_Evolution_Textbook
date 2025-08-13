import numpy as np 

import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

import utils.config.physical_constants as physical_constants 
import utils.config.plot_options as plot_options 







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
def create_profile_plot(profile, history, plot_func, ylabel, ylim, yscale, title, profilexaxis_option): 

    # Initialize figure 
    fig, ax = plt.subplots(figsize=(10.7, 5))
    fig.subplots_adjust(top=0.86, bottom=0.16, left=0.10, right=0.95)

    # The specific plotting logic (composition, fusion, convection, etc)
    plot_func(ax, profile, history, profilexaxis_option) 

    # Select either mass or radius as the x axis 
    x_arr = profilexaxis_option.get_values(profile)
    x_units_str = profilexaxis_option.xlabel_units

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





def plot_profile_convection(profile, history, profilexaxis_option):

    def plot_func(ax, profile, history, profilexaxis_option):

        x_arr = profilexaxis_option.get_values(profile)
        ax.plot(x_arr, 10**profile.log_D_conv, label="Convective", lw=3) 
        ax.plot(x_arr, 10**profile.log_D_semi, label="Semiconvective", lw=3) 
        ax.plot(x_arr, 10**profile.log_D_ovr, label="Overshoot", lw=3) 
        ax.plot(x_arr, 10**profile.log_D_thrm, label="Thermohaline", lw=3) 

    return create_profile_plot(
        profile=profile, 
        history=history, 
        plot_func=plot_func, 
        ylabel="Strength of convection", 
        ylim=(1e0, 1e20), 
        yscale="log", 
        title="Heat transport regions inside star", 
        profilexaxis_option=profilexaxis_option)





def plot_profile_tempgrad(profile, history, profilexaxis_option):

    def plot_func(ax, profile, history, profilexaxis_option):
        
        x_arr = profilexaxis_option.get_values(profile)
        ax.plot(x_arr, profile.gradT, lw=5, color="black", label="Actual") 
        ax.plot(x_arr, profile.grada, lw=2, color="red", label="Theoretical, adiabatic")
        ax.plot(x_arr, profile.gradr, lw=2, color="limegreen", label="Theoretical, radiative")

    return create_profile_plot(
        profile=profile, 
        history=history, 
        plot_func=plot_func, 
        ylabel="Temperature gradient", 
        ylim=(min(profile.gradT)/2, max(profile.gradT)*2), 
        yscale="log", 
        title="Interior temperature gradient", 
        profilexaxis_option=profilexaxis_option)





def plot_profile_fusion(profile, history, profilexaxis_option):

    def plot_func(ax, profile, history, profilexaxis_option):

        x_arr = profilexaxis_option.get_values(profile)
        ax.plot(x_arr, profile.eps_nuc, label = "Total fusion", lw=5, color="black")
        ax.plot(x_arr, profile.pp, label = "Hydrogen (PP chain)", lw=2, color="tab:blue")
        ax.plot(x_arr, profile.cno, label = "Hydrogen (CNO cycle)", lw=2, color="tab:orange")
        ax.plot(x_arr, profile.tri_alfa, label = "Helium (triple alpha)", lw=2, color="tab:green")

        # Set ylim 
        specific_L = np.max(profile.luminosity)*physical_constants.L_sun / (profile.total_mass*physical_constants.M_sun) # Calculate the average ergs/sec/gram of the entire star's mass and luminosity 
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
        title="Interior fusion rate", 
        profilexaxis_option=profilexaxis_option)





def plot_profile_composition(profile, history, profilexaxis_option): 

    def plot_func(ax, profile, history, profilexaxis_option):

        x_arr = profilexaxis_option.get_values(profile) 

        # Loop through your list of Isotope objects
        for isotope in plot_options.ISOTOPES:
            # Use getattr() to dynamically access the correct attribute from the profile
            composition_profile = getattr(profile, isotope.profile_key)

            # Only plot profiles that are significant
            if np.nanmax(composition_profile) > 0.01:
                ax.plot(
                    x_arr,
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
        title="Interior composition", 
        profilexaxis_option=profilexaxis_option)





def plot_profile_mu(profile, history, profilexaxis_option):

    def plot_func(ax, profile, history, profilexaxis_option):

        x_arr = profilexaxis_option.get_values(profile)

        # Plot mass/particle
        ax.plot(x_arr, profile.mu, color="black", lw=3, label="Actual") 
            
        # Horizontal lines at 1.34 and 0.6 to represent mu of pure helium and mu of envelope 
        ax.axhline(0.62, color="dodgerblue", linestyle="dashed", lw=2, label="Theoretical: typical envelope")
        ax.axhline(1.34, color="tab:orange", linestyle="dashed", lw=2, label="Theoretical: Pure helium")
  
        # Set ylim 
        xmax = 0.95*np.max(x_arr) 
        ind_within_xlim = np.where(x_arr<xmax)
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
        title=f"Interior $\mu$ profile", 
        profilexaxis_option=profilexaxis_option)





def plot_profile_temp(profile, history, profilexaxis_option): 

    def plot_func(ax, profile, history, profilexaxis_option):

        x_arr = profilexaxis_option.get_values(profile)

        KE_per_N_temp = 3/2*physical_constants.k*10**profile.logT 
        KE_per_N_actual = 3/2 * profile.pressure * profile.mu*physical_constants.m_p / (10**profile.logRho)

        ax.plot(x_arr, KE_per_N_temp, lw=3, label="Temperature (in energy units)") 
        ax.plot(x_arr, KE_per_N_actual, lw=3, label="Kinetic Energy / particle") 
      
        xmax = 0.95*np.max(profile.mass) 
        ind_within_xlim = np.where(x_arr<xmax)
        
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
        title="Interior temperature profile", 
        profilexaxis_option=profilexaxis_option)







