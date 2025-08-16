import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _(
    HR_diagram_str,
    available_substages_tabs,
    comparison_mode_radio,
    comparison_mode_str,
    comparison_mode_title,
    controls_subtitle,
    fig2,
    flowchart,
    flowchart_subtitle_hstack,
    full_title,
    history_str,
    mo,
    plot_mode_radio,
    plot_mode_title,
    profile_str,
    secondary_plot_subtitle,
    userguide_subtitle_hstack,
    userguide_text,
):
    # MAIN 


    full_interface = mo.vstack(
        [
            full_title, 
            "\u200b", 
            mo.md("---"), 
            "\u200b", 

            userguide_subtitle_hstack, 
            userguide_text, 
            "\u200b", 
            mo.md("---"), 
            "\u200b", 

            controls_subtitle, 
            plot_mode_title, 
            mo.hstack(
                [
                    plot_mode_radio, 
                    mo.vstack(
                        [
                            HR_diagram_str, 
                            history_str, 
                            profile_str
                        ], 
                        gap=0)
                ], 
                gap=0, align="center"), 
            "\u200b", 

            comparison_mode_title,  
            comparison_mode_radio, 
            comparison_mode_str, 
            available_substages_tabs, 
            "\u200b", 
            mo.md("---"), 
            "\u200b", 

            flowchart_subtitle_hstack, 
            flowchart, 
            "\u200b", 
            mo.md("---"), 
            "\u200b", 
        
            secondary_plot_subtitle, 
            mo.mpl.interactive(fig2), 
            "\u200b", 
            mo.md("---"), 

        ], 
        gap=0.7 
    ) 


    full_interface 



    return


@app.cell
def _():
    # To do: 


    # Fix ylims of fusion vs time plot 
    # Bring ylim-setting code into its own function: one for log plots and one for linear plots 
    # Apply to temperature/KE per particle plots 

    # Plots to make work: 
    # HR diagram 
    # Comparison of de broglie wavelength to interparticle spacing 

    # Make loading of profiles/histories dynamic: only load after you need them, then save as you go so you dont have to reload any 

    # Add an option for history plot to be either scaled linearly with time or to evenly space the substages, to make it easier to see the interesting properties that happen all near the end of the star's life
    # How to deal with helium ignition: give an option called is_instantaneous=True which overrides the need for a model_start and model_end. Instead, it uses the model_example and plots a LINE at that point rather than an axhspan, and the even spacing ignores it. 

    # Add a fourth option to comparison_mode_selector that lets the user type in the filepath to a MESA file and then provides a dropdown of all available profiles which they can select from. 

    # Add "we are here" to flowchart: mass and modelnum. Calc which substage the modelnum is within its boundaries. 

    # Add "we are here" back to time plots 

    # Add "1.0 M_sun star at 5 G years age (model number 296)" to profile plot titles 

    # I don't like the way I'm currently finding the available substages. The dictionary key which is currently calculated like set_textcolor_css(sub.mode2_abbrev_with_massrange, sub.flowchart_color) should be an attribute of the substage class. for example, i have mode1_abbrev. i should have mode1_key which would replace mode1_abbrev_with_massrange and do whatever i need to to, such as appending the mass range. 

    return


@app.cell
def _(mo):
    # Title 
    full_title = mo.md("<h1>Stellar Evolution Interactive Tool</h1>") 

    return (full_title,)


@app.cell
def _(mo):
    # User Guide section header with switch to minimize it 
    userguide_subtitle = mo.md("<h2>Tutorial/Documentation</h2>") 
    userguide_switch = mo.ui.switch(value=True, label="Hide/show")
    userguide_subtitle_hstack = mo.hstack([userguide_subtitle, userguide_switch], justify="space-between", align="center")
 
    return userguide_subtitle_hstack, userguide_switch


@app.cell
def _(userguide_switch):
    # User Guide text 

    userguide_text = "" 
    if userguide_switch.value == True: 
        userguide_text = "To do: create user guide/tutorial/documentation for this app. "


    return (userguide_text,)


