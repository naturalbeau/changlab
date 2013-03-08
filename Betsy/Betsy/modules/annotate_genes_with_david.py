##annotate_genes_with_david.py
import os
from Betsy import module_utils
from genomicode import arrayplatformlib


def run(parameters, objects, pipeline):
    """run David"""
    single_object = get_identifier(parameters, objects)
    outfile = get_outfile(parameters, objects, pipeline)
    f = file(single_object.identifier, 'r')
    text = f.read()
    f.close()
    in_list = text.split()
    # guess the idType
    chipname = arrayplatformlib.identify_platform_of_annotations(in_list)
    assert chipname in platform2idtype, 'David does not handle %s' % chipname
    idType = platform2idtype[chipname]    # convert the platform to idtype
    DAVIDenrich(in_list, idType, outfile)
    assert module_utils.exists_nz(outfile), (
        'the outfile for run_david %s does not exist' % outfile)
    new_objects = get_newobjects(parameters, objects, pipeline)
    module_utils.write_Betsy_parameters_file(
        parameters, single_object, pipeline, outfile)
    return new_objects


def make_unique_hash(identifier, pipeline, parameters):
    return module_utils.make_unique_hash(
        identifier, pipeline, parameters)


def get_outfile(parameters, objects, pipeline):
    single_object = get_identifier(parameters, objects)
    original_file = module_utils.get_inputid(single_object.identifier)
    filename = 'david_' + original_file + '.txt'
    outfile = os.path.join(os.getcwd(), filename)
    return outfile


def get_identifier(parameters, objects):
    single_object = module_utils.find_object(
        parameters, objects, 'gene_list_file', 'contents')
    assert os.path.exists(single_object.identifier), (
        'the input file %s for run_gather does not exist'
        % single_object.identifier)
    return single_object


def get_newobjects(parameters, objects, pipeline):
    outfile = get_outfile(parameters, objects, pipeline)
    single_object = get_identifier(parameters, objects)
    new_objects = module_utils.get_newobjects(
        outfile, 'david_file', parameters, objects, single_object)
    return new_objects


def DAVIDenrich(in_list, idType, outfile, bg_list=[], bgName='Background1',
                listName='List1', category='', thd=0.1, ct=2):
    from suds.client import Client
    assert len(in_list) < 3000, (
        'the number of genes to David cannot exceed 3000')
    if len(in_list) > 0:
        inputListIds = ','.join(in_list)
    else:
        raise
    flagBg = False
    if len(bg_list) > 0:
        inputBgIds = ','.join(bg_list)
        flagBg = True
    x = str('http://david.abcc.ncifcrf.gov/') + str(
        'webservice/services/DAVIDWebService?wsdl')
    client = Client(x)
    client.service.authenticate('xiaoling.chen@uth.tmc.edu')
    listType = 0
    client.service.addList(inputListIds, idType, listName, listType)
    if flagBg:
        listType = 1
        client.service.addList(inputBgIds, idType, bgName, listType)
    client.service.setCategories(category)
    chartReport = client.service.getChartReport(thd, ct)
    with open(outfile, 'w') as fOut:
        header = ['Category', 'Term', 'Count', '%', 'Pvalue', 'Genes',
                  'List Total', 'Pop Hits', 'Pop Total', 'Fold Enrichment',
                  'Bonferroni', 'Benjamini', 'FDR\n']
        fOut.write('\t'.join(header))
        for row in chartReport:
            rowDict = dict(row)
            categoryName = str(rowDict['categoryName'])
            termName = str(rowDict['termName'])
            listHits = str(rowDict['listHits'])
            percent = str(rowDict['percent'])
            ease = str(rowDict['ease'])
            Genes = str(rowDict['geneIds'])
            listTotals = str(rowDict['listTotals'])
            popHits = str(rowDict['popHits'])
            popTotals = str(rowDict['popTotals'])
            foldEnrichment = str(rowDict['foldEnrichment'])
            bonferroni = str(rowDict['bonferroni'])
            benjamini = str(rowDict['benjamini'])
            FDR = str(rowDict['afdr'])
            rowList = [categoryName, termName, listHits, percent,
                       ease, Genes, listTotals, popHits, popTotals,
                       foldEnrichment, bonferroni, benjamini, FDR]
            fOut.write('\t'.join(rowList) + '\n')


platform2idtype = {'MG_U74Av2': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'HG_U133_Plus_2': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'Mu11KsubA': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'Mu11KsubB': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'Hu6800': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'HG_U133B': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'Mouse430_2': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'RG_U34A': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'Mouse430A_2': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'HG_U95A': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'HG_U133A': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'RAE230A': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'Hu35KsubC': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'Hu35KsubB': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'MG_U74Cv2': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'HG_U133A_2': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'Hu35KsubA': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'Hu35KsubD': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'MG_U74Bv2': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'HG_U95Av2': 'AFFYMETRIX_3PRIME_IVT_ID',
                   'HumanHT_12': 'ILLUMINA_ID',
                   'HumanWG_6': 'ILLUMINA_ID',
                   'MouseRef_8': 'ILLUMINA_ID',
                   'HumanHT_12_control': 'ILLUMINA_ID',
                   'MouseRef_8_control': 'ILLUMINA_ID',
                   'Entrez_ID_human': 'ENTREZ_GENE_ID',
                   'Entrez_ID_mouse': 'ENTREZ_GENE_ID',
                   'Entrez_symbol_human': 'GENE_SYMBOL',
                   'Entrez_symbol_mouse': 'GENE_SYMBOL'}
