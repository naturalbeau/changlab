#normalize_with_rsem_fastq.py
import os
from Betsy import module_utils, bie3, rulebase
import subprocess
from genomicode import config
import tempfile


def preprocess_single_sample(folder, sample, files, out_file, ref):
    if ref == 'human':
        ref_file = config.rna_human
    elif ref == 'mouse':
        ref_file = config.rna_mouse
    else:
        raise ValueError("we cannot handle %s" % ref)
    if len(files) == 1:
        input_file = os.path.join(folder, files[0])
        command = ['rsem-calculate-expression', input_file, ref_file,
                   '--no-bam-output', '-p', '8', sample]
    elif len(files) == 2:
        input_file1 = os.path.join(folder, files[0])
        input_file2 = os.path.join(folder, files[1])
        command = ['rsem-calculate-expression', '--paired-end', input_file1,
                   input_file2, ref_file, '--no-bam-output', '-p', '8', sample]
    else:
        raise ValueError('number files is not correct')
    process = subprocess.Popen(command,
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    error_message = process.communicate()[1]
    if 'error' in error_message:
        raise ValueError(error_message)
    process.wait()
    slice_BIN = config.slice_matrix
    command = ['python', slice_BIN, sample + '.genes.results',
               '--select_col_ids', 'transcript_id,gene_id,TPM',
               '--replace_col_ids', 'TPM,' + sample]
    f = file(out_file, 'w')
    try:
        process = subprocess.Popen(command,
                                   shell=False,
                                   stdout=f,
                                   stderr=subprocess.PIPE)
        process.wait()
    finally:
        f.close()
    error_message = process.communicate()[1]
    if 'error' in error_message:
        raise ValueError(error_message)
    assert module_utils.exists_nz(out_file), (
        'the output file %s does not exist' % out_file
    )


def preprocess_multiple_sample(folder, group_dict, outfile, ref):
    filenames = os.listdir(folder)
    file_list = []
    for sample in group_dict:
        temp_file = tempfile.mkstemp()[1]
        preprocess_single_sample(folder, sample, group_dict[sample], temp_file,
                                 ref)
        file_list.append(temp_file)
    result_file = file_list[0]
    tmp_list = file_list[:]
    try:
        for filename in file_list[1:]:
            tmp_result = tempfile.mkstemp()[1]
            f = file(tmp_result, 'a+')
            try:
                module_utils.merge_two_files(result_file, filename, f)
            finally:
                f.close()
                tmp_list.append(tmp_result)
            result_file = tmp_result
        os.rename(result_file, outfile)
    finally:
        for filename in tmp_list:
            if os.path.exists(filename):
                os.remove(filename)


def process_group_info(group_file):
    f = file(group_file, 'r')
    text = f.readlines()
    f.close()
    group_dict = {}
    text = [line.strip() for line in text if line.strip()]
    for line in text:
        words = line.split('\t')
        if len(words) == 2:
            group_dict[words[0]] = [words[1]]
        elif len(words) == 3:
            group_dict[words[0]] = [words[2], words[3]]
        else:
            raise ValueError('group file is invalid')
    return group_dict


def run(network, antecedents, out_attributes, user_options, num_cores):
    data_node, group_node = antecedents
    outfile = name_outfile(antecedents, user_options)
    group_dict = process_group_info(group_node.identifier)
    assert 'fastq_ref' in user_options, 'should provide ref in human or mouse'
    preprocess_multiple_sample(data_node.identifier, group_dict, outfile,
                               user_options['fastq_ref'])
    assert module_utils.exists_nz(outfile), (
        'the output file %s for normalize_with_rsem_fastq does not exist' % outfile
    )
    out_node = bie3.Data(rulebase.SignalFile_Postprocess, **out_attributes)
    out_object = module_utils.DataObject(out_node, outfile)
    return out_object


def make_unique_hash(pipeline, antecedents, out_attributes, user_options):
    data_node, group_node = antecedents
    identifier = data_node.identifier
    return module_utils.make_unique_hash(identifier, pipeline, out_attributes,
                                         user_options)


def name_outfile(antecedents, user_options):
    data_node, group_node = antecedents
    original_file = module_utils.get_inputid(data_node.identifier)
    filename = original_file + '.tdf'
    outfile = os.path.join(os.getcwd(), filename)
    return outfile


def get_out_attributes(antecedents, out_attributes):
    return out_attributes


def find_antecedents(network, module_id, out_attributes, user_attributes,
                     pool):
    data_node = module_utils.get_identifier(network, module_id, pool,
                                            user_attributes,
                                            datatype='FastqFolder')
    group_node = module_utils.get_identifier(network, module_id, pool,
                                             user_attributes,
                                             datatype='SampleGroupFile')

    return data_node, group_node
