#sort_sam_file.py
import os
from Betsy import module_utils, bie3, rulebase
import subprocess
from genomicode import config


def run(network, antecedents, out_attributes, user_options, num_cores):
    in_data = antecedents
    outfile = name_outfile(in_data, user_options)
    sortsam_BIN = config.sortsam
    assert os.path.exists(sortsam_BIN), 'cannot find the %s' % sortsam_BIN
    command = ['java', '-Xmx5g', '-jar', sortsam_BIN,
               'I=' + in_data.identifier, 'O=' + outfile, 'SO=coordinate',
               'VALIDATION_STRINGENCY=LENIENT', 'CREATE_INDEX=true']
    process = subprocess.Popen(command,
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    process.wait()
    error_message = process.communicate()[1]
    if 'error' in error_message:
        raise ValueError(error_message)
    
    assert module_utils.exists_nz(outfile), (
        'the output file %s for sort_sam_file does not exist' % outfile
    )
    out_node = bie3.Data(rulebase.BamFile, **out_attributes)
    out_object = module_utils.DataObject(out_node, outfile)
    return out_object


def make_unique_hash(pipeline, antecedents, out_attributes, user_options):
    identifier = antecedents.identifier
    return module_utils.make_unique_hash(identifier, pipeline, out_attributes,
                                         user_options)


def get_out_attributes(antecedents, out_attributes):
    return out_attributes


def name_outfile(antecedents, user_options):
    original_file = module_utils.get_inputid(antecedents.identifier)
    filename = 'sorted_' + original_file + '.bam'
    outfile = os.path.join(os.getcwd(), filename)
    return outfile


def find_antecedents(network, module_id, out_attributes, user_attributes,
                     pool):
    data_node = module_utils.get_identifier(network, module_id, pool,
                                            user_attributes,
                                            datatype='SamFile')

    return data_node
