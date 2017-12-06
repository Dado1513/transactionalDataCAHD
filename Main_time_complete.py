import Dataframe
import AnonymizationCAHD
import time
import matplotlib.pyplot as plt

if __name__ == "__main__":

    dim_finale = 1000
    num_sensibile = 10
    privacy = [4, 6, 8, 10, 16, 20]
    alpha = 3
    time_lista = list()
    print("")
    print("Read Dataset")
    # nameFile = eval(input("Insert name/path file: "))
    # listaItem  = eval(input("Inserire il nome del file contenete gli items: "))
    # testing
    nameFile = "Dataset Paper/dataBMS2_transiction.csv"
    listaItem = "Dataset Paper/lista_items_BMS2.txt"
    # testing
    # nameFile = "Dataset Paper/dataBMS1_transiction.csv"
    # listaItem = "Dataset Paper/lista_items_BMS1.txt"
    # nameFile = "Dataset Paper/dataBMS2_transiction.csv"
    # listaItem = "Dataset Paper/lista_items_BMS2.txt"
    df = Dataframe.Dataframe(nameFile)

    for grado_privacy in privacy:
        start_time = time.time()
        print("")
        print("Calcolo la band matrix")
        df.compute_band_matrix(
            dim_finale=dim_finale,
            nome_file_item=listaItem,
            num_sensibile=num_sensibile, plot = False)

        print("")
        cahd = AnonymizationCAHD.AnonymizationCAHD(
            df,
            grado_privacy=grado_privacy,
            alfa=alpha)

        print("Eseguo Anonimizzazione")
        cahd.CAHD_algorithm()
        end_time = time.time() - start_time
        time_lista.append(end_time)
        print("")
        print("Execution time for privacy %s is %s"%(grado_privacy,end_time))
        # con 1000,5,5,3 crea gruppi con 2 items_sensibili

        #print(cahd.sd_gruppi)
    # BMS1
    # [127.13321161270142, 262.16547203063965, 574.3999593257904, 644.1780500411987, 1198.6934328079224, 1936.6988503932953]
    # BMS2
    # [6.369251489639282, 17.078197956085205, 23.92260766029358, 29.99243950843811, 73.00087451934814, 138.0216190814972]
    print(time_lista)
    plt.plot(privacy,time_lista,marker='o',linestyle='--',color='b')
    plt.xlabel("Privacy")
    plt.ylabel("Time (sec)")
    plt.title("Execution Time (BMS2)  ")
    plt.show()
