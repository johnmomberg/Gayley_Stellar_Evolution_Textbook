import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    # To do: 


    # Add labels showing regions of time plots 
    # Add code to other time plots 

    # Add title color code used by composition plot to other ones 

    # Reorder user interface 

    # Fix ylims of fusion vs time plot 

    # Fix HR diagram plot 

    # Add 

    return


@app.cell
def _(
    fig1,
    fig2_list,
    flowchart_mode_radio,
    lower_tabs,
    mo,
    mode1_massrange_dropdown,
    mode2_parentstage_dropdown,
    plots_dropdown,
    upper_dropdown_vstack,
):
    # MAIN 



    mo.vstack([
        mo.md("<h2>1: Choose comparison mode</h2>"), 
        mo.hstack([flowchart_mode_radio, upper_dropdown_vstack], gap=1), 
        "\u200b", 

        {
            0: "\u200b", 
            1: mo.md(f"<h2>2: View evolution of a {mode1_massrange_dropdown.value} mass star</h2>"), 
            2: mo.md(f"<h2>2: Compare stars of different masses during the {mode2_parentstage_dropdown.value.full_name} stage</h2>")
        }[flowchart_mode_radio.value], 
        lower_tabs,  
        "\u200b", 

        {
            0: "\u200b", 
            1: mo.md(f"<h2>3: Choose parameter to visualize:</h2>"), 
            2: mo.md(f"<h2>3: Choose parameter to visualize:</h2>")  
        }[flowchart_mode_radio.value], 

        {
            0: "\u200b", 
            1: plots_dropdown, 
            2: plots_dropdown  
        }[flowchart_mode_radio.value],    
        "\u200b",

        mo.mpl.interactive(fig1),  
        mo.vstack([mo.mpl.interactive(fig2) for fig2 in fig2_list]), 

    ])

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

    importlib.reload(constants) 
    importlib.reload(data_structures)
    importlib.reload(load_data)
    importlib.reload(plotting)



    return data_structures, load_data, mo, mpatches, np, plotting, plt


@app.cell
def _(
    available_substages,
    data_structures,
    flowchart_mode_radio,
    m_high,
    m_low,
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
        x1 = substage.parent_stage.flowchart_x + 0.03 
        x2 = substage.parent_stage.flowchart_x+1 - 0.03
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

        if flowchart_mode_radio.value==0: 
            custom_yticks = unique_masses 
            custom_xtick_labels = [parent_stage.short_name for parent_stage in data_structures.ParentStage]

        if flowchart_mode_radio.value==1: 
            custom_yticks = [m_low, m_high] 
            custom_xtick_labels = [
                parent_stage.short_name 
                if parent_stage in [stage.parent_stage for stage in available_substages] 
                else "" 
                for parent_stage in data_structures.ParentStage
            ]

        if flowchart_mode_radio.value==2: 
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


        if flowchart_mode_radio.value==0: 
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


        if flowchart_mode_radio.value==1: 
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


        if flowchart_mode_radio.value==2: 
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


@app.cell(hide_code=True)
def _(mo):
    # Interior plots dropdown 


    plots_list = {
        "HR Diagram": 0, 
        "Composition": 1, 
        "Heat transport": 2, 
        "Fusion": 3,  
        "Degeneracy": 4, 
    }

    plots_dropdown = mo.ui.dropdown(options=plots_list) 
    return (plots_dropdown,)


@app.cell
def _(
    flowchart_mode_radio,
    histories_dict,
    model_selected,
    plots_dropdown,
    plotting,
    plt,
    profiles_dict,
):
    # Create figure showing interior plot 






    def create_fig2_list(): 

        def make_error_figure(message="Error"):
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=12, color="gray")
            ax.axis("off")
            fig.tight_layout()
            return fig

        if model_selected == None: 
            return [make_error_figure(message="Select a mass range and evolutionary stage to view plot")] 
        # if len(datapair_selected) == 0: 
        #     return [make_error_figure(message="No data available for this selection")] 

        # Select first item in datapairs list 
        mass_selected = model_selected.mass 
        modelnum_selected = model_selected.model_example 

        # Load history and profile for selected mass/modelnum from preloaded dictionaries 
        profile = profiles_dict[(mass_selected, modelnum_selected)]
        history = histories_dict[mass_selected]

        if plots_dropdown.value == None: 
            return [make_error_figure(message="Select a parameter from the dropdown menu to visualize using plots")] 

        if plots_dropdown.value == 0: # HR diagram, radius  
            fig_HR = make_error_figure(message="HR diagram")
            fig_radius = plotting.plot_history_radius(history, modelnum_now = modelnum_selected)
            return [fig_HR, fig_radius] 



        if plots_dropdown.value == 1: # Composition 

            fig_profile = plotting.plot_profile_composition(profile, history) 
            if flowchart_mode_radio.value == 1: 
                strings = ["Interior composition of a", model_selected.parent_substage.mode1_interior_plot_title, "star"] 
            if flowchart_mode_radio.value == 2: 
                strings = ["Interior composition of a", model_selected.parent_substage.mode2_interior_plot_title, "star"] 
            colors = ['black', model_selected.parent_substage.flowchart_color, 'black']
            plotting.colored_title(fig_profile, strings, colors, fontsize=20)

            fig_history = plotting.plot_history_centercomposition(history, modelnum_now = modelnum_selected) 
            fig_history = plotting.label_substage(fig_history, model_selected, history)

            return [fig_profile, fig_history] 



        if plots_dropdown.value == 2: # Heat transport 
            return [
                plotting.plot_profile_convection(profile, history), 
                plotting.plot_profile_tempgrad(profile, history) ] 

        if plots_dropdown.value == 3: # Fusion 
            fig_profile = plotting.plot_profile_fusion(profile, history)
            fig_history = plotting.plot_history_fusion(history, modelnum_now = modelnum_selected) 
            return [fig_profile, fig_history] 

        if plots_dropdown.value == 4: # Degeneracy 
            return [
                plotting.plot_profile_temp(profile, history), 
                make_error_figure(message="Comparison of de broglie wavelength to interparticle spacing") ] 




    fig2_list = create_fig2_list() 


    print(fig2_list) 

    return (fig2_list,)


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


