#make_heatmap.py
from Betsy.protocol_utils import Parameter
import normalize_file
PRETTY_NAME="Make a heatmap."
COMMON = 'Common Parameters'
NORMALIZE = 'Normalize Parameters'
OPTIONAL = 'Optional Parameters'
ILLUMINA = 'Illumina Normalize Parameters'
CLASS_NEIGHBORS='Class Neighbor Parameters'
CLUSTER = 'Cluster parameters'
CATEGORIES=[COMMON,NORMALIZE,OPTIONAL,ILLUMINA,CLASS_NEIGHBORS,CLUSTER]


#input  datatype
INPUTS = [
    'AgilentFiles',
    'ExpressionFiles',
    'RenameFile',
    'GPRFiles',
    'GEOSeries',
    'IDATFiles',
    'CELFiles',
    '_SignalFile_Postprocess',
    'ClassLabelFile',
    'GeneListFile'
    ]
#output datatype
OUTPUTS = 'Heatmap'


#parameter objects
PARAMETERS=[
    Parameter('format',pretty_name='File Format',default_value='tdf',
                        choices=['tdf', 'gct'],category=COMMON,
                      description='output file format',datatype='SignalFile'),
            Parameter('preprocess',pretty_name='Preprocess',
                         choices=['unknown','rma', 'mas5',
                        'loess', 'illumina', 'agilent',
                        ],category=COMMON,
                         description='preprocess method',datatype='SignalFile'),
            Parameter('missing_values',pretty_name='if has missing value',
                              choices=['no','yes','unknown'],category=COMMON,
                       description='has the missing value or not',datatype='SignalFile'),
            Parameter('missing_algorithm',pretty_name='How to fill missing value',
                      choices=['median_fill','zero_fill'],category=COMMON,
                      description='method to the fill the missing value',datatype='SignalFile'),
            Parameter('logged',pretty_name='Logged or Not',default_value='yes',
                      choices=['no', 'yes'],category=COMMON,
                      description='signal is logged or not',datatype='SignalFile'),
            Parameter('filter',pretty_name='Filter',
                      choices=['yes','no'],default_value='no',
                      category=COMMON,description='filter the missing value or not',
                      datatype='SignalFile'),
            Parameter('quantile_norm',pretty_name='Quantile', 
                     choices=['yes', 'no'],category=NORMALIZE,
                      description='normalize by quanitle',datatype='SignalFile'),
            Parameter('combat_norm',pretty_name='Combat', 
                     choices=['yes', 'no'],category=NORMALIZE,
                      description='normalize by combat',datatype='SignalFile'),
            Parameter('shiftscale_norm',pretty_name='Shiftscale', 
                     choices=['yes', 'no'],category=NORMALIZE,
                      description='normalize by shiftscale',datatype='SignalFile'),
            Parameter('dwd_norm',pretty_name='Dwd', 
                     choices=['yes', 'no'],category=NORMALIZE,
                      description='normalize by dwd',datatype='SignalFile'),
            Parameter('bfrm_norm',pretty_name='BFRM',
                 choices=['yes', 'no'],category=NORMALIZE,
                      description='normalize by bfrm',datatype='SignalFile'),
            Parameter('predataset',pretty_name='Predataset Process',
                       choices=['yes', 'no'],category=COMMON,
                      description='filter and threshold genes',datatype='SignalFile'),
            Parameter('gene_center',pretty_name='Gene Center', 
                        choices=['mean', 'median', 'no','unknown'],
                        category=COMMON,description='gene center method',datatype='SignalFile'),
            Parameter('gene_normalize',pretty_name='Gene Normalize',
                           choices=['variance', 'sum_of_squares', 'no','unknown'],
                           category=COMMON,description='gene normalize method',datatype='SignalFile'),
            Parameter('gene_order',pretty_name='Gene Order',
                 choices=['no', 't_test_p','t_test_fdr','by_class_neighbors','gene_list'],
                      category=NORMALIZE,
                      description='gene order',datatype='SignalFile'),
            Parameter('annotate',pretty_name='Annotation',
                                   choices=['yes','no'],category=OPTIONAL,
                      description='how to annotate the output file',datatype='SignalFile'),
            Parameter('unique_genes',pretty_name='Unique Genes',
                         choices=['average_genes', 'high_var', 'first_gene','no'],
                         category=COMMON,description='how to select unique genes',
                      datatype='SignalFile'),
            Parameter('duplicate_probe',pretty_name='Duplicate Probe',
                      choices=['high_var_probe','closest_probe','no'],
                      category=OPTIONAL,description='how to remove duplicate probe',
                      datatype='SignalFile'),
            Parameter('num_features',pretty_name='Select Gene Number',choices=['yes','no'],
                         category=COMMON,description='select num of genes or not',
                      datatype='SignalFile'),
            Parameter('platform',pretty_name='Platform',choices=['yes','no'],category=OPTIONAL,
                      description='output platform',datatype='SignalFile'),
            
            Parameter('group_fc',pretty_name='Group Fold Change',choices=['yes','no'],
                      category=OPTIONAL,
                      description='filter genes by fold change across classes',datatype='SignalFile'),
            Parameter('rename_sample',pretty_name='Rename samples',choices=['yes','no'],
                      category=OPTIONAL,
                      description='Rename sample name',datatype='SignalFile'),
            
            ###for UserInput
            Parameter('num_factors',pretty_name='Number of Factors',
                           category=OPTIONAL,description='num of factors for bfrm',
                      datatype='UserInput'),
            Parameter('filter_value',pretty_name='Filter missing Value by Percentage',
                           category=OPTIONAL,description='percentage to filter the missing value(0-100)',
                      datatype='UserInput'),
            Parameter('gene_select_threshold',pretty_name='Gene Selection Threshold',
                        category=OPTIONAL,
                      description='gene select threshold',datatype='UserInput'),
            Parameter('platform_name',pretty_name='Platform name',
                  choices = ["'HG_U133_Plus_2'", "'HG_U133B'", "'HG_U133A'",
                 "'HG_U133A_2'", "'HG_U95A'", "'HumanHT_12'", "'HumanWG_6'","'HG_U95Av2'",
                 "'Entrez_ID_human'", "'Entrez_symbol_human'", "'Hu6800'",
                 "'Mouse430A_2'", "'MG_U74Cv2'", "'Mu11KsubB'", "'Mu11KsubA'",
                 "'MG_U74Av2'", "'Mouse430_2'", "'MG_U74Bv2'",
                 "'Entrez_ID_mouse'", "'MouseRef_8'", "'Entrez_symbol_mouse'",
                 "'RG_U34A'", "'RAE230A'", 'unknown_platform'],description = 'output platform name',
                      datatype='UserInput',category=OPTIONAL),
            Parameter('num_features_value',pretty_name='Select Gene Number',
                      category=COMMON,description='select num of genes or not',
                      datatype='UserInput'),
            Parameter('group_fc_num',pretty_name='group_fc value',
                      category=COMMON,description='value for group fold change',
                      datatype='UserInput'),
            
            ###illumina related
            Parameter('ill_manifest', pretty_name='Illumina Manifest File',
                      choices=[
                    'HumanHT-12_V3_0_R2_11283641_A.txt',
                    'HumanHT-12_V4_0_R2_15002873_B.txt',
                    'HumanHT-12_V3_0_R3_11283641_A.txt',
                    'HumanHT-12_V4_0_R1_15002873_B.txt',
                    'HumanMI_V1_R2_XS0000122-MAP.txt',
                    'HumanMI_V2_R0_XS0000124-MAP.txt',
                    'HumanRef-8_V2_0_R4_11223162_A.txt',
                    'HumanRef-8_V3_0_R1_11282963_A_WGDASL.txt',
                    'HumanRef-8_V3_0_R2_11282963_A.txt',
                    'HumanRef-8_V3_0_R3_11282963_A.txt',
                    'HumanWG-6_V2_0_R4_11223189_A.txt',
                    'HumanWG-6_V3_0_R2_11282955_A.txt',
                    'HumanWG-6_V3_0_R3_11282955_A.txt',
                    'MouseMI_V1_R2_XS0000127-MAP.txt',
                    'MouseMI_V2_R0_XS0000129-MAP.txt',
                    'MouseRef-8_V1_1_R4_11234312_A.txt',
                    'MouseRef-8_V2_0_R2_11278551_A.txt',
                    'MouseRef-8_V2_0_R3_11278551_A.txt',
                    'MouseWG-6_V1_1_R4_11234304_A.txt',
                    'MouseWG-6_V2_0_R2_11278593_A.txt',
                    'MouseWG-6_V2_0_R3_11278593_A.txt',
                    'RatRef-12_V1_0_R5_11222119_A.txt'
                    ],category=ILLUMINA,
                      description='Illumina manifest file in tab-delimited (TXT) format',
                      datatype="ILLUFolder"),
            Parameter('ill_chip', pretty_name='Illumina chip File',choices=[
                    'ilmn_HumanHT_12_V3_0_R3_11283641_A.chip',
                    'ilmn_HumanHT_12_V4_0_R1_15002873_B.chip',
                    'ilmn_HumanRef_8_V2_0_R4_11223162_A.chip',
                    'ilmn_HumanReF_8_V3_0_R1_11282963_A_WGDASL.chip',
                    'ilmn_HumanRef_8_V3_0_R3_11282963_A.chip',
                    'ilmn_HumanWG_6_V2_0_R4_11223189_A.chip',
                    'ilmn_HumanWG_6_V3_0_R3_11282955_A.chip',
                    'ilmn_MouseRef_8_V1_1_R4_11234312_A.chip',
                    'ilmn_MouseRef_8_V2_0_R3_11278551_A.chip',
                    'ilmn_MouseWG_6_V1_1_R4_11234304_A.chip',
                    'ilmn_MouseWG_6_V2_0_R3_11278593_A.chip',
                    'ilmn_RatRef_12_V1_0_R5_11222119_A.chip'
                    ], category=ILLUMINA,description='CHIP file to map probes to genes.',
                      datatype="ILLUFolder"),
            Parameter('ill_clm', pretty_name='Illumina clm File',
                     category=ILLUMINA,description='CLM file to map file names to sample names.',
                      datatype="ILLUFolder"),
            Parameter('ill_custom_chip', pretty_name='Illumina Custom Chip File',
                             category=ILLUMINA,
                      description='Other CHIP file to map probes to genes.',datatype="ILLUFolder"),
            Parameter('ill_custom_manifest', pretty_name='Illumina Custom Manifest File',
                                 category=ILLUMINA,
                      description='Other Illumina manifest file in tab-delimited (TXT) format.',
                      datatype="ILLUFolder"),
            Parameter('ill_bg_mode', pretty_name='Illumina Background Mode',
                         choices=['ill_yes', 'ill_no'],category=ILLUMINA,
                      description='Perform background subtraction.',datatype="ILLUFolder"),
            Parameter('ill_coll_mode', pretty_name='Illumina Coll Mode',
                        choices=['none', 'max', 'median'],category=ILLUMINA,
                      description='Collapse probes to genes based on the manifest or CHIP file (if provided).',
                      datatype="ILLUFolder"),
            
            #class neighbors
            Parameter('cn_mean_or_median',pretty_name='cn mean or median',category=CLASS_NEIGHBORS,
                      choices=['mean', 'median'],description='use mean or median for feature selection',
                      datatype='PrettySignalFile'),
            
            Parameter('cn_ttest_or_snr',pretty_name='cn ttest or snr',category=CLASS_NEIGHBORS,
                      choices=['t_test','snr'],description='use signal-to-noise or t-test to select neighbors',
                      datatype='PrettySignalFile'),
            
            Parameter('cn_filter_data',choices=['yes','no'],category=CLASS_NEIGHBORS,
                      pretty_name='cn filter data',description='if no, values below will be ignored',
                      datatype='PrettySignalFile'),

            Parameter('cn_num_neighbors',pretty_name='cn num neighbors',category=CLASS_NEIGHBORS,
                      description='number of neighbors to find',datatype='UserInput'),
            Parameter('cn_num_perm',pretty_name='cn num permutations',category=CLASS_NEIGHBORS,
                      description='number of permutations in permutation test',datatype='UserInput'),
            Parameter('cn_user_pval',pretty_name='cn user pval',category=CLASS_NEIGHBORS,
                      description='user-set significance value for permutation test',datatype='UserInput'),

            Parameter('cn_min_threshold',category=CLASS_NEIGHBORS, pretty_name='cn min threshold',
                      description='minimum threshold for data',datatype='UserInput'),
            Parameter('cn_max_threshold',category=CLASS_NEIGHBORS, pretty_name='cn max threshold',
                     description='maximum threshold for data',datatype='UserInput'), 
            Parameter('cn_min_folddiff',category=CLASS_NEIGHBORS, pretty_name='cn min fold diff',
                     description='minimum fold difference for filtering genes',datatype='UserInput'), 
            Parameter('cn_abs_diff',category=CLASS_NEIGHBORS,pretty_name='cn abs diff',
                     description='minimum absolute difference for filtering genes',datatype='UserInput'),
            #heatmap related
            Parameter('color', pretty_name='Color',choices=['red_green', 'blue_yellow'],
                      category=CLUSTER,description='heatmap color',datatype='Heatmap'),
            Parameter('hm_width', pretty_name='Heatmap Width',
                      category=CLUSTER,description='heatmap width',datatype='Heatmap'),
            Parameter('hm_height', pretty_name='Heatmap Height',category=CLUSTER,
                      description='heatmap height',datatype='Heatmap'),
            Parameter('cluster_alg', pretty_name='Cluster algorithm',default_value='no_cluster_alg',
                        choices=['no_cluster_alg'],category=CLUSTER,
                      description='cluster algorithm',datatype='Heatmap'),
            Parameter('contents',pretty_name='Contents',category=OPTIONAL,
                      choices=["unspecified","train0", "train1", "test", 'class0,class1,test',
                  "class0", "class1", "class0,class1"], description='output group information',
                      datatype='Heatmap'),
            
   ]




    






