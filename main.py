import pandas as pd
import mysql.connector

#List of gene name to include in the database
gene_identifier = ("ENSMUSG00000036061", "ENSMUSG00000000555", "ENSMUSG00000023055", "ENSMUSG00000075394",
                   "ENSMUSG00000001655", "ENSMUSG00000022485", "ENSMUSG00000001657", "ENSMUSG00000001661",
                   "ENSMUSG00000076010", "ENSMUSG00000023048")

#Create table for NCBI data using custom API -

#Create table for ENSEMBL using custom API


#Create table 1 from database:
table1 = pd.DataFrame({'Gene':["Cool",2], "Name":[3,"Method"], "Function":[5,6]})

print(table1)

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

cursor.execute("SELECT * FROM zebra_fish LIMIT 10")

print(cursor.fetchall())

cursor.execute("SHOW TABLES")

print(cursor.fetchall())


db.close()
print("Disconnected from mysql database")

