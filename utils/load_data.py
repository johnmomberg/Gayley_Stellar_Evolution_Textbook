import mesa_reader as mr 
import numpy as np 



data_folder = "C:/Users/johnm/Local Desktop/Gayley/MESA output files/" 





def load_history(M): 
    
    history_filepath = data_folder + f"M={M}" + "/trimmed_history.data"
    history = mr.MesaData(history_filepath)  

    # Set index, modelnum, and age where Zero Age Main Sequence (ZAMS) occurs in history  
    try: 
        #ind_ZAMS = np.where(np.abs(history.center_h1 - history.center_h1[0])/history.center_h1[0] > 0.001)[0][0] 
        ind_ZAMS = np.where(history.log_LH - history.log_L > np.log10(0.999) )[0][0] 
        history.index_ZAMS = ind_ZAMS 
        history.modelnum_ZAMS = ind_ZAMS+1
        history.age_ZAMS = history.star_age[ind_ZAMS]
    except (IndexError, ValueError): 
        history.index_ZAMS = np.nan  
        history.modelnum_ZAMS = np.nan 
        history.age_ZAMS = np.nan 

    # Set index, modelnum, and age where Terminal Age Main Sequence (TAMS) occurs in history 
    try: 
        ind_TAMS = np.where(history.he_core_mass>0)[0][0] 
        history.index_TAMS = ind_TAMS 
        history.modelnum_TAMS = ind_TAMS+1 
        history.age_TAMS = history.star_age[ind_TAMS] 
    except (IndexError, ValueError): 
        history.index_TAMS = np.nan  
        history.modelnum_TAMS = np.nan  
        history.age_TAMS = np.nan 

    # Find the earliest point in time after TAMS where the helium core fraction drops, which indicates helium fusion has started
    try:  
        ind1 = np.where((history.center_he4[history.index_TAMS]-history.center_he4)/history.center_he4[history.index_TAMS] > 0.0001) 
        # ind1 = np.where(history.log_LHe>0)[0][0]
        # ind1 = np.where(history.log_LHe - history.log_L > np.log10(0.999))
        ind2 = np.where(history.star_age>history.age_TAMS)
        ind_both = np.intersect1d(ind1, ind2)
        index_He_fusion = np.nanmin(ind_both) 
        history.index_He_fusion = index_He_fusion 
        history.modelnum_He_fusion = index_He_fusion+1 
        history.age_He_fusion = history.star_age[index_He_fusion] 
        if len(ind_both)==0: 
            history.index_He_fusion = np.nan 
            history.modelnum_He_fusion = np.nan
            history.age_He_fusion = np.nan 

        # ind_He_fusion = np.where(history.c_core_mass>0)[0][0] 
        # history.index_He_fusion = ind_He_fusion 
        # history.modelnum_He_fusion = ind_He_fusion+1 
        # history.age_He_fusion = history.star_age[ind_He_fusion] 

    except (IndexError, ValueError): 
        history.index_He_fusion = np.nan 
        history.modelnum_He_fusion = np.nan  
        history.age_He_fusion = np.nan 

    # Set availbe model numbers 
    folder_mesa = mr.MesaLogDir(data_folder + f"M={M}", history_file="trimmed_history.data") 
    history.model_numbers_available = folder_mesa.model_numbers
    return history 





def load_profile(M, history, index=None, modelnum=None, age=None, skip_n_models=0): 
    
    # Mutually exclusive arguments: Supply either the intended index,  model number, or age, but not multiple of those options. 
    args = [index, modelnum, age]
    given = sum(arg is not None for arg in args)
    if given == 0:
        raise ValueError("You must specify one of: index, modelnum, or age.")
    elif given > 1:
        raise ValueError("Only one of: index, modelnum, or age may be specified.")
    
    # If index was chosen, convert to model number 
    if index is not None: 
        modelnum = index+1 
    
    # If the intended profile doesn't exist, step forward until you find one that does 
    folder_mesa = mr.MesaLogDir(data_folder + f"M={M}", history_file="trimmed_history.data") 
    model_numbers = folder_mesa.model_numbers 
    while modelnum not in model_numbers: 
        modelnum += 1 

    # Skip forward or back n models (useful to check the previous and next model to the intended one)
    index_modelnum = np.where(model_numbers==modelnum)[0][0]
    modelnum = model_numbers[index_modelnum+skip_n_models]

    # Load profile 
    profile = folder_mesa.profile_data(modelnum)     
    profile.modelnum = modelnum 
    profile.index = modelnum-1 
    profile.age = history.star_age[profile.index] 
    profile.total_mass = M 
    return profile




