# SignalFile
#from Betsy import bie3
from Betsy.bie3 import *

ILLU_MANIFEST = [
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
    ]
ILLU_CHIP = [
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
    ]


GEOSeries = DataType("GEOSeries",
                     AttributeDef("contents",[
                         "train0", "train1","test", "class0,class1,test",
                         "class0", "class1", "class0,class1","unspecified"],
                                  'unspecified','unspecified'))

ExpressionFiles = DataType("ExpressionFiles",
                           AttributeDef("contents",
                                        ["train0","train1", "test",
                                         "class0,class1,test","class0",
                                         "class1", "class0,class1","unspecified"],
                                        'unspecified','unspecified'))

CELFiles = DataType(
    "CELFiles",
    AttributeDef("version", ["unknown", "cc", "v3", "v4"], "unknown", "v3"),
    AttributeDef("contents",["train0","train1", "test",
                             "class0,class1,test","class0",
                              "class1", "class0,class1","unspecified"],
                               'unspecified','unspecified')
    )
RenameFile = DataType(
    'RenameFile',
    AttributeDef("contents",["train0","train1", "test",
                             "class0,class1,test","class0",
                             "class1", "class0,class1","unspecified"],
                             'unspecified','unspecified'))
AgilentFiles = DataType(
    "AgilentFiles",
    AttributeDef("contents",["train0","train1", "test",
                            "class0,class1,test","class0",
                              "class1", "class0,class1","unspecified"],
                              'unspecified','unspecified'))

ControlFile = DataType(
    "ControlFile",
    AttributeDef(
        'preprocess',["illumina"],
        "illumina","illumina"),
    AttributeDef(
        'missing_values',["unknown", "no", "yes"],
        "no","no"),
    AttributeDef(
        "missing_algorithm",["none", "median_fill", "zero_fill"],
        "zero_fill", "zero_fill"),
    AttributeDef(
        "logged",["no"],"no","no"),
    AttributeDef(
        'format',["gct"],
        "gct","gct"),
    AttributeDef("contents",["train0","train1", "test",
                            "class0,class1,test","class0",
                              "class1", "class0,class1","unspecified"],
                              'unspecified','unspecified'))
    
    
GPRFiles = DataType(
    "GPRFiles",
    AttributeDef("contents",["train0","train1", "test",
                            "class0,class1,test","class0",
                              "class1", "class0,class1","unspecified"],
                              'unspecified','unspecified'))

IDATFiles = DataType(
    "IDATFiles",
    AttributeDef("contents",["train0","train1", "test",
                            "class0,class1,test","class0",
                              "class1", "class0,class1","unspecified"],
                              'unspecified','unspecified'))

ClassLabelFile = DataType(
    "ClassLabelFile",
    AttributeDef(
    "contents",["train0", "train1", "test", "class0,class1,test",
                  "class0", "class1", "class0,class1",
                  "unspecified"],'unspecified','unspecified'),
    AttributeDef("cls_format",['cls','label','unknown'],"unknown","cls")
    )

ILLUFolder = DataType(
    "ILLUFolder", 
    AttributeDef(
        "illu_manifest",ILLU_MANIFEST,
        'HumanHT-12_V4_0_R2_15002873_B.txt','HumanHT-12_V4_0_R2_15002873_B.txt'),
    AttributeDef(
        'illu_chip',ILLU_CHIP,
        'ilmn_HumanHT_12_V4_0_R1_15002873_B.chip','ilmn_HumanHT_12_V4_0_R1_15002873_B.chip'),
    AttributeDef('illu_bg_mode',['false', 'true'], "false", "false"),
    AttributeDef('illu_coll_mode',['none', 'max', 'median'], "none","none"),
    AttributeDef("contents",["train0","train1", "test",
                            "class0,class1,test","class0",
                              "class1", "class0,class1","unspecified"],
                              'unspecified','unspecified')
    )


GeneListFile=DataType(
    "GeneListFile", 
    AttributeDef('cn_mean_or_median',['mean', 'median'], 'mean','mean'),
    AttributeDef('cn_ttest_or_snr',['t_test','snr'], 't_test','t_test'),
    AttributeDef('cn_filter_data',['yes','no'], 'no','no'),
    AttributeDef('gene_order',['no', "gene_list", "class_neighbors",
                          "t_test_p", "t_test_fdr"], 'gene_list',"gene_list"),
    AttributeDef("contents",["train0","train1", "test",
                            "class0,class1,test","class0",
                              "class1", "class0,class1","unspecified"],
                              'unspecified','unspecified'))
   
