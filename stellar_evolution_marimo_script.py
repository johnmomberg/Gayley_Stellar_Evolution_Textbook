import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    # Title 

    full_title = mo.md("<h1>Stellar Evolution Flowchart</h1>") 
    return (full_title,)


@app.cell
def _(marimo_dropdown_constants, mo):
    # Comparison mode radio and dropdowns 

    # Flowchart comparison mode radio  
    comparison_mode_title = mo.md("<h2>Choose star visualized in bottom plot</h2>") 
    comparison_mode_dict = {
        "No selection": marimo_dropdown_constants.comparison_mode0, 
        "Select mass first": marimo_dropdown_constants.comparison_mode1, 
        "Select stage first": marimo_dropdown_constants.comparison_mode2 
    }
    comparison_mode_radio = mo.ui.radio(comparison_mode_dict, value=list(comparison_mode_dict.keys())[0]) 

    return comparison_mode_radio, comparison_mode_title


@app.cell
def _(data_structures, mo):
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
    marimo_dropdown_constants,
    mo,
    mode1_massrange_dropdown,
    mode2_parentstage_dropdown,
):
    # Comparison mode string 

    # String that appears depending on what comparison mode is selected. Includes a dropdown selector. 
    comparison_mode1_str = mo.md(f"View the evolution of a {mode1_massrange_dropdown} mass star: ") 
    comparison_mode2_str = mo.md(f"Compare how stars of different masses experience the {mode2_parentstage_dropdown} stage: ") 

    comparison_mode_str = "\u200b" 
    if comparison_mode_radio.value == marimo_dropdown_constants.comparison_mode1: 
        comparison_mode_str = comparison_mode1_str 
    if comparison_mode_radio.value == marimo_dropdown_constants.comparison_mode2: 
        comparison_mode_str = comparison_mode2_str 
    return (comparison_mode_str,)


@app.cell
def _(marimo_dropdown_constants, mo):
    # Plot mode radio selector. Empty because the strings are calculated and displayed next to the empty selector 
    plot_mode_title = mo.md("<h2>Choose variable displayed in bottom plot</h2>") 
    plot_mode_dict = {
        "": marimo_dropdown_constants.plot_mode_HR_diagram, 
        " ": marimo_dropdown_constants.plot_mode_history, 
        "  ": marimo_dropdown_constants.plot_mode_profile
    }
    plot_mode_radio = mo.ui.radio(options=plot_mode_dict, value=list(plot_mode_dict.keys())[0] ) 

    return plot_mode_radio, plot_mode_title


@app.cell
def _(marimo_dropdown_constants, mo):
    # option 0: HR Diagram 
    HR_diagram_str = mo.md("HR diagram")



    # option 1: history vs time  
    history_plot_options = {
        "Center composition": marimo_dropdown_constants.history_composition, 
        "Radius": marimo_dropdown_constants.history_radius, 
        "Fusion rate": marimo_dropdown_constants.history_fusion 

    }
    history_plot_dropdown = mo.ui.dropdown(options=history_plot_options, value=list(history_plot_options.keys())[0] )
    history_str = mo.md(f"History: {history_plot_dropdown} vs time") 

    return HR_diagram_str, history_plot_dropdown, history_str


@app.cell
def _(marimo_dropdown_constants, mo):

    # option 2: Interior profile 
    profile_plot_options = {
        "Composition": marimo_dropdown_constants.profile_composition, 
        "Convection": marimo_dropdown_constants.profile_convection, 
        "Temperature gradient (heat transport)": marimo_dropdown_constants.profile_tempgrad, 
        "Temperature (degeneracy)": marimo_dropdown_constants.profile_temp, 
        "Fusion rate": marimo_dropdown_constants.profile_fusion, 
    } 
    profile_plot_dropdown = mo.ui.dropdown(options=profile_plot_options, value=list(profile_plot_options.keys())[0] )

    return (profile_plot_dropdown,)


