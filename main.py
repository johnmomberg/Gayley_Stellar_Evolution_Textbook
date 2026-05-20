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
    # Flowchart header "flowchart_subtitle" 
    with mo.status.spinner(title="Creating flowchart section...") as _: 
        flowchart_subtitle = mo.md("<h3>2. Choose type of star</h3>") 


    return (flowchart_subtitle,)


@app.cell(hide_code=True)
def _(mo):
    # Controls section header ("controls_subtitle") and secondary plot section header ("secondary_plot_subtitle")
    with mo.status.spinner(title="Creating Controls section subheaders...") as _: 
        controls_subtitle = mo.md("<h2>Controls</h2>") 
        secondary_plot_subtitle = mo.md("<h2>Plot</h2>") 

    return controls_subtitle, secondary_plot_subtitle


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
def _(mo, profile_plot_dropdown, profile_plot_x_dropdown, selected_row, src):
    # Plot mode profile string ("profile_str") which contains two dropdowns: "profile_plot_dropdown" and "profile_plot_x_dropdown" 

    with mo.status.spinner(title="Creating Profile plot mode text...") as _: 

        # Default values (if no substage is selected): Display an empty white line 
        substage_selected_str = "______" 
        substage_selected_color = "white"

        # Selected value 
        if selected_row is not None: 
            substage_selected_str = selected_row['Name'] 
            substage_selected_color = selected_row['Color'] 

        profile_str = mo.md(
            f"Interior profile: {profile_plot_dropdown} vs {profile_plot_x_dropdown} of a"
            f"{src.misc.set_textcolor_css(substage_selected_str, substage_selected_color)} star" )




    return (profile_str,)


@app.cell
def _(mo, src):
    # Create history browser free selection mode 

    with mo.status.spinner(title="Creating History data file browser...") as _: 

        history_browser = mo.ui.file_browser( 
            multiple=False, 
            selection_mode="directory", 
            restrict_navigation=True, 
            label="Select MESA data folder to be plotted...", 
            initial_path=src.data.file_paths.MESA_data_folder)



    return


@app.cell
def _(mo, src):
    # Create profile dropdown for free selection mode 

    with mo.status.spinner(title="Creating Profile data dropdown selector...") as _: 

        history_selected = None 
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






    return


@app.cell
def _(mo):
    # Create file uploader for mode 4 

    with mo.status.spinner(title="Creating file uploader...") as _: 
        uploaded_file = mo.ui.file(kind="button", max_size=500_000_000) 

    return (uploaded_file,)


@app.cell
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


@app.cell
def _():
    # "model_selector": either use "available_substages_tabs" or an hstack of "history_browser" and "profile_dropdown", depending on value of "comparison_mode_radio" 

    '''

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



    '''

    return