@app.cell(hide_code=True)
def _(data_structures, mo):
    # Create flowchart mode radio and the dropdowns associated with mode1 and mode2 


    # The main radio button to switch between modes
    flowchart_mode_radio = mo.ui.radio(
        options={"No selection": 0, "Select mass first": 1, "Select stage first": 2}, value="No selection"
    )

    # Mode1 
    unique_masses = sorted({m for s in data_structures.SUBSTAGES_LIST for m in [s.mass_min, s.mass_max]})
    mode1_massrange_options = [f"{unique_masses[i]:.1f}-{unique_masses[i+1]:.1f}" for i in range(len(unique_masses)-1)]
    mode1_massrange_dropdown = mo.ui.dropdown(mode1_massrange_options, value=next(iter(mode1_massrange_options)))

    # Mode2 
    mode2_parentstage_options = {stage.full_name: stage for stage in data_structures.ParentStage}
    mode2_parentstage_dropdown = mo.ui.dropdown(options=mode2_parentstage_options, value=next(iter(mode2_parentstage_options))) 



    return (
        flowchart_mode_radio,
        mode1_massrange_dropdown,
        mode2_parentstage_dropdown,
        unique_masses,
    )


@app.cell(hide_code=True)
def _(
    data_structures,
    flowchart_mode_radio,
    mo,
    mode1_massrange_dropdown,
    mode2_parentstage_dropdown,
):
    # Create UI (upper_dropdown_vstack and lower_tabs) 



    if flowchart_mode_radio.value == 1 and mode1_massrange_dropdown.value is not None:
        # Find all substages that exist within the currently selected mass range 
        m_low, m_high = map(float, mode1_massrange_dropdown.value.split('-')) 
        available_substages = [
            s for s in data_structures.SUBSTAGES_LIST
            if not (s.mass_max <= m_low or s.mass_min >= m_high)
        ]
        upper_dropdown_vstack = mo.vstack(["\u200b", mo.md(f"{mode1_massrange_dropdown}"), "\u200b"], gap=0.1) 

        # Create the tabs using the data from the filtered substages
        tabs_options = {sub.mode1_abbrev: sub.mode1_desc for sub in available_substages}
        lower_tabs = mo.ui.tabs(tabs_options, value=next(iter(tabs_options)))



    elif flowchart_mode_radio.value == 2 and mode2_parentstage_dropdown.value is not None:
        # Find all substages that belong to the currently selected parent stage
        selected_parent_stage = mode2_parentstage_dropdown.value 
        available_substages = [
            s for s in data_structures.SUBSTAGES_LIST
            if s.parent_stage.name == selected_parent_stage.name 
        ] 
        upper_dropdown_vstack = mo.vstack(["\u200b", "\u200b", mo.md(f"{mode2_parentstage_dropdown}")], gap=0.1)

        # Create the tabs using the data from the filtered substages
        if available_substages: 
            tabs_options = {sub.mode2_abbrev_with_massrange: sub.mode2_desc_with_massrange for sub in available_substages} 
            lower_tabs = mo.ui.tabs(tabs_options, value=next(iter(tabs_options)))
        else: 
            lower_tabs = "" 



    else: # No selection
        upper_dropdown_vstack = mo.vstack(["\u200b", "\u200b", "\u200b"], gap=0.1)
        lower_tabs = "" 



    return (
        available_substages,
        lower_tabs,
        m_high,
        m_low,
        upper_dropdown_vstack,
    )


@app.cell(hide_code=True)
def _(available_substages, flowchart_mode_radio, lower_tabs, m_high, m_low):
    # Choose substage selected and model used to represent this substage 


    substage_selected = None 
    model_selected = None 

    if flowchart_mode_radio.value == 1 and len(available_substages)>0: 
        substage_selected = [s for s in available_substages if s.mode1_abbrev==lower_tabs.value][0] 
        if len(substage_selected.models) > 0: 
            model_selected = [model for model in substage_selected.models if m_low<=model.mass<=m_high][0]
        else: 
            model_selected = None 

    if flowchart_mode_radio.value == 2 and len(available_substages)>0: 
        substage_selected = [s for s in available_substages if s.mode2_abbrev_with_massrange==lower_tabs.value][0]
        if len(substage_selected.models) > 0: 
            model_selected = next((model for model in substage_selected.models if model.is_default==True), None) 
            if model_selected is None: 
                model_selected = substage_selected.models[0]
        else: 
            model_selected = None 




    return model_selected, substage_selected


if __name__ == "__main__":
    app.run()
