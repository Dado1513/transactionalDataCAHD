import matplotlib.pyplot as plt
# BMS2 10
privacy = [4, 6, 8, 10, 16, 20]
KL = [0.056, 0.06, 0.067, 0.072, 0.085, 0.11]
plt.ylim(ymax=0.4)
plt.plot(privacy, KL, marker='o', linestyle='--', color='b')
plt.xlabel("p")
plt.ylabel("KL_Divergence")
plt.title("Reconstruction Error vs p (r = 4) BMS2 m = 10")
plt.show()

# BMS2 m = 20
KL = [0.12, 0.16, 0.2, 0.22, 0.272, 0.29]
plt.plot(privacy, KL, marker='o', linestyle='--', color='b')
plt.xlabel("p")
plt.ylim(ymax=0.4)
plt.ylim(ymin=0)
plt.ylabel("KL_Divergence")
plt.title("Reconstruction Error vs p (r = 4) BMS2 m = 10")
plt.show()
