import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    # 
    # 
    # 
    # 
    # 
    # NOTE: Type "CTRL + ." or click the button with 3 rectangles on the bottom right of the screen to hide the code. 
    # 
    # 
    # 
    # 
    # 
    return


@app.cell(hide_code=True)
def _(mo):
    # Create title string "full_title"

    with mo.status.spinner(title="Creating title text...") as _: 
        full_title = mo.md("<h1>Interactive Stellar Evolution Visualizer</h1>") 

    return (full_title,)


@app.cell(hide_code=True)
def _(mo):
    # Add link to the Github under the title 

    with mo.status.spinner(title="Setting User Guide section text...") as _: 
        github_URL = "https://github.com/johnmomberg/Interactive_Stellar_Evolution_Visualizer"
        userguide_text = mo.md(
            f"""
            For detailed instructions on how to use this tool, see here: [{github_URL}]({github_URL}) 
            """
        )


    return (userguide_text,)


@app.cell(hide_code=True)
def _(mo):
    # Flowchart header "flowchart_subtitle" with switch to minimize it "flowchart_switch"
    with mo.status.spinner(title="Creating flowchart section...") as _: 
        flowchart_subtitle = mo.md("<h2>Flowchart</h2>") 
        flowchart_switch = mo.ui.switch(value=True, label="Hide / show") 
        flowchart_subtitle_hstack = mo.hstack([flowchart_subtitle, flowchart_switch], justify="space-between", align="center")


    return flowchart_subtitle_hstack, flowchart_switch


@app.cell(hide_code=True)
def _(mo):
    # Controls section header ("controls_subtitle") and secondary plot section header ("secondary_plot_subtitle")
    with mo.status.spinner(title="Creating Controls section subheaders...") as _: 
        controls_subtitle = mo.md("<h2>Controls</h2>") 
        secondary_plot_subtitle = mo.md("<h2>Plot</h2>") 

    return controls_subtitle, secondary_plot_subtitle


@app.cell(hide_code=True)
def _(mo, src):
    # Comparison mode radio 
    with mo.status.spinner(title="Creating Comparison Mode selector and subheader...") as _: 
        comparison_mode_title = mo.md("<h3>2. Choose type of star</h3>") 
        comparison_mode_radio = src.data.marimo_ui_options.create_radio(src.data.marimo_ui_options.COMPAREMODE_OPTIONS) 

    return comparison_mode_radio, comparison_mode_title


@app.cell(hide_code=True)
def _(mo, src):
    # Dropdowns used by "comparison_mode_str": either "mode1_massrange_dropdown" or "mode2_parentstage_dropdown" 

    with mo.status.spinner(title="Creating comparison mode dropdowns...") as _: 

        # Mode1 
        unique_masses = sorted({m for s in src.data.stars.sub_stages.ALL_SUBSTAGES_LIST for m in [s.mass_min, s.mass_max]})
        mode1_massrange_options = [f"{unique_masses[i]:.1f}-{unique_masses[i+1]:.1f}" for i in range(len(unique_masses)-1)]
        mode1_massrange_dropdown = mo.ui.dropdown(mode1_massrange_options, value=next(iter(mode1_massrange_options)))

        # Mode2 
        mode2_parentstage_options = {stage.full_name: stage for stage in src.data.stars.parent_stages.ALL_PARENTSTAGES_LIST} 
        mode2_parentstage_dropdown = mo.ui.dropdown(options=mode2_parentstage_options, value=next(iter(mode2_parentstage_options))) 



    return mode1_massrange_dropdown, mode2_parentstage_dropdown, unique_masses


@app.cell(hide_code=True)
def _(mo, mode1_massrange_dropdown, mode2_parentstage_dropdown):
    # Strings that go next to "comparison_mode_radio" containing dropdowns 

    with mo.status.spinner(title="Creating Comparison Mode radio options...") as _: 

        noselection_str = mo.md(f"No selection: \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b \u200b View entire flowchart")
        massfirst_str = mo.md(f"Select mass first: \u200b \u200b \u200b \u200b {mode1_massrange_dropdown} $M_{{sun}}$")
        stagefirst_str = mo.md(f"Select stage first: \u200b \u200b \u200b \u200b {mode2_parentstage_dropdown} stage") 
        freeselection_str = mo.md(f"Free exploration: \u200b \u200b \u200b \u200b \u200b Load MESA folder directly") 

    return freeselection_str, massfirst_str, noselection_str, stagefirst_str


@app.cell(hide_code=True)
def _(mo, src):
    # Plot mode section header ("plot_mode_title") and radio selector ("plot_mode_radio")  
    with mo.status.spinner(title="Creating Plot Mode selector and subheader...") as _: 
        plot_mode_title = mo.md("<h3>1. Choose variable to plot</h3>") 
        plot_mode_radio = src.data.marimo_ui_options.create_radio(src.data.marimo_ui_options.PLOTMODE_OPTIONS)

    return plot_mode_radio, plot_mode_title


