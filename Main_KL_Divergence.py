import Dataframe
import AnonymizationCAHD
import time
import numpy as np
import KLDivergence
import random
import operator

if __name__ == "__main__":

    #dim_finale = eval(input("Dimensione del dataset: "))
    #dim_finale = 1000
    dim_finale = 1000
    #num_sensibile = eval(input("Numero di item sensibili da testare: "))
    num_sensibile = 20
    #grado_privacy = eval(input("Grado di privacy desiderato: "))
    #privacy_list = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    privacy_list = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    KLs = list()
    for grado_privacy in privacy_list:
        #alpha = eval(input(
        #    "Inserire valore di alpha (p*alfa check, valore ottimale = 3): "))
        alpha = 3
        #nameFile = eval(input("Insert name/path file: "))
        #listaItem = eval(input("Inserire il nome del file contenete gli items: "))
        # testing
        nameFile = "Dataset Paper/dataBMS1_transiction.csv"
        listaItem = "Dataset Paper/lista_items_BMS1.txt"
        #nameFile = "Dataset Paper/dataBMS2_transiction.csv"
        #listaItem = "Dataset Paper/lista_items_BMS2.txt"
        print("")
        print("Read Dataset")
        df = Dataframe.Dataframe(nameFile)
        start_time = time.time()
        print("")
        print("Calcolo la band matrix")
        df.compute_band_matrix(
            dim_finale=dim_finale,
            nome_file_item=listaItem,
            num_sensibile=num_sensibile)

        print("")
        cahd = AnonymizationCAHD.AnonymizationCAHD(
            df,
            grado_privacy=grado_privacy,
            alfa=alpha)

        cahd.compute_hist()
        hist_item = cahd.hist
        print("Eseguo Anonimizzazione")
        cahd.CAHD_algorithm()
        end_time = time.time() - start_time
        print("Execution time for privacy %s is %s" %(grado_privacy, end_time))
        print("")
        # con 1000,5,5,3 crea gruppi con 2 items_sensibili
        # dict degli item dove la key sono relativi al dataframe bandizzato

        # bisogna settare il numero di QID da tenere in consideraione
        # r (quindi sono 2^r possibili combinazioni) di solito r = 4
        # item sensibili sono definiti sopra
        # p fissato vedi sopra con p e m variabile

        # per saper i dati sensibili
        r = 4 # numero di QID nella query
        all_item = list(df.items_final.keys())
        columns_item_sensibili = df.lista_sensibili.values.tolist()
        dataframe_bandizzato = df.dataframe_bandizzato
        QID = cahd.lista_gruppi[0].columns.tolist()

        # 816 --> Item sensibile
        # ToDo da fare per ogni cella C per i QID identificati --> 1217 e 1
        # get r from QID value randomicamente
        QID_select = list()
        while len(QID_select) < r:
            temp = random.choice(QID)
            if temp not in QID_select:
                QID_select.append(temp)
        all_value = KLDivergence.get_all_combination_of_n(r)
        # get max value of sensibile data

        item_sensibile = int(max(hist_item.keys(), key=(lambda k: hist_item[k])))
        print(hist_item)
        print(item_sensibile)
        KL_Divergence = 0
        for valori in all_value:
            actsc = KLDivergence.compute_act_s_in_c(dataframe_bandizzato, QID_select, valori, item_sensibile)
            #print("acts", actsc)
            estsc = KLDivergence.compute_est_s_in_c(dataframe_bandizzato,cahd.sd_gruppi,
                                                    cahd.lista_gruppi, QID_select, valori, item_sensibile)
            #print("est", estsc)
            if actsc > 0 and estsc > 0:
                temp = actsc * np.log(actsc/estsc)
            else:
                temp = 0
            #print("KL_Divergence i = ", temp )
            KL_Divergence = KL_Divergence + temp
        KLs.append(KL_Divergence)
        print("p: "+str(grado_privacy)+" m: "+str(num_sensibile)+" KL: "+str(KL_Divergence))
    if nameFile == "Dataset Paper/dataBMS2_transiction.csv":
        open_file = "valoriKLD_BMS2_"+str(num_sensibile)+".txt"
    else:
        open_file = "valoriKLD_BMS1_"+str(num_sensibile)+".txt"

    file = open(open_file,"w")
    file.write("num_sensibili " + str(num_sensibile) + "\n")
    file.write("dimension " + str(dim_finale) + "\n")

    for index in range(0, len(privacy_list)):
        file.write(str(privacy_list[index]) + " " + str(KLs[index]) + "\n")
    file.close()