@app.cell
def _(alt, mo, np, pd):
    # Load csv and draw the flowchart


    with mo.status.spinner(title="Drawing flowchart...") as _: 

        # Load data 
        mesa_data_csv = pd.read_csv(
            "src/data/stars/evolutionary_stages.csv", 
            dtype={
                "model_start": "Int64", 
                "model_example": "Int64", 
                "model_end": "Int64"
            }, 
        ) 

        # Add extra fields to all data 
        mesa_data_csv["id"] = np.arange(len(mesa_data_csv))
        mesa_data_csv["x_min"] = mesa_data_csv["x"] - 0.5
        mesa_data_csv["x_max"] = mesa_data_csv["x"] + 0.5
        mesa_data_csv["x_mid"] = mesa_data_csv["x"]  # same as x, but explicit for clarity
        mesa_data_csv["y_mid"] = np.sqrt(mesa_data_csv["y_min"] * mesa_data_csv["y_max"])
        mesa_data_csv["Mass Range"] = (
            mesa_data_csv["Minimum Mass"].astype(str)
            + " - "
            + mesa_data_csv["Maximum Mass"].astype(str)
        )    
        mesa_data_csv["Text Location"] = np.sqrt(mesa_data_csv["Minimum Mass"] * mesa_data_csv["Maximum Mass"])

        # Create dataframe used by text boxes 
        mesa_data_csv_unique = mesa_data_csv.copy().drop_duplicates(subset=["Name"], keep="first")



        # X axis labels 
        stage_labels = {
            0: "Hayashi",
            1: "Henyey",
            2: "MS",
            3: "Post-MS", 
            4: "RG", 
            5: "He ign.", 
            6: "He MS", 
            7: "AGB", 
            8: "WD", 
        }
        label_expr = (
            "{"
            + ",".join(
                [f"'{k}':'{v}'" for k, v in stage_labels.items()]
            )
            + "}[datum.value]"
        )

        # Selection 
        selection = alt.selection_point(fields=["id"], empty=False)

        # X axis 
        xaxis = alt.X(
            "x_min:Q",
            scale=alt.Scale(domain=[-0.5, 8.5]),
            axis=alt.Axis(
                values=list(stage_labels.keys()),
                labelExpr=label_expr,
                grid=False,
            ),
            title="Evolutionary phase",
        )

        # Y axis 
        yaxis = alt.Y(
            "y_min:Q",
            scale=alt.Scale(type="log"),
            title="Initial mass",
        )

        # Bars (interactive layer)
        bars = (
            alt.Chart(mesa_data_csv)
            .mark_bar()
            .encode(
                x=xaxis,
                x2="x_max:Q",

                y=yaxis,
                y2="y_max:Q",

                color=alt.Color(
                    "Color:N",
                    scale=None,
                ),

                # Specify which parameters appear when you hover over a box 
                tooltip=[
                    "Name",
                    "Mass Range", 
                    "Displayed Mass (for plots)", 
                ],

                # Dim unselected boxes 
                opacity=alt.condition(
                    selection,
                    alt.value(1.0),
                    alt.value(0.6),
                ),

                # Thicker border on selected
                stroke=alt.condition(
                    selection,
                    alt.value("white"),
                    alt.value("lightgray"),
                ),
                strokeWidth=alt.condition(
                    selection,
                    alt.value(3),
                    alt.value(1),
                ),        
                strokeDash=alt.condition(
                    selection,
                    alt.value([]),        # solid line when selected (empty = solid)
                    alt.value([4, 6]),    # dashed when unselected (4px dash, 6px gap)
                ),

            )
            .add_params(selection)
        )



        # Borders around full boxes 
        text_bg = (
            alt.Chart(mesa_data_csv_unique)
            .mark_rect(
                color="transparent",
                stroke="white",
                strokeWidth=1,
            )
            .encode(
                x=alt.X("x_min:Q", scale=alt.Scale(domain=[-0.5, 8.5]), axis=None),
                x2="x_max:Q",
                y=alt.Y("Minimum Mass:Q", scale=alt.Scale(type="log")),
                y2="Maximum Mass:Q",
            )
        )

        # Text (centered in full box)
        text = (
            alt.Chart(mesa_data_csv_unique)
            .mark_text(
                align="center",
                baseline="middle",
                color="white",
                fontSize=16, 
                lineBreak="\n", 
            )
            .encode(
                x=alt.X("x_mid:Q", scale=alt.Scale(domain=[-0.5, 8.5]), axis=None),
                y=alt.Y("Text Location:Q", scale=alt.Scale(type="log")),
                text="Name:N",
            )
        )





        # Create figure 
        chart = (bars + text_bg + text).properties(width=1500,height=500)
        flowchart_marimo = mo.ui.altair_chart(chart)





    return flowchart_marimo, mesa_data_csv


@app.cell
def _(flowchart_marimo, mesa_data_csv, mo, pd, src):
    # Load history and profile files 

    with mo.status.spinner(title="Loading selected MESA files...") as _: 

        # If no box in flowchart is selected, return None for both history and profile 
        selected_rows = flowchart_marimo.apply_selection(mesa_data_csv) 
        if len(selected_rows) != 1: 
            history = None 
            profile = None 
            selected_row = None 

        # Otherwise, access data from the selected row 
        else: 
            selected_row = flowchart_marimo.apply_selection(mesa_data_csv).iloc[0]
            mesa_folder_path = src.data.file_paths.MESA_data_folder / selected_row["MESA_folder_path"]
            history = src.load_data.load_history(mesa_folder_path)

            if pd.isna(selected_row["model_example"]): 
                profile = None 

            else: 
                profile = src.load_data.load_profile(mesa_folder_path, selected_row["model_example"], history) 


    return history, profile, selected_row


