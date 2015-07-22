#call_variants_GATK.py
import os
from Betsy import module_utils, bie3, rulebase
import subprocess
from genomicode import config


def run(network, antecedents, out_attributes, user_options, num_cores):
    in_data = antecedents
    outfile = name_outfile(in_data, user_options)
    GATK_path = config.Gatk
    GATK_BIN = module_utils.which(GATK_path)
    assert os.path.exists(GATK_path), ('cannot find the %s' % GATK_path)
    species = out_attributes['ref']
    if species == 'hg18':
        ref_file = config.hg18_ref
    elif species == 'hg19':
        ref_file = config.hg19_ref
    elif species == 'dm3':
        ref_file = config.dm3_ref
    elif species == 'mm9':
        ref_file = config.mm9_ref
    
    assert os.path.exists(ref_file), 'the ref file %s does not exsits' % ref_file
    command = ['java', '-jar', GATK_path, '-T', 'UnifiedGenotyper', '-R',
               ref_file, '-I', in_data.identifier, '-o', outfile, '-rf',
               'BadCigar', '-stand_call_conf', '50.0', '-stand_emit_conf',
               '10.0']
    process = subprocess.Popen(command,
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    #process.wait()
    error_message = process.communicate()[1]
    #print error_message
    if 'error' in error_message:
        raise ValueError(error_message)
    
    assert module_utils.exists_nz(outfile), (
        'the output file %s for call_variants_GATK does not exist' % outfile
    )
    out_node = bie3.Data(rulebase.VcfFile, **out_attributes)
    out_object = module_utils.DataObject(out_node, outfile)
    return out_object


def set_out_attributes(antecedents, out_attributes):
    return out_attributes


def make_unique_hash(pipeline, antecedents, out_attributes, user_options):
    identifier = antecedents.identifier
    return module_utils.make_unique_hash(identifier, pipeline, out_attributes,
                                         user_options)


def name_outfile(antecedents, user_options):
    original_file = module_utils.get_inputid(antecedents.identifier)
    filename = 'GATK_' + original_file + '.vcf'
    outfile = os.path.join(os.getcwd(), filename)
    return outfile


def find_antecedents(network, module_id, out_attributes, user_attributes,
                     pool):
    filter1 = module_utils.AntecedentFilter(datatype_name='BamFile')
    data_node = module_utils.find_antecedents(
        network, module_id, user_attributes, pool, filter1)
    return data_node
