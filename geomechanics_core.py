import pandas as pd
import numpy as np
from data_input import load_well_data

def calculate_effective_stresses(df, biot_alpha=1.0):
    """
    Calculates Effective Stresses using Biot's poroelastic equation.
    """
    print("⚙️ Calculating effective stresses...")
    df['Eff_Sv_psi'] = df['Sv_psi'] - (biot_alpha * df['Pp_psi'])
    df['Eff_Shmin_psi'] = df['Shmin_psi'] - (biot_alpha * df['Pp_psi'])
    return df

def calculate_plane_stresses(df, theta_degrees):
    """
    Resolves the principal effective stresses into Normal and Shear stress 
    acting on a natural fault plane inclined at theta_degrees.
    """
    print(f"📐 Calculating stresses on a {theta_degrees}° fault plane...")
    
    # Python trig functions require radians
    theta_rad = np.radians(theta_degrees)
    
    # Define max and min principal stresses for a normal faulting regime
    sigma_1 = df['Eff_Sv_psi']
    sigma_3 = df['Eff_Shmin_psi']
    
    # Calculate Normal Stress
    df['Normal_Stress_psi'] = ((sigma_1 + sigma_3) / 2) + ((sigma_1 - sigma_3) / 2) * np.cos(2 * theta_rad)
    
    # Calculate Shear Stress
    df['Shear_Stress_psi'] = ((sigma_1 - sigma_3) / 2) * np.sin(2 * theta_rad)
    
    return df

if __name__ == "__main__":
    well_data = load_well_data('well_data.csv')
    
    if well_data is not None:
        processed_data = calculate_effective_stresses(well_data)
        
        # Test the new function assuming a fault dipping at 30 degrees
        final_data = calculate_plane_stresses(processed_data, theta_degrees=30)
        
        print("✅ Plane stress calculations complete!")
        print("-" * 40)
        # Display the new Normal and Shear stresses alongside depth
        print(final_data[['Depth_ft', 'Normal_Stress_psi', 'Shear_Stress_psi']])