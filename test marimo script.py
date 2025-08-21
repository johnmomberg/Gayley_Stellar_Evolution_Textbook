import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _(Path):
    data_folder = Path("C:/Users/johnm/Local Desktop/Gayley/MESA output files/")

    return


@app.cell
def _():
    # Goal: Rewrite loading data functions 

    import marimo as mo 
    import mesa_reader as mr 
    from pathlib import Path 
    from functools import lru_cache 
    import matplotlib.pyplot as plt 







    # lru_cache allows you to cache function calls. maxsize is the number of distinct calls it can hold in memory at once. 
    # If you run load_history() on the same input a 2nd time, it doesn't actually run the function again; 
    # it just loads the pre-saved data. This makes load_history much faster. 
    @lru_cache(maxsize=32) 
    def load_history(MESA_folder_path): 

        try: 
            history = mr.MesaData(str(MESA_folder_path/"history.data"))  
            folder_mesa = mr.MesaLogDir(MESA_folder_path, history_file="history.data") 

        except FileNotFoundError: 
            history = mr.MesaData(str(MESA_folder_path/"trimmed_history.data"))  
            folder_mesa = mr.MesaLogDir(MESA_folder_path, history_file="trimmed_history.data") 

        history.model_numbers_available = folder_mesa.model_numbers
        return history 




    @lru_cache(maxsize=128)
    def load_profile(MESA_folder_path, modelnum, history=None): 

        try: 
            folder_mesa = mr.MesaLogDir(str(MESA_folder_path), history_file="history.data") 

        except mr.BadPathError: 
            folder_mesa = mr.MesaLogDir(str(MESA_folder_path), history_file="trimmed_history.data") 

        # Load profile; add some additional important info to profile variable 
        profile = folder_mesa.profile_data(modelnum) 
        profile.modelnum = modelnum 
        profile.index = modelnum-1 
        if history is not None: 
            profile.age = history.star_age[profile.index] 
            profile.initial_mass = history.star_mass[0]
        return profile 





    return Path, mo, plt


@app.cell
def _():
    # history_browser = mo.ui.file_browser( 
    #     multiple=False, 
    #     selection_mode="directory", 
    #     restrict_navigation=True, 
    #     label="Choose MESA data folder to load history + profile from", 
    #     initial_path=data_folder) 

    # history_browser 
    return


@app.cell
def _():
    # profile_selector = mo.ui.dropdown(options=history.model_numbers_available) 
    # profile_selector 
    return


@app.cell
def _():
    # history = load_history(Path(history_browser.value[0].id) ) 

    return


@app.cell
def _():
    # profile = load_profile(Path(history_browser.value[0].id), modelnum=profile_selector.value, history=history)

    return


@app.cell
def _(mo):
    test_dropdown = mo.ui.dropdown(options=["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]) 
    test_dropdown 
    return (test_dropdown,)


@app.cell
def _(plt, test_dropdown):
    def f(): 
        fig, ax = plt.subplots(figsize=(10.7, 7))
        ax.plot([0,1,2,3,4,5,6,7], [0,1,1,2,1,2,0,1]) 
        ax.set_title(test_dropdown.value) 
        return fig 

    fig = f() 


    return (fig,)


@app.cell
def _(fig, mo):
    test = mo.mpl.interactive(fig) 
    test


    return


if __name__ == "__main__":
    app.run()
