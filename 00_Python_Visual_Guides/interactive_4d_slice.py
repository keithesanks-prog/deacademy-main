import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def generate_quaternion_slice(h, w, 
                            slice_w, slice_z, 
                            c_w, c_x, c_y, c_z, 
                            max_iter=30):
    """
    Generates a 2D slice of a 4D Quaternion Julia Set.
    
    The 4D space is (w, x, y, z).
    We plot the (x, y) plane.
    We fix 'w' and 'z' to specific values (the slice).
    """
    # Create the grid for x and y
    y_grid, x_grid = np.ogrid[-1.5:1.5:h*1j, -1.5:1.5:w*1j]
    
    # Initialize the Quartz components
    # q = w + xi + yj + zk
    # We fix w and z for every pixel in this slice
    q_w = np.full((h, w), slice_w)
    q_x = x_grid # This broadcasts to (h, w) naturally in operations
    q_y = y_grid # This broadcasts to (h, w) naturally in operations
    q_z = np.full((h, w), slice_z)
    
    # divtime needs to match the shape of the grid (h, w)
    # x_grid from ogrid is (1, w), y_grid is (h, 1)
    # The result of calculations will be broadcast to (h, w)
    # So we must initialize divtime as (h, w) explicitly
    divtime = max_iter + np.zeros((h, w), dtype=int)
    
    # Iterate q = q^2 + c
    for i in range(max_iter):
        # Calculate q^2 components
        # (w+xi+yj+zk)^2 = (w^2 - x^2 - y^2 - z^2) + (2wx)i + (2wy)j + (2wz)k
        w2 = q_w**2
        x2 = q_x**2
        y2 = q_y**2
        z2 = q_z**2
        
        # New q components
        new_w = w2 - x2 - y2 - z2 + c_w
        new_x = 2 * q_w * q_x + c_x
        new_y = 2 * q_w * q_y + c_y
        new_z = 2 * q_w * q_z + c_z
        
        q_w, q_x, q_y, q_z = new_w, new_x, new_y, new_z
        
        # Check divergence: |q|^2 > 4
        dist_sq = q_w**2 + q_x**2 + q_y**2 + q_z**2
        diverge = dist_sq > 4
        
        div_now = diverge & (divtime == max_iter)
        divtime[div_now] = i
        
        # Prevent overflow for diverged points
        q_w[diverge] = 0
        q_x[diverge] = 0
        q_y[diverge] = 0
        q_z[diverge] = 0
        
    return divtime

if __name__ == "__main__":
    print("Generating 4D Hyper-Slicer...")
    print("This visualizes a 4D Quaternion fractal by taking a 2D slice of it.")
    
    h, w = 400, 400 # Lower res for 4D math speed
    
    # Initial Slice Position (Moving through the 4th dimension)
    init_slice_w = 0.0
    init_slice_z = 0.0
    
    # The Constant C defining the Fractal Shape
    # Only changing this morphs the fractal itself
    init_c_w = -0.5
    init_c_x = 0.0
    init_c_y = 0.0
    init_c_z = 0.0

    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(bottom=0.35)
    
    img_data = generate_quaternion_slice(h, w, init_slice_w, init_slice_z, init_c_w, init_c_x, init_c_y, init_c_z)
    
    masked_set = np.ma.masked_where(img_data == 30, img_data)
    cmap = plt.cm.twilight_shifted # Mystical colors
    cmap.set_bad(color='black')
    
    im = ax.imshow(masked_set, cmap=cmap, extent=[-1.5, 1.5, -1.5, 1.5], origin='lower')
    ax.set_title(f"4D Slice: W={init_slice_w:.2f}, Z={init_slice_z:.2f}")
    
    # Sliders for Slicing (Moving through dimensions)
    ax_sw = plt.axes([0.25, 0.20, 0.65, 0.03])
    ax_sz = plt.axes([0.25, 0.15, 0.65, 0.03])
    
    # Sliders for Fractal Shape (The constant C)
    ax_cw = plt.axes([0.25, 0.05, 0.65, 0.03])
    
    slider_sw = Slider(ax_sw, 'Slice W (Time)', -1.0, 1.0, valinit=init_slice_w)
    slider_sz = Slider(ax_sz, 'Slice Z (Depth)', -1.0, 1.0, valinit=init_slice_z)
    slider_cw = Slider(ax_cw, 'Shape Constant', -1.0, 0.0, valinit=init_c_w)
    
    def update(val):
        new_data = generate_quaternion_slice(h, w, 
                                           slider_sw.val, slider_sz.val, 
                                           slider_cw.val, init_c_x, init_c_y, init_c_z)
        
        masked_new = np.ma.masked_where(new_data == 30, new_data)
        im.set_data(masked_new)
        ax.set_title(f"4D Slice: W={slider_sw.val:.2f}, Z={slider_sz.val:.2f}")
        fig.canvas.draw_idle()

    slider_sw.on_changed(update)
    slider_sz.on_changed(update)
    slider_cw.on_changed(update)
    
    print("-" * 50)
    print("Done! The window is open.")
    print("1. 'Slice W' moves you through the 4th dimension.")
    print("2. Watch how the isolated islands MERGE and separate.")
    print("3. This proves the 2D islands are actually connected in 4D!")
    print("-" * 50)
    
    plt.show()