@app.cell(hide_code=True)
def _(mo):
    # Plot mode HR diagram string "HR_diagram_str"
    with mo.status.spinner(title="Creating HR Diagram plot mode text...") as _: 
        HR_diagram_str = mo.md("HR diagram")

    return (HR_diagram_str,)


@app.cell(hide_code=True)
def _(mo, src):
    # Plot mode history string "history_str" which contains the dropdown "history_plot_dropdown" 
    with mo.status.spinner(title="Creating History plot mode dropdown and text...") as _: 
        history_plot_dropdown = src.data.marimo_ui_options.create_dropdown(src.data.marimo_ui_options.HISTORYPLOT_OPTIONS)
        history_str = mo.md(f"History: {history_plot_dropdown} vs time") 

    return history_plot_dropdown, history_str


@app.cell(hide_code=True)
def _(mo, src):
    # Plot mode profile Y coord dropdown ("profile_plot_dropdown") 
    with mo.status.spinner(title="Creating Profile plot mode dropdown...") as _: 
        profile_plot_dropdown = src.data.marimo_ui_options.create_dropdown(src.data.marimo_ui_options.PROFILEPLOT_OPTIONS) 

    return (profile_plot_dropdown,)


@app.cell(hide_code=True)
def _(mo, src):
    # Plot mode profile x coord dropdown ("profile_plot_x_dropdown") 
    with mo.status.spinner(title="Creating Profile X Coord plot mode dropdown...") as _: 
        profile_plot_x_dropdown = src.data.marimo_ui_options.create_dropdown(src.plot.profile.xaxis_options.PROFILEXAXIS_OPTIONS)

    return (profile_plot_x_dropdown,)


@app.cell(hide_code=True)
def _(
    comparison_mode_radio,
    mo,
    profile_plot_dropdown,
    profile_plot_x_dropdown,
    src,
    substage_selected,
):
    # Plot mode profile string ("profile_str") which contains two dropdowns: "profile_plot_dropdown" and "profile_plot_x_dropdown" 

    with mo.status.spinner(title="Creating Profile plot mode text...") as _: 

        # Default values (if no substage is selected): Display an empty white line 
        substage_selected_str = "______" 
        substage_selected_color = "white"

        if comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_MASSFIRST: 
            substage_selected_str = substage_selected.mode1_interior_plot_title 

        if comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_STAGEFIRST: 
            substage_selected_str = substage_selected.mode2_interior_plot_title 

        # Text color of substage's name in the displayed text should match its flowchart color 
        if substage_selected: 
            substage_selected_color = substage_selected.flowchart_color 


        profile_str = mo.md(
            f"Interior profile: {profile_plot_dropdown} vs {profile_plot_x_dropdown} of a "
            f"{src.misc.set_textcolor_css(substage_selected_str, substage_selected_color)} star" )





    return profile_str, substage_selected_color, substage_selected_str


@app.cell(hide_code=True)
def _(
    comparison_mode_radio,
    mo,
    mode1_massrange_dropdown,
    mode2_parentstage_dropdown,
    src,
):
    # Identify available substages 

    with mo.status.spinner(title="Identifying available substages...") as _: 

        selected_massrange = [float(num) for num in mode1_massrange_dropdown.value.split('-')] 
        selected_parentstage = mode2_parentstage_dropdown.value 

        if comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_NOSELECTION or comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_FREE: 
            available_substages = []

        elif comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_MASSFIRST: 
            available_substages = src.misc.CustomList([
                substage for substage in src.data.stars.sub_stages.ALL_SUBSTAGES_LIST 
                if not (substage.mass_max <= selected_massrange[0] 
                        or substage.mass_min >= selected_massrange[1])])

        elif comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_STAGEFIRST: 
            available_substages = src.misc.CustomList([
                substage for substage in src.data.stars.sub_stages.ALL_SUBSTAGES_LIST
                if hasattr(substage.parent_stage, "id") and substage.parent_stage.id == selected_parentstage.id
            ])

    return available_substages, selected_massrange, selected_parentstage


