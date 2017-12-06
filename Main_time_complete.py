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
    df = Dataframe.Dataframe('Data/online_retail_transaction.csv')

    for grado_privacy in privacy:
        start_time = time.time()
        print("")
        print("Calcolo la band matrix")
        df.compute_band_matrix(
            dim_finale=dim_finale,
            nome_file_item="Data/lista_items.txt",
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

    print(time_lista)
    plt.plot(privacy,time_lista,marker='o',linestyle='--',color='b')
    plt.xlable("Privacy")
    plt.ylable("Time (sec)")
    plt.title("Execution Time   ")
