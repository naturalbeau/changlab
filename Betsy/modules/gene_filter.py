#gene_filter.py
import os
import module_utils

def run(parameters,objects,pipeline):
    identifier,single_object = get_identifier(parameters,objects)
    outfile,new_objects = get_outfile(parameters,objects,pipeline)
    import arrayio
    f_out = file(outfile,'w')
    M = arrayio.read(identifier)
    I_good = []
    #get the percentage of gene filter
    percent=float(parameters['filter'])/100
    for i in range(M.dim()[0]):
       missing_count = 0
       for j in range(M.dim()[1]):
           if M._X[i][j] == None:
                missing_count = missing_count + 1
       if float(missing_count)/M.dim()[1]<percent:
            I_good.append(i)
    M_c = M.matrix(I_good,None)
    arrayio.pcl_format.write(M_c,f_out)
    f_out.close()
    module_utils.write_Betsy_parameters_file(parameters,single_object,pipeline)
    return new_objects
    
def make_unique_hash(parameters,objects,pipeline):
    return module_utils.make_unique_hash(
        parameters,objects,'signal_file','Contents,DatasetId',pipeline)

def get_outfile(parameters,objects,pipeline):
    return module_utils.get_outfile(
        parameters,objects,'signal_file','Contents,DatasetId','signal_file',pipeline)
    
def get_identifier(parameters,objects):
    return module_utils.find_object(parameters,objects,'signal_file','Contents,DatasetId')
