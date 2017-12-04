import Dataframe
import AnonymizationCAHD

if __name__ == "__main__":

    dim_finale = eval(input("Dimensione del dataset: "))
    num_sensibile = eval(input("Numero di item sensibili da testare: "))
    grado_privacy = eval(input("Grado di privacy desiderato: "))
    alpha = eval(input(
        "Inserire valore di alpha (p*alfa check, valore ottimale = 3): "))
    print("")
    print("Read Dataset")
    df = Dataframe.Dataframe('online_retail_transaction.csv')
    print("")
    print("Calcolo la band matrix")
    df.compute_band_matrix(
        dim_finale=dim_finale,
        nome_file_item="lista_items.txt",
        num_sensibile=num_sensibile)
    print("")
    print("Eseguo Anonimizzazione")
    cahd = AnonymizationCAHD.AnonymizationCAHD(
        df,
        grado_privacy=grado_privacy,
        alfa=alpha)
    print("Anonimizzazione eseguita")
    cahd.CAHD_algorithm()
    #print(cahd.sd_gruppi)
