import matplotlib.pyplot as plt
import numpy as np
from data_input import load_well_data
from geomechanics_core import calculate_effective_stresses, calculate_plane_stresses

def plot_mohrs_circle(df, depth_index=0, cohesion=500, friction_angle_deg=30):
    """
    Plots the Mohr's Circle and Failure Envelope for a specific depth.
    """
    print("⭕ Drawing Mohr's Circle...")
    
    # Extract data for the chosen depth (default is the first row: index 0)
    sigma_1 = df['Eff_Sv_psi'].iloc[depth_index]
    sigma_3 = df['Eff_Shmin_psi'].iloc[depth_index]
    tau = df['Shear_Stress_psi'].iloc[depth_index]
    sigma_n = df['Normal_Stress_psi'].iloc[depth_index]
    depth = df['Depth_ft'].iloc[depth_index]

    # Calculate circle center and radius
    center = (sigma_1 + sigma_3) / 2
    radius = (sigma_1 - sigma_3) / 2

    # Generate points to draw the circle
    theta = np.linspace(0, np.pi, 100)
    x_circle = center + radius * np.cos(theta)
    y_circle = radius * np.sin(theta)

    # Generate points for the failure envelope
    phi_rad = np.radians(friction_angle_deg)
    x_env = np.linspace(0, sigma_1 + 500, 100)
    y_env = cohesion + x_env * np.tan(phi_rad)

    # Create the plot
    plt.figure(figsize=(8, 6))
    plt.plot(x_circle, y_circle, label=f"Mohr's Circle (Depth: {depth} ft)", color='blue', linewidth=2)
    plt.plot(x_env, y_env, label="Failure Envelope", color='red', linestyle='--')
    
    # Plot the specific stress state on our 30-degree fault
    plt.scatter(sigma_n, tau, color='black', s=80, zorder=5, label="Stress on 30° Fault")

    # Formatting the graph
    plt.title(f"Mohr's Circle Analysis at {depth} ft", fontsize=14, fontweight='bold')
    plt.xlabel("Effective Normal Stress (psi)", fontsize=12)
    plt.ylabel("Shear Stress (psi)", fontsize=12)
    plt.xlim(0, sigma_1 + 1000)
    plt.ylim(0, radius + 1000)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    
    # Keep the circle perfectly round
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

if __name__ == "__main__":
    well_data = load_well_data('well_data.csv')
    
    if well_data is not None:
        processed_data = calculate_effective_stresses(well_data)
        final_data = calculate_plane_stresses(processed_data, theta_degrees=30)
        
        # Plot the Mohr's circle for the very first depth (row 0, which is 5000 ft)
        plot_mohrs_circle(final_data, depth_index=0)