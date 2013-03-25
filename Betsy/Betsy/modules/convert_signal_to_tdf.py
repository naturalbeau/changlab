#convert_signal_to_tdf.py
import os
from Betsy import module_utils
import shutil
import xlrd 
import openpyxl
import arrayio
import subprocess
from genomicode import config, arrayplatformlib
from time import strftime,localtime


def run(parameters, objects, pipeline,user,jobname):
    """check an input file is xls or xlsx format"""
    starttime = strftime(module_utils.FMT, localtime())
    single_object = get_identifier(parameters, objects)
    outfile = get_outfile(parameters, objects, pipeline)
    if single_object.identifier.endswith('.gz'):
        unzip_file = module_utils.gunzip(single_object.identifier)
    else:
        unzip_file = single_object.identifier
    M = None
    xls_file = None
    txt_file = unzip_file
    try:
        xlrd.open_workbook(unzip_file)
        xls_file = 'tmp.xls'
    except Exception, XLRDError:
        try:
            book = openpyxl.load_workbook(unzip_file)
            xls_file = 'tmp.xlsx'
        except Exception, InvalidFileException:
            xls_file = None
        except (SystemError, MemoryError, KeyError), x:
            raise
    if xls_file:
        shutil.copyfile(unzip_file, xls_file)
        xls2txt_path = config.xls2txt
        xls2txt_BIN = module_utils.which(xls2txt_path)
        assert xls2txt_BIN, 'cannot find the %s' % xls2txt_path
        f = file('tmp1.txt', 'w')
        command = ['python', xls2txt_BIN, tmp_file]
        process = subprocess.Popen(command, shell=False,
                                   stdout=f,
                                   stderr=subprocess.PIPE)
        error_message = process.communicate()[1]
        if error_message:
            raise ValueError(error_message)
        os.remove(tmp_file)
        f.close()
        txt_file = 'tmp1.txt'
    M = arrayio.choose_format(txt_file)
    M = guess_and_change_gct_header(txt_file)
    M_c = arrayio.convert(M, to_format=arrayio.tab_delimited_format)
    f = file(outfile, 'w')
    arrayio.tab_delimited_format.write(M_c, f)
    f.close()
    assert module_utils.exists_nz(outfile), (
        'the output file %s for convert_signal_to_tdf does not exists'
        % outfile)
    new_objects = get_newobjects(parameters, objects, pipeline)
    module_utils.write_Betsy_parameters_file(parameters, single_object,
                                             pipeline, outfile,starttime,user,jobname)
    return new_objects


def make_unique_hash(identifier, pipeline, parameters):
    return module_utils.make_unique_hash(identifier, pipeline, parameters)


def get_outfile(parameters, objects, pipeline):
    single_object = get_identifier(parameters, objects)
    original_file = module_utils.get_inputid(single_object.identifier)
    filename = 'signal_' + original_file + '.tdf'
    outfile = os.path.join(os.getcwd(), filename)
    return outfile


def get_newobjects(parameters, objects, pipeline):
    outfile = get_outfile(parameters, objects, pipeline)
    single_object = module_utils.find_object(
        parameters, objects, 'input_signal_file', 'contents')
    if single_object:
        parameters = module_utils.renew_parameters(parameters, ['status'])
        attributes = parameters.values()
        new_object = module_utils.DataObject('signal_file',
                                             attributes, outfile)
        new_objects = objects[:]
        new_objects.append(new_object)
        return new_objects
    else:
        single_object = get_identifier(parameters, objects)
        return module_utils.get_newobjects(outfile, 'signal_file',
                                           parameters, objects, single_object)


def get_identifier(parameters, objects):
    single_object = module_utils.find_object(
        parameters, objects, 'input_signal_file', 'contents')
    if not single_object:
        single_object = module_utils.find_object(parameters, objects,
                                                 'signal_file',
                                                 'contents,preprocess')
    assert os.path.exists(single_object.identifier), (
        'the input file %s for convert_signal_to_tdf does not exist'
        % single_object.identifier)
    return single_object


def guess_and_change_gct_header(filename):
    M_name = arrayio.choose_format(filename)
    M = arrayio.read(filename)
    ids = M._row_order
    if not M_name.__name__ == 'arrayio.gct_format':
        return M
    all_platforms = arrayplatformlib.identify_all_platforms_of_matrix(M)
    if not all_platforms:
        return M
    old_header = all_platforms[0][0]
    platform = all_platforms[0][1]
    new_header = platform2header[platform]
    M = module_utils.replace_matrix_header(M, old_header, new_header)
    return M

platform2header = {'Agilent_Human1A':'Probe ID',
                   'HG_U133A_2':'Probe ID',
                   'HG_U133A':'Probe ID',
                   'HG_U133B':'Probe ID',
                   'HG_U133_Plus_2':'Probe ID',
                   'HG_U95A':'Probe ID',
                   'HG_U95Av2':'Probe ID',
                   'Hu35KsubA':'Probe ID',
                   'Hu35KsubB':'Probe ID',
                   'Hu35KsubC':'Probe ID',
                   'Hu35KsubD':'Probe ID',
                   'Hu6800':'Probe ID',
                   'HumanHT_12_control':'Probe ID',
                   'HumanHT_12':'Probe ID',
                   'MG_U74Av2':'Probe ID',
                   'MG_U74Bv2':'Probe ID',
                   'MG_U74Cv2':'Probe ID',
                   'Mouse430_2':'Probe ID',
                   'Mouse430A_2':'Probe ID',
                   'MouseRef_8_control':'Probe ID',
                   'MouseRef_8':'Probe ID',
                   'Mu11KsubA':'Probe ID',
                   'Mu11KsubB':'Probe ID',
                   'RAE230A':'Probe ID',
                   'RG_U34A':'Probe ID',
                   'Entrez_ID_human':'Gene ID',
                   'Entrez_ID_mouse':'Gene ID',
                   'Entrez_symbol_human':'Gene symbol',
                   'Entrez_symbol_mouse':'Gene symbol'}
