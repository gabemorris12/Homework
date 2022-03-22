import numpy as np
import matplotlib.pyplot as plt

plt.style.use('maroon_py.mplstyle')

# Insert the parameters here
# See the project free body diagram for what each parameter represents
k1 = 1.6e4
k2 = 2.5e4
L1 = 1.5
L2 = 1.1
m = 730
IG = 1350

# Finding the natural frequencies of the system
A = IG*m
B = IG*k1 + IG*k2 + L1**2*k1*m + L2**2*k2*m
C = L1**2*k1*k2 + 2*L1*L2*k1*k2 + L2**2*k1*k2
coefficients = [A, 0, B, 0, C]
roots = np.roots(coefficients)
w1, w2 = np.abs(np.imag(roots[0])), np.abs(np.imag(roots[-1]))

# Get the mode shape
mode_shape = lambda w: (L1*k1 - L2*k2)/(k1 + k2 + -m*w**2)
mode1, mode2 = mode_shape(np.array([w1, w2]))
print(f'Mode 1: {mode1:.3f}')
print(f'Mode 2: {mode2:.3f}')

# Plot the mode shapes across a range of natural frequencies
w_range = np.linspace(6.5, 8, 1000)
plt.plot(w_range, mode_shape(w_range), zorder=2)
plt.scatter(w1, mode1, marker='o', label='Mode 1', zorder=3, color='black')
plt.scatter(w2, mode2, marker='s', label='Mode 2', zorder=3, color='black')
plt.legend()
plt.xlabel(r'$\omega$')
plt.ylabel(r'$\frac{x}{\theta}$')
plt.show()
