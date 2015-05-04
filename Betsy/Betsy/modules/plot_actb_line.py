#plot_actb_line.py

import os
from genomicode import mplgraph, arrayplatformlib, config
import arrayio
import subprocess
from Betsy import module_utils, bie3, rulebase


def run(network, antecedents, out_attributes, user_options, num_cores):
    in_data = antecedents
    outfile = name_outfile(in_data, user_options)
    M = arrayio.read(in_data.identifier)
    header = M._row_names
    header_name = M._row_order
    column_id = None
    for i in header_name:
        column = [j.upper() for j in header[i]]
        if 'ACTB' in column:
            column_id = i
            break
    
    if not column_id:
        x = arrayplatformlib.identify_all_platforms_of_matrix(M)
        id = x[0][0]
        platform = x[0][1]
        if platform in ['HG_U133_Plus_2', 'HG_U133B', 'HG_U133A', 'HG_U133A_2',
                        'HG_U95A', 'HumanHT_12', 'HG_U95Av2',
                        'Entrez_ID_human', 'Entrez_Symbol_human', 'Hu6800']:
            out_platform = 'Entrez_Symbol_human'
        elif platform in ['Mouse430A_2', 'MG_U74Cv2', 'Mu11KsubB', 'Mu11KsubA',
                          'MG_U74Av2', 'Mouse430_2', 'MG_U74Bv2',
                          'Entrez_ID_mouse', 'MouseRef_8',
                          'Entrez_Symbol_mouse']:
            out_platform = 'Entrez_Symbol_mouse'
        Annot_path = config.annotate_matrix
        Annot_BIN = module_utils.which(Annot_path)
        assert Annot_BIN, 'cannot find the %s' % Annot_path

        command = ['python', Annot_BIN, in_data.identifier, '--platform',
                   out_platform]
        f = file('tmp', 'w')
        try:
            process = subprocess.Popen(command,
                                       shell=False,
                                       stdout=f,
                                       stderr=subprocess.PIPE)
        finally:
            f.close()
        error_message = process.communicate()[1]
        if error_message:
            raise ValueError(error_message)
        assert module_utils.exists_nz('tmp'), 'the platform conversion fails'
        column_id = out_platform
        M = arrayio.read('tmp')
    
    label = M._col_names['_SAMPLE_NAME']
    keywords = ['ACTB', 'TUBB']
    lines = []
    data = []
    legend_name = []
    for keyword in keywords:
        for i in range(M.dim()[0]):
            if M._row_names[column_id][i].upper() == keyword:
                data.append(M.slice()[i])
                legend_name.append(
                    keyword + '(' + M._row_names[header_name[0]][i] + ')')
    
    for i in range(len(data)):
        line = [(j, data[i][j]) for j in range(len(data[i]))]
        lines.append(line)
        fig = mplgraph.lineplot(*lines,
                                legend=legend_name,
                                box_label=label,
                                ylim_min=0,
                                ylabel='Gene Expression Value')
        fig.savefig(outfile)
    
    if not lines:
        import matplotlib.pyplot as plt
        plt.clf()
        plt.plot([0, 0, 0, 0])
        plt.title('no ACTB or TUBB probes are found')
        plt.savefig(outfile)
    
    assert module_utils.exists_nz(outfile), (
        'the output file %s for plot_actb_line fails' % outfile
    )
    out_node = bie3.Data(rulebase.ActbPlot, **out_attributes)
    out_object = module_utils.DataObject(out_node, outfile)
    return out_object


def make_unique_hash(pipeline, antecedents, out_attributes, user_options):
    identifier = antecedents.identifier
    return module_utils.make_unique_hash(identifier, pipeline, out_attributes,
                                         user_options)


def name_outfile(antecedents, user_options):
    original_file = module_utils.get_inputid(antecedents.identifier)
    filename = 'actb_plot' + original_file + '.png'
    outfile = os.path.join(os.getcwd(), filename)
    return outfile


def get_out_attributes(antecedents, out_attributes):
    return out_attributes


def find_antecedents(network, module_id, out_attributes, user_attributes,
                     pool):
    data_node = module_utils.get_identifier(network, module_id, pool,
                                            user_attributes)

    return data_node
