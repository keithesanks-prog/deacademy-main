import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def mandelbrot_grid(h, w, max_iter=50):
    """
    Generates Mandelbrot iteration counts.
    """
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
        
    return x, y, divtime

if __name__ == "__main__":
    print("Generating 3D Landscape of the Mandelbrot Set...")
    print("This treats the 'Escape Time' as 'Elevation'.")
    print("Black areas (converged) = Valleys")
    print("Colored areas (diverged) = Mountains")
    
    # Needs lower resolution for fast 3D interactivity
    h, w = 200, 200 
    
    x, y, divtime = mandelbrot_grid(h, w)
    
    # Prepare Plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Meshgrid for plotting
    X = x.ravel()
    Y = y.ravel()
    X_grid, Y_grid = np.meshgrid(np.linspace(-2.0, 1.0, w), np.linspace(-1.5, 1.5, h))
    
    # Z is the iteration count (Height)
    Z = divtime
    
    # Plot Surface
    # cmap='terrain' makes it look like a map
    surf = ax.plot_surface(X_grid, Y_grid, Z, cmap='terrain', 
                          linewidth=0, antialiased=False)
    
    ax.set_title("Mandelbrot Landscapes (Side View)")
    ax.set_xlabel("Real Axis")
    ax.set_ylabel("Imaginary Axis")
    ax.set_zlabel("Iterations (Elevation)")
    
    # Rotate for specific "Side View" angle
    ax.view_init(elev=60, azim=-45)
    
    fig.colorbar(surf, shrink=0.5, aspect=5)
    
    print("-" * 50)
    print("Done! You can rotate the 3D landscape with your mouse.")
    print("Notice how the Mandelbrot set looks like a flat valley or lake,")
    print("surrounded by steep cliffs of divergence.")
    print("-" * 50)
    
    plt.show()
