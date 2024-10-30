import requests, sys
import time
import pandas as pd

gene_identifier = ("ENSMUSG00000036061", "ENSMUSG00000000555", "ENSMUSG00000023055", "ENSMUSG00000075394",
                   "ENSMUSG00000001655", "ENSMUSG00000022485", "ENSMUSG00000001657", "ENSMUSG00000001661",
                   "ENSMUSG00000076010", "ENSMUSG00000023048")

ENSEMBL = []
GO = []
Function = []

for id in range(len(gene_identifier)):
    server = "https://rest.uniprot.org"
    ext = f"/uniprotkb/search?query={gene_identifier[id]}+AND+reviewed:true&fields=go"
    r = requests.get(server + ext, headers={"Accept" : "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    decoded = r.json()

    # print the whole thing as text
    print(repr(decoded), "\n")

    #print(decoded['results'][0]['uniProtKBCrossReferences'])

    if decoded['results'] == []:
        continue
    else:
        for i in decoded['results'][0]['uniProtKBCrossReferences']:
            #print(f"{i['id']}", f"{i['properties'][0]['value']}")
            ENSEMBL.append(gene_identifier[id])
            GO.append(i['id'])
            Function.append(i['properties'][0]['value'])

        time.sleep(0.5)


UNIPROT_data = {
    'ENSEMBL_id' : ENSEMBL,
    'GO' : GO,
    'Function' : Function
}

UNIPROT_table = pd.DataFrame(UNIPROT_data)
UNIPROT_table.to_csv('UNIPROT_table.csv', index = False)