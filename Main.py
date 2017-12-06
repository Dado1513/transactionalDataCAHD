import Dataframe
import AnonymizationCAHD
if __name__ == "__main__":

    dim_finale = eval(input("Dimensione del dataset: "))
    num_sensibile = eval(input("Numero di item sensibili da testare: "))
    grado_privacy = eval(input("Grado di privacy desiderato: "))
    alpha = eval(input(
        "Inserire valore di alpha (p*alfa check, valore ottimale = 3): "))
    nameFile = eval(input("Insert name/path file: "))
    listaItem  = eval(input("Inserire il nome del file contenete gli items: "))
    # testing
    # nameFile = "Dataset Paper/dataBMS1_transiction.csv"
    # listItem = "Dataset Paper/lista_items_BMS1.txt"
    print("")
    print("Read Dataset")
    df = Dataframex.Dataframe(nameFile)

    print("")
    print("Calcolo la band matrix")
    df.compute_band_matrix(
        dim_finale=dim_finale,
        nome_file_item=listItem,
        num_sensibile=num_sensibile)

    print("")
    cahd = AnonymizationCAHD.AnonymizationCAHD(
        df,
        grado_privacy=grado_privacy,
        alfa=alpha)

    print("Eseguo Anonimizzazione")
    cahd.CAHD_algorithm()
    # con 1000,5,5,3 crea gruppi con 2 items_sensibili
    print(cahd.sd_gruppi)
