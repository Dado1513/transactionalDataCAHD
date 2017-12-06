import matplotlib.pyplot as plt
# 1000 item
# 10 items sensibili
# p = 10
# alfa = 3
privacy = [4, 6, 8, 10, 16, 20]
time_lista = [127.13321161270142, 262.16547203063965, 574.3999593257904, 644.1780500411987, 1198.6934328079224, 1936.6988503932953]
print(time_lista)
plt.plot(privacy,time_lista,marker='o',linestyle='--',color='b')
plt.xlabel("Privacy")
plt.ylabel("Time (sec)")
plt.title("Execution Time  ")
plt.show()
