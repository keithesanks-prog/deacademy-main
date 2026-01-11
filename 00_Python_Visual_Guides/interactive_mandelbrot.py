import numpy as np
import matplotlib.pyplot as plt

def generate_mandelbrot_grid(h, w, max_iter=100, x_min=-2.0, x_max=0.5, y_min=-1.25, y_max=1.25):
    """
    Generates the Mandelbrot set grid.
    
    Args:
        h, w: Height and Width of grid
        max_iter: Max iterations to check
        x_min, x_max: Real axis range
        y_min, y_max: Imaginary axis range
    """
    # Use origin='lower' convention for y (increasing upwards)
    y, x = np.ogrid[y_min:y_max:h*1j, x_min:x_max:w*1j]
    c = x + y*1j
    z = c
    divtime = max_iter + np.zeros(z.shape, dtype=int)

    for i in range(max_iter):
        z = z**2 + c
        diverge = z*np.conj(z) > 4
        div_now = diverge & (divtime == max_iter)
        divtime[div_now] = i
        z[diverge] = 0

    return divtime

def calculate_point_stats(c, max_iter=1000):
    """
    Calculates detailed stats for a single point.
    Returns: iterations, trajectory_values
    """
    z = 0
    traj = []
    
    print(f"\n--- CALCULATION DETAILS for c = {c.real:.3f} + {c.imag:.3f}i ---")
    print(f"Formula: z_new = z^2 + c")
    print(f"Broken down: Real = (x^2 - y^2) + c_real  |  Imag = (2*x*y) + c_imag")
    
    for i in range(max_iter):
        if abs(z) > 2:
            print(f"Step {i+1}: |z| is {abs(z):.3f} (Values > 2 diverge!) -> STOP")
            return i, traj
        
        # Calculate components for display
        x = z.real
        y = z.imag
        x_sq = x*x
        y_sq = y*y
        two_xy = 2*x*y
        
        # The Math
        new_real = x_sq - y_sq + c.real
        new_imag = two_xy + c.imag
        
        # Only print first 5 steps to avoid spam
        if i < 5:
            print(f"\nStep {i+1}:")
            print(f"  Current z: {x:.3f} + {y:.3f}i")
            print(f"  Squares:   x^2={x_sq:.3f}, y^2={y_sq:.3f}")
            print(f"  New Real:  {x_sq:.3f} - {y_sq:.3f} + {c.real:.3f} = {new_real:.3f}")
            print(f"  New Imag:  2*{x:.3f}*{y:.3f} + {c.imag:.3f} = {new_imag:.3f}")
        
        z = complex(new_real, new_imag)
        if len(traj) < 5:
            traj.append(z)
            
    return max_iter, traj

def onclick(event):
    """Handle mouse clicks on the plot."""
    # Check if click is within the axes
    if event.inaxes:
        # Get the complex coordinate from the inverted x/y data
        real_part = event.xdata
        imag_part = event.ydata
        c = complex(real_part, imag_part)
        
        # Calculate precise status
        check_limit = 2000
        iters, traj = calculate_point_stats(c, check_limit)
        
        # Determine status message
        if iters == check_limit:
            status = f"Status: CONVERGES (Stable)"
            color_code = "green"
        else:
            status = f"Status: DIVERGES (Escaped in {iters} iterations)"
            color_code = "red"
            
        print(f"\nClicked: {real_part:.5f} + {imag_part:.5f}i -> {status}")
        
        # Update the plot title with info
        plt.title(f"Clicked: {real_part:.4f} + {imag_part:.4f}i\n{status}", color=color_code, fontweight='bold')
        plt.draw()

if __name__ == "__main__":
    print("Generating base map... (Window will open shortly)")
    # Higher resolution for better detail
    h, w = 2000, 2000 
    x_min, x_max = -2.0, 0.5
    y_min, y_max = -1.25, 1.25
    
    # Generate the base visualization with more iterations for deeper zoom capability
    max_iter_view = 500
    m_set = generate_mandelbrot_grid(h, w, max_iter_view, x_min, x_max, y_min, y_max)
    
    # Mask converged points for better plotting
    masked_set = np.ma.masked_where(m_set == max_iter_view, m_set)
    cmap = plt.cm.magma
    cmap.set_bad(color='black')

    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Use origin='lower' to match standard Cartesian coordinates
    im = ax.imshow(masked_set, cmap=cmap, extent=[x_min, x_max, y_min, y_max], origin='lower')
    
    plt.title("INTERACTIVE MODE: Click anywhere on the graph!", fontsize=14)
    plt.xlabel("Real Axis (Re)")
    plt.ylabel("Imaginary Axis (Im)")
    plt.colorbar(im, label=f"Iterations to Diverge (Cap: {max_iter_view})")
    
    # Connect the click event
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    print("-" * 50)
    print("Done! The Mandelbrot window is open.")
    print("1. Click on black areas to see convergence.")
    print("2. Click on colored areas to see divergence counts.")
    print("-" * 50)
    
    plt.show()