SignalFile_Postprocess = DataType(
    "SignalFile_Postprocess",
    AttributeDef("format", ["unknown", "tdf", "pcl", "gct", "res", "jeffs"],
              "unknown", "tdf"),
    # Properties of the data.
    AttributeDef("preprocess",
              ["unknown", "illumina", "agilent", "mas5", "rma", "loess"],
              "unknown", "unknown"),
    AttributeDef("logged", ["unknown", "no", "yes"], "unknown", "yes"),
    AttributeDef("predataset", ["no", "yes"], "no", "no"),
    AttributeDef("contents", [
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"],
              "unspecified", "unspecified"))

SignalFile_Impute = DataType(
    "SignalFile_Impute",
    # Properties of the data.
    AttributeDef("preprocess",
              ["unknown", "illumina", "agilent", "mas5", "rma", "loess"],
              "unknown", "unknown"),
    AttributeDef("predataset", ["no", "yes"], "no", "no"),
    AttributeDef("missing_values", ["unknown", "no", "yes"], "unknown", "no"),
    AttributeDef("missing_algorithm", ["none", "median_fill", "zero_fill"],
              "zero_fill","zero_fill"),
    AttributeDef("filter", ["no", "yes"], "no", "no"),
    AttributeDef("contents", [
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"],
              "unspecified", "unspecified"))


SignalFile_Merge = DataType(
    "SignalFile_Merge",
    # Properties of the data.
    AttributeDef("preprocess",
              ["unknown", "illumina", "agilent", "mas5", "rma", "loess"],
              "unknown", "unknown"),
    AttributeDef("predataset", ["no", "yes"], "no", "no"),
    AttributeDef("missing_algorithm", ["none", "median_fill", "zero_fill"],
              "zero_fill","zero_fill"),
    AttributeDef("filter", ["no", "yes"], "no", "no"),
    AttributeDef("dwd_norm", ["no", "yes"], "no", "no"),
    AttributeDef("bfrm_norm", ["no", "yes"], "no", "no"),
    AttributeDef("quantile_norm", ["no", "yes"], "no", "no"),
    AttributeDef("shiftscale_norm", ["no", "yes"], "no", "no"),
    AttributeDef("combat_norm", ["no", "yes"], "no", "no"),
    AttributeDef("contents", [
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"],
              "unspecified", "unspecified"))

SignalFile_Normalize = DataType(
    "SignalFile_Normalize",
    # Properties of the data.
    AttributeDef("preprocess",
              ["unknown", "illumina", "agilent", "mas5", "rma", "loess"],
              "unknown", "unknown"),
    AttributeDef("predataset", ["no", "yes"], "no", "no"),
    AttributeDef("missing_algorithm", ["none", "median_fill", "zero_fill"],
              "zero_fill","zero_fill"),
    AttributeDef("format", ["tdf", "pcl"], "tdf", "tdf"),
    AttributeDef("filter", ["no", "yes"], "no", "no"),
    AttributeDef("dwd_norm", ["no", "yes"], "no", "no"),
    AttributeDef("bfrm_norm", ["no", "yes"], "no", "no"),
    AttributeDef("quantile_norm", ["no", "yes"], "no", "no"),
    AttributeDef("shiftscale_norm", ["no", "yes"], "no", "no"),
    AttributeDef("combat_norm", ["no", "yes"], "no", "no"),
    AttributeDef(
        "gene_center", ["unknown", "no", "mean", "median"],
        "unknown", "no"),
    AttributeDef(
        "gene_normalize", ["unknown", "no", "variance", "sum_of_squares"],
        "unknown", "no"),
    AttributeDef("contents", [
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"],
              "unspecified", "unspecified"))    
    
    
    

SignalFile_Order = DataType(
    "SignalFile_Order",
    # Properties of the data.
    AttributeDef("preprocess",
              ["unknown", "illumina", "agilent", "mas5", "rma", "loess"],
              "unknown", "unknown"),
    AttributeDef("missing_algorithm", ["none", "median_fill", "zero_fill"],
              "zero_fill","zero_fill"),
    AttributeDef("filter", ["no", "yes"], "no", "no"),
    # Normalization of the data.
    AttributeDef("dwd_norm", ["no", "yes"], "no", "no"),
    AttributeDef("bfrm_norm", ["no", "yes"], "no", "no"),
    AttributeDef("quantile_norm", ["no", "yes"], "no", "no"),
    AttributeDef("shiftscale_norm", ["no", "yes"], "no", "no"),
    AttributeDef("combat_norm", ["no", "yes"], "no", "no"),
    AttributeDef("predataset", ["no", "yes"], "no", "no"),
    AttributeDef(
        "gene_center", [ "no", "mean", "median"],
        "no", "no"),
    AttributeDef(
        "gene_normalize", [ "no", "variance", "sum_of_squares"],
        "no", "no"),
    AttributeDef(
        "gene_order",
        ["no", "class_neighbors", "gene_list", "t_test_p", "t_test_fdr"],
       "no", "no"),
    AttributeDef("contents", [
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"],
              "unspecified", "unspecified"))

SignalFile_Annotate= DataType( 
    "SignalFile_Annotate",
    # Properties of the data.
    AttributeDef("preprocess",
              ["unknown", "illumina", "agilent", "mas5", "rma", "loess"],
              "unknown", "unknown"),
    AttributeDef("missing_algorithm", ["none", "median_fill", "zero_fill"],
              "zero_fill","zero_fill"),
    AttributeDef("filter", ["no", "yes"], "no", "no"),
    # Normalization of the data.
    AttributeDef("dwd_norm", ["no", "yes"], "no", "no"),
    AttributeDef("bfrm_norm", ["no", "yes"], "no", "no"),
    AttributeDef("quantile_norm", ["no", "yes"], "no", "no"),
    AttributeDef("shiftscale_norm", ["no", "yes"], "no", "no"),
    AttributeDef("combat_norm", ["no", "yes"], "no", "no"),
    AttributeDef("predataset", ["no", "yes"], "no", "no"),
    AttributeDef(
        "gene_center", [ "no", "mean", "median"],
        "no", "no"),
    AttributeDef(
        "gene_normalize", [ "no", "variance", "sum_of_squares"],
        "no", "no"),
    AttributeDef(
        "gene_order",
        ["no", "class_neighbors", "gene_list", "t_test_p", "t_test_fdr"],
       "no", "no"),
    AttributeDef("annotate", ["no", "yes"], "no", "no"),
    AttributeDef("rename_sample", ["no", "yes"], "no", "no"),
    AttributeDef("platform", ["yes","no"], "no", "no"),
    AttributeDef("contents", [
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"],
              "unspecified", "unspecified"))

SignalFile= DataType( 
    "SignalFile",
    # Properties of the data.
    AttributeDef("preprocess",
              ["unknown", "illumina", "agilent", "mas5", "rma", "loess"],
              "unknown", "unknown"),
    AttributeDef("missing_algorithm", ["none", "median_fill", "zero_fill"],
              "zero_fill","zero_fill"),
    AttributeDef("filter", ["no", "yes"], "no", "no"),
    # Normalization of the data.
    AttributeDef("dwd_norm", ["no", "yes"], "no", "no"),
    AttributeDef("bfrm_norm", ["no", "yes"], "no", "no"),
    AttributeDef("quantile_norm", ["no", "yes"], "no", "no"),
    AttributeDef("shiftscale_norm", ["no", "yes"], "no", "no"),
    AttributeDef("combat_norm", ["no", "yes"], "no", "no"),
    AttributeDef("predataset", ["no", "yes"], "no", "no"),
    AttributeDef(
        "gene_center", [ "no", "mean", "median"],
        "no", "no"),
    AttributeDef(
        "gene_normalize", [ "no", "variance", "sum_of_squares"],
        "no", "no"),
    AttributeDef(
        "gene_order",
        ["no", "class_neighbors", "gene_list", "t_test_p", "t_test_fdr"],
       "no", "no"),
    AttributeDef("annotate", ["no", "yes"], "no", "no"),
    AttributeDef("rename_sample", ["no", "yes"], "no", "no"),
    AttributeDef("platform", ["yes","no"], "no", "no"),
    AttributeDef("num_features", ["yes","no"], "no", "no"),
    AttributeDef(
        "unique_genes", ["no", "average_genes", "high_var", "first_gene"],
        "no", "no"),
    AttributeDef(
        "duplicate_probe", ["no", "closest_probe", "high_var_probe"],
        "no", "no"),
    AttributeDef("group_fc", ["yes","no"], "no","no"),
    AttributeDef("contents", [
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"],
              "unspecified", "unspecified"),
    AttributeDef("logged", [ "no", "yes"], "yes", "yes"),
    AttributeDef("format", [ "tdf", "gct"], "tdf", "tdf"),)

    

all_modules = [
    Module(
        "download_geo", GEOSeries, ExpressionFiles,
         UserInputDef("GSEID"), UserInputDef("GPLID",""),
         Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
         Consequence("contents",SAME_AS_CONSTRAINT),
        ),
    #CELFiles
    Module(
        "extract_CEL_files", ExpressionFiles, CELFiles,
         Consequence("version", SET_TO, "unknown"),
         Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
         Consequence("contents",SAME_AS_CONSTRAINT),
        ),
    Module(
        "detect_CEL_version",
        CELFiles, CELFiles,
        Constraint("version", MUST_BE, "unknown"),
        Consequence("version", BASED_ON_DATA, ["cc", "v3", "v4"]),
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
        Consequence("contents",SAME_AS_CONSTRAINT),
        ),
    Module(
        "convert_CEL_cc_to_CEL_v3",
        CELFiles, CELFiles,
        Constraint("version", MUST_BE, "cc"),
        Consequence("version", SET_TO, "v3"),
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
         Consequence("contents",SAME_AS_CONSTRAINT),
        ),
     # IDATFiles
    Module("extract_illumina_idat_files",
            ExpressionFiles, IDATFiles,
           Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
         Consequence("contents",SAME_AS_CONSTRAINT),),
    Module(
        "preprocess_illumina",
        IDATFiles, ILLUFolder,
        Consequence('illu_manifest',SET_TO_ONE_OF,ILLU_MANIFEST),
        Consequence('illu_chip',SET_TO_ONE_OF,ILLU_CHIP),
        Consequence('illu_bg_mode',SET_TO_ONE_OF,["false", "true"]),
        Consequence('illu_coll_mode',SET_TO_ONE_OF,["none", "max", "median"]),
        UserInputDef("illu_clm",''),
        UserInputDef("illu_custom_chip",''),
        UserInputDef("illu_custom_manifest",''),
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
        Consequence("contents",SAME_AS_CONSTRAINT),
        ),
       Module(
        "get_illumina_signal",
         ILLUFolder, SignalFile_Postprocess,
         Consequence('preprocess',SET_TO,"illumina"),
         Consequence('format', SET_TO, "gct"),
         Consequence('logged', SET_TO, "no"),
         Consequence('predataset', SET_TO, "no"),
         Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
         Consequence("contents",SAME_AS_CONSTRAINT),),
    Module(
        "get_illumina_control",
         ILLUFolder,ControlFile,
         Consequence('preprocess',SET_TO,"illumina"),
         Consequence("format",SET_TO,"gct"),
         Consequence("logged",SET_TO,"no"),
         Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
         Consequence("contents",SAME_AS_CONSTRAINT), 
        ),
    
    # AgilentFiles
    Module(
        "extract_agilent_files", ExpressionFiles, AgilentFiles,
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
         Consequence("contents",SAME_AS_CONSTRAINT)),
    Module(
        "preprocess_agilent",
         AgilentFiles,SignalFile_Postprocess,
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
        Consequence("contents",SAME_AS_CONSTRAINT),
        Consequence('logged',SET_TO,"unknown"),
        Consequence('predataset', SET_TO, "no"),
        Consequence('preprocess',SET_TO,"agilent"),
        Consequence('format',SET_TO,"tdf")),

    # GPRFiles
    Module(
        "extract_gpr_files", ExpressionFiles, GPRFiles,
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
         Consequence("contents",SAME_AS_CONSTRAINT)),
    Module(
        "normalize_with_loess",
        GPRFiles,SignalFile_Postprocess,
        Consequence("format",SET_TO,"tdf"),
        Consequence("logged",SET_TO,"unknown"),
        Consequence('predataset', SET_TO, "no"),
        Consequence("preprocess",SET_TO,"loess"),
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
         Consequence("contents",SAME_AS_CONSTRAINT)),
    
    Module(
        "preprocess_rma",
        CELFiles, SignalFile_Postprocess,
        Constraint("version", CAN_BE_ANY_OF, ["v3", "v4"]),
        Consequence("logged", SET_TO, "yes"),
        Consequence("preprocess", SET_TO, "rma"),
        Consequence("format", SET_TO, "jeffs"),
        Consequence('predataset', SET_TO, "no"),
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
         Consequence("contents",SAME_AS_CONSTRAINT),
        ),
    Module(
        "preprocess_mas5",
        CELFiles, SignalFile_Postprocess,
        Constraint("version", CAN_BE_ANY_OF, ["v3", "v4"]),
        Consequence("logged", SET_TO, "no"),
        Consequence("preprocess", SET_TO, "mas5"),
        Consequence('predataset', SET_TO, "no"),
        Consequence("format", SET_TO, "jeffs"),
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"]),
         Consequence("contents",SAME_AS_CONSTRAINT),
        ),
    ####postprocess
    Module(
        "convert_signal_to_tdf",
        SignalFile_Postprocess, SignalFile_Postprocess,
        Constraint("format", CAN_BE_ANY_OF, ["unknown", "pcl", "gct", "res", "jeffs"]),
        Consequence("format", SET_TO, "tdf")
        ),
    Module(
        "check_for_log",
        SignalFile_Postprocess, SignalFile_Postprocess,
        Constraint("format", MUST_BE, "tdf"),
        Constraint("logged", MUST_BE, "unknown"),
        Consequence("format", SAME_AS_CONSTRAINT),
        Consequence("logged", BASED_ON_DATA, ["yes", "no"]),
        ),
    Module(
        "filter_and_threshold_genes",
        SignalFile_Postprocess,SignalFile_Postprocess,
        Constraint('format',MUST_BE,"tdf"),
        Constraint('logged',MUST_BE,"no"),
        Constraint('predataset',MUST_BE,"no"),
        Consequence('format',SAME_AS_CONSTRAINT),
        Consequence('logged',SAME_AS_CONSTRAINT),
        Consequence('predataset',SET_TO,'yes')),
    Module(
        "log_signal",
        SignalFile_Postprocess, SignalFile_Postprocess,
        Constraint("format", MUST_BE, "tdf"),
        Constraint("logged", MUST_BE, "no"),
        Consequence("format", SAME_AS_CONSTRAINT),
        Consequence("logged", SET_TO, "yes")),
    
    #impute
    Module(
        "convert_postprocess_impute",
        SignalFile_Postprocess, SignalFile_Impute,
        Constraint("format", MUST_BE,"tdf"),
        Constraint("logged", MUST_BE,"yes"),
        Constraint("preprocess",
            CAN_BE_ANY_OF,
            ["unknown", "illumina", "agilent", "mas5", "rma", "loess"]),
        Constraint("contents", CAN_BE_ANY_OF,
            ["train0", "train1", "test", "class0", "class1",
             "class0,class1","class0,class1,test", "unspecified"]),
        Constraint("predataset", CAN_BE_ANY_OF, ["no", "yes"]),
        Consequence("contents", SAME_AS_CONSTRAINT),
        Consequence("preprocess", SAME_AS_CONSTRAINT),
        Consequence("predataset", SAME_AS_CONSTRAINT),
        Consequence("missing_algorithm",SET_TO, 'zero_fill'),
        Consequence("missing_values", SET_TO, "unknown"),
        Consequence("filter", SET_TO, 'no')),
        
    Module(
        "check_for_missing_values",
        SignalFile_Impute, SignalFile_Impute,
        Constraint("missing_values", MUST_BE, "unknown"),
        Consequence("missing_values", BASED_ON_DATA, ["no", "yes"]),
        ),
    
    Module(
        "filter_genes_by_missing_values",
        SignalFile_Impute, SignalFile_Impute,
        UserInputDef("filter_value", 0.50),
        Constraint("missing_values", MUST_BE, "yes"),
        Constraint("filter", MUST_BE, "no"),
        Consequence("missing_values", SAME_AS_CONSTRAINT),
        Consequence("filter", SET_TO, "yes"),
        ),
    Module(
        "fill_missing_with_zeros",
        SignalFile_Impute, SignalFile_Impute,
        Constraint("missing_values", MUST_BE, "yes"),
        Consequence("missing_values", SET_TO, "no"),
        Consequence(
            "missing_algorithm", SET_TO, "zero_fill", side_effect=True),
        ),
    Module(
        "fill_missing_with_median",
        SignalFile_Impute,SignalFile_Impute,
        Constraint('missing_values',MUST_BE,'yes'),
        Consequence('missing_algorithm',SET_TO,"median_fill",side_effect=True),
        Consequence('missing_values',SET_TO,'no')),
    #merge
    Module(
        "convert_impute_merge",
        SignalFile_Impute, SignalFile_Merge,
        Constraint("preprocess",
            CAN_BE_ANY_OF,
            ["unknown", "illumina", "agilent", "mas5", "loess"]),
        Constraint("contents", CAN_BE_ANY_OF,
            ["train0", "train1", "test", "class0", "class1",
             "class0,class1","class0,class1,test", "unspecified"]),
        Constraint("predataset", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("filter",CAN_BE_ANY_OF,["no", "yes"]),
        Constraint("missing_values",MUST_BE,"no"),
        Constraint("missing_algorithm",CAN_BE_ANY_OF,['none','zero_fill','median_fill']),
        Consequence("contents", SAME_AS_CONSTRAINT),
        Consequence("preprocess", SAME_AS_CONSTRAINT),
        Consequence("predataset", SAME_AS_CONSTRAINT),
        Consequence("missing_algorithm",SAME_AS_CONSTRAINT),
        Consequence("filter", SAME_AS_CONSTRAINT),
        Consequence("quantile_norm", SET_TO,'no'),
        Consequence("dwd_norm", SET_TO,'no'),
        Consequence("combat_norm", SET_TO,'no'),
        Consequence("bfrm_norm",SET_TO,'no'),
        Consequence("shiftscale_norm", SET_TO,'no')),
    Module(
        "convert_impute_merge",
        SignalFile_Impute, SignalFile_Merge,
        Constraint("preprocess",
            MUST_BE,"rma"),
        Constraint("contents", CAN_BE_ANY_OF,
            ["train0", "train1", "test", "class0", "class1",
             "class0,class1","class0,class1,test", "unspecified"]),
        Constraint("predataset", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("filter",CAN_BE_ANY_OF,["no", "yes"]),
        Constraint("missing_values",MUST_BE,"no"),
        Constraint("missing_algorithm",CAN_BE_ANY_OF,['none','zero_fill','median_fill']),
        Consequence("contents", SAME_AS_CONSTRAINT),
        Consequence("preprocess", SAME_AS_CONSTRAINT),
        Consequence("predataset", SAME_AS_CONSTRAINT),
        Consequence("missing_algorithm",SAME_AS_CONSTRAINT),
        Consequence("filter", SAME_AS_CONSTRAINT),
        Consequence("quantile_norm", SET_TO,'yes'),
        Consequence("dwd_norm", SET_TO,'no'),
        Consequence("combat_norm", SET_TO,'no'),
        Consequence("bfrm_norm",SET_TO,'no'),
        Consequence("shiftscale_norm", SET_TO,'no')),
    
    Module(  
        "merge_two_classes", [SignalFile_Merge, SignalFile_Merge], SignalFile_Merge,  
         Constraint("contents", MUST_BE, "class0", 0),
         Constraint("combat_norm",MUST_BE,'no',0),
         Constraint("quantile_norm",MUST_BE,'no',0), 
         Constraint("dwd_norm",MUST_BE,"no",0),
         Constraint("bfrm_norm",MUST_BE,"no",0),
         Constraint("shiftscale_norm",MUST_BE,"no",0),
         Constraint("contents", MUST_BE, "class1", 1),
         Constraint("combat_norm",MUST_BE,'no',1),
         Constraint("quantile_norm",MUST_BE,"no",1),
         Constraint("dwd_norm",MUST_BE,"no",1),
         Constraint("bfrm_norm",MUST_BE,"no",1),
         Constraint("shiftscale_norm",MUST_BE,"no",1),
         Consequence("contents", SET_TO, "class0,class1"),
         
         Consequence("combat_norm",SAME_AS_CONSTRAINT,0),
         Consequence("quantile_norm",SAME_AS_CONSTRAINT,0),
         Consequence("dwd_norm",SAME_AS_CONSTRAINT,0),
         Consequence("bfrm_norm",SAME_AS_CONSTRAINT,0),
         Consequence("shiftscale_norm",SAME_AS_CONSTRAINT,0),
         DefaultAttributesFrom(0),
         DefaultAttributesFrom(1),
        ),
        Module(
        "normalize_samples_with_quantile",
        SignalFile_Merge, SignalFile_Merge,
        Constraint("quantile_norm", MUST_BE, "no"),
        Consequence("quantile_norm", SET_TO, "yes"),
        ),
    Module(
        "normalize_samples_with_bfrm",
        SignalFile_Merge,SignalFile_Merge,
        UserInputDef("num_factors",1),
        Constraint('bfrm_norm',MUST_BE,"no"),
        Consequence('bfrm_norm',SET_TO,'yes')),

    Module(
        "normalize_samples_with_combat",  
        [ClassLabelFile,SignalFile_Merge],SignalFile_Merge,
        Constraint("cls_format",MUST_BE,'cls',0),
        Constraint("combat_norm",MUST_BE,"no",1),
        Consequence("combat_norm",SET_TO,"yes"),
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"],0),
        Constraint("contents",SAME_AS,0,1),
        Consequence("contents", SAME_AS_CONSTRAINT,0),
        DefaultAttributesFrom(1)),
           
    Module(
        "normalize_samples_with_dwd",  
        [ClassLabelFile,SignalFile_Merge],SignalFile_Merge,
        Constraint("cls_format",MUST_BE,'cls',0),
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"],0),
        Constraint("dwd_norm",MUST_BE,"no",1),
        Consequence("dwd_norm",SET_TO,"yes"),
        Constraint("contents",SAME_AS,0,1),
        Consequence("contents", SAME_AS_CONSTRAINT,0),
        DefaultAttributesFrom(1),),

    Module(
        "normalize_samples_with_shiftscale",  
        [ClassLabelFile,SignalFile_Merge],SignalFile_Merge,
        Constraint("cls_format",MUST_BE,'cls',0),
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"],0),
        Constraint("shiftscale_norm",MUST_BE,"no",1),
        Consequence("shiftscale_norm",SET_TO,"yes"),
        Constraint("contents",SAME_AS,0,1),
        Consequence("contents", SAME_AS_CONSTRAINT,0),
        DefaultAttributesFrom(1)),
    ###normalize
    Module(
        "convert_merge_normalize",
        SignalFile_Merge, SignalFile_Normalize,
        Constraint("preprocess",
            CAN_BE_ANY_OF,
            ["unknown", "illumina", "agilent", "mas5", "rma", "loess"]),
        Constraint("contents", CAN_BE_ANY_OF,
            ["train0", "train1", "test", "class0", "class1",
             "class0,class1","class0,class1,test", "unspecified"]),
        Constraint("predataset", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("filter",CAN_BE_ANY_OF,["no", "yes"]),
        Constraint("missing_algorithm",CAN_BE_ANY_OF,['none','zero_fill','median_fill']),
        Consequence("contents", SAME_AS_CONSTRAINT),
        Consequence("preprocess", SAME_AS_CONSTRAINT),
        Consequence("predataset", SAME_AS_CONSTRAINT),
        Consequence("missing_algorithm",SAME_AS_CONSTRAINT),
        Consequence("filter", SAME_AS_CONSTRAINT),
        Constraint("quantile_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("combat_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("shiftscale_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("bfrm_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("dwd_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Consequence("quantile_norm", SAME_AS_CONSTRAINT),
        Consequence("dwd_norm", SAME_AS_CONSTRAINT),
        Consequence("combat_norm", SAME_AS_CONSTRAINT),
        Consequence("bfrm_norm",SAME_AS_CONSTRAINT),
        Consequence("shiftscale_norm", SAME_AS_CONSTRAINT),
        Consequence("gene_center", SET_TO,'unknown'),
        Consequence("gene_normalize", SET_TO,'unknown'),
        Consequence("format", SET_TO,'tdf'),
        ),
    Module(
        "check_gene_center",
        SignalFile_Normalize,SignalFile_Normalize,
        Constraint("format",MUST_BE,'tdf'),
        Constraint("gene_center",MUST_BE,"unknown"),
        Constraint("gene_normalize", MUST_BE, "unknown"),
        Consequence("format", SAME_AS_CONSTRAINT),
        Consequence("gene_center",BASED_ON_DATA,["no", "mean", "median"]),
        Consequence("gene_normalize", SAME_AS_CONSTRAINT)),
        
    Module(
        "check_gene_normalize",
        SignalFile_Normalize,SignalFile_Normalize,
        Constraint("format",MUST_BE,'tdf'),
        Constraint("gene_normalize",MUST_BE,"unknown"),
        Consequence("format", SAME_AS_CONSTRAINT),
        Consequence(
            "gene_normalize", BASED_ON_DATA,
            ["no", "variance", "sum_of_squares"])),
        
    Module(   
        "convert_signal_to_pcl",
        SignalFile_Normalize,SignalFile_Normalize,
        Constraint("format",MUST_BE,'tdf'),
        Consequence("format",SET_TO,'pcl')),
    
    Module(
        "center_genes",
        SignalFile_Normalize,SignalFile_Normalize,
        Constraint("format",MUST_BE,"pcl"),
        Constraint("gene_center",MUST_BE,"no"),
        Constraint("gene_normalize",MUST_BE,'unknown'),
        Consequence("format",SET_TO,"tdf"),
        Consequence("gene_center",SET_TO_ONE_OF,["mean", "median"]),
        Consequence("gene_normalize",SAME_AS_CONSTRAINT)),
    
    Module(
        "normalize_genes",
        SignalFile_Normalize,SignalFile_Normalize,
        Constraint("format",MUST_BE,"pcl"),
        Constraint("gene_normalize",MUST_BE,"no"),
        Consequence("format",SET_TO,"tdf"),
        Consequence("gene_normalize",SET_TO_ONE_OF,["variance", "sum_of_squares"])),
    ##Order
    Module(
        "convert_normalize_order",
        SignalFile_Normalize, SignalFile_Order,
        Constraint("preprocess",
            CAN_BE_ANY_OF,
            ["unknown", "illumina", "agilent", "mas5", "rma", "loess"]),
        Constraint("contents", CAN_BE_ANY_OF,
            ["train0", "train1", "test", "class0", "class1",
             "class0,class1","class0,class1,test", "unspecified"]),
        Constraint("predataset", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("filter",CAN_BE_ANY_OF,["no", "yes"]),
        Constraint("missing_algorithm",CAN_BE_ANY_OF,['none','zero_fill','median_fill']),
        Constraint("format",MUST_BE,'tdf'),
        Consequence("contents", SAME_AS_CONSTRAINT),
        Consequence("preprocess", SAME_AS_CONSTRAINT),
        Consequence("predataset", SAME_AS_CONSTRAINT),
        Consequence("missing_algorithm",SAME_AS_CONSTRAINT),
        Consequence("filter", SAME_AS_CONSTRAINT),
        Constraint("quantile_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("combat_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("shiftscale_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("bfrm_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("dwd_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("gene_center", CAN_BE_ANY_OF, ["no", "median","mean"]),
        Constraint("gene_normalize", CAN_BE_ANY_OF, ["no", "variance","sum_of_squares"]),
        Consequence("quantile_norm", SAME_AS_CONSTRAINT),
        Consequence("dwd_norm", SAME_AS_CONSTRAINT),
        Consequence("combat_norm", SAME_AS_CONSTRAINT),
        Consequence("bfrm_norm",SAME_AS_CONSTRAINT),
        Consequence("shiftscale_norm", SAME_AS_CONSTRAINT),
        Consequence("gene_center", SAME_AS_CONSTRAINT),
        Consequence("gene_normalize", SAME_AS_CONSTRAINT),
        Consequence("gene_order", SET_TO,'no'),
        ),


    Module(  
        "rank_genes_by_class_neighbors",
        [ClassLabelFile,SignalFile_Order],GeneListFile,
        UserInputDef("cn_num_neighbors",50),
        UserInputDef("cn_num_perm",100),
        UserInputDef("cn_user_pval",0.5),
        UserInputDef("cn_min_threshold",10),
        UserInputDef("cn_max_threshold",16000),
        UserInputDef("cn_min_folddiff",5),
        UserInputDef("cn_abs_diff",50),
        Constraint("cls_format", MUST_BE,'cls',0),
        Constraint(
            "contents", CAN_BE_ANY_OF,
            ["train0", "train1", "test", "class0", "class1",
             "class0,class1","class0,class1,test", "unspecified"],0),
        Constraint("contents",SAME_AS,0,1),
        Constraint("gene_order", MUST_BE,"no",1),
        Consequence("gene_order",SET_TO,"class_neighbors"),
        Consequence("cn_mean_or_median",SET_TO_ONE_OF, ['mean', 'median']),
        Consequence("cn_ttest_or_snr",SET_TO_ONE_OF, ['t_test','snr']),
        Consequence("cn_filter_data",SET_TO_ONE_OF, ['yes','no']),
        Consequence("contents",SAME_AS_CONSTRAINT,0),
        ),
    
    Module(
        "rank_genes_by_sample_ttest",
        [ClassLabelFile, SignalFile_Order], GeneListFile,
        UserInputDef("gene_select_threshold", 0.05),
        Constraint("cls_format", MUST_BE, 'cls', 0),
        Constraint("gene_order", MUST_BE, "no", 1),
        Constraint(
            "contents", CAN_BE_ANY_OF,
            ["train0", "train1", "test", "class0", "class1",
             "class0,class1","class0,class1,test", "unspecified"],0),
        Constraint("contents",SAME_AS,0,1),
        Consequence("gene_order",SET_TO_ONE_OF, ["t_test_p", "t_test_fdr"]),
        Consequence("contents",SAME_AS_CONSTRAINT,0),
       ),
         
    Module(  
         "reorder_genes",  
         [GeneListFile,SignalFile_Order], SignalFile_Order,
         Constraint("gene_order", CAN_BE_ANY_OF, ['t_test_p', "t_test_fdr",
                                   'class_neighbors', "gene_list"],0),
         Constraint("gene_order", MUST_BE,"no",1),
         Constraint(
            "preprocess", CAN_BE_ANY_OF,
            ["unknown", "illumina", "agilent", "mas5", "rma", "loess"], 1),
         Constraint(
            "contents", CAN_BE_ANY_OF,
            ["train0", "train1", "test", "class0", "class1",
             "class0,class1","class0,class1,test", "unspecified"],0),
         Constraint("contents",SAME_AS,0,1),
         Constraint("gene_center",CAN_BE_ANY_OF,['median','mean','no'],1),
         Constraint("gene_normalize",CAN_BE_ANY_OF,['sum_of_squares','variance','no'],1),
         Consequence("gene_center",SAME_AS_CONSTRAINT,1),
         Consequence("gene_normalize",SAME_AS_CONSTRAINT,1),
         Consequence("gene_order",SAME_AS_CONSTRAINT,0),
         Consequence("preprocess", SAME_AS_CONSTRAINT, 1),
         Consequence("contents",SAME_AS_CONSTRAINT,0),
         
         DefaultAttributesFrom(1),
        ),
    ##Annotate
    Module(
        "convert_order_annotate",
        SignalFile_Order, SignalFile_Annotate,
        Constraint("preprocess",
            CAN_BE_ANY_OF,
            ["unknown", "illumina", "agilent", "mas5", "rma", "loess"]),
        Constraint("contents", CAN_BE_ANY_OF,
            ["train0", "train1", "test", "class0", "class1",
             "class0,class1","class0,class1,test", "unspecified"]),
        Constraint("predataset", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("filter",CAN_BE_ANY_OF,["no", "yes"]),
        Constraint("missing_algorithm",CAN_BE_ANY_OF,['none','zero_fill','median_fill']),
        Consequence("contents", SAME_AS_CONSTRAINT),
        Consequence("preprocess", SAME_AS_CONSTRAINT),
        Consequence("predataset", SAME_AS_CONSTRAINT),
        Consequence("missing_algorithm",SAME_AS_CONSTRAINT),
        Consequence("filter", SAME_AS_CONSTRAINT),
        Constraint("quantile_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("combat_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("shiftscale_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("bfrm_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("dwd_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("gene_center", CAN_BE_ANY_OF, ["no", "median","mean"]),
        Constraint("gene_normalize", CAN_BE_ANY_OF, ["no", "variance","sum_of_squares"]),
        Constraint("gene_order", CAN_BE_ANY_OF,["no",'t_test_p', "t_test_fdr",
                                   'class_neighbors', "gene_list"]),
        Consequence("dwd_norm", SAME_AS_CONSTRAINT),
        Consequence("combat_norm", SAME_AS_CONSTRAINT),
        Consequence("bfrm_norm",SAME_AS_CONSTRAINT),
        Consequence("shiftscale_norm", SAME_AS_CONSTRAINT),
        Consequence("quantile_norm", SAME_AS_CONSTRAINT),
        Consequence("gene_center", SAME_AS_CONSTRAINT),
        Consequence("gene_normalize", SAME_AS_CONSTRAINT),
        Consequence("gene_order",SAME_AS_CONSTRAINT),
        Consequence("annotate",SET_TO,"no"),
        Consequence("rename_sample",SET_TO,"no"),
        Consequence("platform",SET_TO,"no"),
        ),
    Module(
         'annotate_probes',
         SignalFile_Annotate,SignalFile_Annotate,
         Constraint("annotate", MUST_BE,"no"),
         Constraint("platform", MUST_BE,"no"),
         Consequence("annotate",SET_TO,"yes"),
         Consequence("platform",SAME_AS_CONSTRAINT)),
    Module( 
       "relabel_samples",  
        [RenameFile,SignalFile_Annotate],SignalFile_Annotate,
         Constraint("rename_sample",MUST_BE,"no",1),
         Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"],0),
         Constraint("contents",SAME_AS,0,1),
         Consequence("rename_sample",SET_TO,"yes"),
         Consequence("contents", SAME_AS_CONSTRAINT,0),
         DefaultAttributesFrom(1),
       ),
    Module(
         'add_crossplatform_probeid',
         SignalFile_Annotate,SignalFile_Annotate,
         UserInputDef("platform_name"),
         Constraint("platform", MUST_BE,"no"),
         Consequence("platform",SET_TO,"yes")),
    
    #Filter
    Module(
        "convert_annotate_filter",
        SignalFile_Annotate, SignalFile,
        Constraint("preprocess",
            CAN_BE_ANY_OF,
            ["unknown", "illumina", "agilent", "mas5", "rma", "loess"]),
        Constraint("contents", CAN_BE_ANY_OF,
            ["train0", "train1", "test", "class0", "class1",
             "class0,class1","class0,class1,test", "unspecified"]),
        Constraint("predataset", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("filter",CAN_BE_ANY_OF,["no", "yes"]),
        Constraint("missing_algorithm",CAN_BE_ANY_OF,['none','zero_fill','median_fill']),
        Consequence("contents", SAME_AS_CONSTRAINT),
        Consequence("preprocess", SAME_AS_CONSTRAINT),
        Consequence("predataset", SAME_AS_CONSTRAINT),
        Consequence("missing_algorithm",SAME_AS_CONSTRAINT),
        Consequence("filter", SAME_AS_CONSTRAINT),
        Constraint("quantile_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("combat_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("shiftscale_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("bfrm_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("dwd_norm", CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("gene_center", CAN_BE_ANY_OF, ["no", "median","mean"]),
        Constraint("gene_normalize", CAN_BE_ANY_OF, ["no", "variance","sum_of_squares"]),
        Constraint("gene_order", CAN_BE_ANY_OF,["no",'t_test_p', "t_test_fdr",
                                   'class_neighbors', "gene_list"]),
        Constraint("annotate",CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("rename_sample",CAN_BE_ANY_OF, ["no", "yes"]),
        Constraint("platform",CAN_BE_ANY_OF, ["no", "yes"]),
        Consequence("dwd_norm", SAME_AS_CONSTRAINT),
        Consequence("combat_norm", SAME_AS_CONSTRAINT),
        Consequence("bfrm_norm",SAME_AS_CONSTRAINT),
        Consequence("shiftscale_norm", SAME_AS_CONSTRAINT),
        Consequence("quantile_norm", SAME_AS_CONSTRAINT),
        Consequence("combat_norm", SAME_AS_CONSTRAINT),
        Consequence("bfrm_norm",SAME_AS_CONSTRAINT),
        Consequence("shiftscale_norm", SAME_AS_CONSTRAINT),
        Consequence("gene_center", SAME_AS_CONSTRAINT),
        Consequence("gene_normalize", SAME_AS_CONSTRAINT),
        Consequence("gene_order",SAME_AS_CONSTRAINT),
        Consequence("annotate",SAME_AS_CONSTRAINT),
        Consequence("rename_sample",SAME_AS_CONSTRAINT),
        Consequence("platform",SAME_AS_CONSTRAINT),
        Consequence("logged",SET_TO,"yes"),
        Consequence("format",SET_TO,"tdf"),
        Consequence("num_features",SET_TO,"no"),
        Consequence("unique_genes",SET_TO,"no"),
        Consequence("duplicate_probe",SET_TO,"no"),
        Consequence("group_fc",SET_TO,"no"),
        ),
    Module(
        'remove_duplicate_genes',
        SignalFile, SignalFile,
        Constraint("annotate", MUST_BE,"yes"),
        Constraint("num_features", MUST_BE,"no"),
        Constraint("duplicate_probe", MUST_BE,'no'),
        Constraint("unique_genes", MUST_BE,'no'),
        Consequence("annotate", SAME_AS_CONSTRAINT),
        Consequence("num_features", SAME_AS_CONSTRAINT),
        Consequence("duplicate_probe", SAME_AS_CONSTRAINT),
        Consequence(
            "unique_genes", SET_TO_ONE_OF,
            ['average_genes', 'high_var', 'first_gene'])),
      
    Module(
         'select_first_n_genes',
        SignalFile,SignalFile,
        UserInputDef("num_features_value",500),
        Constraint("num_features", MUST_BE,"no"),
        Constraint("duplicate_probe", MUST_BE,'no'),
        Consequence("num_features",SET_TO,"yes"),
        Consequence("duplicate_probe",SAME_AS_CONSTRAINT)), 
      
     Module(
        'remove_duplicate_probes',
        SignalFile,SignalFile,
        Constraint("duplicate_probe", MUST_BE,'no'),
        Consequence("duplicate_probe",SET_TO,'high_var_probe'),
        Constraint("platform", MUST_BE,"yes"),
        Consequence("platform",SAME_AS_CONSTRAINT)),
    Module(
         'select_probe_by_best_match',
        SignalFile,SignalFile,
        Constraint("duplicate_probe", MUST_BE,'no'),
        Consequence("duplicate_probe",SET_TO,'closest_probe'),
        Constraint("platform", MUST_BE,"yes"),
        Consequence("platform",SAME_AS_CONSTRAINT)),
    
    Module(
        "filter_genes_by_fold_change_across_classes",
        [ClassLabelFile,SignalFile],SignalFile,
        UserInputDef("group_fc_num"),
        Constraint("cls_format", MUST_BE,'cls',0),
        Constraint("group_fc", MUST_BE,"no",1),
        Constraint("num_features", MUST_BE,"no",1),
        Constraint("duplicate_probe", MUST_BE,"no",1),
        Constraint("unique_genes", MUST_BE,"no",1),
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"],0),
        Constraint("contents",SAME_AS,0,1),
        Consequence("contents",SAME_AS_CONSTRAINT,0),
        Consequence("num_features",SAME_AS_CONSTRAINT,1),
        Consequence("duplicate_probe",SAME_AS_CONSTRAINT,1),
        Consequence("unique_genes",SAME_AS_CONSTRAINT,1),
        Consequence("group_fc",SET_TO,"yes"),
        DefaultAttributesFrom(1),),
    Module(   
        "convert_signal_to_gct",
        SignalFile,SignalFile,
        Constraint("format",MUST_BE,'tdf'),
        Consequence("format",SET_TO,'gct')),
    Module( 
        'unlog_signal',
        SignalFile,SignalFile,
        Constraint("format", MUST_BE,"tdf"),
        Constraint("logged", MUST_BE,"yes"),
        Consequence("format",SAME_AS_CONSTRAINT),
        Consequence("logged",SET_TO,"no")),
    
    Module(
        "convert_label_to_cls",   
        [ClassLabelFile,SignalFile_Impute],ClassLabelFile,
        Constraint("cls_format",MUST_BE,'label',0),
        Constraint("contents",CAN_BE_ANY_OF,[
        "unspecified", "train0", "train1", "test", 'class0,class1,test',
        "class0", "class1", "class0,class1"],0),
        Constraint("contents",SAME_AS,0,1),
        Consequence("contents", SAME_AS_CONSTRAINT,0),
        Consequence("cls_format",SET_TO,'cls'),
        )

    ]

list_files=[RenameFile,AgilentFiles,CELFiles,ControlFile,ExpressionFiles,
            GPRFiles,GEOSeries,IDATFiles,ClassLabelFile,ILLUFolder,GeneListFile,
           SignalFile,SignalFile_Postprocess,SignalFile_Impute, SignalFile_Merge,
            SignalFile_Normalize,SignalFile_Order,SignalFile_Annotate]

