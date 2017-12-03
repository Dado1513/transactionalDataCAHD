import pandas as pd
import numpy as np
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csr_matrix
import matplotlib.pylab as plt
import scipy.sparse as sps
from random import randint
import operator

class AnonymizationCAHD:

    # DATA
    dataframe_bandizzato = None # dataframe after RCM
    items_sensibili = None # list all sensibile data
    nome_item = None # dict index--> nome_item
    grado_privacy = None # grado privacy richiesto
    alfa = None # controllo le alfa * grado_privacy transizoni
    hist = None # hist delle frequenze dei dati sensibili
    transizioni_sensibili = None # id transizioni sensibii
    transizioni_sensibili_all = None # tutte le transizioni mapping con ite sensibii
    items_sensibili_per_tranzioni = None

    dict_group = None
    dataframe_anonimizzato = None
    lista_gruppi = None
    sd_gruppi = None

    def __init__(self, dataframe=None, grado_privacy=4, alfa = 3):
        """
            Anonymization through CAHD algorithm , euristico and greedy
        """
        self.dataframe_bandizzato = dataframe.dataframe_bandizzato.copy()
        self.items_sensibili = dataframe.lista_sensibili
        self.nome_item = dataframe.items_final
        self.grado_privacy = grado_privacy
        self.alfa = alfa

    def compute_hist(self):
        self.hist = dict(self.dataframe_bandizzato[self.items_sensibili].sum())
        print(self.hist)

    def check_grado_privacy(self):
        """
        compute se il grado della privacy può essere soddisfatto, se così non fosse
        si diminuisce il grado della privacy per averne uno ottimale, oppure si può
        decidere di modificare gli item sensibili
        """
        for value in self.hist.values():
            if value * self.grado_privacy >=len(self.dataframe_bandizzato)-1:
                return False
        return True

    def get_id_transazioni_sensibili(self):
        self.transazioni_sensibili = set(list(np.where(self.dataframe_bandizzato[self.items_sensibili] == 1)[0]))
        self.transizioni_sensibili_all = list(np.where(self.dataframe_bandizzato[self.items_sensibili] == 1)[0])
        # item sensibili della transazione iesime
        self.item_sensibile_per_transazioni = list(np.where(self.dataframe_bandizzato[self.items_sensibili] == 1)[1])

    def check_conflict(self, row_i, row_j):
        # se hanno un items sensibile in comune allora sono in conflitto
        dati_sensibili_row_i = self.items_sensibili[np.where(self.dataframe_bandizzato.iloc[row_i][self.items_sensibili] == 1)]
        dati_sensibili_row_j = self.items_sensibili[np.where(self.dataframe_bandizzato.iloc[row_j][self.items_sensibili] == 1)]
        # create set
        set_j = set(dati_sensibili_row_j)
        set_i = set(dati_sensibili_row_i)
        # check intersection
        return len(set_i.intersection(set_j)) > 0

    def select_best_transactions(self, candidate_list, transaction_target):
        all_items = list(self.dataframe_bandizzato)
        QID_items = [x for x in all_items if x not in self.items_sensibili]

        #lista riportante gli item in comune con transactionTarget
        distance = list()
        # remove list che hanno items_sensibili in comune
        # bisogna controllare che nella lista candidate non vi siano transizioni in conflitto con loro

        #for id in index[0]:

        for row in candidate_list:
            list1 = self.dataframe_bandizzato.iloc[transaction_target][QID_items]
            list2 = self.dataframe_bandizzato.iloc[row][QID_items]
            #da queste due liste, devo escludere le transazioni sensibili.

            #num. elementi in comune di due liste
            distance.append(sum([x and y for x, y in zip(list1, list2)]))

        #ottengo i p-1 indici della lista candidata con distanza maggiore
        major_indexs = list()
        for i in range(0, self.grado_privacy-1):
            max_index,max_value = max(enumerate(distance), key=operator.itemgetter(1))
            major_indexs.append(max_index)
            distance[max_index] = -1

        #seleziono gli indici delle righe del dataframe con maggior QIitems in comune
        best_rows = list()
        for i in major_indexs:
            best_rows.append(candidate_list[i])

        return best_rows


    def compute_candidate_list(self, indice_transizione_sensibile):
        alpha_p = self.alfa * self.grado_privacy
        lc = list()  # lista candidate
        k = 1
        # controllo gli alpha*p transazioni precedenti non sono in conflitto
        cond = max(indice_transizione_sensibile - alpha_p - k, -1)
        i = indice_transizione_sensibile - 1;
        while (i > cond):
            if i not in self.transizioni_sensibili_all:
                lc.append(i)
            else:
                if self.check_conflict(indice_transizione_sensibile, i):
                    k = k + 1
                else:
                    # controllo che nella lista non vi siano gia delle transizioni con quelli item sensibili
                    # se si non la posso inserire
                    conflitto_lista = False
                    for index in lc:
                        if self.check_conflict(index, i):
                            conflitto_lista = True
                    if not conflitto_lista:
                        lc.append(i)
                    else:
                        k = k + 1

            cond = max(indice_transizione_sensibile - alpha_p - k, -1)
            i -= 1

        # alpha*p transizioni successive che non sono in conflitto
        k = 1
        cond = min(indice_transizione_sensibile + alpha_p + k, len(self.dataframe_bandizzato))
        i = indice_transizione_sensibile + 1
        while(i < cond):
            if i not in self.transizioni_sensibili_all:
                lc.append(i)
            else:
                if self.check_conflict(indice_transizione_sensibile, i):
                    k = k + 1
                else:
                    conflitto_lista = False
                    for index in lc:
                        if self.check_conflict(index, i):
                            conflitto_lista = True
                    if not conflitto_lista:
                        lc.append(i)
                    else:
                        k = k + 1
            cond = min(indice_transizione_sensibile + alpha_p + k, len(self.dataframe_bandizzato))
            i += 1

        error = False
        if len(lc) < self.grado_privacy:
            error = True

        return lc,error



    def CAHD_algorithm(self):
        """
            algoritmo di anonimizzazion
        """
        self.compute_hist()
        soddisfabile = False
        while not soddisfabile and self.grado_privacy > 0:
            soddisfabile = self.check_grado_privacy()
            if not soddisfabile:
                self.grado_privacy -= 1
        print("grado di privacy soddisfabile: ", self.grado_privacy)
        # lunghezza del dataframe
        remaining = len(self.dataframe_bandizzato)
        # compute le transizioni sensibili
         # inidice delle righe delle transazioni sensibili non ripetute
        # indice delle transizioni sensibili con mapping 1-1 con item_sensibile_per_transizione
        # transazioni_sensibili_completa[i] --> indice della transizione
        # item_sensibile_per_transazioni[i] --> item sensibile per la transizione sopra
        self.get_id_transazioni_sensibili()
        # riempo il dizionario (hash_map) indicizzata con il numero della riga
        for t in self.transazioni_sensibili:
            index_t = np.where(np.array(self.transizioni_sensibili_all) == t)[0]


        lc = dict()     # lista candidata
        #FORMO IL DATAFRAME ANONIMIZZATO [item sensibili sono riportati a destra]
        #Nota: codice aggiunto. Molti di questi argomenti possono essere passati esternamente e passati a loro volta
        #a funzioni interne
        df_square = self.dataframe_bandizzato.copy()
        all_items = list(df_square.columns)
        QID_items = [x for x in all_items if x not in self.items_sensibili]
        columns_list = QID_items.copy()
        for x in self.items_sensibili:
            columns_list.append(x)
        # dataframe anonimizzato dopo aver sopostato tutte le colonne degli item sensibili a destra
        dataframe_anonimizzato = pd.DataFrame(columns = columns_list,index = df_square.index)
        dict_group = list()

        # index delle row del datframe bandizzato relativo alle row sensibili
        id_sensitive_transaction = self.dataframe_bandizzato.iloc[list(self.transazioni_sensibili)].index

        #Ciclo finchè ho gruppi da anonimizzare
        done = False

        # lista dei gruppi con i relativi dati sensibili all'interno
        lista_gruppi =list()
        sd_gruppi = list()

        #indice che cicla tra gli id_delle transazioni sensibili
        ts_index = 0
        while not done:
            #se ho terminato di scorrere la lista delle transazioni sensibili esco dal ciclo
            if(ts_index > len(id_sensitive_transaction)-1):
                done = True
                break

            #seleziono la iesima transazione sensibile
            q = id_sensitive_transaction[ts_index]
            #passo da label a num.di riga
            t = self.dataframe_bandizzato.index.get_loc(q)

            #nel caso di cancellazioni, devo aggiornare la lista degli indici delle transazioni sensibili
            transazioni_sensibili = list()
            for i in id_sensitive_transaction:
                transazioni_sensibili.append(self.dataframe_bandizzato.index.get_loc(i))

            #lista candidata LC
            lc,errore = self.compute_candidate_list( t)
            # se posso creare il gruppo
            if not errore:
                group = self.select_best_transactions(lc, t)
                #aggiungo la transazione bersaglio
                group.append(t)

                # somma degli items sensibili del gruppo iesimo relativo
                selected_sensitive_items = self.dataframe_bandizzato.iloc[group][self.items_sensibili].sum()
                # temp hist
                temp_hist = self.hist.copy()
                # aggiorno le occorrenze di ogni item sensbile

                for index in selected_sensitive_items.index:
                    temp_hist[index] -= selected_sensitive_items.loc[index]

                # controllo se il gruppo creato va bene
                found = False
                for index in temp_hist.keys():
                    # se non si può più soddisfare il grado di privacy

                    if temp_hist[index] * self.grado_privacy > remaining:
                        found = True
                        ts_index += 1
                        break

                # se il gruppo invece va bene
                if not found:
                    # update hist
                    self.hist = temp_hist.copy()
                    #DEVO RIMUOVERE EVENTUALI TRANSAZIONI SENSIBILI COMPRESE NEL GRUPPO DA id_sensitive_transaction
                    label_group = self.dataframe_bandizzato.iloc[group].index
                    id_sensitive_transaction = [x for x in id_sensitive_transaction if x not in label_group]

                    # indice iesimo -> indice delle transazioni del gruppo iesimo
                    dict_group.append(self.dataframe_bandizzato.index[group])

                    # metto i QID nel datframe anonimizzato
                    dataframe_anonimizzato.loc[list(self.dataframe_bandizzato.index[group])] = \
                    self.dataframe_bandizzato.loc[list(self.dataframe_bandizzato.index[group])]

                    lista_gruppi.append(self.dataframe_bandizzato.loc[list(self.dataframe_bandizzato.index[group]),QID_items])

                    for index in list(self.dataframe_bandizzato.index[group]):
                        # metto la somma dei SD del gruppo per ogni row del gruppo
                        dataframe_anonimizzato.loc[index][selected_sensitive_items.index] = selected_sensitive_items

                    sd_gruppi.append(selected_sensitive_items) # aggiungo somma item sensibili relativi al gruppo iesimo

                    # le droppo dal df iniziale
                    self.dataframe_bandizzato = self.dataframe_bandizzato.drop(list(self.dataframe_bandizzato.index[group]))

                    # compute row rimanenti
                    remaining = len(self.dataframe_bandizzato.index)

            else:
                ts_index += 1

        #terminato il ciclo di formazione dei gruppi, mi rimane un supergruppo con le transazioni sensibili rimanenti o meno.

        # somma item sensibili nel gruppo rimasto
        #for i in range(0,dataframe_bandizzato.shape[0]):
        #    transaction = dataframe_bandizzato.index[i]
        #    dataframe_anonimizzato.loc[transaction] = dataframe_bandizzato.iloc[i]

        # update del dataframe anonimizzato con il super gruppo finale
        selected_sensitive_items = self.dataframe_bandizzato[self.items_sensibili].sum()
        dataframe_anonimizzato.loc[self.dataframe_bandizzato.index] = self.dataframe_bandizzato
        # metto la somma degli item
        for index in list(self.dataframe_bandizzato.index):
            dataframe_anonimizzato.loc[index,self.items_sensibili]= selected_sensitive_items
        lista_gruppi.append(self.dataframe_bandizzato[QID_items])
        sd_gruppi.append(selected_sensitive_items)
        # del datframe iniziale
        self.dataframe_bandizzato = None
        self.sd_gruppi = sd_gruppi
        self.lista_gruppi = lista_gruppi
        self.dict_group = dict_group