@app.cell
def _(mo):
    # Flowchart header with switch to minimize it 
    flowchart_subtitle = mo.md("<h2>Flowchart</h2>") 
    flowchart_switch = mo.ui.switch(value=True, label="Hide/show")
    flowchart_subtitle_hstack = mo.hstack([flowchart_subtitle, flowchart_switch], justify="space-between", align="center")
 

    return flowchart_subtitle_hstack, flowchart_switch


@app.cell
def _(mo):
    # Other headers 
    controls_subtitle = mo.md("<h2>Controls</h2>") 
    secondary_plot_subtitle = mo.md("<h2>Secondary Plot</h2>") 

    return controls_subtitle, secondary_plot_subtitle


@app.cell
def _(mo, ui_options):
    # Comparison mode radio 
    comparison_mode_title = mo.md("<h3>Choose mass/evolutionary stage highlighted by secondary plot</h3>") 
    comparison_mode_radio = ui_options.create_radio(ui_options.COMPAREMODE_OPTIONS) 

    return comparison_mode_radio, comparison_mode_title


@app.cell
def _(mo, stellar_evolution_data):
    # Stage and mass selector dropdowns used by comparison mode string 

    # Mode1 
    unique_masses = sorted({m for s in stellar_evolution_data.SUBSTAGES_LIST for m in [s.mass_min, s.mass_max]})
    mode1_massrange_options = [f"{unique_masses[i]:.1f}-{unique_masses[i+1]:.1f}" for i in range(len(unique_masses)-1)]
    mode1_massrange_dropdown = mo.ui.dropdown(mode1_massrange_options, value=next(iter(mode1_massrange_options)))

    # Mode2 
    mode2_parentstage_options = {stage.full_name: stage for stage in stellar_evolution_data.ParentStage}
    mode2_parentstage_dropdown = mo.ui.dropdown(options=mode2_parentstage_options, value=next(iter(mode2_parentstage_options))) 

    return mode1_massrange_dropdown, mode2_parentstage_dropdown, unique_masses


@app.cell
def _(
    comparison_mode_radio,
    mo,
    mode1_massrange_dropdown,
    mode2_parentstage_dropdown,
    ui_options,
):
    # Comparison mode string 

    # String that appears depending on what comparison mode is selected. Includes a dropdown selector. 
    comparison_mode1_str = mo.md(f"View the evolution of a {mode1_massrange_dropdown} mass star: ") 
    comparison_mode2_str = mo.md(f"Compare how stars of different masses experience the {mode2_parentstage_dropdown} stage: ") 

    comparison_mode_str = "\u200b" 
    if comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
        comparison_mode_str = comparison_mode1_str 
    if comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
        comparison_mode_str = comparison_mode2_str 

    return (comparison_mode_str,)


@app.cell
def _(mo, ui_options):
    # Plot mode radio selector 
    plot_mode_title = mo.md("<h3>Choose secondary plot</h3>") 
    plot_mode_radio = ui_options.create_radio(ui_options.PLOTMODE_OPTIONS)

    return plot_mode_radio, plot_mode_title


@app.cell
def _(mo):
    # Plot mode option 0: HR Diagram 
    HR_diagram_str = mo.md("HR diagram")

    return (HR_diagram_str,)


@app.cell
def _(mo, ui_options):
    # Plot mode option 1: history vs time  
    history_plot_dropdown = ui_options.create_dropdown(ui_options.HISTORYPLOT_OPTIONS)
    history_str = mo.md(f"History: {history_plot_dropdown} vs time") 

    return history_plot_dropdown, history_str


@app.cell
def _(ui_options):
    # Plot mode option 2: Interior profile 
    profile_plot_dropdown = ui_options.create_dropdown(ui_options.PROFILEPLOT_OPTIONS) 

    return (profile_plot_dropdown,)


@app.cell
def _(ui_options):
    # Plot mode option 2: X coord to represeent location within interior 
    profile_plot_x_dropdown = ui_options.create_dropdown(ui_options.PROFILEXAXIS_OPTIONS)

    return (profile_plot_x_dropdown,)