@app.cell(hide_code=True)
def _(
    available_substages,
    comparison_mode_radio,
    mo,
    np,
    selected_massrange,
    selected_parentstage,
    src,
):
    # Create available models 

    with mo.status.spinner(title="Finding models to go with available substages...") as _: 

        if comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_NOSELECTION or comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_FREE: 
            available_models = []

        elif comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_MASSFIRST: 
            available_models = src.misc.CustomList(
                [model for model in src.data.stars.MESA_models.ALL_MODELS_LIST 
                 if model.mass<=selected_massrange[1] and model.mass>=selected_massrange[0]]) 


        elif comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_STAGEFIRST: 

            potential_models = src.misc.CustomList([
                model for model in src.data.stars.MESA_models.ALL_MODELS_LIST
                if hasattr(model.substage, "parent_stage")
                and hasattr(model.substage.parent_stage, "id")
                and model.substage.parent_stage.id == selected_parentstage.id ]) 

            available_models = []
            for substage in available_substages:

                # Pick the model closest to the geometric center of this mass range 
                models_in_stage = src.misc.CustomList([m for m in potential_models if m.substage.id == substage.id])
                substage_geometric_center = np.sqrt(substage.mass_min*substage.mass_max)
                if models_in_stage:

                    closest_model = min(
                        models_in_stage,
                        key=lambda m: np.abs(np.log(m.mass) - np.log(substage_geometric_center))
                    )                

                    available_models.append(closest_model)

            available_models = src.misc.CustomList(available_models)



    return (available_models,)


@app.cell(hide_code=True)
def _(available_substages, comparison_mode_radio, mo, src):
    # Create available substage tab selector (if there are any available substages)


    with mo.status.spinner(title="Creating substages selector...") as _: 

        if len(available_substages) == 0: 
            available_substages_tabs = "" 
            available_substages_tabs_title = ""

        elif comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_MASSFIRST: 

            available_substages_options = {
                src.misc.set_textcolor_css(sub.mode1_abbrev, sub.flowchart_color): 
                sub.mode1_desc 
                for sub in available_substages}

            available_substages_tabs = mo.ui.tabs(
                available_substages_options, 
                value=list(available_substages_options.keys())[0]) 
            available_substages_tabs_title = mo.md("<h4>Choose an evolutionary stage:</h4>") 

        elif comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_STAGEFIRST: 

            available_substages_options = {
                src.misc.set_textcolor_css(sub.mode2_abbrev_with_massrange, sub.flowchart_color): 
                sub.mode2_desc_with_massrange 
                for sub in available_substages} 

            available_substages_tabs = mo.ui.tabs(
                available_substages_options, 
                value=list(available_substages_options.keys())[0]) 
            available_substages_tabs_title = mo.md("<h4>Choose a mass range:</h4>") 


    return available_substages_tabs, available_substages_tabs_title


@app.cell(hide_code=True)
def _(mo, src):
    # Create history browser free selection mode 

    with mo.status.spinner(title="Creating History data file browser...") as _: 

        history_browser = mo.ui.file_browser( 
            multiple=False, 
            selection_mode="directory", 
            restrict_navigation=True, 
            label="Select MESA data folder to be plotted...", 
            initial_path=src.data.file_paths.MESA_data_folder)



    return (history_browser,)


@app.cell(hide_code=True)
def _(history_selected, mo, src):
    # Create profile dropdown for free selection mode 

    with mo.status.spinner(title="Creating Profile data dropdown selector...") as _: 

        if history_selected is not None: 

            profile_dropdown = src.data.marimo_ui_options.create_dropdown(
                label="Profile selected: ", 
                options_list = [
                    src.data.marimo_ui_options.AvailableModelnumsOption(
                        modelnum=modelnum_, 
                        age=history_selected.star_age[modelnum_-1], 
                        display=f"Modelnum={modelnum_}, Age={history_selected.age_strings[modelnum_-1]}") 
                    for modelnum_ in history_selected.model_numbers_available]
            )

        else: 
            profile_dropdown = None  






    return (profile_dropdown,)


@app.cell(hide_code=True)
def _(mo):
    # Create file uploader for mode 4 

    with mo.status.spinner(title="Creating file uploader...") as _: 
        uploaded_file = mo.ui.file(kind="button", max_size=500_000_000) 

    return (uploaded_file,)


@app.cell(hide_code=True)
def _(Path, mo, src, uploaded_file, zipfile):
    # Download the file uploaded using the file uploader 



    def download_file(uploaded_file, target_dir = src.data.file_paths.MESA_data_folder): 

        # No file uploaded yet
        if not uploaded_file.value:
            print("Error: no file uploaded") 
            return 

        # Choose a target directory
        uploaded_zip_name = uploaded_file.name() # e.g. "mydata.zip"
        uploaded_bytes = uploaded_file.contents() # bytes
        download_zip_filepath = target_dir / uploaded_zip_name 



        # Uploaded file is not a .zip folder 
        if Path(uploaded_zip_name).suffix.lower() != ".zip": 
            print("Error: filename must end in .zip (uploaded file should be a zipped MESA data folder)") 
            return 

        # File already downloaded 
        if download_zip_filepath.with_suffix("").exists(): 
            print(f"Error: {download_zip_filepath.with_suffix('')} already exists") 
            return 



        # Save the uploaded zip to the target directory 
        with open(download_zip_filepath, "wb") as f:
            f.write(uploaded_bytes)
        print(f"Downloading zipped folder \'{uploaded_zip_name}\' to \'{download_zip_filepath}\'") 



        # Unzip the folder 
        with zipfile.ZipFile(download_zip_filepath, "r") as zf:
            zf.extractall(target_dir) 
        print(f"Extracting \'{download_zip_filepath}\' into \'{target_dir}\' folder")




        # Delete the zipped folder (only keep the extracted data)
        download_zip_filepath.unlink()
        print(f"Deleting ZIP file '{download_zip_filepath}'") 




    with mo.status.spinner(title="Downloading uploaded file...") as _: 
        download_file(uploaded_file)



    return