@app.cell
def _(marimo_dropdown_constants, mo):

    # X coord of interior: Either mass coord or radius coord 
    profile_plot_x_options = {
        "mass coordinate": marimo_dropdown_constants.profile_x_mass, 
        "radius coordinate": marimo_dropdown_constants.profile_x_radius
    }
    profile_plot_x_dropdown = mo.ui.dropdown(options=profile_plot_x_options, value=list(profile_plot_x_options.keys())[0] )

    return (profile_plot_x_dropdown,)


@app.cell
def _(
    comparison_mode_radio,
    marimo_dropdown_constants,
    mo,
    profile_plot_dropdown,
    profile_plot_x_dropdown,
    substage_selected,
):
    # Create string to show profile information 
    substage_selected_str = "______"
    if comparison_mode_radio.value==marimo_dropdown_constants.comparison_mode1: 
        substage_selected_str = substage_selected.mode1_interior_plot_title 
    if comparison_mode_radio.value==marimo_dropdown_constants.comparison_mode2: 
        substage_selected_str = substage_selected.mode2_interior_plot_title 
    profile_str = mo.md(f"Interior profile: {profile_plot_dropdown} vs {profile_plot_x_dropdown} of a **{substage_selected_str}** star")

    return (profile_str,)


@app.cell
def _(
    comparison_mode_radio,
    data_structures,
    marimo_dropdown_constants,
    mo,
    mode1_massrange_dropdown,
    mode2_parentstage_dropdown,
):
    # Available substages tabs 



    # Find all substages that exist within the currently selected mass range 
    if comparison_mode_radio.value == marimo_dropdown_constants.comparison_mode1 and mode1_massrange_dropdown.value is not None:
        m_low, m_high = map(float, mode1_massrange_dropdown.value.split('-')) 
        available_substages = [
            s for s in data_structures.SUBSTAGES_LIST
            if not (s.mass_max <= m_low or s.mass_min >= m_high)
        ]
        available_substages_options = {sub.mode1_abbrev: sub.mode1_desc for sub in available_substages}
        available_substages_tabs = mo.ui.tabs(available_substages_options, value=list(available_substages_options.keys())[0]) 

    # Find all substages that belong to the currently selected parent stage
    elif comparison_mode_radio.value == marimo_dropdown_constants.comparison_mode2 and mode2_parentstage_dropdown.value is not None:
        selected_parent_stage = mode2_parentstage_dropdown.value 
        available_substages = [
            s for s in data_structures.SUBSTAGES_LIST
            if s.parent_stage.name == selected_parent_stage.name 
        ] 
        if available_substages: 
            available_substages_options = {sub.mode2_abbrev_with_massrange: sub.mode2_desc_with_massrange for sub in available_substages} 
            available_substages_tabs = mo.ui.tabs(available_substages_options, value=list(available_substages_options.keys())[0]) 
        else: 
            available_substages_tabs = "" 

    # No selection 
    else: 
        available_substages_tabs = "" 


    return available_substages, available_substages_tabs, m_high, m_low


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


@app.cell(hide_code=True)
def _(
    available_substages,
    available_substages_tabs,
    comparison_mode_radio,
    m_high,
    m_low,
    marimo_dropdown_constants,
):
    # Choose substage selected and model used to represent this substage in bottom plot 

    substage_selected = None 
    model_selected = None 

    if comparison_mode_radio.value == marimo_dropdown_constants.comparison_mode1 and len(available_substages)>0: 
        substage_selected = [s for s in available_substages if s.mode1_abbrev==available_substages_tabs.value][0] 
        if len(substage_selected.models) > 0: 
            model_selected = [model for model in substage_selected.models if m_low<=model.mass<=m_high][0]
        else: 
            model_selected = None 

    if comparison_mode_radio.value == marimo_dropdown_constants.comparison_mode2 and len(available_substages)>0: 
        substage_selected = [s for s in available_substages if s.mode2_abbrev_with_massrange==available_substages_tabs.value][0]
        if len(substage_selected.models) > 0: 
            model_selected = next((model for model in substage_selected.models if model.is_default==True), None) 
            if model_selected is None: 
                model_selected = substage_selected.models[0]
        else: 
            model_selected = None 




    return model_selected, substage_selected


