# The "Chaos" Fractal: Markus-Lyapunov

You found it! The video was about **Lyapunov Fractals** (specifically the Markus-Lyapunov type).

## 1. How it's Different from Mandelbrot
*   **Mandelbrot**: Based on complex numbers ($z^2 + c$).
*   **Lyapunov**: Based on **Chaos Theory** and population growth (The Logistic Map).

## 2. The Logistic Map (Population Growth)
The core equation is: **x_next = r × x × (1 - x)**

*   **x** = Population as a percentage (0 to 1, where 1 = max capacity).
*   **r** = Growth rate (how fast the population reproduces).
*   **(1 - x)** = The "limiting factor" (less food when crowded).

**How it works:**
*   When **x is small** (few rabbits): `(1 - x) ≈ 1`, so population grows fast.
*   When **x is large** (too many rabbits): `(1 - x) ≈ 0`, so growth crashes (starvation).
*   **Low r**: Population stabilizes.
*   **High r**: Population becomes chaotic (unpredictable yearly jumps).

## 3. The "Recipe" (The String)
Instead of a coordinate, these fractals use a **Sequence** (like a DNA string) of growth rates, such as `"AB"` or `"AAB"`.
*   **A**: A certain growth rate (r1).
*   **B**: A different growth rate (r2).
*   The computer switches between these rates periodically.

## 3. Stability vs. Chaos
The image you see is a map of **Stability**.
*   **Dark Blue (Stable)**: The population stabilizes (Converges).
*   **Yellow/White (Chaos)**: The population explodes into chaos (Sensitive dependence on initial conditions).
*   **The Shape**: It looks like a "Z-shape" or a "Swallow-tail" because of the weird way stability islands interact.

## 4. The 3D Version
The "Stalactites" you saw in the video were likely a **3D Plot of the Lyapunov Exponent**.
*   **Height = Chaos Level**.
*   Stable areas are flat valleys.
*   Chaotic areas are jagged spikes (stalagmites).