@app.cell(hide_code=True)
def _(
    Path,
    available_substages_tabs,
    comparison_mode_radio,
    history_browser,
    mo,
    profile_dropdown,
    src,
    uploaded_file,
):
    # "model_selector": either use "available_substages_tabs" or an hstack of "history_browser" and "profile_dropdown", depending on value of "comparison_mode_radio" 

    with mo.status.spinner(title="Choosing model selector...") as _: 

        first_3_options = [
            src.data.marimo_ui_options.COMPAREMODE_NOSELECTION, 
            src.data.marimo_ui_options.COMPAREMODE_MASSFIRST, 
            src.data.marimo_ui_options.COMPAREMODE_STAGEFIRST
        ]

        if comparison_mode_radio.value in first_3_options:  
            model_selector = available_substages_tabs 



        if comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_FREE: 

            if profile_dropdown is not None: 
                profile_dropdown_display = mo.vstack([f"File selected: \u200b \u200b \u200b \u200b \u200b {Path(history_browser.value[0].id)}", profile_dropdown]) 
            if profile_dropdown is None: 
                profile_dropdown_display = ""

            model_selector = mo.vstack(
                [
                    mo.md("<h4>File Browser</h4>"), 
                    history_browser, 
                    mo.hstack(
                        [
                            "Upload your own MESA file:", 
                            uploaded_file, 
                            "(Uploaded file must be a .zip compressed MESA data folder)"
                        ], 
                        justify="start", 
                        gap=0.2, 
                        widths=[0.4, 0.2, 1]
                    ), 
                    "(Don’t see your file? Try refreshing the File Browser.)", 
                    "\u200b", 
                    profile_dropdown_display
                ], 
                justify='space-around'
            ) 





    return (model_selector,)


@app.cell(hide_code=True)
def _(
    available_substages,
    available_substages_tabs,
    comparison_mode_radio,
    mo,
    src,
):
    # Identify available substage tab that is currently selected (if there are any available substages)

    with mo.status.spinner(title="Identifying currently selected substage...") as _: 

        if len(available_substages) == 0: 
            substage_selected = None 

        elif comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_MASSFIRST: 
            substage_selected = [
                s for s in available_substages 
                if src.misc.set_textcolor_css(s.mode1_abbrev, s.flowchart_color) == available_substages_tabs.value
            ][0] 

        elif comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_STAGEFIRST: 
            substage_selected = [
                s for s in available_substages 
                if src.misc.set_textcolor_css(s.mode2_abbrev_with_massrange, s.flowchart_color) == available_substages_tabs.value
            ][0]

    return (substage_selected,)


@app.cell(hide_code=True)
def _(available_models, mo, substage_selected):
    # Identify model used to represent selected substage 

    with mo.status.spinner(title="Finding model to represent selected substage...") as _: 

        model_selected = next((model for model in available_models if model.substage == substage_selected), None)

    return (model_selected,)


@app.cell(hide_code=True)
def _(
    Path,
    available_models,
    comparison_mode_radio,
    history_browser,
    mo,
    model_selected,
    src,
):
    # Load selected history 

    with mo.status.spinner(title="Loading MESA history file...") as _: 

        if model_selected is not None: 
            history_selected = src.load_data.load_history(model_selected.MESA_folder_path)
        elif comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_FREE: 
            if len(history_browser.value) > 0: 
                history_selected = src.load_data.load_history(Path(history_browser.value[0].id))
            else: 
                history_selected = None 

        # If we're in mode 1 and we're currently selecting the "no selection" tab, load the history from another tab and display it 
        elif comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_MASSFIRST: 
            history_selected = src.load_data.load_history(available_models[0].MESA_folder_path)
        else: 
            history_selected = None


    return (history_selected,)


@app.cell(hide_code=True)
def _(
    Path,
    history_browser,
    history_selected,
    mo,
    model_selected,
    profile_dropdown,
    src,
):
    # Load selected profile and modelnum 

    with mo.status.spinner(title="Loading MESA profile file...") as _: 

        if model_selected is not None: 
            modelnum_selected = model_selected.model_example 
            if modelnum_selected is None: 
                profile_selected = None 
            else: 
                profile_selected = src.load_data.load_profile(model_selected.MESA_folder_path, modelnum_selected, history_selected) 

        elif profile_dropdown is not None and profile_dropdown.value is not None and len(history_browser.value)>0: 
            modelnum_selected = profile_dropdown.value.modelnum 
            profile_selected = src.load_data.load_profile(Path(history_browser.value[0].id), modelnum_selected, history_selected)

        else: 
            modelnum_selected = None 
            profile_selected = None 

    return modelnum_selected, profile_selected


