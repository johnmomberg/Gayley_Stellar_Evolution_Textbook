import numpy as np 
import math 




def to_engineering(x): 

    exponent = int(np.floor(np.log10(x)))
    coeff = x / 10**exponent 

    while exponent % 3 != 0: 
        exponent = exponent = exponent-1
        coeff = x / 10**exponent  

    return f"{coeff:.3g} x 10^{exponent}" 



# Input: mass (solar masses) 
# Output: luminosity (solar luminosities) 
def mass_luminosity_relation(M): 
    if M<0.43: 
        L_predicted = 0.23 * M**2.3
    if 0.43<=M<2: 
        L_predicted = M**4 
    if 2<=M<55: 
        L_predicted = 1.4 * M**3.5 
    if M>=55: 
        L_predicted = 32000 * M 
    return L_predicted 