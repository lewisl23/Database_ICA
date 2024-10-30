#Use NCBI to get more protein information and about the gene ontology


#Another custom API to access NCBI related database
#modified from https://entrezpy.readthedocs.io/en/master/functions/efetch_func.html

gene_identifier = ("ENSMUSG00000036061", "ENSMUSG00000000555", "ENSMUSG00000023055", "ENSMUSG00000075394",
                   "ENSMUSG00000001655", "ENSMUSG00000022485", "ENSMUSG00000001657", "ENSMUSG00000001661",
                   "ENSMUSG00000076010", "ENSMUSG00000023048")


import entrezpy.esearch.esearcher
import entrezpy.log.logger
import entrezpy.efetch.efetcher
import time

entrezpy.log.logger.set_level('WARN')
for i in gene_identifier:
    e = entrezpy.esearch.esearcher.Esearcher("entrezpy",
                                             "s2106664@ed.ac.uk",
                                             apikey=None,
                                             apikey_var=None,
                                             threads=None,
                                             qid=None)
    analyzer_result = e.inquire({'db' : 'gene',
                                 'term' : i,
                                 'rettype' : 'uilist'})
    time.sleep(0.01)

gene_id_list = analyzer_result.result.uids

print(gene_id_list)

#just fecth a couple of the hits
e = entrezpy.efetch.efetcher.Efetcher("entrezpy",
                                      "simon.tomlinson@ed.ac.uk",
                                      apikey=None,
                                      apikey_var=None,
                                      threads=None,
                                      qid=None)

analyzer = e.inquire({'db' : 'gene',
                      'id' : gene_id_list,
                      'retmode' : 'text',
                      'rettype' : 'gene_table'})
print(analyzer.get_result())
