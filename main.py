import pandas as pd
import mysql.connector
from pybiomart import Dataset
from pybiomart import Server
import requests
import sys
import time

#List of gene name for query
gene_identifier = ["ENSMUSG00000036061", "ENSMUSG00000000555", "ENSMUSG00000023055", "ENSMUSG00000075394",
                   "ENSMUSG00000001655", "ENSMUSG00000022485", "ENSMUSG00000001657", "ENSMUSG00000001661",
                   "ENSMUSG00000076010", "ENSMUSG00000023048"]


#-----------------------------------------------------------------------------------------------------------------------

#Access ENSEMBL database using custom api pybiomart
print("Begin searching with ENSEMBL database")

server = Server(host='http://www.ensembl.org')
#print(server.list_marts())

#list the datasets from the server
mart = server['ENSEMBL_MART_ENSEMBL']
mart.list_datasets()

#grab the required dataset
dataset = Dataset(name='mmusculus_gene_ensembl',host='http://www.ensembl.org')

#print attributes
#print(dataset.list_attributes())
ENSEMBL_attributes = pd.DataFrame(dataset.list_attributes())
ENSEMBL_attributes.to_csv('ENSEMBL_attributes.csv', index=False, header=True)

#print filters
#print(dataset.list_filters())

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


print("Search completed with ENSEMBL database")

#-----------------------------------------------------------------------------------------------------------------------

#Access UNIPROT database using RESTful API
print("Begin searching with UNIPROT database")

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
        print("System error, the database cannot be reached")
        sys.exit()

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

print("Search completed with UNIPROT database")

#-----------------------------------------------------------------------------------------------------------------------
"""
#Access STRING database using RESTful API
print("Begin searching with STRING database")

#Create lists to store the query data
protein_a = []
protein_b = []
interaction_score = []

server = "https://string-db.org"
ext = f"/api/json/network?identifiers={'%0d'.join(gene_identifier)}"
r = requests.get(server + ext, headers={"Accept" : "application/json"})

if not r.ok:
    r.raise_for_status()
    print("System error, the database cannot be reached")
    sys.exit()

decoded = r.json()

# print the whole thing as text
#print(repr(decoded), "\n")

for i in decoded:
    #print(i['preferredName_A'], i['preferredName_B'], i['score'])
    protein_a.append(i['preferredName_A'])
    protein_b.append(i['preferredName_B'])
    interaction_score.append(i['score'])

#Join the list and convert into a pandas dataframe
string_data = {"protein_1" : protein_a,
               "protein_2" : protein_b,
               "interaction_score" : interaction_score}
STRING_table = pd.DataFrame(string_data)

#Create a csv file can be visualised if required
STRING_table.to_csv("STRING_table.csv", index = False)

print("Search completed with STRING database")

#-----------------------------------------------------------------------------------------------------------------------
"""

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
cursor.execute("CREATE DATABASE IF NOT EXISTS s2106664")
cursor.execute("USE s2106664")

#Create ENSEMBL table in mysql

cursor.execute("CREATE TABLE IF NOT EXISTS ENSEMBL (ENSEMBL_id VARCHAR(25), Gene_type VARCHAR(25), Gene_name VARCHAR(25),"
               "Gene_start_bp INT, Gene_end_bp INT, Chromosome INT, GO_term VARCHAR(25), GO_domain VARCHAR(25),"
               "GO_definition VARCHAR(1000))")


ENSEMBL_list = ENSEMBL_table.where(pd.notnull(ENSEMBL_table), None).values.tolist()

#Load the data into mysql using a for loop to iterate through the nested lists
insert_value = (
    "INSERT INTO ENSEMBL(ENSEMBL_id, Gene_type, Gene_name, Gene_start_bp, Gene_end_bp,"
    "Chromosome, GO_term, GO_domain, GO_definition)"
    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
)

for ENSEMBL_value in ENSEMBL_list:
    cursor.execute(insert_value, ENSEMBL_value)


db.commit()

cursor.execute("DROP TABLE IF EXISTS UNIPROT")

cursor.execute("CREATE TABLE IF NOT EXISTS UNIPROT (ENSEMBL_id VARCHAR(25), Protein_name VARCHAR(100),"
               "Protein_function VARCHAR(1500))")
insert_value = (
    "INSERT INTO UNIPROT(ENSEMBL_id, Protein_name, Protein_function)"
    "VALUES (%s,%s,%s)"
)

UNIPROT_list = UNIPROT_table.where(pd.notnull(UNIPROT_table), None).values.tolist()

for UNIPROT_value in UNIPROT_list:
    cursor.execute(insert_value, UNIPROT_value)

db.commit()

#cursor.execute("SELECT * FROM zebra_fish LIMIT 10")
#print(cursor.fetchall())

#cursor.execute("SHOW TABLES")

#print(cursor.fetchall())

db.close()
print("Disconnected from mysql database")

