from dataclasses import dataclass
from enum import Enum
from typing import Optional






class ParentStage(Enum):
    """Defines the primary, high-level stages of stellar evolution."""
    HAYASHI = ("Hayashi", "Hayashi track", 0) 
    HENYEY = ("Henyey", "Henyey track", 1)
    MAIN_SEQUENCE = ("MS", "Main Sequence", 2)
    POST_MAIN_SEQUENCE = ("Post-MS", "Post-Main Sequence", 3)
    RED_GIANT_BRANCH = ("RG", "Red Giant", 4)
    HELIUM_IGNITION = ("He ign.", "Helium ignition", 5)
    HELIUM_MAIN_SEQUENCE = ("He MS", "Helium Main Sequence", 6)
    ASYMPTOTIC_GIANT_BRANCH = ("AGB", "Asymptotic Giant Branch", 7)
    WHITE_DWARF = ("WD", "White Dwarf", 8)

    @property
    def short_name(self):
        return self.value[0]

    @property
    def full_name(self):
        return self.value[1]
    
    @property 
    def flowchart_x(self): 
        return self.value[2]  





@dataclass
class SubStageModel:
    """The model number used to represent a particular substage at a particular mass"""
    mass: float 
    model_example: int 
    is_default: bool = False # Choose one datapoint (i.e., a particular mass) for each substage to take precedence as the "default" mass used to represent that stage 
    model_start: int | None = None # Allow None, default to None 
    model_end: int | None = None # Allow None, default to None 
    parent_substage: Optional["SubStage"] = None  # allow it to be set later





@dataclass
class SubStage:
    """
    Represents a specific substage of stellar evolution,
    containing all UI text and the data needed to locate examples.
    """
    # --- Core Identity ---
    id: str  # A unique string identifier, e.g., "ms_convective_core"
    parent_stage: ParentStage # A direct link to the Enum 

    # --- Physical Boundaries ---
    mass_min: float # Minimum mass that exhibits this substage 
    mass_max: float # Maximum mass that exhibits this substage 

    # --- Data Links ---
    models: list[SubStageModel] # A list of blueprints for finding this phase at different masses

    # --- UI and Descriptive Text ---
    plot_text: str      # Text for the flowchart box (e.g., "Conv. core\n+ rad. env.") 
    
    mode1_abbrev: str   # Mode1: Choose mass and compare evolutionary phases. Abbreviation goes inside the tab
    mode1_desc: str     # Full description of phase is displayed below the tabs element when this tab is selected 
    
    mode2_abbrev: str   # Mode2: Choose an evolutionary phase and compare masses. Abbreviation goes inside the tab
    mode2_desc: str     # Full description of phase is displayed below the tabs element when this tab is selected 

    history_plot_label: str | None = None 
    history_plot_color: str | None = None 

    @property
    def mode2_abbrev_with_massrange(self) -> str:
        return f"{self.mass_min:.1f}-{self.mass_max:.1f}: {self.mode2_abbrev}"

    @property
    def mode2_desc_with_massrange(self) -> str:
        return f"{self.mass_min:.1f}-{self.mass_max:.1f}: {self.mode2_desc}"

    def __str__(self): 
        return f"SubStage: {self.id}" 
    
    def __post_init__(self):
        for model in self.models:
            model.parent_substage = self 





hayashi_substage = SubStage(
    id="hayashi",
    parent_stage=ParentStage.HAYASHI, 
    plot_text = "Hayashi", 
    mode1_abbrev="Hayashi", 
    mode1_desc="Hayashi track", 
    mode2_abbrev="Hayashi", 
    mode2_desc="Hayashi track", 
    # history_plot_label="Hayashi track", 
    history_plot_color="tab:blue", 
    mass_min=0.1, 
    mass_max=6.0, 
    models=[ 
        SubStageModel(
            mass=0.2,
            model_start=None,
            model_end=None,
            model_example=150,
        ), 
        SubStageModel(
            mass=0.5,
            model_start=None,
            model_end=None,
            model_example=150,
        ), 
        SubStageModel(
            mass=1.0,
            model_start=None,
            model_end=None,
            model_example=150, 
            is_default=True, 
        ), 
        SubStageModel(
            mass=3.0,
            model_start=None,
            model_end=None,
            model_example=150,
        ), 
    ]
)


henyey_substage = SubStage(
    id="henyey",
    parent_stage=ParentStage.HENYEY, 
    plot_text = "Henyey", 
    mode1_abbrev="Henyey", 
    mode1_desc="Henyey track", 
    mode2_abbrev="Heyney", 
    mode2_desc="Henyey track", 
    # history_plot_label="Henyey track", 
    history_plot_color="tab:orange", 
    mass_min=0.3, 
    mass_max=6.0, 
    models=[
    ]
)