@app.cell(hide_code=True)
def _(
    available_substages,
    comparison_mode_radio,
    flowchart_switch,
    lru_cache,
    mo,
    mpatches,
    mticker,
    mtransforms,
    np,
    plt,
    selected_massrange,
    src,
    substage_selected,
    unique_masses,
):
    # Draw the flowchart






    def draw_spectraltype_labels_on_flowchart(fig, ax, yticks):

        # Find the closest spectral subtype to each y-tick 
        def _sample_visible_subtypes(ax, yticks):

            all_subtypes = [] 
            for stype in src.plot.hr.spectral_types.SPECTRAL_TYPES: 
                for subtype in stype.subtypes: 
                    all_subtypes.append(subtype)

            result = [] 
            for y in yticks:
                closest = min(all_subtypes, key=lambda s: abs(s.MS_mass - y))
                result.append(closest)            

            return result 



        subtypes_to_display = _sample_visible_subtypes(ax, yticks)
        transform = ax.get_yaxis_transform(which='grid')

        for subtype in subtypes_to_display:
            x = subtype.MS_mass 

            # Connector line (like a tick)
            connector = ax.plot(
                [1.0, 1.01], [x, x], 
                transform=transform, color='black', lw=0.8, clip_on=False
            )[0]

            # Text label
            txt = ax.text(
                1.012, x,
                f"{subtype.label.replace('V', '')} ({subtype.MS_mass} $M_{{sun}}$)",
                transform=transform,
                ha='left', va='center',
                fontsize=10, color='black'
            )

        # custom plt.ylabel on right side 
        fig.text(
            0.98, 0.56,
            "Spectral type on main sequence",
            va="center", 
            rotation=90, 
            fontsize = 11
        )

        # Add background colors for spectral PARENT types 
        for st in src.plot.hr.spectral_types.SPECTRAL_TYPES: 
            trans = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)
            ymin = st.MS_mass_range[0] 
            ymax = st.MS_mass_range[1]
            color = st.color 

            # Add colored rectangle above plot
            span = mpatches.Rectangle(
                xy = (1.00, ymin), 
                width = 0.01, 
                height = ymax-ymin, 
                transform = trans, 
                facecolor = color, 
                alpha = 1.0, 
                edgecolor = "white", 
                linewidth = 2, 
                clip_on = True ) 
            ax.add_patch(span) 

            # Set clip boundary of rectangle 
            clip_fig_rect = mpatches.Rectangle( 
                xy = (0, fig.subplotpars.bottom), 
                width = 1.0, 
                height = fig.subplotpars.top - fig.subplotpars.bottom, 
                transform=fig.transFigure, 
                facecolor="none", 
                edgecolor="none")
            span.set_clip_path(clip_fig_rect) 







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
            zorder=0 
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
    @lru_cache(maxsize=32) 
    def draw_flowchart():

        # Allow flowchart to be minimized 
        if flowchart_switch.value == False: 
            return "Flowchart minimized by user" 

        # If the user is freely selecting a MESA file, minimize the flowchart 
        if comparison_mode_radio.value==src.data.marimo_ui_options.COMPAREMODE_FREE: 
            return "Flowchart unavailable"

        fig, ax = plt.subplots(figsize=(15, 5))
        fig.subplots_adjust(top=0.95, bottom=0.16, left=0.07, right=0.90)

        if comparison_mode_radio.value==src.data.marimo_ui_options.COMPAREMODE_NOSELECTION: 
            custom_yticks = unique_masses 
            custom_xtick_labels = [parent_stage.short_name for parent_stage in src.data.stars.parent_stages.ALL_PARENTSTAGES_LIST] 

        if comparison_mode_radio.value==src.data.marimo_ui_options.COMPAREMODE_MASSFIRST: 
            custom_yticks = [selected_massrange[0], selected_massrange[1]] 
            custom_xtick_labels = [
                parent_stage.short_name 
                if parent_stage in [stage.parent_stage for stage in available_substages] 
                else "" 
                for parent_stage in src.data.stars.parent_stages.ALL_PARENTSTAGES_LIST
            ]

        if comparison_mode_radio.value==src.data.marimo_ui_options.COMPAREMODE_STAGEFIRST: 
            custom_yticks = sorted({m for substage in available_substages for m in (substage.mass_min, substage.mass_max)})
            custom_xtick_labels = [
                parent_stage.short_name 
                if parent_stage in [stage.parent_stage for stage in available_substages] 
                else "" 
                for parent_stage in src.data.stars.parent_stages.ALL_PARENTSTAGES_LIST
            ]

        # Y axis: Mass
        ax.set_ylabel("Initial Mass ($M_{{sun}}$)", fontsize=18, labelpad=14)
        ax.set_ylim(min(unique_masses), max(unique_masses))
        ax.set_yscale("log") 
        ax.yaxis.set_minor_formatter(mticker.NullFormatter())
        ax.set_yticks(custom_yticks)
        ax.set_yticklabels([str(tick) for tick in custom_yticks], fontsize=14)
        ax.tick_params(axis="y", which="minor", length=0)
        ax.grid(alpha=0.5, axis="y", color="black")
        draw_spectraltype_labels_on_flowchart(fig, ax, custom_yticks)  

        # X axis: Evolution
        ax.set_xlabel("Evolutionary phase", fontsize=18, labelpad=14)
        ax.set_xlim(0, 9)
        custom_xticks = np.arange(0, len(src.data.stars.parent_stages.ALL_PARENTSTAGES_LIST)) + 0.5
        ax.set_xticks(custom_xticks)
        ax.set_xticklabels(custom_xtick_labels, fontsize=14)




        # Draw selected substage 

        for substage in src.data.stars.sub_stages.ALL_SUBSTAGES_LIST: 
            if substage.parent_stage is None: 
                continue 

            if comparison_mode_radio.value==src.data.marimo_ui_options.COMPAREMODE_NOSELECTION: 
                draw_substage_box(
                    ax = ax, 
                    substage = substage, 
                    bg_color = substage.flowchart_color, 
                    bg_alpha = 1.0, 
                    border_color="black", 
                    border_linewidth = 1, 
                    text_color = "white", 
                    text_fontsize = 11, 
                ) 

            # Selected substage 
            elif substage is substage_selected: 
                draw_substage_box(
                    ax = ax, 
                    substage = substage, 
                    bg_color = substage.flowchart_color, 
                    bg_alpha = 1.0, 
                    border_color="black", 
                    border_linewidth = 4, 
                    text_color = "white", 
                    text_fontsize = 11, 
                ) 

            # Unselected, but available for comparision 
            elif substage in available_substages:             
                draw_substage_box(
                    ax = ax, 
                    substage = substage, 
                    bg_color = substage.flowchart_color, 
                    bg_alpha = 0.6, 
                    border_color="black", 
                    border_linewidth = 2, 
                    text_color = "white", 
                    text_fontsize = 11, 
                ) 

            # Unavailable substages (barely visible)
            else: 
                draw_substage_box(
                    ax = ax, 
                    substage = substage, 
                    bg_color = substage.flowchart_color, 
                    bg_alpha = 0.05, 
                    border_color="gray", 
                    border_linewidth = 1, 
                    text_color = "gray", 
                    text_fontsize = 11, 
                ) 



        return mo.mpl.interactive(fig)





    with mo.status.spinner(title="Drawing flowchart...") as _: 
        flowchart = draw_flowchart()

    return (flowchart,)


