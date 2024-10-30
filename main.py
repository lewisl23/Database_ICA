import pandas as pd
import mysql.connector
from pybiomart import Dataset
from pybiomart import Server
import requests
import sys
import time

#List of gene name to include in the database
gene_identifier = ("ENSMUSG00000036061", "ENSMUSG00000000555", "ENSMUSG00000023055", "ENSMUSG00000075394",
                   "ENSMUSG00000001655", "ENSMUSG00000022485", "ENSMUSG00000001657", "ENSMUSG00000001661",
                   "ENSMUSG00000076010", "ENSMUSG00000023048")

#-----------------------------------------------------------------------------------------------------------------------
#Access ENSEMBL database using custom api pybiomart

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
print(dataset.list_filters())

#generate query results from the chosen attributes and filters
result = dataset.query(attributes=["ensembl_gene_id",
                                   "gene_biotype",
                                   "external_gene_name",
                                   "start_position",
                                   "end_position",
                                   "chromosome_name",
                                   "go_id",
                                   "namespace_1003",
                                   "definition_1006"],
                       filters={'link_ensembl_gene_id': gene_identifier})

#print query and save in as a pandas dataframe
#print(result)
ENSEMBL_table = pd.DataFrame(result)

#Create a csv file can be visualised if required
ENSEMBL_table.to_csv('ENSEMBL_table.csv', index = False)


#-----------------------------------------------------------------------------------------------------------------------
#Access UNIPROT database using RESTful API

#Create lists to store the query data
ENSEMBL = []
Protein_Name = []
Function = []

for id in range(len(gene_identifier)):
    print(f"Searching for {gene_identifier[id]} using UNIPROT database")
    server = "https://rest.uniprot.org"
    ext = f"/uniprotkb/search?query={gene_identifier[id]}+AND+reviewed:true&fields=protein_name,cc_function"
    r = requests.get(server + ext, headers={"Accept" : "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()
        print("System error, the database cannot be reached")

    decoded = r.json()

    # print the whole thing as text to understand the data structure
    #print(repr(decoded), "\n")

    if decoded['results'] == []:
        print(f"The given gene identifier {gene_identifier[id]} cannot be accessed through the UNIPROT database")
        continue
    else:
        ENSEMBL.append(gene_identifier[id])
        Protein_Name.append(decoded['results'][0]['proteinDescription']['recommendedName']['fullName']['value'])
        Function.append(decoded['results'][0]['comments'][0]['texts'][0]['value'])
        print("Search completed")

    time.sleep(0.1)

#Join the list and convert into a pandas dataframe
UNIPROT_data = {
    'ENSEMBL_id' : ENSEMBL,
    'Protein_Name' : Protein_Name,
    'Function' : Function
}
UNIPROT_table = pd.DataFrame(UNIPROT_data)

#Create a csv file can be visualised if required
UNIPROT_table.to_csv('UNIPROT_table.csv', index = False)


#-----------------------------------------------------------------------------------------------------------------------











#connection to mysql database on the server
db = mysql.connector.connect (
	host = "localhost",
	port = 9999,
	user = "s2106664",
	password = "82kPR7XM"
)

print("Successfully connected to mysql database")

cursor = db.cursor()

#Create the database s2106664 if it not exist and use the database
#cursor.execute("CREATE DATABASE IF NOT EXISTS s2106664")
#cursor.execute("USE s2106664")

#cursor.execute("SELECT * FROM zebra_fish LIMIT 10")

#print(cursor.fetchall())

#cursor.execute("SHOW TABLES")

#rint(cursor.fetchall())


db.close()
print("Disconnected from mysql database")

