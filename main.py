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
#ENSEMBL_attributes = pd.DataFrame(dataset.list_attributes())
#ENSEMBL_attributes.to_csv('ENSEMBL_attributes.csv', index=False, header=True)

#print filters
#print(dataset.list_filters())
#dataset.list_filters().to_csv('ENSEMBL_filter.csv', index=False, header=True)

#generate query results from the chosen attributes and filters
result = dataset.query(attributes=["ensembl_gene_id",
                                   "gene_biotype",
                                   "external_gene_name",
                                   "start_position",
                                   "end_position",
                                   "chromosome_name"],
                                   #"go_id",
                                   #"namespace_1003",
                                   #"definition_1006"],
                       filters={'link_ensembl_gene_id': gene_identifier})

#print query and save in as a pandas dataframe
#print(result)
ENSEMBL_table = pd.DataFrame(result)

#Create a csv file can be visualised if required
ENSEMBL_table.to_csv('ENSEMBL_table.csv', index = False)

print("Search completed with ENSEMBL database")

#-----------------------------------------------------------------------------------------------------------------------

GO_result = dataset.query(attributes=["ensembl_gene_id",
                                   "go_id",
                                   "namespace_1003",
                                   "definition_1006"],
                          filters={'link_ensembl_gene_id': gene_identifier})

#print query and save in as a pandas dataframe
#print(result)
GO_table = GO_result.dropna()

print(GO_table)

#Create a csv file can be visualised if required
GO_table.to_csv('GO_table.csv', index = False)

def concatenate(series):
    return ', '.join(map(str, series))

grouped_GO_table = GO_table.groupby('Gene stable ID').agg({
    'GO term accession': concatenate,
    'GO domain': concatenate,
    'GO term definition': concatenate}).reset_index()

grouped_GO_table.to_csv('Grouped_GO_table.csv', index = False)

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


#connection to mysql database on the server
db = mysql.connector.connect (
	host = "localhost",
	port = 9999,
	user = "s2106664",
	password = "82kPR7XM"
)
print("Successfully connected to mysql database")

cursor = db.cursor()

#Create the database s2106664 if not existed and use the database
cursor.execute("CREATE DATABASE IF NOT EXISTS s2106664")
cursor.execute("USE s2106664")

cursor.execute("DROP TABLE IF EXISTS ENSEMBL")

#Create the ENSEMBL table in mysql and load the ENSEMBL data into it
cursor.execute("CREATE TABLE IF NOT EXISTS ENSEMBL (ENSEMBL_id VARCHAR(25), Gene_type VARCHAR(25), Gene_name VARCHAR(25),"
               "Gene_start_bp INT, Gene_end_bp INT, Chromosome INT, PRIMARY KEY (ENSEMBL_id))")

ENSEMBL_list = ENSEMBL_table.where(pd.notnull(ENSEMBL_table), None).values.tolist()

insert_value = (
    "INSERT INTO ENSEMBL(ENSEMBL_id, Gene_type, Gene_name, Gene_start_bp, Gene_end_bp, Chromosome)"
    "VALUES (%s,%s,%s,%s,%s,%s)"
)

for ENSEMBL_value in ENSEMBL_list:
    cursor.execute(insert_value, ENSEMBL_value)


cursor.execute("DROP TABLE IF EXISTS UNIPROT")
#Create the UNIPROT table in mysql and load the UNIPROT data into it
cursor.execute("CREATE TABLE IF NOT EXISTS UNIPROT (ENSEMBL_id VARCHAR(25), Protein_name VARCHAR(100),"
               "Protein_function VARCHAR(1500), PRIMARY KEY (ENSEMBL_id))")
insert_value = (
    "INSERT INTO UNIPROT(ENSEMBL_id, Protein_name, Protein_function)"
    "VALUES (%s,%s,%s)"
)

UNIPROT_list = UNIPROT_table.where(pd.notnull(UNIPROT_table), None).values.tolist()

for UNIPROT_value in UNIPROT_list:
    cursor.execute(insert_value, UNIPROT_value)


cursor.execute("DROP TABLE IF EXISTS STRING")
#Create the STRING table in mysql and load the STRING data into it
cursor.execute("CREATE TABLE IF NOT EXISTS STRING (Protein_1 VARCHAR(25), Protein_2 VARCHAR(125),"
               "Interaction_score DECIMAL(5,3))")

STRING_list = STRING_table.where(pd.notnull(STRING_table), None).values.tolist()

insert_value = (
    "INSERT INTO STRING(Protein_1, Protein_2, Interaction_score)"
    "VALUES (%s,%s,%s)"
)

for STRING_value in STRING_list:
    cursor.execute(insert_value, STRING_value)

#---------------------- NEW STUFF -------------------------

cursor.execute("DROP TABLE IF EXISTS GO")
#Create the ENSEMBL table in mysql and load the ENSEMBL data into it
cursor.execute("CREATE TABLE IF NOT EXISTS GO (ENSEMBL_id VARCHAR(25), GO_term VARCHAR(1000), GO_domain VARCHAR(1000),"
               "GO_description VARCHAR(10000))")

GO_list = grouped_GO_table.where(pd.notnull(grouped_GO_table), None).values.tolist()

insert_value = (
    "INSERT INTO GO(ENSEMBL_id, GO_term, GO_domain, GO_description)"
    "VALUES (%s,%s,%s,%s)"
)

for GO_value in GO_list:
    cursor.execute(insert_value, GO_value)

db.commit()

#Query the summary tabld from the 3 tables
#cursor.execute("SELECT * FROM ENSEMBL JOIN UNIPROT ON ENSEMBL.ENSEMBL_id=UNIPROT.ENSEMBL_id")
cursor.execute("SELECT ENSEMBL.*, UNIPROT.Protein_name, UNIPROT.Protein_function, STRING.*, GO.* "
               "FROM ENSEMBL "
               "LEFT JOIN UNIPROT ON ENSEMBL.ENSEMBL_id=UNIPROT.ENSEMBL_id "
               "LEFT JOIN STRING ON ENSEMBL.Gene_name=STRING.Protein_1 OR ENSEMBL.Gene_name=STRING.Protein_2 "
               "LEFT JOIN GO ON ENSEMBL.ENSEMBL_id=GO.ENSEMBL_id")




integrated_table = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

db.close()
print("Disconnected from mysql database")

integrated_table = pd.DataFrame(integrated_table, columns=columns)
integrated_table.to_csv('integrated_table.csv', index = False)

