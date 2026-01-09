# Interactive Stellar Evolution Visualizer

## Quick Start

This tool uses MESA stellar models to create visualizations of the key properties of different types of stars. 

Click here to load the tool in your browser: https://marimo.app/github.com/johnmomberg/Interactive_Stellar_Evolution_Visualizer/blob/main/main.py 
- To hide the code, click the button with **three boxes** in the bottom-right corner of the screen.

--- 

## How to give feedback  

There are several ways that you can give feedback (report a bug, make suggestions, etc):
- Add an issue to this repository’s **Issues** tab.  
- Email me at john-momberg@uiowa.edu 
- Fill out this survey about your experience using this program:  
  https://docs.google.com/forms/d/e/1FAIpQLSfM8DIz6Jri5ruX6axiyvR9M9x5XapsTQQrbQr-yVbNdOL2TA/viewform?usp=header 

--- 

## Detailed Walkthrough / User Guide 

### Controls 
To use this tool, first make a selection using the Controls section. Depending on the options you select, the corresponding plot will be generated and displayed in the Plot section below. 


#### 1. Choose variable to plot 
Select the type of plot you want to generate:

- **HR diagram**: Shows the star’s path across the HR diagram. 
- **History**: a variable vs. time (e.g., radius vs. time). 
- **Interior profile**: interior structure (variable vs. location inside the star) at a snapshot in time.

For **Interior profile**, you can additionally select the units used on the x-axis: 
- **Radius**: Distance from the center (standard) 
- **Mass coordinate**: The amount of mass interior to each point. (For example, 'x = 1.5' means the location in the star where a sphere extending to your current radius would contain a total of 1.5 solar masses). 


#### 2. Choose type of star 
This tool emphasizes the ability to make comparisons. There are two types of comparisons students might want to make: 

- A: Compare one star at different points in its life
- B: Compare stars of different masses at the same point in their lives

In order to allow for both types of comparison, the way that you select a star depends on what you want to compare it to. Before selecting a star, you must choose a "comparison mode" from the following options: 

##### A. Select *mass* first
Use this when you want to follow one star through its evolution. (For example: for a 1.0 solar mass star, how does the star change from the main sequence to the red giant phase?) 

1. First, select a **mass range** from the dropdown. 
2. The UI will show the evolutionary stages your selected mass goes through. (Different masses go through different stages, so the options displayed will depend on your previous selection.) 
3. Next, choose an **evolutionary stage** from the tabs that appear.  

Use this mode to answer the question: *"How does a particular star change over time?"*

##### B. Select *stage* first
Use this to compare how a particular evolutionary stage is experienced by stars of different masses. (For example: during the main sequence, what is the difference between a low-mass star and a high-mass star?) 

1. First, select an **evolutionary stage** from the dropdown.  
2. The UI will display which mass ranges have distinct behavior during that stage. (Different stages have different mass ranges where distinct behavior occurs, so the options displayed will depend on your previous selection.)
3. Next, choose a **mass range** from the tabs that appear.

Use this mode to answer the question: *“How do stars of different masses look at this particular stage?”*

##### C. Free exploration

This tool also functions as a general MESA file explorer. Rather than viewing types of stars in the context of their evolutionary stage ("main sequence", "red giant", "low mass", "high mass", etc), you can instead directly select the MESA file you would like to visualize. 

1. Use the File Browser to select a MESA folder. To select a folder, click on the icon to the left of its name. (Don't click the folder name; that enters the folder) 
2. Once a MESA folder has been selected, choose a specific point in time. Each point in time that can be selected is given a "model number" or "modelnum", which simply tells the program which MESA file to load. (Model numbers are used because models are not spaced linearly in time; more models are created during times where the star changes rapidly, and fewer models are created during times where the star goes long periods of time without changing.)

##### Upload your own MESA folder 

You can upload MESA run in order to apply the visualizations I've created to your own data. 

1. A proper MESA folder should contain 'history.data' or 'trimmed_history.data' and a sequence of profile files like 'profile1.data', 'profile2.data', etc.  
2. Compress your MESA folder (right-click -> compress to .zip) 
3. Click **Upload** and select your .zip MESA folder

After uploading, the folder may not immediately appear in the file browser. To fix this, follow these steps to refresh the file browser: 
1. Click the special folder **“Click HERE to refresh file browser”** to enter it.  
2. Inside is another fake folder labeled **“Click Back Arrow to refresh file browser”**. This folder simply exists so that its title instructs you what to do next: Click the **back arrow** to return to the parent folder.  
3. Entering and leaving a subfolder forces the file browser to refresh, and your uploaded folder should now be visible.

If you are unfamiliar with MESA, but want to try it out for yourself, there is any easy way to generate your own MESA file in your web browser. Simply go to the following website: http://user.astro.wisc.edu/~townsend/static.php?ref=mesa-web-submit 

### Flowchart 

Below the controls section, you will see the **Evolutionary Flowchart**. This diagram gives an overview of stellar evolution as a whole and shows how stars of different masses evolve. 

- Y-axis: Initial mass. For a given value of mass, you can move horizontally to see how stars of that mass evolve. 
- X-axis: Evolutionary stage. This axis can be thought of as corresponding to age, but note that it is not actually linear in time, since stars spend different amounts of time in each stage, and their lifetimes depend heavily on their mass. 

Various types of stars at different points in their lives are represented as boxes in the flowchart. The vertical extent of each box represents the range of masses that pass through this particular evolutionary stage. Moving vertically between two boxes allows users to see the boundary between two distinct types of evolution. 

Blank space represents a range of masses that does not experience a certain stage at all. (For example, stars smaller than 0.5 solar masses never get hot enough to fuse helium, so they skip directly from the Red Giant phase to the White Dwarf phase.) As you move horizontally, if you encounter a blank region, you can skip immediatly through the blank region until you reach the next box. 

The right side of the flowchart shows the corresponding **spectral type** for each mass. Note that this spectral type denotes the spectral type that star has *when it's on the main sequence*, not its spectral type at any other point in its life (since spectral type can change over time). The goal of these labels is to provide a conversion between describing stars as their spectral type to what mass that correlates to. For instance, if you're reading a paper that talks about the evolution of B3 stars, you might wonder where in this flowchart do those types of stars occur? This spectral type axis provides a way to make that conversion. 

The flowchart will highlight the evolutionary stages which are currently available for comparison, depending on the comparison mode selected. 
- Select mass first: A horizontal row will be highlighted, corresponding to the mass you've selected
- Select stage first: A vertical column will be highlighted, corresponding to the evolutionary stage you've selected

Either way, the specific evolutionary stage selected will be additionally highlighted, with the other stages currently available for comparison highlighted as well but to a lesser degree. 

To minimize the flowchart, click the "Hide/show" slider. 

### Plot 

After making your selections in the Controls section, the requested plot will be generated and displayed in the Plot section. 


--- 

## Acknowledgements 

This project was funded by the OpenHawks Open Educational Resources (OER) Grant, provided by the University of Iowa Office of the Provost and the UI Libraries. 

This project would not be possible without the MESA (Modules for Experimentes in Stellar Astrophysics) stellar evolution modeling software. For more information about MESA, see here: https://mesastar.org/ 

I would like to thank Ken Gayley, my PhD advisor, for support and guidance throughout this project. 

Next, I would like to thank Philip Griffin for introducing me to Marimo, which forms the backbone of the interactivity of this entire project. For more information about Marimo, see here: https://marimo.io/ 

Finally, I want to thank everyone who has helped me test this project and gave me feedback, including but not limited to: Andi Swirbul, Nathan Helvy, Scott Call, Chris Piker 

---