@app.cell
def _(
    history,
    history_plot_dropdown,
    lru_cache,
    mesa_data_csv,
    mo,
    mpatches,
    np,
    pd,
    plot_mode_radio,
    profile,
    profile_plot_dropdown,
    profile_plot_x_dropdown,
    selected_row,
    src,
):
    # Create secondary figure 


    @lru_cache(maxsize=32) 
    def create_figure_2(): 

        # HR Diagram 
        if plot_mode_radio.value == src.data.marimo_ui_options.PLOTMODE_HRDIAGRAM: 
            hr = src.plot.hr.hr.HRDiagram() 

            # Escape if no file selected 
            if history is None: 
                return "ERROR: HR Diagram is unavailable for current selection." 

            for index, row in mesa_data_csv.iterrows():

                if row["Displayed Mass (for plots)"] != selected_row["Displayed Mass (for plots)"] or pd.isna(row["model_start"]) or pd.isna(row["model_end"]): 
                    continue 

                if index == selected_row.name: 
                    hr.add_path(
                        history, 
                        modelnum_start = row["model_start"], 
                        modelnum_end = row["model_end"], 
                        color = "black", 
                        lw = 3, 
                    )
                    lw=2 

                else: 
                    lw=1

                hr.add_path(
                    history, 
                    modelnum_start = row["model_start"], 
                    modelnum_end = row["model_end"], 
                    color = row["Color"], 
                    lw = lw, 
                    label = row["Short Name"], 
                )

            # Add extra stuff 
            # hr.add_age_labels(history)
            hr.legend(fontsize=12, loc="center left", bbox_to_anchor=(1, 0.5)) 
            hr.add_spectral_type_labels()  
            hr.add_radius_contours() 
            hr.ax.set_title(f"Evolutionary Path of {selected_row['Displayed Mass (for plots)']} $M_{{sun}}$", fontsize=20, pad=50)

            # Return figure 
            fig2 = hr.fig 
            return mo.mpl.interactive(fig2) 





        # History plots 
        if plot_mode_radio.value == src.data.marimo_ui_options.PLOTMODE_HISTORY: 

            # Escape if no file selected 
            if history is None: 
                return "ERROR: History Plot is unavailable for current selection." 

            # Create figure 
            selected_plot_func = history_plot_dropdown.value.plot_func 
            fig2 = selected_plot_func(history) 

            # Set view window to center on currently selected stage 
            if not pd.isna(selected_row["model_start"]) and not pd.isna(selected_row["model_end"]):
                x_stage_min = history.star_age[selected_row["model_start"]-1] 
                x_stage_max = history.star_age[selected_row["model_end"]-1] 
                x_stage_size = x_stage_max-x_stage_min 
                x_view_min = np.max([x_stage_min - x_stage_size/3, 0])
                x_view_max = np.min([x_stage_max + x_stage_size/3, np.max(history.star_age)])
                fig2.axes[0].set_xlim(x_view_min, x_view_max)

                # Highlight selected stage 
                src.plot.history.add_substage_highlight(
                    fig2, 
                    selected_row, 
                    history, 
                    include_label=True, 

                    lower_alpha=0.08, 
                    lower_border_linewidth=0, 
                    lower_border_color="black", 

                    upper_alpha=1.0, 
                    upper_border_linewidth=2, 
                    upper_border_color="black"
                )

            # Label all other stages with the same mass as the selected stage 
            for index, row in mesa_data_csv.iterrows():
                if row["Displayed Mass (for plots)"] != selected_row["Displayed Mass (for plots)"] or pd.isna(row["model_start"]) or pd.isna(row["model_end"]): 
                    continue 
                src.plot.history.add_substage_highlight(
                    fig2, 
                    row, 
                    history, 
                )

        #     # Add model number labels (if in mode 4)
        #     if comparison_mode_radio.value == src.data.marimo_ui_options.COMPAREMODE_FREE: 
        #         src.plot.history.add_model_labels_time(
        #             ax=fig2.axes[0], 
        #             history=history, 
        #             modelnum_now=modelnum_selected) 

            return mo.mpl.interactive(fig2) 





        # Interior profile plots 
        if plot_mode_radio.value == src.data.marimo_ui_options.PLOTMODE_PROFILE:

            if history is None or profile is None: 
                return "ERROR: Profile Plot is unavailable for current selection. Please select both a mass and an evolutionary stage to view plot. " 

            # Create profile plot depending on selected options in dropdown 
            selected_plot_func = profile_plot_dropdown.value.plot_func 
            selected_x_axis = profile_plot_x_dropdown.value  
            fig2 = selected_plot_func(profile = profile, xaxis = selected_x_axis, history = history)

            # Add colored text to title and colored background to figure 
            # if comparison_mode_radio.value != src.data.marimo_ui_options.COMPAREMODE_FREE: 
            if True: 

                # List of strings used in the title (i.e., "Interior composition of a" + "Subgiant" (with red text) + "star")
                profile_str = profile_plot_dropdown.value.title_str
                title_str_list = [profile_str, selected_row["Short Name"], "star"]  

                # List of colors used in title (i.e., "black" + "red" + "black") 
                title_colors_list = ['black', selected_row["Color"], 'black'] 

                # Add colored title 
                if profile_plot_dropdown.value.line_or_circle == "circle": 
                    title_fontsize = fig2._suptitle.get_fontsize() 
                    title_y = fig2._suptitle.get_position()[1] 
                    src.plot.profile.profile.add_colored_title(fig2, title_str_list, title_colors_list, y=title_y, fontsize=title_fontsize) 

                if profile_plot_dropdown.value.line_or_circle == "line": 
                    title_fontsize = fig2.axes[0].title.get_fontsize() 
                    src.plot.profile.profile.add_colored_title(fig2, title_str_list, title_colors_list, fontsize=title_fontsize) 

                # Face color of figure with low alpha 
                src.misc.set_bg_color(fig2, src.misc.blend_with_white(input_color=selected_row["Color"], alpha=0.06))

                # Draw a separate edge rectangle on top with full alpha
                rect = mpatches.Rectangle(
                    xy=(0, 0), 
                    width=1, 
                    height=1, 
                    transform=fig2.transFigure, 
                    facecolor='none', 
                    edgecolor=selected_row["Color"], 
                    linewidth=10, 
                    zorder=0, 
                )
                fig2.patches.append(rect)

            return mo.mpl.interactive(fig2) 






    with mo.status.spinner(title="Drawing secondary plot...") as _: 

        secondary_plot2 = create_figure_2() 

    return (secondary_plot2,)


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
        import pandas as pd 
        import altair as alt 

        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        import matplotlib.colors as mcolors 
        import matplotlib.ticker as mticker 
        import matplotlib.transforms as mtransforms 

        import mesa_reader as mr 
        import src

        plt.style.use('default') # Make sure the plots appear with a white background, even if the user is in dark mode 


    return Path, alt, lru_cache, mo, mpatches, np, pd, src, zipfile


@app.cell
def _(
    HR_diagram_str,
    controls_subtitle,
    flowchart_marimo,
    flowchart_subtitle,
    full_title,
    history_str,
    mo,
    plot_mode_radio,
    plot_mode_title,
    profile_str,
    secondary_plot2,
    secondary_plot_subtitle,
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

            flowchart_subtitle, 
            flowchart_marimo, 
            "\u200b", 
            mo.md("---"), 
            "\u200b", 

            secondary_plot_subtitle, 
            secondary_plot2, 
            "\u200b", 
            mo.md("---"), 

        ], 
        gap=0.7 
    ) 


    full_interface 



    return


if __name__ == "__main__":
    app.run()