@app.cell
def _(mcolors):
    # Convert from matlotlib color name (i.e., "dodgerblue") to the string used in CSS to set text color
    def set_textcolor_css(text, mpl_color): 
        css_color = mcolors.to_hex(mpl_color) 
        colored_text = f"<span style='color:{css_color}'>{text}</span>" 
        return colored_text 

    return (set_textcolor_css,)


@app.cell
def _(
    comparison_mode_radio,
    mo,
    profile_plot_dropdown,
    profile_plot_x_dropdown,
    set_textcolor_css,
    substage_selected,
    ui_options,
):
    # Plot mode option 2: Add that together to create string with all profile dropdowns 


    # Default values (if no substage is selected): Display an empty white line 
    substage_selected_str = "______" 
    substage_selected_color = "white"

    if comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
        substage_selected_str = substage_selected.mode1_interior_plot_title 

    if comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
        substage_selected_str = substage_selected.mode2_interior_plot_title 

    # Text color of substage's name in the displayed text should match its flowchart color 
    if substage_selected: 
        substage_selected_color = substage_selected.flowchart_color 


    profile_str = mo.md(
        f"Interior profile: {profile_plot_dropdown} vs {profile_plot_x_dropdown} of a "
        f"{set_textcolor_css(substage_selected_str, substage_selected_color)} star" )


    return (profile_str,)


@app.cell
def _(
    comparison_mode_radio,
    mode1_massrange_dropdown,
    mode2_parentstage_dropdown,
    stellar_evolution_data,
    ui_options,
):
    # Identify available substages 

    selected_massrange = [float(num) for num in mode1_massrange_dropdown.value.split('-')] 
    selected_parentstage = mode2_parentstage_dropdown.value 

    if comparison_mode_radio.value == ui_options.COMPAREMODE_NOSELECTION: 
        available_substages = []

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
        available_substages = [
            s for s in stellar_evolution_data.SUBSTAGES_LIST 
            if not (s.mass_max <= selected_massrange[0] 
                    or s.mass_min >= selected_massrange[1])]

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
        available_substages = [
            s for s in stellar_evolution_data.SUBSTAGES_LIST 
            if s.parent_stage.name == selected_parentstage.name] 

    return available_substages, selected_massrange


@app.cell
def _(
    available_substages,
    comparison_mode_radio,
    mo,
    set_textcolor_css,
    ui_options,
):
    # Create available substage tab selector (if there are any available substages)

    if len(available_substages) == 0: 
        available_substages_tabs = "" 

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
    
        available_substages_options = {
            set_textcolor_css(sub.mode1_abbrev, sub.flowchart_color): 
            sub.mode1_desc 
            for sub in available_substages}
    
        available_substages_tabs = mo.ui.tabs(
            available_substages_options, 
            value=list(available_substages_options.keys())[0]) 

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
    
        available_substages_options = {
            set_textcolor_css(sub.mode2_abbrev_with_massrange, sub.flowchart_color): 
            sub.mode2_desc_with_massrange 
            for sub in available_substages} 
    
        available_substages_tabs = mo.ui.tabs(
            available_substages_options, 
            value=list(available_substages_options.keys())[0]) 


    return (available_substages_tabs,)


@app.cell
def _(
    available_substages,
    available_substages_tabs,
    comparison_mode_radio,
    set_textcolor_css,
    ui_options,
):
    # Identify available substage tab that is currently selected (if there are any available substages)

    if len(available_substages) == 0: 
        substage_selected = None 

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
        substage_selected = [
            s for s in available_substages 
            if set_textcolor_css(s.mode1_abbrev, s.flowchart_color) == available_substages_tabs.value
        ][0] 

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
        substage_selected = [
            s for s in available_substages 
            if set_textcolor_css(s.mode2_abbrev_with_massrange, s.flowchart_color) == available_substages_tabs.value
        ][0]

    return (substage_selected,)


