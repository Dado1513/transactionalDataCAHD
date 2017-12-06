import pandas as pd
import numpy as np
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csr_matrix
import matplotlib.pylab as plt
import scipy.sparse as sps
from random import randint

class Dataframe:

    dataframe = None # datframe iniziale
    dataframe_bandizzato = None # dataframe after RCM e square
    items_final = None # lista di tutti i prodotti indicizzati con colonna
    lista_sensibili = None # lista prodotti sensibili
    original_band = None
    band_after_rcm = None

    def __init__(self,nome_file=None):
        """
            Costruttore che legge il file csv
        """
        self.dataframe = pd.read_csv(nome_file,header=None,index_col=None)

    def compute_band_matrix(self,dim_finale = 1000, nome_file_item = None, num_sensibile = 1,plot = True):
        """
            Compute band_matrix , permutazione casuale di righe e colonne
            estrapola a caso item_sensibili
        """
        original_dataset = self.dataframe
        if original_dataset is not None and len(original_dataset) >= dim_finale and len(original_dataset.columns) >= dim_finale:

            # leggo nomi items
            file = open(nome_file_item, "r")
            items = file.read().splitlines()
            # permuto righe e colonne del df inizale e prendo le prime :dim_finale
            np.random.seed(seed=13)
            random_column = np.random.permutation(original_dataset.shape[1])[:dim_finale]
            random_row = np.random.permutation(original_dataset.shape[0])[:dim_finale]
            # recupero gli item selezionati nel relativo ordine == colonne
            items_reordered = [items[i] for i in random_column]
            # df selezionato e square
            # eliminare le righe nulle a priori
            df_square = original_dataset.iloc[random_row][random_column];
            # eliminare solo se items sensibili nulli
            # selezioni gli utlimi num_sensibili come item sensibili
            # check se esiste almeno un item sensibile
            f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
            # check che le colonne sensibili non siano nulle
            lista_sensibili = df_square.columns[-num_sensibile:]
            # plot matrice sparsa iniziale
            # plt
            ax1.spy(df_square, marker='.', markersize='1')
            #ax1.show()
            # applicazione algoritmo RCM
            sparse = csr_matrix(df_square)
            order = reverse_cuthill_mckee(sparse)
            # solo se add gli 0
            # riordino i dati sensibili
            # df_sensibili = df_sensibili.iloc[order]
            # ora devo prendere gli item selzionati prima e riordinarli ancora
            # secondo quello scritto in order quindi
            items_final = [items_reordered[i] for i in order]
            column_reordered = [df_square.columns[i] for i in order]
            # creo gl item indicizzati con la colonna
            items_final = dict(zip(column_reordered,items_final))
            # df bandizzato
            df_square_band = df_square.iloc[order][column_reordered]
            # plotto
            ax2.spy(df_square_band, marker='.', markersize='1')
            #ax2.show()
            if plot:
                plt.show()
            # banda dataframe inizale
            [i, j] = np.where(df_square == 1)
            bw = max(i-j) + 1
            self.original_band = bw
            print("Bandwidth first RCM", bw)

            # banda dataframe dopo RCM
            [i, j] = np.where(df_square_band == 1)
            bw = max(i-j) + 1
            self.band_after_rcm = bw
            print("Bandwidth after RCM", bw)

            self.dataframe_bandizzato = df_square_band
            self.items_final = items_final
            self.lista_sensibili = lista_sensibili
        elif original_dataset is not None and len(original_dataset) >= dim_finale:
            # devo essere sicuro di avere il numero di righe giusto
            # allora devo squadrarlo con la dimensione finale definita dall'utente
            file = open(nome_file_item, "r")
            items = file.read().splitlines()
            columns = original_dataset.columns
            zero_data_to_add = np.zeros(shape=(len(original_dataset),len(original_dataset)-len(columns)))
            # aggiungo li zero con la dimensione finale relativa
            #zero_data_to_add.shape
            columns_to_add = ["temp"+str(x) for x in range(0,len(df_ridotto)-len(columns))]
            #columns_to_add
            df_to_add = pd.DataFrame(zero_data_to_add, columns=columns_to_add,index=original_dataset.index,dtype='uint8')
            #df_to_add
            # creo il dataset completo aggiungendo tutti gli zeri che mancano
            original_dataset = pd.concat([original_dataset, df_to_add], axis=1)
            # permuto righe e colonne del df inizale e prendo le prime :dim_finale
            np.random.seed(seed=13)
            random_column = np.random.permutation(original_dataset.shape[1])
            random_row = np.random.permutation(original_dataset.shape[0])[:dim_finale]
            # recupero gli item selezionati nel relativo ordine == colonne
            # aggiungo gli item casuali
            items.extend(columns_to_add)
            items_reordered = [items[i] for i in random_column]

            # df selezionato e square
            # eliminare le righe nulle a priori
            df_square = original_dataset.iloc[random_row][random_column];
            # eliminare solo se items sensibili nulli
            # selezioni gli utlimi num_sensibili come item sensibili
            # check se esiste almeno un item sensibile
            f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
            # check che le colonne sensibili non siano nulle
            lista_sensibili = df_square.columns[-num_sensibile:]
            # plot matrice sparsa iniziale
            # plt
            ax1.spy(df_square, marker='.', markersize='1')
            #ax1.show()
            # applicazione algoritmo RCM
            sparse = csr_matrix(df_square)
            order = reverse_cuthill_mckee(sparse)
            # solo se add gli 0
            # riordino i dati sensibili
            # df_sensibili = df_sensibili.iloc[order]
            # ora devo prendere gli item selzionati prima e riordinarli ancora
            # secondo quello scritto in order quindi
            items_final = [items_reordered[i] for i in order]
            column_reordered = [df_square.columns[i] for i in order]
            # creo gl item indicizzati con la colonna
            items_final = dict(zip(column_reordered,items_final))
            # df bandizzato
            df_square_band = df_square.iloc[order][column_reordered]
            # plotto
            ax2.spy(df_square_band, marker='.', markersize='1')
            #ax2.show()
            if plot:
                plt.show()
            # banda dataframe inizale
            [i, j] = np.where(df_square == 1)
            bw = max(i-j) + 1
            self.original_band = bw
            print("Bandwidth first RCM", bw)

            # banda dataframe dopo RCM
            [i, j] = np.where(df_square_band == 1)
            bw = max(i-j) + 1
            self.band_after_rcm = bw
            print("Bandwidth after RCM", bw)

            self.dataframe_bandizzato = df_square_band
            self.items_final = items_final
            self.lista_sensibili = lista_sensibili
