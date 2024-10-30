import requests, sys
import pandas as pd

#Define variables
protein_a = []
protein_b = []
interaction_score = []

gene_identifier = ("ENSMUSG00000036061", "ENSMUSG00000000555", "ENSMUSG00000023055", "ENSMUSG00000075394",
                   "ENSMUSG00000001655", "ENSMUSG00000022485", "ENSMUSG00000001657", "ENSMUSG00000001661",
                   "ENSMUSG00000076010", "ENSMUSG00000023048")

server = "https://string-db.org"
ext = f"/api/json/network?identifiers={'%0d'.join(gene_identifier)}"
r = requests.get(server + ext, headers={"Accept" : "application/json"})

if not r.ok:
    r.raise_for_status()
    sys.exit()

decoded = r.json()

# print the whole thing as text
print(repr(decoded), "\n")

for i in decoded:
    print(i['preferredName_A'], i['preferredName_B'], i['score'])
    protein_a.append(i['preferredName_A'])
    protein_b.append(i['preferredName_B'])
    interaction_score.append(i['score'])

string_data = {"protein_1" : protein_a,
               "protein_2" : protein_b,
               "interaction_score" : interaction_score}

STRING_table = pd.DataFrame(string_data)
STRING_table.to_csv("STRING_table.csv", index = False)


