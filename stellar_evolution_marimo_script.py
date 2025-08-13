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
    fig1,
    fig2,
    full_title,
    history_str,
    mo,
    plot_mode_radio,
    plot_mode_title,
    profile_str,
):
    # MAIN 


    full_interface = mo.vstack(
        [
            mo.mpl.interactive(fig1), 
            "\u200b", 

            full_title, 
            "\u200b", 

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

            mo.mpl.interactive(fig2), 

        ], 
        gap=0.7 
    ) 


    full_interface 



    return


@app.cell
def _():
    # To do: 

    # Fix ylims of fusion vs time plot 

    # Plots to make work: 
    # HR diagram 
    # History: composition, radius, fusion  
    # Comparison of de broglie wavelength to interparticle spacing 

    # Rewrite implementation of add_substage_highlight and add_colored_title 

    # Make loading of profiles/histories dynamic: only load after you need them, then save as you go so you dont have to reload any 

    # Rewrite profile and history plotting functions with the boilerplate function so that the way they are used actually makes sense 

    return


@app.cell
def _(mo):
    # Title 
    full_title = mo.md("<h1>Stellar Evolution Flowchart</h1>") 

    return (full_title,)


@app.cell
def _(mo, ui_options):
    # Comparison mode radio 
    comparison_mode_title = mo.md("<h2>Choose star visualized in bottom plot</h2>") 
    comparison_mode_radio = ui_options.create_radio(ui_options.COMPAREMODE_OPTIONS) 

    return comparison_mode_radio, comparison_mode_title


@app.cell
def _(data_structures, mo):
    # Stage and mass selector dropdowns used by comparison mode string 

    # Mode1 
    unique_masses = sorted({m for s in data_structures.SUBSTAGES_LIST for m in [s.mass_min, s.mass_max]})
    mode1_massrange_options = [f"{unique_masses[i]:.1f}-{unique_masses[i+1]:.1f}" for i in range(len(unique_masses)-1)]
    mode1_massrange_dropdown = mo.ui.dropdown(mode1_massrange_options, value=next(iter(mode1_massrange_options)))

    # Mode2 
    mode2_parentstage_options = {stage.full_name: stage for stage in data_structures.ParentStage}
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
    plot_mode_title = mo.md("<h2>Choose variable displayed in bottom plot</h2>") 
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
def _(
    comparison_mode_radio,
    mo,
    profile_plot_dropdown,
    profile_plot_x_dropdown,
    substage_selected,
    ui_options,
):
    # Plot mode option 2: Add that together to create string with all profile dropdowns 
    substage_selected_str = "______" 

    if comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
        substage_selected_str = substage_selected.mode1_interior_plot_title 

    if comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
        substage_selected_str = substage_selected.mode2_interior_plot_title 

    profile_str = mo.md(f"Interior profile: {profile_plot_dropdown} vs {profile_plot_x_dropdown} of a **{substage_selected_str}** star")

    return (profile_str,)


@app.cell
def _(
    comparison_mode_radio,
    data_structures,
    mode1_massrange_dropdown,
    mode2_parentstage_dropdown,
    ui_options,
):
    # Identify available substages 

    selected_massrange = [float(num) for num in mode1_massrange_dropdown.value.split('-')] 
    selected_parentstage = mode2_parentstage_dropdown.value 

    if comparison_mode_radio.value == ui_options.COMPAREMODE_NOSELECTION: 
        available_substages = []

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
        available_substages = [
            s for s in data_structures.SUBSTAGES_LIST 
            if not (s.mass_max <= selected_massrange[0] 
                    or s.mass_min >= selected_massrange[1])]

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
        available_substages = [
            s for s in data_structures.SUBSTAGES_LIST 
            if s.parent_stage.name == selected_parentstage.name] 

    return available_substages, selected_massrange


@app.cell
def _(available_substages, comparison_mode_radio, mo, ui_options):
    # Create available substage tab selector (if there are any available substages)

    if len(available_substages) == 0: 
        available_substages_tabs = "" 

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
        available_substages_options = {sub.mode1_abbrev: sub.mode1_desc for sub in available_substages}
        available_substages_tabs = mo.ui.tabs(available_substages_options, value=list(available_substages_options.keys())[0]) 

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
        available_substages_options = {sub.mode2_abbrev_with_massrange: sub.mode2_desc_with_massrange for sub in available_substages} 
        available_substages_tabs = mo.ui.tabs(available_substages_options, value=list(available_substages_options.keys())[0]) 

    return (available_substages_tabs,)


