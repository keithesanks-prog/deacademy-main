import numpy as np
import matplotlib.pyplot as plt

def generate_orbit_trap(h, w, c, max_iter=100):
    """
    Generates a Julia set using 'Orbit Traps' for coloring.
    Instead of checking escape time, we check how close the point gets 
    to the axes (Real or Imaginary) during its orbit.
    """
    y, x = np.ogrid[-1.5:1.5:h*1j, -1.5:1.5:w*1j]
    z = x + y*1j
    
    # We will track the "closest approach" to the axes
    # Initialize with a large number
    min_dist = np.full(z.shape, 100.0)

    for i in range(max_iter):
        z = z**2 + c
        
        # --- THE TRAP ---
        # "Trap" 1: How close is the point to the X or Y axis?
        # |z.real| is dist to Y-axis, |z.imag| is dist to X-axis
        dist_to_axis = np.minimum(np.abs(z.real), np.abs(z.imag))
        
        # Keep track of the closest it ever got
        min_dist = np.minimum(min_dist, dist_to_axis)
        
        # Standard escape check to stop calculation
        mask = z*np.conj(z) > 4
        z[mask] = 0 # Prevent overflow
        
    return min_dist

if __name__ == "__main__":
    print("Generating Orbit Trap Visualization...")
    print("This reveals the 'Stalks' and 'Geometry' hidden in the data.")
    
    h, w = 1000, 1000
    c = complex(-0.7269, 0.1889) # A nice Julia value
    
    # Compute the "Distance to Axis" map
    trap_map = generate_orbit_trap(h, w, c)
    
    # Visualization Magic (NASA Style)
    # We use a log scale because the distances get very tiny
    data = np.log(trap_map + 0.0001) 
    
    plt.figure(figsize=(10, 10))
    # 'hot' colormap looks like glowing electricity/stalks
    plt.imshow(data, cmap='hot', extent=[-1.5, 1.5, -1.5, 1.5])
    
    plt.title(f"Orbit Trap Coloring (c={c})")
    plt.colorbar(label="Log(Closest Distance to Axis)")
    print("Done! Notice how this looks like 'stalks' or 'electricity' instead of just blobs.")
    plt.show()
