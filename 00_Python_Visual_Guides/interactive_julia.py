import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def generate_julia_grid(h, w, c, max_iter=100, x_min=-1.5, x_max=1.5, y_min=-1.5, y_max=1.5):
    """
    Generates a Julia Set for a specific constant c.
    Notice the difference: Here 'c' is constant, and 'z' (the grid) varies.
    """
    y, x = np.ogrid[y_min:y_max:h*1j, x_min:x_max:w*1j]
    z = x + y*1j
    divtime = max_iter + np.zeros(z.shape, dtype=int)

    for i in range(max_iter):
        z = z**2 + c  # c is FIXED for the whole image!
        diverge = z*np.conj(z) > 4
        div_now = diverge & (divtime == max_iter)
        divtime[div_now] = i
        z[diverge] = 0

    return divtime

if __name__ == "__main__":
    print("Generating Julia Set Explorer...")
    
    # 1. Define resolution
    h, w = 800, 800
    
    # 2. Start with a famous Julia Set value
    c_init = complex(-0.7, 0.27015)

    # 3. Create Plot
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(bottom=0.25) # Make room for sliders
    
    img_data = generate_julia_grid(h, w, c_init)
    
    masked_set = np.ma.masked_where(img_data == 100, img_data)
    cmap = plt.cm.magma
    cmap.set_bad(color='black')
    
    im = ax.imshow(masked_set, cmap=cmap, extent=[-1.5, 1.5, -1.5, 1.5], origin='lower')
    ax.set_title(f"Julia Set for c = {c_init.real:.3f} + {c_init.imag:.3f}i")
    
    # 4. Add Sliders
    ax_real = plt.axes([0.25, 0.1, 0.65, 0.03])
    ax_imag = plt.axes([0.25, 0.05, 0.65, 0.03])
    
    slider_real = Slider(ax_real, 'Real Part', -2.0, 1.0, valinit=c_init.real)
    slider_imag = Slider(ax_imag, 'Imag Part', -1.5, 1.5, valinit=c_init.imag)
    
    def update(val):
        """Update the plot when sliders change."""
        c_new = complex(slider_real.val, slider_imag.val)
        
        # Re-calc image
        new_data = generate_julia_grid(h, w, c_new)
        
        # Update display
        masked_new = np.ma.masked_where(new_data == 100, new_data)
        im.set_data(masked_new)
        ax.set_title(f"Julia Set for c = {c_new.real:.3f} + {c_new.imag:.3f}i")
        fig.canvas.draw_idle()

    slider_real.on_changed(update)
    slider_imag.on_changed(update)
    
    print("Done! Use the sliders to morph the fractal.")
    plt.show()
