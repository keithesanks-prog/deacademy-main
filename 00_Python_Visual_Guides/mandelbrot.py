import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(h, w, max_iter=100):
    """
    Generates the Mandelbrot set.
    
    Args:
        h (int): Height of the image
        w (int): Width of the image
        max_iter (int): Maximum number of iterations
        
    Returns:
        numpy.ndarray: A 2D array containing the iteration counts
    """
    # Define the region of the complex plane to visualize
    # Real axis: -2.0 to 0.5
    # Imaginary axis: -1.25 to 1.25
    y, x = np.ogrid[-1.25:1.25:h*1j, -2.0:0.5:w*1j]
    c = x + y*1j
    z = c
    divtime = max_iter + np.zeros(z.shape, dtype=int)

    for i in range(max_iter):
        # The core Mandelbrot formula: z = z^2 + c
        z = z**2 + c
        
        # Check for divergence (bound is usually 2, so 2^2 = 4)
        diverge = z*np.conj(z) > 4
        div_now = diverge & (divtime == max_iter)
        
        # Record at what iteration it diverged
        divtime[div_now] = i
        
        # Set diverged points to 0 to avoid overflow in subsequent calculations
        z[diverge] = 0

    return divtime

if __name__ == "__main__":
    print("Generating Mandelbrot set...")
    height, width = 1000, 1000
    mandelbrot_set = mandelbrot(height, width)
    
    print("Plotting...")
    plt.figure(figsize=(10, 10))
    
    # 1. Mask the converged points (value == max_iter)
    #    so we can color them differently (e.g., Black)
    #    'mandelbrot_set' contains iteration counts (0..max_iter)
    masked_set = np.ma.masked_where(mandelbrot_set == 100, mandelbrot_set) # 100 is default max_iter
    
    # 2. Set the colormap to use 'black' for masked (bad) values
    cmap = plt.cm.magma
    cmap.set_bad(color='black')
    
    # 3. Plot
    plt.imshow(masked_set, cmap=cmap, extent=[-2.0, 0.5, -1.25, 1.25])
    
    plt.title("The Mandelbrot Set (Black = Converged)")
    plt.xlabel("Re")
    plt.ylabel("Im")
    plt.colorbar(label="Iterations to Diverge")
    
    output_file = "mandelbrot.png"
    plt.savefig(output_file, dpi=300)
    print(f"Done! Saved visualization to {output_file}")
    plt.show()