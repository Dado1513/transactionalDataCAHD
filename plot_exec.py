import matplotlib.pyplot as plt
# 1000 item
# 10 items sensibili
# p = 10
# alfa = 3
# BMS1
privacy = [4, 6, 8, 10, 16, 20]
time_lista = [127.13321161270142, 262.16547203063965, 574.3999593257904, 644.1780500411987, 1198.6934328079224, 1936.6988503932953]
print(time_lista)
plt.plot(privacy,time_lista,marker='o',linestyle='--',color='b')
plt.xlabel("Privacy")
plt.ylabel("Time (sec)")
plt.title("Execution Time (BMS1)  ")
plt.show()

# BMS2
time_lista = [6.369251489639282, 17.078197956085205, 23.92260766029358, 29.99243950843811, 73.00087451934814, 138.0216190814972]
print(time_lista)
plt.plot(privacy,time_lista,marker='o',linestyle='--',color='b')
plt.xlabel("Privacy")
plt.ylabel("Time (sec)")
plt.title("Execution Time (BMS2)  ")
plt.show()
