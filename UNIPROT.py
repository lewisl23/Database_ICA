import requests, sys
import time
import pandas as pd


gene_identifier = ("ENSMUSG00000036061", "ENSMUSG00000000555", "ENSMUSG00000023055", "ENSMUSG00000075394",
                   "ENSMUSG00000001655", "ENSMUSG00000022485", "ENSMUSG00000001657", "ENSMUSG00000001661",
                   "ENSMUSG00000076010", "ENSMUSG00000023048")

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
UNIPROT_table.to_csv('UNIPROT_table.csv', index = False)