import time
from pybiomart import Dataset
from pybiomart import Server
import pandas as pd

gene_identifier = ("ENSMUSG00000036061", "ENSMUSG00000000555", "ENSMUSG00000023055", "ENSMUSG00000075394",
                   "ENSMUSG00000001655", "ENSMUSG00000022485", "ENSMUSG00000001657", "ENSMUSG00000001661",
                   "ENSMUSG00000076010", "ENSMUSG00000023048")

gene_name = ("Itga5", "Hoxc13", "Hoxc8", "Hoxc6", "Hoxc5", "Prr13", "Calcoco1", "Smug1", "Hoxc4", "Mir615")

#Custom API using Biomart to accrss ENSEMBL
server = Server(host='http://www.ensembl.org')
#print(server.list_marts())


#list the datasets from the server
mart = server['ENSEMBL_MART_ENSEMBL']
mart.list_datasets()

#grab the required dataset
dataset = Dataset(name='mmusculus_gene_ensembl',host='http://www.ensembl.org')

#print attributes
#print(dataset.list_attributes())
table_2 = pd.DataFrame(dataset.list_attributes())
table_2.to_csv('table_2.csv', index=False, header=True)

#print filters
#print(dataset.list_filters())
table_3 = pd.DataFrame(dataset.list_filters())
table_3.to_csv('table_3.csv', index=False, header=True)


#generate query results- from chosen filters and attributes
result = dataset.query(attributes=["ensembl_gene_id",
                                   "gene_biotype",
                                   "external_gene_name",
                                   "start_position",
                                   "end_position",
                                   "chromosome_name",
                                   "name_1006",
                                   "definition_1006",
                                   "description"],
                       filters={'link_ensembl_gene_id': gene_identifier})

#print query
#print(result)
table_4 = pd.DataFrame(result)
#print(table_4)
table_4.to_csv('table_4.csv', index = False)