low_ms_substage = SubStage(
    id="low_ms",
    parent_stage=ParentStage.MAIN_SEQUENCE, 
    plot_text = "Main sequence \n(fully convective)", 
    mode1_abbrev="MS", 
    mode1_desc="Main sequence (fully convective)", 
    mode2_abbrev="Fully convective", 
    mode2_desc="Fully convective", 
    # history_plot_label="Main sequence", 
    history_plot_color="tab:orange", 
    mass_min=0.1, 
    mass_max=0.3, 
    models=[
        SubStageModel(
            mass=0.2,
            model_start=None,
            model_end=None,
            model_example=250,
        ), 
    ]
)


med_ms_substage = SubStage(    
    id="med_ms",
    parent_stage=ParentStage.MAIN_SEQUENCE, 
    plot_text = "Main sequence \n(rad. core \n+ conv. env.)",     
    mode1_abbrev="MS", 
    mode1_desc="Main sequence (radiative core + convective envelope)", 
    mode2_abbrev="Rad. core + conv. env.", 
    mode2_desc="Radiative core + convective envelope", 
    # history_plot_label="Main sequence", 
    history_plot_color="tab:red", 
    mass_min=0.3, 
    mass_max=1.5, 
    models=[
        SubStageModel(
            mass=0.5,
            model_start=None,
            model_end=None,
            model_example=250,
        ), 
        SubStageModel(
            mass=1.0,
            model_start=1,
            model_end=300,
            model_example=296, 
            is_default=True, 
        ), 
    ]
)


hi_ms_substage = SubStage(    
    id="hi_ms",
    parent_stage=ParentStage.MAIN_SEQUENCE, 
    plot_text = "Main sequence \n(conv. core \n+ rad. env.)", 
    mode1_abbrev="MS", 
    mode1_desc="Main sequence (convective core + radiative envelope)", 
    mode2_abbrev="Conv. core + rad. env.", 
    mode2_desc="Convective core + radiative envelope", 
    # history_plot_label="Main sequence", 
    history_plot_color="tab:purple", 
    mass_min=1.5, 
    mass_max=6.0, 
    models=[
        SubStageModel(
            mass=3.0,
            model_start=None,
            model_end=None,
            model_example=300,
        ), 
    ]
)


subgiant_substage = SubStage( 
    id="subgiant", 
    parent_stage=ParentStage.POST_MAIN_SEQUENCE, 
    plot_text="Subgiant", 
    mode1_abbrev="Subgiant", 
    mode1_desc="Subgiant", 
    mode2_abbrev="Subgiant", 
    mode2_desc="Subgiant", 
    # history_plot_label="Subgiant", 
    history_plot_color="tab:purple", 
    mass_min=0.3, 
    mass_max=1.5, 
    models=[
        SubStageModel(
            mass=0.5, 
            model_start=None, 
            model_end=None, 
            model_example=350
        ), 
        SubStageModel( 
            mass=1.0, 
            model_start=None, 
            model_end=None, 
            model_example=389
        )
    ]
)


hertzsprung_gap_substage = SubStage( 
    id="hertzsprung_gap", 
    parent_stage=ParentStage.POST_MAIN_SEQUENCE, 
    plot_text="Hertzsprung gap", 	
    mode1_abbrev="Hertzsprung gap", 
    mode1_desc="Hertzsprung gap", 
    mode2_abbrev="Hertzsprung gap", 
    mode2_desc="Hertzsprung gap", 
    # history_plot_label="Hertzsprung gap", 
    history_plot_color="tab:red", 
    mass_min=1.5, 
    mass_max=6.0, 
    models=[
        SubStageModel(
            mass=3.0, 
            model_start=None, 
            model_end=None, 
            model_example=348
        )
    ]
) 


red_giant_substage = SubStage( 
    id="red_giant", 
    parent_stage=ParentStage.RED_GIANT_BRANCH, 
    plot_text="Red giant", 	
    mode1_abbrev="RG", 
    mode1_desc="Red giant", 
    mode2_abbrev="RG", 
    mode2_desc="Red giant", 
    history_plot_label="Red giant", 
    history_plot_color="tab:gray", 
    mass_min=0.3, 
    mass_max=6.0, 
    models=[
        SubStageModel(
            mass=0.5, 
            model_start=None, 
            model_end=None, 
            model_example=7000
        ),
        SubStageModel(
            mass=1.0, 
            model_start=None, 
            model_end=None, 
            model_example=5000
        ), 
        SubStageModel(
            mass=3.0, 
            model_start=None, 
            model_end=None, 
            model_example=400
        )
    ]
)