@app.cell(hide_code=True)
def _():
    # To do: 


    # Add labels showing regions of time plots 
    # Add code to other time plots 

    # Add title color code used by composition plot to other ones 

    # Reorder user interface 

    # Fix ylims of fusion vs time plot 

    # Fix HR diagram plot 

    # Make loading of profiles/histories dynamic: only load after you need them, then save as you go so you dont have to reload any 

    return


@app.cell(hide_code=True)
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
    import utils.marimo_dropdown_constants as marimo_dropdown_constants

    importlib.reload(constants) 
    importlib.reload(data_structures)
    importlib.reload(load_data)
    importlib.reload(plotting)
    importlib.reload(marimo_dropdown_constants)


    return (
        data_structures,
        importlib,
        load_data,
        marimo_dropdown_constants,
        mo,
        mpatches,
        np,
        plotting,
        plt,
    )


@app.cell(hide_code=True)
def _(
    available_substages,
    comparison_mode_radio,
    data_structures,
    m_high,
    m_low,
    marimo_dropdown_constants,
    mpatches,
    np,
    plt,
    substage_selected,
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

        if comparison_mode_radio.value==marimo_dropdown_constants.comparison_mode0: 
            custom_yticks = unique_masses 
            custom_xtick_labels = [parent_stage.short_name for parent_stage in data_structures.ParentStage]

        if comparison_mode_radio.value==marimo_dropdown_constants.comparison_mode1: 
            custom_yticks = [m_low, m_high] 
            custom_xtick_labels = [
                parent_stage.short_name 
                if parent_stage in [stage.parent_stage for stage in available_substages] 
                else "" 
                for parent_stage in data_structures.ParentStage
            ]

        if comparison_mode_radio.value==marimo_dropdown_constants.comparison_mode2: 
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


        if comparison_mode_radio.value==marimo_dropdown_constants.comparison_mode0: 
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


        if comparison_mode_radio.value==marimo_dropdown_constants.comparison_mode1: 
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
                        text_y=np.sqrt(m_low*m_high)
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
                        text_y=np.sqrt(m_low*m_high)
                    )


        if comparison_mode_radio.value==marimo_dropdown_constants.comparison_mode2: 
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
    marimo_dropdown_constants,
    model_selected,
    plot_mode_radio,
    plotting,
    plt,
    profile_plot_dropdown,
    profile_plot_x_dropdown,
    profiles_dict,
):
    # Create figure showing interior plot 






    # Rewrite this cell 
    # Rewrite implementation of label_substage and colored_title 




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
        if plot_mode_radio.value == marimo_dropdown_constants.plot_mode_HR_diagram: 
            return make_error_figure("HR diagram not yet implemented")



        # History plots 
        if plot_mode_radio.value == marimo_dropdown_constants.plot_mode_history: 

            if history_plot_dropdown.value == marimo_dropdown_constants.history_composition: 
                return make_error_figure("Center composition vs time")

            if history_plot_dropdown.value == marimo_dropdown_constants.history_radius: 
                return make_error_figure("Radius vs time")

            if history_plot_dropdown.value == marimo_dropdown_constants.history_fusion: 
                return make_error_figure("Fusion vs time")

    

        # Interior profile plots 
        if plot_mode_radio.value == marimo_dropdown_constants.plot_mode_profile:

            # Choose which plotting function to use based on which profile plot is selected 
            figure_options = {
                marimo_dropdown_constants.profile_composition: plotting.plot_profile_composition,
                marimo_dropdown_constants.profile_convection: plotting.plot_profile_convection,
                marimo_dropdown_constants.profile_tempgrad: plotting.plot_profile_tempgrad,
                marimo_dropdown_constants.profile_temp: plotting.plot_profile_temp, 
                marimo_dropdown_constants.profile_fusion: plotting.plot_profile_fusion, 
            }
            selected_plot_func = figure_options[profile_plot_dropdown.value]
            selected_x_axis = profile_plot_x_dropdown.value         
            fig2 = selected_plot_func(profile, history, )#x_axis=selected_x_axis) 

            # Add colored text to title of profile plots 
            profile_str_options = {
                marimo_dropdown_constants.profile_composition: "Interior composition of a", 
                marimo_dropdown_constants.profile_convection: "Heat transport regions inside a", 
                marimo_dropdown_constants.profile_tempgrad: "Temperature gradient across interior of a", 
                marimo_dropdown_constants.profile_temp: "Interior temperature profile of a", 
                marimo_dropdown_constants.profile_fusion: "Fusion rate across interior of a", 
            }
            substage_str_options = {
                marimo_dropdown_constants.comparison_mode1: model_selected.parent_substage.mode1_interior_plot_title,
                marimo_dropdown_constants.comparison_mode2: model_selected.parent_substage.mode2_interior_plot_title
            }
            title_str_list = [profile_str_options[profile_plot_dropdown.value], substage_str_options[comparison_mode_radio.value], "star"]
            title_colors_list = ['black', model_selected.parent_substage.flowchart_color, 'black']
            plotting.add_colored_title(fig2, title_str_list, title_colors_list, fontsize=20) 
            return fig2





    fig2 = create_fig2() 


    # comparison_mode_radio.value == 
    # comparison_mode0 
    # comparison_mode1
    # comparison_mode2

    # plot_mode_radio.value == 
    # plot_mode_HR_diagram
    # plot_mode_history
    # plot_mode_profile

    # history_plot_dropdown.value == 
    # history_composition
    # history_radius 
    # history_fusion

    # profile_plot_dropdown.value == 
    # profile_composition
    # profile_convection 
    # profile_tempgrad
    # profile_temp

    # profile_x_plot_dropdown.value == 
    # profile_x_mass
    # profile_x_radius 




    # def create_fig2_list(): 

    #     def make_error_figure(message="Error"):
    #         fig, ax = plt.subplots(figsize=(5, 3))
    #         ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=12, color="gray")
    #         ax.axis("off")
    #         fig.tight_layout()
    #         return fig

    #     if model_selected == None: 
    #         return [make_error_figure(message="Select a mass range and evolutionary stage to view plot")] 

    #     # Select first item in datapairs list 
    #     mass_selected = model_selected.mass 
    #     modelnum_selected = model_selected.model_example 

    #     # Load history and profile for selected mass/modelnum from preloaded dictionaries 
    #     profile = profiles_dict[(mass_selected, modelnum_selected)]
    #     history = histories_dict[mass_selected]



    #     if plots_dropdown.value == None: 
    #         return [make_error_figure(message="Select a parameter from the dropdown menu to visualize using plots")] 



    #     if plots_dropdown.value == 0: # HR diagram, radius  
    #         fig_HR = make_error_figure(message="HR diagram")
    #         fig_radius = plotting.plot_history_radius(history, modelnum_now = modelnum_selected)
    #         return [fig_HR, fig_radius] 



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



    #     if plots_dropdown.value == 2: # Heat transport 
    #         return [
    #             plotting.plot_profile_convection(profile, history), 
    #             plotting.plot_profile_tempgrad(profile, history) ] 

    #     if plots_dropdown.value == 3: # Fusion 
    #         fig_profile = plotting.plot_profile_fusion(profile, history)
    #         fig_history = plotting.plot_history_fusion(history, modelnum_now = modelnum_selected) 
    #         return [fig_profile, fig_history] 

    #     if plots_dropdown.value == 4: # Degeneracy 
    #         return [
    #             plotting.plot_profile_temp(profile, history), 
    #             make_error_figure(message="Comparison of de broglie wavelength to interparticle spacing") ] 





    return (fig2,)


@app.cell(hide_code=True)
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


if __name__ == "__main__":
    app.run()