@app.cell
def _(
    comparison_mode_radio,
    selected_massrange,
    substage_selected,
    ui_options,
):
    # Identify model used to represent selected substage 

    if substage_selected is None: 
        model_selected = None 

    elif len(substage_selected.models) == 0: 
        model_selected = None 

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
        model_selected = next((m for m in substage_selected.models if selected_massrange[0]<=m.mass<=selected_massrange[1]), None)

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
        model_selected = next((m for m in substage_selected.models if m.is_default), substage_selected.models[0])

    return (model_selected,)


@app.cell
def _(
    available_substages,
    comparison_mode_radio,
    flowchart_switch,
    mo,
    mpatches,
    np,
    plt,
    selected_massrange,
    stellar_evolution_data,
    substage_selected,
    ui_options,
    unique_masses,
):
    # Draw the flowchart




    def draw_substage_box(
        ax, substage, 
        bg_color, bg_alpha, 
        border_linewidth, border_color, 
        text_color, text_fontsize, text_y=None):

        # Define rectangle bounds
        x1 = substage.parent_stage.flowchart_x + 0.02 
        x2 = substage.parent_stage.flowchart_x+1 - 0.02 
        y1 = substage.mass_min
        y2 = substage.mass_max
        width = x2 - x1
        height = y2 - y1

        # Add the rectangle
        rect = mpatches.Rectangle(
            (x1, y1), width, height,
            linewidth=border_linewidth,
            edgecolor=border_color,
            facecolor=bg_color, 
            alpha=bg_alpha, 
        )
        ax.add_patch(rect)

        # Add text inside the rectangle 
        if text_y is None: 
            text_y = np.sqrt(y1*y2)
        ax.text(
            x1 + width/2, text_y, #np.sqrt(y1*y2),
            substage.flowchart_text,
            ha='center', va='center',
            fontsize=text_fontsize, color=text_color
        )





    # Function to draw the flowchart, updating highlights/labels based on selection
    def draw_flowchart():

        # Allow flowchart to be minimized 
        if flowchart_switch.value == False: 
            return "" 
    
        fig, ax = plt.subplots(figsize=(15, 5))
        fig.subplots_adjust(top=0.95, bottom=0.16, left=0.07, right=1)

        if comparison_mode_radio.value==ui_options.COMPAREMODE_NOSELECTION: 
            custom_yticks = unique_masses 
            custom_xtick_labels = [parent_stage.short_name for parent_stage in stellar_evolution_data.ParentStage]

        if comparison_mode_radio.value==ui_options.COMPAREMODE_MASSFIRST: 
            custom_yticks = [selected_massrange[0], selected_massrange[1]] 
            custom_xtick_labels = [
                parent_stage.short_name 
                if parent_stage in [stage.parent_stage for stage in available_substages] 
                else "" 
                for parent_stage in stellar_evolution_data.ParentStage
            ]

        if comparison_mode_radio.value==ui_options.COMPAREMODE_STAGEFIRST: 
            custom_yticks = sorted({m for substage in available_substages for m in (substage.mass_min, substage.mass_max)})
            custom_xtick_labels = [
                parent_stage.short_name 
                if parent_stage in [stage.parent_stage for stage in available_substages] 
                else "" 
                for parent_stage in stellar_evolution_data.ParentStage
            ]

        # Y axis: Mass
        ax.set_ylabel("Mass", fontsize=18, labelpad=14)
        ax.set_ylim(min(unique_masses), max(unique_masses))
        ax.set_yscale("log")
        ax.set_yticks(custom_yticks)
        ax.set_yticklabels([str(tick) for tick in custom_yticks], fontsize=14)
        ax.tick_params(axis="y", which="minor", length=0)
        for y in custom_yticks:
            ax.axhline(y, color="black", lw=0.5, ls=(0, (4, 3.6123)), zorder=0)

        # X axis: Evolution
        ax.set_xlabel("Evolutionary phase", fontsize=18, labelpad=14)
        ax.set_xlim(0, 9)
        custom_xticks = np.arange(0, len(stellar_evolution_data.ParentStage)) + 0.5
        ax.set_xticks(custom_xticks)
        ax.set_xticklabels(custom_xtick_labels, fontsize=14)


        if comparison_mode_radio.value==ui_options.COMPAREMODE_NOSELECTION: 
            for substage in stellar_evolution_data.SUBSTAGES_LIST: 
                draw_substage_box(
                    ax, 
                    substage, 
                    bg_color=substage.flowchart_color, 
                    bg_alpha=1.0, 
                    border_color="black", 
                    border_linewidth=1, 
                    text_color="black", 
                    text_fontsize=12, 
                )


        if comparison_mode_radio.value==ui_options.COMPAREMODE_MASSFIRST: 
            for substage in available_substages: 
                if substage.id == substage_selected.id: 
                    draw_substage_box(
                        ax, 
                        substage, 
                        bg_color=substage.flowchart_color, 
                        bg_alpha=1.0, 
                        border_color="black", 
                        border_linewidth=2, 
                        text_color="black", 
                        text_fontsize=12, 
                        text_y=np.sqrt(selected_massrange[0]*selected_massrange[1])
                    ) 
                else: 
                    draw_substage_box(
                        ax, 
                        substage, 
                        bg_color=substage.flowchart_color, 
                        bg_alpha=0.2, 
                        border_color="black", 
                        border_linewidth=1, 
                        text_color="black", 
                        text_fontsize=12, 
                        text_y=np.sqrt(selected_massrange[0]*selected_massrange[1])
                    )


        if comparison_mode_radio.value==ui_options.COMPAREMODE_STAGEFIRST: 
            for substage in available_substages: 
                if substage.id == substage_selected.id: 
                    draw_substage_box(
                        ax, 
                        substage, 
                        bg_color=substage.flowchart_color, 
                        bg_alpha=1.0, 
                        border_color="black", 
                        border_linewidth=2, 
                        text_color="black", 
                        text_fontsize=12 
                    ) 
                else: 
                    draw_substage_box(
                        ax, 
                        substage, 
                        bg_color=substage.flowchart_color, 
                        bg_alpha=0.2, 
                        border_color="black", 
                        border_linewidth=1, 
                        text_color="black", 
                        text_fontsize=12, 
                    ) 


        return mo.mpl.interactive(fig)






    flowchart = draw_flowchart()
    return (flowchart,)


