import time

from pybiomart import Dataset
from pybiomart import Server
import pandas as pd

gene_identifier = ("ENSMUSG00000036061", "ENSMUSG00000000555", "ENSMUSG00000023055", "ENSMUSG00000075394",
                   "ENSMUSG00000001655", "ENSMUSG00000022485", "ENSMUSG00000001657", "ENSMUSG00000001661",
                   "ENSMUSG00000076010", "ENSMUSG00000023048")



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
                                   "description"],
                       filters={'link_ensembl_gene_id': gene_identifier})

#print query
#print(result)
table_4 = pd.DataFrame(result)
print(table_4)
table_4.to_csv('table_4.csv', index = False)




#modified from https://entrezpy.readthedocs.io/en/master/functions/efetch_func.html

import entrezpy.esearch.esearcher
import entrezpy.log.logger
import entrezpy.efetch.efetcher

#entrezpy.log.logger.set_level('WARN')

#e = entrezpy.esearch.esearcher.Esearcher("entrezpy",
#                                         "simon.tomlinson@ed.ac.uk",
#                                         apikey=None,
#                                         apikey_var=None,
#                                         threads=None,
#                                         qid=None)
#analyzer_result = e.inquire({'db' : 'pubmed',
#                      'term' : 'Mouse [orgn] and Nanog',
#                      'retmax' : '20',
#                      'rettype' : 'uilist'})
#print(analyzer_result.result.count, analyzer_result.result.uids)



#just fecth a couple of the hits
#e = entrezpy.efetch.efetcher.Efetcher("entrezpy",
#                                      "simon.tomlinson@ed.ac.uk",
#                                      apikey=None,
#                                      apikey_var=None,
#                                      threads=None,
#                                      qid=None)
#analyzer = e.inquire({'db' : 'pubmed',
#                      'id' : [36243240,36213683],
#                      'retmode' : 'text',
#                      'rettype' : 'abstract'})
#print(analyzer.get_result())


#RESTAPI
import requests, sys

for i in range (len(gene_identifier)):

    server = "https://rest.ensembl.org"
    ext = f"/lookup/id/{gene_identifier[i]}"

    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    decoded = r.json()

    # print the whole thing as text
    #print(repr(decoded),"\n")
    #print(decoded["id"], ",",
    #      decoded["display_name"], ",",
    #      decoded["biotype"], ",",
    #      decoded["description"], ",",
    #      decoded["species"]
    #      )
    #time.sleep(0.5)
    # extract and print element
    # Notice here I am using a different format of the print statement using f-strings in Python