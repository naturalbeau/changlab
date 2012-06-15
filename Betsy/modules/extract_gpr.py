#extract_gpr.py
import os
import gzip
import shutil
import rule_engine
import module_utils
import hash_method
import gpr_module

def run(parameters,objects,pipeline,options=None):
    """extract the files that are gpr format"""
    single_object = get_identifier(parameters,objects)
    outfile = get_outfile(parameters,objects,pipeline)
    check = []
    files = os.listdir(single_object.identifier)
    for i in files:
        if i == '.DS_Store':
            pass
        else:
            gpr = gpr_module.check_gpr(os.path.join(single_object.identifier,i))
            check.append(gpr)
    os.mkdir(outfile)
    for i in range(len(check)):
        if check[i]:
            old_file = os.path.join(single_object.identifier,i)
            new_file = os.path.join(outfile,i)
            shutil.copyfile(old_file,new_file)
    assert module_utils.exists_nz(outfile),'the output file %s\
                              for extract_gpr fails'%outfile
    new_objects = get_newobjects(parameters,objects,pipeline)
    module_utils.write_Betsy_parameters_file(
            parameters,single_object,pipeline)
    return new_objects


def make_unique_hash(identifier,pipeline,parameters):
    inputid = module_utils.get_inputid(identifier)
    hash_profile = {'version': 'gpr',
                   'number of files':str(len(os.listdir(identifier)))}
    hash_result = hash_method.hash_parameters(
                 inputid,pipeline,**hash_profile)
    return hash_result


def get_outfile(parameters,objects,pipeline):
    single_object = get_identifier(parameters,objects)
    original_file = module_utils.get_inputid(single_object.identifier)
    filename = 'gpr_files_'+ original_file
    outfile = os.path.join(os.getcwd(),filename)
    return outfile

def get_newobjects(parameters,objects,pipeline):
    outfile = get_outfile(parameters,objects,pipeline)
    single_object = get_identifier(parameters,objects)
    new_objects = module_utils.get_newobjects(
        outfile,'gpr_files',parameters,objects,single_object)
    return new_objects


def get_identifier(parameters,objects):
    single_object = module_utils.find_object(
        parameters,objects,'gpr_files','contents')
    assert os.path.exists(single_object.identifier),'folder %s for are_all_gpr does not exit.' %single_object.identifier
    assert os.path.isdir(single_object.identifier),"input %s for are_all_gpr is not a folder" %single_object.identifier
    return single_object

 