@app.cell
def _(
    HR_diagram_plotting,
    comparison_mode_radio,
    histories_dict,
    history_plot_dropdown,
    model_selected,
    plot_mode_radio,
    plt,
    profile_plot_dropdown,
    profile_plot_x_dropdown,
    profile_plotting,
    profiles_dict,
    substage_selected,
    ui_options,
):
    # Create figure showing interior plot 







    def create_fig2(): 

        # Create small figure with an error message 
        def make_error_figure(message="Error"):
                fig, ax = plt.subplots(figsize=(6, 3))
                ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=12, color="gray")
                ax.axis("off")
                fig.tight_layout()
                return fig

        # If no data has been selected or no data is available for the current selection, return an error plot and escape 
        if model_selected == None: 
            return make_error_figure()



        # Otherwise, load history and profile for selected mass/modelnum from preloaded dictionaries 
        mass_selected = model_selected.mass 
        modelnum_selected = model_selected.model_example 
        profile = profiles_dict[(mass_selected, modelnum_selected)]
        history = histories_dict[mass_selected]



        # HR Diagram 
        if plot_mode_radio.value == ui_options.PLOTMODE_HRDIAGRAM: 
            hr = HR_diagram_plotting.HRDiagram() 
            hr.add_path(history, label=f"{history.star_mass[0]:.1f} $M_{{sun}}$", color=substage_selected.flowchart_color) 
            hr.legend() 
            fig2 = hr.fig 
            return fig2


    
        # History plots 
        if plot_mode_radio.value == ui_options.PLOTMODE_HISTORY: 

            selected_plot_func = history_plot_dropdown.value.plot_func 
            fig2 = selected_plot_func(history) 
            # history_plotting.add_substage_highlight(fig2, model_selected, history) 
            return fig2 



        # Interior profile plots 
        if plot_mode_radio.value == ui_options.PLOTMODE_PROFILE:

            # Create profile plot depending on selected options in dropdown 
            selected_plot_func = profile_plot_dropdown.value.plot_func 
            selected_x_axis = profile_plot_x_dropdown.value  
            fig2 = selected_plot_func(profile, selected_x_axis, history)

            # List of strings used in the title (i.e., "Interior composition of a" + "Subgiant" (with red text) + "star")
            if comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
                substage_str = model_selected.parent_substage.mode1_interior_plot_title
            if comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
                substage_str = model_selected.parent_substage.mode2_interior_plot_title
            profile_str = profile_plot_dropdown.value.title_str
            title_str_list = [profile_str, substage_str, "star"]  

            # List of colors used in title (i.e., "black" + "red" + "black") 
            substage_color = model_selected.parent_substage.flowchart_color 
            title_colors_list = ['black', substage_color, 'black'] 

            # Add colored region to title 
            profile_plotting.add_colored_title(fig2, title_str_list, title_colors_list, fontsize=20) 
            return fig2





    fig2 = create_fig2() 








    return (fig2,)