he_flash_substage=SubStage( 
    id="he_flash", 
    parent_stage=ParentStage.HELIUM_IGNITION, 
    plot_text="Helium flash", 	
    mode1_abbrev="He flash", 
    mode1_desc="Helium ignition (unstable; helium flash)", 
    mode2_abbrev="Unstable", 
    mode2_desc="Unstable helium ignition (helium flash)", 
    # history_plot_label="Helium flash", 
    history_plot_color="tab:olive", 
    mass_min=2.0, 
    mass_max=6.0, 
    models=[
    ]
)


he_stable_substage=SubStage(
    id="he_stable", 
    parent_stage=ParentStage.HELIUM_IGNITION, 
    plot_text="Helium ignites \nstably", 	
    mode1_abbrev="He ign.", 
    mode1_desc="Helium ignition (stable)", 
    mode2_abbrev="Stable", 
    mode2_desc="Stable helium ignition", 
    # history_plot_label="Helium ign.", 
    history_plot_color="tab:cyan", 
    mass_min=0.8, 
    mass_max=2.0, 
    models=[
    ]
)


he_ms_substage=SubStage(
    id="he_ms", 
    parent_stage=ParentStage.HELIUM_MAIN_SEQUENCE, 
    plot_text="Helium main \nsequence", 	
    mode1_abbrev="He MS", 
    mode1_desc="Helium main sequence", 
    mode2_abbrev="He MS", 
    mode2_desc="Helium main sequence", 
    # history_plot_label="Helium main sequence", 
    history_plot_color="tab:pink", 
    mass_min=0.8, 
    mass_max=6.0, 
    models=[
        SubStageModel( 
            mass=1.0, 
            model_start=None, 
            model_end=None, 
            model_example=10650
        ), 
        SubStageModel( 
            mass=3.0, 
            model_start=None, 
            model_end=None, 
            model_example=650
        )
    ]
)


agb_substage=SubStage(
    id="agb", 
    parent_stage=ParentStage.ASYMPTOTIC_GIANT_BRANCH, 
    plot_text="Asymptotic \ngiant", 	
    mode1_abbrev="AGB", 
    mode1_desc="Asymptotic giant", 
    mode2_abbrev="AGB", 
    mode2_desc="Asymptotic giant", 
    # history_plot_label="AGB", 
    history_plot_color="tab:brown", 
    mass_min=0.8, 
    mass_max=6.0, 
    models=[
        SubStageModel( 
            mass=1.0, 
            model_start=None, 
            model_end=None, 
            model_example=12300
        ), 
        SubStageModel( 
            mass=3.0, 
            model_start=None, 
            model_end=None, 
            model_example=1000
        )    
    ]
)


he_wd_substage=SubStage(
    id="he_wd", 
    parent_stage=ParentStage.WHITE_DWARF, 
    plot_text="Helium \nwhite dwarf", 	
    mode1_abbrev="He WD", 
    mode1_desc="Helium white dwarf", 
    mode2_abbrev="He WD", 
    mode2_desc="Helium white dwarf", 
    # history_plot_label="Helium white dwarf", 
    history_plot_color="tab:olive", 
    mass_min = 0.1, 
    mass_max = 0.8,
    models=[
        SubStageModel( 
            mass=0.2, 
            model_start=None, 
            model_end=None, 
            model_example=1200
        ), 
        SubStageModel( 
            mass=0.5, 
            model_start=None, 
            model_end=None, 
            model_example=10100
        )    
    ]
)


co_wd_substage=SubStage(
    id="co_wd", 
    parent_stage=ParentStage.WHITE_DWARF, 
    plot_text="Carbon + \noxygen \nwhite dwarf", 	
    mode1_abbrev="C+O WD", 
    mode1_desc="Carbon + oxygen white dwarf", 
    mode2_abbrev="C+O WD", 
    mode2_desc="Carbon + oxygen white dwarf",   
    # history_plot_label="Carbon + oxygen white dwarf", 
    history_plot_color="tab:green", 
    mass_min = 0.8, 
    mass_max = 6.0,
    models=[
        SubStageModel( 
            mass=1.0, 
            model_start=None, 
            model_end=None, 
            model_example=14300
        ),   
    ]
)



SUBSTAGES_LIST = [
    hayashi_substage, 
    henyey_substage, 
    low_ms_substage, 
    med_ms_substage, 
    hi_ms_substage, 
    subgiant_substage, 
    hertzsprung_gap_substage, 
    red_giant_substage, 
    he_flash_substage, 
    he_stable_substage, 
    he_ms_substage, 
    agb_substage, 
    he_wd_substage, 
    co_wd_substage
    ]