@app.cell(hide_code=True)
def _(
    available_models,
    comparison_mode_radio,
    history_plot_dropdown,
    history_selected,
    lru_cache,
    mo,
    model_selected,
    modelnum_selected,
    mpatches,
    np,
    plot_mode_radio,
    profile_plot_dropdown,
    profile_plot_x_dropdown,
    profile_selected,
    src,
    substage_selected_color,
    substage_selected_str,
):
    # Create figure showing interior plot 






    @lru_cache(maxsize=32) 
    def create_fig2(): 



        # HR Diagram 
        if plot_mode_radio.value == src.data.marimo_ui_options.PLOTMODE_HRDIAGRAM: 
            hr = src.plot.hr.hr.HRDiagram() 

            if history_selected is None: 
                return "ERROR: HR Diagram is unavailable for current selection." 


            if comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_MASSFIRST: 

                hr.ax.set_title(f"Evolution of {model_selected.mass} $M_{{sun}}$ star across HR Diagram", fontsize=20, pad=50) 
                hr.add_age_labels(history_selected) 

                for index, model in enumerate(available_models): 

                    if model.substage.parent_stage is None: 
                        continue 

                    if model.model_start is None: 
                        continue 

                    history = src.load_data.load_history(model.MESA_folder_path) 

                    # Selected substage: thicker linewidth with black border 
                    if model.id == model_selected.id: 

                        # Black border 
                        hr.add_path(
                            history, 
                            modelnum_start = model.model_start, 
                            modelnum_end = model.model_end, 
                            color = "black",  
                            alpha = 1, 
                            lw = 3 
                        )

                        hr.add_path(
                            history, 
                            modelnum_start = model.model_start, 
                            modelnum_end = model.model_end, 
                            color = model.substage.flowchart_color, 
                            label = f"{index}: {model.substage.mode1_abbrev}", 
                            alpha = 1, 
                            lw = 2 
                        ) 

                    # "No selection" selected: apply thicker lines to all, but not black border 
                    elif model_selected.substage.parent_stage is None: 

                        hr.add_path(
                            history, 
                            modelnum_start = model.model_start, 
                            modelnum_end = model.model_end, 
                            color = model.substage.flowchart_color, 
                            label = f"{index}: {model.substage.mode1_abbrev}", 
                            alpha = 1, 
                            lw = 2 
                        )

                    # Available for comparison but unselected substages: thinner linewidths 
                    else: 

                        hr.add_path(
                            history, 
                            modelnum_start = model.model_start, 
                            modelnum_end = model.model_end, 
                            color = model.substage.flowchart_color, 
                            label = f"{index}: {model.substage.mode1_abbrev}", 
                            alpha = 1, 
                            lw = 1 
                        )

            if comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_STAGEFIRST: 

                hr.ax.set_title(f"Location of {model_selected.substage.parent_stage.full_name} on HR Diagram", fontsize=20, pad=50) 
                hr.add_age_labels(history_selected) 

                for model in available_models: 

                    if model.substage.parent_stage is None: 
                        continue 

                    # Add thin-linewidth tracks showing entire evolution 
                    history = src.load_data.load_history(model.MESA_folder_path) 
                    hr.add_path(
                        history, 
                        color = model.substage.flowchart_color, 
                        lw = 0.5, 
                        alpha = 0.8, 
                        label = f"{model.mass} $M_{{sun}}$"
                    )

                    # Selected substage: thicker linewidth with black border 
                    if model.id == model_selected.id or model_selected.substage.parent_stage is None: 

                        # Black border 
                        hr.add_path(
                            history, 
                            modelnum_start = model.model_start, 
                            modelnum_end = model.model_end, 
                            color = "black",  
                            alpha = 1, 
                            lw = 3 
                        )

                        # Thick linewidth 
                        hr.add_path(
                            history, 
                            modelnum_start = model.model_start, 
                            modelnum_end = model.model_end, 
                            color = model.substage.flowchart_color, 
                            label = f"{model.substage.mode2_abbrev}", 
                            alpha = 1, 
                            lw = 2 
                        )



                    # Available for comparison but unselected substages: thicker linewidths but no black border 
                    else: 

                        hr.add_path(
                            history, 
                            modelnum_start = model.model_start, 
                            modelnum_end = model.model_end, 
                            color = model.substage.flowchart_color, 
                            label = f"{model.substage.mode2_abbrev}", 
                            alpha = 1, 
                            lw = 2 
                        )

            if comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_FREE: 
                hr.add_path(
                    history = history_selected, 
                    label = f"{history_selected.initial_mass_string} $M_{{sun}}$" )
                hr.add_modelnum_labels(
                    history = history_selected, 
                    modelnum_now = modelnum_selected) 

            hr.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5)) 
            hr.add_spectral_type_labels()  
            hr.add_radius_contours() 

            fig2 = hr.fig 
            return mo.mpl.interactive(fig2) 





        # History plots 
        if plot_mode_radio.value == src.data.marimo_ui_options.PLOTMODE_HISTORY: 

            if history_selected is None: 
                return "ERROR: History Plot is unavailable for current selection." 

            selected_plot_func = history_plot_dropdown.value.plot_func 
            fig2 = selected_plot_func(history_selected) 

            # Set view window to center on currently selected stage 
            if model_selected is not None: 
                if model_selected.model_start is not None: 
                    if model_selected.model_end is not None: 
                        x_stage_min = history_selected.star_age[model_selected.model_start-1] 
                        x_stage_max = history_selected.star_age[model_selected.model_end-1] 
                        x_stage_size = x_stage_max-x_stage_min 
                        x_view_min = np.max([x_stage_min - x_stage_size/3, 0])
                        x_view_max = np.min([x_stage_max + x_stage_size/3, np.max(history_selected.star_age)])
                        fig2.axes[0].set_xlim(x_view_min, x_view_max)

            # Highlight all regions 
            for model in available_models: 

                if model.mass != model_selected.mass: 
                    continue 

                if model.id == model_selected.id: 
                    src.plot.history.add_substage_highlight(
                        fig2, 
                        model, 
                        history_selected, 
                        include_label=model.id==model_selected.id, 

                        lower_alpha=0.1, 
                        lower_border_linewidth=0, 
                        lower_border_color="black", 

                        upper_alpha=1.0, 
                        upper_border_linewidth=2, 
                        upper_border_color="black", ) 
                else: 
                    src.plot.history.add_substage_highlight(
                        fig2, 
                        model, 
                        history_selected, 
                        include_label=model.id==model_selected.id, ) 

            # Add model number labels (if in mode 4)
            if comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_FREE: 
                src.plot.history.add_model_labels_time(
                    ax=fig2.axes[0], 
                    history=history_selected, 
                    modelnum_now=modelnum_selected) 

            return mo.mpl.interactive(fig2) 





        # Interior profile plots 
        if plot_mode_radio.value == src.data.marimo_ui_options.PLOTMODE_PROFILE:

            if history_selected is None or profile_selected is None: 
                return "ERROR: Profile Plot is unavailable for current selection. Please select both a mass and an evolutionary stage to view plot. " 

            # Create profile plot depending on selected options in dropdown 
            selected_plot_func = profile_plot_dropdown.value.plot_func 
            selected_x_axis = profile_plot_x_dropdown.value  
            fig2 = selected_plot_func(profile = profile_selected, xaxis = selected_x_axis, history = history_selected)



            # Add colored region to title 
            if comparison_mode_radio.value != src.data.marimo_ui_options.COMPAREMODE_FREE: 

                # List of strings used in the title (i.e., "Interior composition of a" + "Subgiant" (with red text) + "star")
                profile_str = profile_plot_dropdown.value.title_str
                title_str_list = [profile_str, substage_selected_str, "star"]  

                # List of colors used in title (i.e., "black" + "red" + "black") 
                title_colors_list = ['black', substage_selected_color, 'black'] 


                # Add colored title 
                if profile_plot_dropdown.value.line_or_circle == "circle": 
                    title_fontsize = fig2._suptitle.get_fontsize() 
                    title_y = fig2._suptitle.get_position()[1] 
                    src.plot.profile.profile.add_colored_title(fig2, title_str_list, title_colors_list, y=title_y, fontsize=title_fontsize)             
                if profile_plot_dropdown.value.line_or_circle == "line": 
                    title_fontsize = fig2.axes[0].title.get_fontsize() 
                    src.plot.profile.profile.add_colored_title(fig2, title_str_list, title_colors_list, fontsize=title_fontsize) 

            
                # Face color of figure with low alpha 
                src.misc.set_bg_color(fig2, src.misc.blend_with_white(input_color=substage_selected_color, alpha=0.06))

                # Draw a separate edge rectangle on top with full alpha
                rect = mpatches.Rectangle(
                    xy=(0, 0), 
                    width=1, 
                    height=1, 
                    transform=fig2.transFigure, 
                    facecolor='none', 
                    edgecolor=substage_selected_color, 
                    linewidth=10, 
                    zorder=0, 
                )
                fig2.patches.append(rect)


        
            return mo.mpl.interactive(fig2) 






    with mo.status.spinner(title="Drawing secondary plot...") as _: 

        secondary_plot = create_fig2() 








    return (secondary_plot,)


