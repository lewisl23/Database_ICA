# Biological database ICA

This is a biological database coursework for MSc Bioinformatics that searches the 
ENSEMBL, UNIPROT, GO, and STRING database. 10 gene identifier IDs are used to search 
through the databases and result tables of each search are loaded into the mysql database.

10 gene identifier IDs: \
"ENSMUSG00000036061", "ENSMUSG00000000555", "ENSMUSG00000023055", "ENSMUSG00000075394", \
"ENSMUSG00000001655", "ENSMUSG00000022485", "ENSMUSG00000001657", "ENSMUSG00000001661", \
"ENSMUSG00000076010", "ENSMUSG00000023048"

## Database searched:
1. ENSEMBL (http://www.ensembl.org)
2. UNIPROT (https://www.uniprot.org)
3. GO (https://geneontology.org)
4. STRING (https://string-db.org)

## Steps
1. ### Database access
The search results from each database are organised into individual table and 
saved in the *search_results* folder. Depending on the database type, the databases 
are accessed using REST API (returns JSON) or directly using Biomart (returns pandas dataframe). 

2. ### Loading into mysql server
The tables saved in the *search_results* folder are loaded into the mysql server 
by creating the *gene_search_db* database. When loading each results table, the 
ENSEMBL_id is set as the primary keys so ensure the relational design of the 
database so that different tables can be easily accessed with SQL query.

3. ### SQL query of *gene_search_db*
The final table that includes results from each database are queried using SQL queries 
and laoded into an integrated table *integrated_table.csv*