import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def compute_orbit(c, max_iter=50):
    """
    Compute the orbit (sequence of z values) for a given c.
    Returns the list of complex values z takes.
    """
    z = 0
    orbit = [z]
    
    for i in range(max_iter):
        z = z**2 + c
        orbit.append(z)
        
        # Stop if it escapes
        if abs(z) > 2:
            break
            
    return orbit

def generate_mandelbrot_background(h, w, max_iter=50):
    """Generate the base Mandelbrot set for background."""
    y, x = np.ogrid[-1.5:1.5:h*1j, -2.0:1.0:w*1j]
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

# Global variables for interactive plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
orbit_plot = None

def onclick(event):
    """Handle mouse clicks on the Mandelbrot set."""
    global orbit_plot
    
    if event.inaxes == ax1:
        # Get the clicked complex number
        c = complex(event.xdata, event.ydata)
        print(f"\nClicked: c = {c.real:.3f} + {c.imag:.3f}i")
        
        # Compute the orbit
        orbit = compute_orbit(c, max_iter=30)
        
        # Clear the right plot
        ax2.clear()
        
        # Extract real and imaginary parts
        real_parts = [z.real for z in orbit]
        imag_parts = [z.imag for z in orbit]
        
        # Plot the orbit trajectory
        ax2.plot(real_parts, imag_parts, 'o-', 
                color='cyan', linewidth=2, markersize=8, 
                markerfacecolor='yellow', markeredgecolor='black', markeredgewidth=1.5)
        
        # Annotate the start
        ax2.plot(real_parts[0], imag_parts[0], 'go', markersize=12, label='Start (z=0)')
        ax2.text(real_parts[0], imag_parts[0], '  START', fontsize=10, color='green', weight='bold')
        
        # Annotate the end
        ax2.plot(real_parts[-1], imag_parts[-1], 'ro', markersize=12, label=f'End (iter {len(orbit)-1})')
        
        # Add iteration numbers
        for i, (x, y) in enumerate(zip(real_parts[:10], imag_parts[:10])):
            ax2.text(x, y, f' {i}', fontsize=8, color='white')
        
        # Draw the "escape circle" (radius 2)
        circle = Circle((0, 0), 2, fill=False, color='red', linestyle='--', linewidth=2, label='Escape Boundary (|z|=2)')
        ax2.add_patch(circle)
        
        # Formatting
        ax2.set_xlim(-3, 3)
        ax2.set_ylim(-3, 3)
        ax2.axhline(0, color='gray', linewidth=0.5)
        ax2.axvline(0, color='gray', linewidth=0.5)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel("Real Part (Re)")
        ax2.set_ylabel("Imaginary Part (Im)")
        ax2.set_title(f"Orbit for c = {c.real:.3f} + {c.imag:.3f}i")
        ax2.legend(loc='upper right')
        ax2.set_aspect('equal')
        
        # Determine if it escaped
        if abs(orbit[-1]) > 2:
            status = f"DIVERGES (Escaped in {len(orbit)-1} iterations)"
            color = 'red'
        else:
            status = f"CONVERGES (Stable after {len(orbit)-1} iterations)"
            color = 'green'
            
        ax2.text(0.5, 0.95, status, transform=ax2.transAxes, 
                ha='center', fontsize=12, color=color, weight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        fig.canvas.draw()

if __name__ == "__main__":
    print("Generating Orbit Viewer...")
    print("Click anywhere on the Mandelbrot set to see its iteration orbit!")
    
    # Generate background
    h, w = 400, 400
    mandelbrot_bg = generate_mandelbrot_background(h, w)
    
    # Plot Mandelbrot set on left
    masked_set = np.ma.masked_where(mandelbrot_bg == 50, mandelbrot_bg)
    cmap = plt.cm.magma
    cmap.set_bad(color='black')
    
    ax1.imshow(masked_set, cmap=cmap, extent=[-2.0, 1.0, -1.5, 1.5], origin='lower')
    ax1.set_title("Mandelbrot Set (Click to Explore)", fontsize=14, weight='bold')
    ax1.set_xlabel("Real Axis (Re)")
    ax1.set_ylabel("Imaginary Axis (Im)")
    
    # Setup right plot
    ax2.set_xlim(-3, 3)
    ax2.set_ylim(-3, 3)
    ax2.set_title("Click a point to see its orbit", fontsize=14)
    ax2.set_xlabel("Real Part (Re)")
    ax2.set_ylabel("Imaginary Part (Im)")
    ax2.grid(True, alpha=0.3)
    ax2.axhline(0, color='gray', linewidth=0.5)
    ax2.axvline(0, color='gray', linewidth=0.5)
    
    # Connect click event
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    plt.tight_layout()
    print("-" * 60)
    print("INSTRUCTIONS:")
    print("1. Click on the BLACK area (inside the set) to see stable orbits")
    print("2. Click on COLORED areas (outside) to see explosive orbits")
    print("3. Try clicking near the edge to see complex behavior!")
    print("-" * 60)
    
    plt.show()