@app.cell(hide_code=True)
async def _():
    # Imports/setup 

    import marimo as mo



    with mo.status.spinner(title="Importing packages...") as _: 

        # Manually install packages in requirements.txt (in order to install packages whose pip install ___ name does not match their import ___ name) 
        import micropip # type: ignore
        await micropip.install([x.strip() for x in open("requirements.txt","r").readlines()])

        import os 
        import numpy as np 
        from pathlib import Path 
        import zipfile
        from functools import lru_cache 

        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        import matplotlib.colors as mcolors 
        import matplotlib.ticker as mticker 
        import matplotlib.transforms as mtransforms 

        import mesa_reader as mr 
        import src

        plt.style.use('default') # Make sure the plots appear with a white background, even if the user is in dark mode 


    return (
        Path,
        lru_cache,
        mo,
        mpatches,
        mticker,
        mtransforms,
        np,
        plt,
        src,
        zipfile,
    )


@app.cell(hide_code=True)
def _(
    HR_diagram_str,
    available_substages_tabs_title,
    comparison_mode_radio,
    comparison_mode_title,
    controls_subtitle,
    flowchart,
    flowchart_subtitle_hstack,
    freeselection_str,
    full_title,
    history_str,
    massfirst_str,
    mo,
    model_selector,
    noselection_str,
    plot_mode_radio,
    plot_mode_title,
    profile_str,
    secondary_plot,
    secondary_plot_subtitle,
    stagefirst_str,
    userguide_text,
):
    # MAIN 



    full_interface = mo.vstack(
        [
            full_title, 
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
            mo.hstack( 
                [     
                mo.hstack(
                    [
                        comparison_mode_radio, 
                        mo.vstack(
                            [
                                noselection_str, 
                                massfirst_str, 
                                stagefirst_str, 
                                freeselection_str
                            ], 
                            gap=0), 
                    ],
                    gap=0, align="center"), 
                mo.vstack([available_substages_tabs_title, model_selector]) 
                ], widths=[5, 10], align="start"), 
            "\u200b", 
            mo.md("---"), 
            "\u200b", 

            flowchart_subtitle_hstack, 
            flowchart, 
            "\u200b", 
            mo.md("---"), 
            "\u200b", 

            secondary_plot_subtitle, 
            secondary_plot, 
            "\u200b", 
            mo.md("---"), 

        ], 
        gap=0.7 
    ) 


    full_interface 



    return


if __name__ == "__main__":
    app.run()
