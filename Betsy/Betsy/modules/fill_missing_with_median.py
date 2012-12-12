#fill_missing_with_median.py
import os
import shutil
from Betsy import module_utils
import arrayio
import numpy

def run(parameters, objects, pipeline):
    single_object = get_identifier(parameters, objects)
    outfile = get_outfile(parameters, objects, pipeline)
    if not is_missing(single_object.identifier):
            shutil.copyfile(single_object.identifier, outfile)
    else:
        M = arrayio.read(single_object.identifier)
        f_out = file(outfile, 'w')
        X = M.slice()
        for i in range(M.dim()[0]):
            med = numpy.median([j for j in X[i] if j])
            for j in range(M.dim()[1]):
                if M._X[i][j] is None:
                    M._X[i][j] = med
        arrayio.tab_delimited_format.write(M, f_out)
        f_out.close()
    assert module_utils.exists_nz(outfile), (
        'the output file %s for median_fill_if_missing does not exist'
        % outfile)
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
    filename = 'signal_median_fill_' + original_file + '.tdf'
    outfile = os.path.join(os.getcwd(), filename)
    return outfile


def get_identifier(parameters, objects):
    single_object = module_utils.find_object(
        parameters, objects, 'signal_file', 'contents,preprocess')
    assert os.path.exists(single_object.identifier), (
        'the input file %s for median_fill_if_missing does not exist'
        % single_object.identifier)
    return single_object


def get_newobjects(parameters, objects, pipeline):
    outfile = get_outfile(parameters, objects, pipeline)
    single_object = get_identifier(parameters, objects)
    new_objects = module_utils.get_newobjects(
        outfile, 'signal_file', parameters, objects, single_object)
    return new_objects