@app.cell
def _(load_data, mo, stellar_evolution_data):
    # Preload profiles and histories 

    fast_load = False  



    if fast_load == True: 
        fast_history = load_data.load_history(1.0)
        fast_profile = load_data.load_profile(1.0, 296, fast_history)






    # Get list of all models and masses that need to be loaded  
    models_list = [] 
    mass_list = [] 
    for substage in stellar_evolution_data.SUBSTAGES_LIST: 
        for model in substage.models: 
            models_list.append(model)  
            if model.mass not in mass_list: 
                mass_list.append(model.mass)



    # Load histories 
    histories_dict = {} 
    for mass in mo.status.progress_bar(
        mass_list, 
        remove_on_exit=True, 
        title="Loading histories", 
    ): 
        if mass in histories_dict: 
            continue 
        if fast_load == False: 
            histories_dict[mass] = load_data.load_history(mass) 
        if fast_load == True: 
            histories_dict[mass] = fast_history 


    # Load profiles 
    profiles_dict = {} 
    for model in mo.status.progress_bar(
        models_list, 
        remove_on_exit=True, 
        title="Loading profiles", 
    ): 
        mass = model.mass 
        modelnum = model.model_example 
        if fast_load == False: 
            profiles_dict[(mass, modelnum)] = load_data.load_profile(mass, histories_dict[mass], modelnum=modelnum) 
        if fast_load == True: 
            profiles_dict[(mass, modelnum)] = fast_profile



    return histories_dict, profiles_dict


@app.cell
def _():
    # Standard packages 
    import importlib 
    import os 
    import numpy as np 
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import matplotlib.colors as mcolors 

    # Nonstandard packages 
    import marimo as mo
    import mesa_reader as mr 

    # Packages I wrote 
    import utils.load_data as load_data 
    import utils.plotting.history_plotting as history_plotting 
    import utils.plotting.profile_plotting as profile_plotting 
    import utils.plotting.HR_diagram_plotting as HR_diagram_plotting
    import utils.config.stellar_evolution_data as stellar_evolution_data 
    import utils.config.ui_options as ui_options 

    importlib.reload(load_data)
    importlib.reload(history_plotting) 
    importlib.reload(profile_plotting) 
    importlib.reload(HR_diagram_plotting) 
    importlib.reload(stellar_evolution_data) 
    importlib.reload(ui_options) 

    plt.style.use('default') # Make sure the plots appear with a white background, even if the user is in dark mode 

    return (
        HR_diagram_plotting,
        load_data,
        mcolors,
        mo,
        mpatches,
        np,
        plt,
        profile_plotting,
        stellar_evolution_data,
        ui_options,
    )


if __name__ == "__main__":
    app.run()
