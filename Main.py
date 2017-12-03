import Dataframe
import AnonymizationCAHD

if __name__ == "__main__":
    df =Dataframe.Dataframe('online_retail_transaction.csv')
    df.compute_band_matrix(dim_finale=50,nome_file_item="lista_items.txt",num_sensibile=4)
    cahd = AnonymizationCAHD.AnonymizationCAHD(df)
    cahd.CAHD_algorithm()
    print(cahd.sd_gruppi)
