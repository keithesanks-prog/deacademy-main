import json

nb_path = 'training.ipynb'

try:
    with open(nb_path, 'r') as f:
        nb = json.load(f)
    
    # 1. Create Palindrome Fix Cell
    palindrome_source = [
        "# --- PALINDROME FIX ---\n",
        "def is_palindrome(s):\n",
        "    # Keep only letters/numbers and lower them. This fixes the punctuation issue.\n",
        "    clean_s = \"\".join(c.lower() for c in s if c.isalnum())\n",
        "    return clean_s == clean_s[::-1]\n",
        "\n",
        "test_str = \"A man, a plan, a canal: Panama\"\n",
        "print(f\"Is '{test_str}' a palindrome? {is_palindrome(test_str)}\")\n"
    ]
    
    palindrome_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": palindrome_source
    }
    
    # 2. Create Mandelbrot Set Cell
    mandelbrot_source = [
        "# --- MANDELBROT SET GENERATOR ---\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "def mandelbrot(h, w, max_iter=20):\n",
        "    \"\"\"Create a Mandelbrot set grid.\"\"\"\n",
        "    y, x = np.ogrid[-1.4:1.4:h*1j, -2:0.8:w*1j]\n",
        "    c = x + y*1j\n",
        "    z = c\n",
        "    divtime = max_iter + np.zeros(z.shape, dtype=int)\n",
        "\n",
        "    for i in range(max_iter):\n",
        "        z = z**2 + c\n",
        "        diverge = z*np.conj(z) > 2**2            # who is diverging\n",
        "        div_now = diverge & (divtime == max_iter)  # who is diverging NOW\n",
        "        divtime[div_now] = i                  # note when\n",
        "        z[diverge] = 2                        # avoid diverging too much\n",
        "\n",
        "    return divtime\n",
        "\n",
        "plt.figure(figsize=(10, 10))\n",
        "plt.imshow(mandelbrot(1000, 1000), cmap='magma')\n",
        "plt.title(\"The Mandelbrot Set\")\n",
        "plt.show()\n"
    ]
    
    mandelbrot_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": mandelbrot_source
    }
    
    # Append both cells to the notebook
    nb['cells'].append(palindrome_cell)
    nb['cells'].append(mandelbrot_cell)
    
    with open(nb_path, 'w') as f:
        json.dump(nb, f, indent=1)
        
    print("\n\u2705 Added Palindrome Fix and Mandelbrot Set to training.ipynb")

except Exception as e:
    print(f"Error: {e}")
