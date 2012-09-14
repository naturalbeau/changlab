#convert_signal_to_pcl.py
import os
import module_utils
import shutil

def run(parameters,objects,pipeline):
    """convert not xls signal file to pcl format"""
    import arrayio
    single_object = get_identifier(parameters,objects)
    outfile = get_outfile(parameters,objects,pipeline)
    f = file(outfile,'w')
    M = arrayio.choose_format(single_object.identifier)
    if M.__name__[8:-7] == 'pcl':
        shutil.copyfile(single_object.identifier,outfile)
        f.close()
    else:
        M = arrayio.read(single_object.identifier)
        M_c = arrayio.convert(M,to_format = arrayio.pcl_format)
        arrayio.pcl_format.write(M_c,f)
        f.close()
    assert module_utils.exists_nz(outfile),(
        'the output file %s for convert_to_pcl_if_not_pcl fails'%outfile)
    new_objects = get_newobjects(parameters,objects,pipeline)
    module_utils.write_Betsy_parameters_file(
        parameters,single_object,pipeline,outfile)
   
    return new_objects

def make_unique_hash(identifier,pipeline,parameters):
    return module_utils.make_unique_hash(
        identifier,pipeline,parameters)

def get_outfile(parameters,objects,pipeline):
    single_object = get_identifier(parameters,objects)
    original_file = module_utils.get_inputid(single_object.identifier)
    filename = 'signal_'+original_file+'.pcl'
    outfile = os.path.join(os.getcwd(),filename)
    return outfile
    
def get_identifier(parameters,objects):
    single_object = module_utils.find_object(
        parameters,objects,'signal_file','contents,preprocess')
    assert os.path.exists(single_object.identifier),(
        'the input file %s for convert_to_pcl_if_not_pcl does not exist'
        %single_object.identifier)
    return single_object

def get_newobjects(parameters,objects,pipeline):
    outfile = get_outfile(parameters,objects,pipeline)
    single_object = get_identifier(parameters,objects)
    new_objects = module_utils.get_newobjects(
        outfile,'signal_file',parameters,objects,single_object)
    return new_objects