@app.cell
def _(
    available_substages,
    available_substages_tabs,
    comparison_mode_radio,
    ui_options,
):
    # Identify available substage tab that is currently selected (if there are any available substages)

    if len(available_substages) == 0: 
        substage_selected = None 

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_MASSFIRST: 
        substage_selected = [s for s in available_substages if s.mode1_abbrev==available_substages_tabs.value][0] 

    elif comparison_mode_radio.value == ui_options.COMPAREMODE_STAGEFIRST: 
        substage_selected = [s for s in available_substages if s.mode2_abbrev_with_massrange==available_substages_tabs.value][0]

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
    data_structures,
    mpatches,
    np,
    plt,
    selected_massrange,
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

        fig, ax = plt.subplots(figsize=(15, 5))
        fig.subplots_adjust(top=0.95, bottom=0.16, left=0.07, right=1)

        if comparison_mode_radio.value==ui_options.COMPAREMODE_NOSELECTION: 
            custom_yticks = unique_masses 
            custom_xtick_labels = [parent_stage.short_name for parent_stage in data_structures.ParentStage]

        if comparison_mode_radio.value==ui_options.COMPAREMODE_MASSFIRST: 
            custom_yticks = [selected_massrange[0], selected_massrange[1]] 
            custom_xtick_labels = [
                parent_stage.short_name 
                if parent_stage in [stage.parent_stage for stage in available_substages] 
                else "" 
                for parent_stage in data_structures.ParentStage
            ]

        if comparison_mode_radio.value==ui_options.COMPAREMODE_STAGEFIRST: 
            custom_yticks = sorted({m for substage in available_substages for m in (substage.mass_min, substage.mass_max)})
            custom_xtick_labels = [
                parent_stage.short_name 
                if parent_stage in [stage.parent_stage for stage in available_substages] 
                else "" 
                for parent_stage in data_structures.ParentStage
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
        custom_xticks = np.arange(0, len(data_structures.ParentStage)) + 0.5
        ax.set_xticks(custom_xticks)
        ax.set_xticklabels(custom_xtick_labels, fontsize=14)


        if comparison_mode_radio.value==ui_options.COMPAREMODE_NOSELECTION: 
            for substage in data_structures.SUBSTAGES_LIST: 
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


        return fig


    fig1 = draw_flowchart()
    return (fig1,)


@app.cell
def _(
    comparison_mode_radio,
    histories_dict,
    history_plot_dropdown,
    importlib,
    model_selected,
    plot_mode_radio,
    plotting,
    plt,
    profile_plot_dropdown,
    profile_plot_x_dropdown,
    profiles_dict,
    ui_options,
):
    # Create figure showing interior plot 




    importlib.reload(plotting)



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
            return make_error_figure("HR diagram not yet implemented")



        # History plots 
        if plot_mode_radio.value == ui_options.PLOTMODE_HISTORY: 

            selected_plot_func = history_plot_dropdown.value.plot_func 
            fig2 = selected_plot_func(history, modelnum_selected) 
            plotting.add_substage_highlight(fig2, model_selected, history)
            return fig2 



        # Interior profile plots 
        if plot_mode_radio.value == ui_options.PLOTMODE_PROFILE:

            # Create profile plot depending on selected options in dropdown 
            selected_plot_func = profile_plot_dropdown.value.plot_func 
            selected_x_axis = profile_plot_x_dropdown.value  
            fig2 = selected_plot_func(profile, history, profilexaxis_option=selected_x_axis) 

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
            plotting.add_colored_title(fig2, title_str_list, title_colors_list, fontsize=20) 
            return fig2





    fig2 = create_fig2() 







    #     if plots_dropdown.value == 1: # Composition 

    #         fig_profile = plotting.plot_profile_composition(profile, history) 
    #         if flowchart_mode_radio.value == 1: 
    #             strings = ["Interior composition of a", model_selected.parent_substage.mode1_interior_plot_title, "star"] 
    #         if flowchart_mode_radio.value == 2: 
    #             strings = ["Interior composition of a", model_selected.parent_substage.mode2_interior_plot_title, "star"] 
    #         colors = ['black', model_selected.parent_substage.flowchart_color, 'black']
    #         plotting.colored_title(fig_profile, strings, colors, fontsize=20)

    #         fig_history = plotting.plot_history_centercomposition(history, modelnum_now = modelnum_selected) 
    #         fig_history = plotting.label_substage(fig_history, model_selected, history)

    #         return [fig_profile, fig_history] 







    return (fig2,)


@app.cell
def _(data_structures, load_data, mo):
    # Preload profiles and histories 

    fast_load = False  



    if fast_load == True: 
        fast_history = load_data.load_history(1.0)
        fast_profile = load_data.load_profile(1.0, 296, fast_history)






    # Get list of all models and masses that need to be loaded  
    models_list = [] 
    mass_list = [] 
    for substage in data_structures.SUBSTAGES_LIST: 
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
    # Imports 
    import marimo as mo
    import mesa_reader as mr 
    import importlib 
    import os 
    import numpy as np 

    import matplotlib.pyplot as plt
    plt.style.use('default') # Make sure the plots appear with a white background, even if the user is in dark mode 
    import matplotlib.patches as mpatches

    import utils.constants as constants 
    import utils.data_structures as data_structures 
    import utils.load_data as load_data 
    import utils.plotting as plotting 
    import utils.ui_options as ui_options 

    importlib.reload(constants) 
    importlib.reload(data_structures)
    importlib.reload(load_data)
    importlib.reload(plotting)
    importlib.reload(ui_options)
    return (
        data_structures,
        importlib,
        load_data,
        mo,
        mpatches,
        np,
        plotting,
        plt,
        ui_options,
    )


if __name__ == "__main__":
    app.run()
