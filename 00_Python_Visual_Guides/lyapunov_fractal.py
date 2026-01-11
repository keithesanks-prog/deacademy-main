import numpy as np
import matplotlib.pyplot as plt

def lyapunov_exponent(s_seq, h, w, r_min=2.0, r_max=4.0):
    """
    Generates a Markus-Lyapunov Fractal.
    
    Args:
        s_seq (str): The sequence string like "AB" or "AAB"
        h, w: Resolution
        r_min, r_max: Range of growth rates (A and B)
    """
    # 1. Setup the grid of Growth Rates (A and B)
    # The X-axis represents rate 'A'
    # The Y-axis represents rate 'B'
    a_vals = np.linspace(r_min, r_max, w)
    b_vals = np.linspace(r_min, r_max, h)
    
    # Broadcast to grid
    A, B = np.meshgrid(a_vals, b_vals)
    
    # 2. Build the sequence array (e.g. "AB" -> [A, B, A, B...])
    # We construct a 3D array where the 3rd dimension is the sequence steps
    seq_map = []
    for char in s_seq:
        if char == 'A':
            seq_map.append(A)
        else:
            seq_map.append(B)
            
    # Stack them: Shape (len(s_seq), h, w)
    r_sequence = np.stack(seq_map, axis=0)
    seq_len = len(s_seq)
    
    # 3. Iterate the Logistic Map: x = r * x * (1 - x)
    x = 0.5 * np.ones((h, w)) # Initial population 0.5
    
    # Warmup iterations (to let it settle)
    print("  Warming up...")
    for i in range(100):
        # Pick rate based on sequence step
        r = r_sequence[i % seq_len]
        x = r * x * (1 - x)
        
    # 4. Calculate Lyapunov Exponent
    # Lambda = Sum( log( |r * (1 - 2x)| ) ) / N
    # The sum calculates the average rate of divergence/convergence
    print("  Calculating Lyapunov exponent...")
    lyap_sum = np.zeros(x.shape)
    
    # Accumulate log derivatives
    calc_steps = 400
    for i in range(calc_steps):
        r = r_sequence[i % seq_len]
        x = r * x * (1 - x)
        
        # Derivative of logistic map is r * (1 - 2x)
        # We take abs because log takes positive numbers
        # We clip to avoid log(0)
        derivative = np.abs(r * (1 - 2 * x))
        derivative = np.clip(derivative, 1e-9, None) 
        
        lyap_sum += np.log(derivative)
        
    return lyap_sum / calc_steps

if __name__ == "__main__":
    print("Generating Markus-Lyapunov Fractal...")
    print("This maps the chaotic behavior of sequence 'AB'.")
    
    h, w = 800, 800
    seq = "AB" # The classic "Z-shape"
    
    lyap = lyapunov_exponent(seq, h, w, 2.0, 4.0)
    
    plt.figure(figsize=(10, 10))
    
    # Colors:
    # Negative (Stable) = Blue/Dark
    # Positive (Chaotic) = Yellow/White
    plt.imshow(lyap, cmap='nipy_spectral', vmin=-2, vmax=0.5, 
               origin='lower', extent=[2.0, 4.0, 2.0, 4.0])
    
    plt.colorbar(label="Lyapunov Exponent (Stability)")
    plt.title(f"Markus-Lyapunov Fractal (Sequence: {seq})")
    plt.xlabel("Growth Rate A")
    plt.ylabel("Growth Rate B")
    
    print("Done! Stable regions are dark, Chaotic regions are bright.")
    plt.show()
