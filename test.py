import numpy as np
import matplotlib.pyplot as plt
t = np.arange(0.0, 2.0, 0.01)
s = np.sin(2*np.pi*t)

# plt.plot(t, s)
# plt.title(r'$\alpha_i > \beta_i$', fontsize=20)
# plt.text(1, -0.6, r'$\sum_{i=0}^\infty x_i$', fontsize=20)
# plt.text(1, 0, r'$\mathcal{A}\mathrm{sin}(2 \omega t)$',
#          fontsize=20)

# build a rectangle in axes coords
left, width = .25, .5
bottom, height = .25, .5
right = left + width
top = bottom + height

x = 0.5*(left+right)
y = 0.5*(bottom+top)

plt.text(x, y, r'$\alpha_i > \beta_i$',
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=20, color='black')


# plt.xlabel('time (s)')
# plt.ylabel('volts (mV)')
plt.axis('off')
plt.show()