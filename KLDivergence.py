def compute_act_s_in_c(dataframe_bandizzato, listaQID, valoriQID, itemSensibile):
    """
    funzione che calcola la pdf di un dato sensibile s in una cella C
    dove la cella C e identificata dalla lista dei QID con i valori in QID
    :param dataframe_bandizzato:
    :param listaQID:
    :param itemSensibile:
    :return: number occorrence in C / number occorrence in T
    """
    # numero di occorrenze di s in T (tutto il dataset)
    # se itemSensibile è solo 1 ok
    row_sensibile = list()

    if type(itemSensibile) is int:
        row_sensibile = dataframe_bandizzato[dataframe_bandizzato[itemSensibile] == 1].index.tolist()
        number_s_t = len(row_sensibile)
        set_row = set(row_sensibile)
        # tutti i valori li controllo
        for i in range(0,len(listaQID)):
            set_temp = dataframe_bandizzato[dataframe_bandizzato[listaQID[i]]==valoriQID[i]].index.tolist()
            set_temp = set(set_temp)
            # essendo un and controllo solo la intersezione
            set_row = set_row.intersection(set_temp)
            # numero di occorrenze di s in C (dove le condizioni listaQID sono verificate)
        number_s_c = len(set_row)

        return number_s_c/number_s_t
    elif type(itemSensibile) is list:
        listOccurrence = list()
        for s in itemSensibile:
            value = compute_act_s_in_c(dataframe_bandizzato,listaQID,valoriQID,s)
            listOccurrence.append(value)
        return  listOccurrence
    else:
        return None

    def compute_est_s_in_c(dataframe_bandizzato, gruppi_sd,lista_gruppi):
        return None
