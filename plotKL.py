import matplotlib.pyplot as plt
# BMS1  m 10
privacy = [4, 6, 8, 10, 12, 14, 16, 18, 20]
KL = [0.421762794226, 0.532449965110, 0.663534201725,
      0.70104552912504, 0.756830173042, 0.8283291791928,
      0.936801039041, 0.9970881412696, 1.1421762794226]

plt.ylim(ymax=3)
plt.ylim(ymin=0)

plt.plot(privacy, KL, marker='o', linestyle='--', color='b', label="m=10")
plt.xlabel("p")
plt.ylabel("KL_Divergence")
plt.title("Reconstruction Error vs p (r = 4) BMS1 m = 10 & m = 20 ")

# BMS1 m = 20
KL = [0.451729374528, 0.652718203984, 0.832366636706,
      1.04971057264901, 1.21257454178071, 1.4936044275956,
      1.562335667726, 1.752513310405, 1.953343640001]
plt.plot(privacy, KL, marker='^', linestyle='--', color='g', label="m=20")
# plt.ylabel("KL_Divergence")
# plt.title("Reconstruction Error vs p (r = 4) BMS1 m = 20")
plt.legend(loc='upper left')
plt.show()

# BMS2 10
KL = [0.03743134132121, 0.042233486799129, 0.05187387346376,
      0.06378746307678, 0.074304245359641, 0.07223892898292,
      0.08256128792189, 0.095436683343, 0.102347450733]
plt.ylim(ymax=0.4)
plt.ylim(ymin=0)

plt.plot(privacy, KL, marker='o', linestyle='--', color='b', label="m=10")
plt.xlabel("p")
plt.ylabel("KL_Divergence")
plt.title("Reconstruction Error vs p (r = 4) BMS2 m = 10 & m = 20 ")

#BMS2 m 20
KL = [0.117387834734, 0.12467879809129, 0.187387346376,
      0.196327667678, 0.204255961441, 0.223892898292,
      0.256128792189, 0.288377343932, 0.292388346433]
plt.plot(privacy, KL, marker='^', linestyle='--', color='g', label="m=20")
plt.legend(loc='upper left')

plt.show()


