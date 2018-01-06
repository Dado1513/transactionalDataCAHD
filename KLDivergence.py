import itertools


def compute_act_s_in_c(dataframe_bandizzato, listaQID, valoriQID, itemSensibile):
    """
    funzione che calcola la pdf di un dato sensibile s in una cella C
    dove la cella C e identificata dalla lista dei QID con i valori in QID
    :param dataframe_bandizzato:
    :param listaQID:
    :param itemSensibile:
    :return: number occorrence s in C / number occorrence s in T
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
            set_temp = dataframe_bandizzato[dataframe_bandizzato[listaQID[i]] == valoriQID[i]].index.tolist()
            set_temp = set(set_temp)
            # essendo un and controllo solo la intersezione
            set_row = set_row.intersection(set_temp)
            # numero di occorrenze di s in C (dove le condizioni listaQID sono verificate)
        number_s_c = len(set_row)
        if number_s_t > 0:
            return number_s_c/number_s_t
        else:
            return 0
    elif type(itemSensibile) is list:
        listOccurrence = list()
        for s in itemSensibile:
            value = compute_act_s_in_c(dataframe_bandizzato,listaQID,valoriQID,s)
            listOccurrence.append(value)
        return listOccurrence
    else:
        return 0


def compute_est_s_in_c(dataframe_bandizzato, gruppi_sd, lista_gruppi, listaQID, valoriQID, itemSensibile):
    """
    a *b/|G|
    dove a è il numero di item sensibibile nel gruppo G
    b il numero di transizioni che matchano i QID nel gruppo
    |G| è la cardinalità del gruppo
    e si calcolca con tutti i gruppi che intersecano la cella C
    :param dataframe_bandizzato:
    :param gruppi_sd:
    :param lista_gruppi:
    :return:
    """
    value_tot = 0
    # per ogni gruppo cerco le celle che matchano la mia condizione
    # print("len",len(lista_gruppi))

    for index in range(0, len(lista_gruppi)):
        cardinality_G = len(lista_gruppi[index])
        set_row = set(lista_gruppi[index].index.tolist())
        for i in range(0, len(listaQID)):

            set_temp = lista_gruppi[index][lista_gruppi[index][listaQID[i]] == valoriQID[i]].index.tolist()
            set_temp = set(set_temp)
            # essendo un and controllo solo la intersezione
            set_row = set_row.intersection(set_temp)
            # numero di occorrenze di s in C (dove le condizioni listaQID sono verificate)

        # value B per il gruppo index
        value_b = len(set_row)
        # print("b",value_b)
        # numero item sensibile nel gruppo index
        value_a = gruppi_sd[index][itemSensibile]
        # print("a",value_a)
        value_tot = value_tot + ((value_a * value_b) / cardinality_G)

    row_sensibile = dataframe_bandizzato[dataframe_bandizzato[itemSensibile] == 1].index.tolist()
    number_s_t = len(row_sensibile)
    if number_s_t > 0:
        value_tot = value_tot / number_s_t
    else:
        value_tot = 0
    return value_tot


def get_all_combination_of_n(n):
    """
    compute all possible combination of n bit
    :param n: numero di QID item
    :return lst: all possibile combination of n value
    """
    lst = [list(i) for i in itertools.product([0, 1], repeat=n)]
    return lst