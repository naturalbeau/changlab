# ReportFile
from Betsy.bie3 import *
from Betsy.bie_rules import SignalFile_rule,ClusterFile_rule,ClassifyFile_rule,PcaAnalysis_rule,plot_rule
from Betsy.bie_rules import GenesetAnalysis_rule, DiffExprFile_rule,GatherFile_rule,GseaFile_rule

ReportFile = DataType(
    'ReportFile',
    AttributeDef(
        "report_type",
        ['normalize_file', 'batch_effect_remove', 'classify', 'cluster',
         'diffgenes', 'heatmap', 'geneset', 'all'],
        'normalize_file', 'normalize_file',help="report type"),
    help="Report file"
    )

list_files = [ReportFile]

                                  
all_modules = [
    Module(
        'make_normalize_report',
        [
            SignalFile_rule.SignalFile,
            plot_rule.IntensityPlot,
            plot_rule.ControlPlot,
            PcaAnalysis_rule.PcaPlot,
            plot_rule.ActbPlot,
            PcaAnalysis_rule.PcaPlot,
            ],
        ReportFile,
        Constraint(
            'preprocess', CAN_BE_ANY_OF,
            ['mas5','agilent','loess','unknown','tcga','rsem'],
            0),
        Constraint("annotate", MUST_BE, "yes", 0),
        Constraint(
            "contents", CAN_BE_ANY_OF, [
                "train0","train1", "test", "class0,class1,test","class0",
                "class1", "class0,class1", "unspecified"],
            0),

        #SignalFile
        Constraint('quantile_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('combat_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('shiftscale_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('bfrm_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('dwd_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('gene_center', CAN_BE_ANY_OF, ['median', 'mean', 'no'], 0),
        Constraint(
            'gene_normalize', CAN_BE_ANY_OF,
            ['variance', 'sum_of_squares', 'no'], 0),
        Constraint(
            'unique_genes', CAN_BE_ANY_OF,
            ['no','average_genes', 'high_var', 'first_gene'], 0),
        Constraint('platform', CAN_BE_ANY_OF, ['yes', 'no'], 0),
        Constraint('group_fc', CAN_BE_ANY_OF, ['yes', 'no'], 0),
        Constraint('num_features', CAN_BE_ANY_OF, ['yes', 'no'], 0),
        Constraint(
            'duplicate_probe', CAN_BE_ANY_OF,
            ["no", "closest_probe", "high_var_probe"], 0),
        
        # First PcaPlot.
        Constraint('quantile_norm', SAME_AS, 0, 3),
        Constraint('combat_norm', SAME_AS, 0, 3),
        Constraint('shiftscale_norm', SAME_AS, 0, 3),
        Constraint('bfrm_norm', SAME_AS, 0, 3),
        Constraint('dwd_norm', SAME_AS, 0, 3),
        Constraint('gene_center', SAME_AS, 0, 3),
        Constraint('gene_normalize', SAME_AS, 0, 3),
        Constraint('unique_genes', SAME_AS, 0, 3),
        Constraint('platform', SAME_AS, 0, 3),
        Constraint('group_fc', SAME_AS, 0, 3),
        Constraint('num_features', SAME_AS, 0, 3),
        Constraint('duplicate_probe', SAME_AS, 0, 3),
        
        # Second PcaPlot.
        Constraint('quantile_norm', MUST_BE, 'no', 5),
        Constraint('combat_norm', MUST_BE, 'no', 5),
        Constraint('shiftscale_norm', MUST_BE, 'no', 5),
        Constraint('bfrm_norm', MUST_BE, 'no', 5),
        Constraint('dwd_norm', MUST_BE, 'no', 5),
        Constraint('gene_center', MUST_BE, 'no', 5),
        Constraint('gene_normalize', MUST_BE, 'no', 5),
        Constraint('unique_genes', MUST_BE, 'no', 5),
        Constraint('platform', MUST_BE, 'no', 5),
        Constraint('group_fc', MUST_BE, 'no',5 ),
        Constraint('num_features', MUST_BE, 'no', 5),
        Constraint('duplicate_probe', MUST_BE, 'no', 5),
        
        Constraint('contents', SAME_AS, 0, 1),
        Constraint('contents', SAME_AS, 0, 2),
        Constraint('contents', SAME_AS, 0, 3),
        Constraint('contents', SAME_AS, 0, 4),
        Constraint('contents', SAME_AS, 0, 5),
        Constraint("preprocess", SAME_AS, 0, 3),
        Constraint("preprocess", SAME_AS, 0, 4),
        Constraint("preprocess", SAME_AS, 0, 5),
        Consequence('report_type', SET_TO, 'normalize_file'),
        help="make normalize report for mas5,agilent,loess,unknown,tcga,rsem"
        ),
    Module(
        'make_normalize_report_rma',
         [SignalFile_rule.SignalFile,
         plot_rule.IntensityPlot,
         plot_rule.ControlPlot,
         PcaAnalysis_rule.PcaPlot,
         plot_rule.ActbPlot,
         PcaAnalysis_rule.PcaPlot],
          
         ReportFile,
         Constraint('preprocess',MUST_BE,'rma',0),
         Constraint("annotate",MUST_BE,"yes",0),
         Constraint("contents",CAN_BE_ANY_OF,SignalFile_rule.CONTENTS,0),
        #SignalFile
        Constraint('quantile_norm', MUST_BE, 'yes', 0),
        Constraint('combat_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('shiftscale_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('bfrm_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('dwd_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('gene_center', CAN_BE_ANY_OF, ['median', 'mean', 'no'], 0),
        Constraint(
            'gene_normalize', CAN_BE_ANY_OF,
            ['variance', 'sum_of_squares', 'no'], 0),
        Constraint(
            'unique_genes', CAN_BE_ANY_OF,
            ['no','average_genes', 'high_var', 'first_gene'], 0),
        Constraint('platform', CAN_BE_ANY_OF, ['yes', 'no'], 0),
        Constraint('group_fc', CAN_BE_ANY_OF, ['yes', 'no'], 0),
        Constraint('num_features', CAN_BE_ANY_OF, ['yes', 'no'], 0),
        Constraint(
            'duplicate_probe', CAN_BE_ANY_OF,
            ["no", "closest_probe", "high_var_probe"], 0),
        
        # First PcaPlot.
        Constraint('quantile_norm', SAME_AS, 0, 3),
        Constraint('combat_norm', SAME_AS, 0, 3),
        Constraint('shiftscale_norm', SAME_AS, 0, 3),
        Constraint('bfrm_norm', SAME_AS, 0, 3),
        Constraint('dwd_norm', SAME_AS, 0, 3),
        Constraint('gene_center', SAME_AS, 0, 3),
        Constraint('gene_normalize', SAME_AS, 0, 3),
        Constraint('unique_genes', SAME_AS, 0, 3),
        Constraint('platform', SAME_AS, 0, 3),
        Constraint('group_fc', SAME_AS, 0, 3),
        Constraint('num_features', SAME_AS, 0, 3),
        Constraint('duplicate_probe', SAME_AS, 0, 3),
         # Second PcaPlot.
         Constraint('quantile_norm',MUST_BE,'yes',5),
         Constraint('combat_norm',MUST_BE,'no',5),
         Constraint('shiftscale_norm',MUST_BE,'no',5),
         Constraint('bfrm_norm',MUST_BE,'no',5),
         Constraint('dwd_norm',MUST_BE,'no',5),
         Constraint('gene_center',MUST_BE,'no',5),
         Constraint('gene_normalize',MUST_BE,'no',5),
         Constraint('unique_genes',MUST_BE,'no',5),
         Constraint('platform',MUST_BE,'no',5),
         Constraint('group_fc',MUST_BE,'no',5),
         Constraint('num_features',MUST_BE,'no',5),
         Constraint('duplicate_probe', MUST_BE,'no', 5),
        
         Constraint('contents',SAME_AS,0,1),
         Constraint('contents',SAME_AS,0,2),
         Constraint('contents',SAME_AS,0,3),
         Constraint('contents',SAME_AS,0,4),
         Constraint('contents',SAME_AS,0,5),
         Constraint("preprocess",SAME_AS,0,3),
         Constraint("preprocess",SAME_AS,0,4),
         Constraint("preprocess",SAME_AS,0,5),
         Consequence('report_type',SET_TO,'normalize_file'),
        help="make normalize report for rma"
        ),
Module(
        'make_normalize_report_illumina',
       [ SignalFile_rule.SignalFile,
         plot_rule.IntensityPlot,
         plot_rule.BiotinPlot,
         PcaAnalysis_rule.PcaPlot,
         plot_rule.ActbPlot,
         PcaAnalysis_rule.PcaPlot,
         plot_rule.HousekeepingPlot,
         plot_rule.Hyb_barPlot,
         SignalFile_rule.ControlFile],ReportFile,
         Constraint("contents",CAN_BE_ANY_OF,SignalFile_rule.CONTENTS,0),
         Constraint('preprocess',MUST_BE,'illumina',0),
         Constraint('annotate',MUST_BE,'yes',0),

         #SignalFile
        Constraint('quantile_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('combat_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('shiftscale_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('bfrm_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('dwd_norm', CAN_BE_ANY_OF, ['yes','no'], 0),
        Constraint('gene_center', CAN_BE_ANY_OF, ['median', 'mean', 'no'], 0),
        Constraint(
            'gene_normalize', CAN_BE_ANY_OF,
            ['variance', 'sum_of_squares', 'no'], 0),
        Constraint(
            'unique_genes', CAN_BE_ANY_OF,
            ['no','average_genes', 'high_var', 'first_gene'], 0),
        Constraint('platform', CAN_BE_ANY_OF, ['yes', 'no'], 0),
        Constraint('group_fc', CAN_BE_ANY_OF, ['yes', 'no'], 0),
        Constraint('num_features', CAN_BE_ANY_OF, ['yes', 'no'], 0),
        Constraint(
            'duplicate_probe', CAN_BE_ANY_OF,
            ["no", "closest_probe", "high_var_probe"], 0),
        
        # First PcaPlot.
        Constraint('quantile_norm', SAME_AS, 0, 3),
        Constraint('combat_norm', SAME_AS, 0, 3),
        Constraint('shiftscale_norm', SAME_AS, 0, 3),
        Constraint('bfrm_norm', SAME_AS, 0, 3),
        Constraint('dwd_norm', SAME_AS, 0, 3),
        Constraint('gene_center', SAME_AS, 0, 3),
        Constraint('gene_normalize', SAME_AS, 0, 3),
        Constraint('unique_genes', SAME_AS, 0, 3),
        Constraint('platform', SAME_AS, 0, 3),
        Constraint('group_fc', SAME_AS, 0, 3),
        Constraint('num_features', SAME_AS, 0, 3),
        Constraint('duplicate_probe', SAME_AS, 0, 3),
         # Second PcaPlot.
         Constraint('quantile_norm',MUST_BE,'no',5),
         Constraint('combat_norm',MUST_BE,'no',5),
         Constraint('shiftscale_norm',MUST_BE,'no',5),
         Constraint('bfrm_norm',MUST_BE,'no',5),
         Constraint('dwd_norm',MUST_BE,'no',5),
         Constraint('gene_center',MUST_BE,'no',5),
         Constraint('gene_normalize',MUST_BE,'no',5),
         Constraint('unique_genes',MUST_BE,'no',5),
         Constraint('platform',MUST_BE,'no',5),
         Constraint('group_fc',MUST_BE,'no',5),
         Constraint('num_features',MUST_BE,'no',5),
         Constraint('duplicate_probe', MUST_BE, 'no', 5),
        
         Constraint('preprocess',MUST_BE,'illumina',3),
         Constraint('preprocess',MUST_BE,'illumina',5),
         Constraint('preprocess',MUST_BE,'illumina',8),
         Constraint('format',MUST_BE,'gct',8),
         Constraint("logged",MUST_BE,'no',8),
        
         Constraint('contents',SAME_AS,0,1),
         Constraint('contents',SAME_AS,0,2),
         Constraint('contents',SAME_AS,0,3),
         Constraint('contents',SAME_AS,0,4),
         Constraint('contents',SAME_AS,0,5),
         Constraint('contents',SAME_AS,0,6),
         Constraint('contents',SAME_AS,0,7),
         Constraint('contents',SAME_AS,0,8),
         Constraint("preprocess",SAME_AS,0,4),
         Consequence('report_type',SET_TO,'normalize_file'),
         help="make normalize report for illumina"),
                                   
    Module(
        'make_cluster_report',
        [ClusterFile_rule.ClusterFile,
         ClusterFile_rule.Heatmap],ReportFile,
         Constraint("cluster_alg",CAN_BE_ANY_OF,['som','pca','kmeans','hierarchical'],0),
         Constraint("distance",CAN_BE_ANY_OF,['correlation','euclidean'],0),
         Constraint("cluster_alg",SAME_AS,0,1),
         Constraint("distance",SAME_AS,0,1),
         Consequence('report_type',SET_TO,'cluster'),
         help="make cluster report"),
    Module(
        'make_classify_report',
        [SignalFile_rule.SignalFile,
         ClassifyFile_rule.ClassifyFile,
         ClassifyFile_rule.ClassifyFile,
         ClassifyFile_rule.PredictionPlot,
         ClassifyFile_rule.PredictionPlot,
         ClassifyFile_rule.PredictionPCAPlot,
         ClassifyFile_rule.ClassifyFile,
         ClassifyFile_rule.ClassifyFile,
         ClassifyFile_rule.PredictionPlot,
         ClassifyFile_rule.PredictionPlot,
         ClassifyFile_rule.PredictionPCAPlot
         ],ReportFile,
         Constraint('contents',MUST_BE,'class0,class1,test',0),
         Constraint('logged',MUST_BE,'yes',0),
         Constraint("format",MUST_BE,'gct',0),
         Constraint("classify_alg",MUST_BE,'svm',1),
         Constraint("actual_label",MUST_BE,'yes',1),
         Constraint("classify_alg",MUST_BE,'svm',2),
         Constraint("actual_label",MUST_BE,'no',2),
         Constraint("loocv",MUST_BE,'yes',2),
         Constraint("classify_alg",MUST_BE,'svm',3),
         Constraint("actual_label",MUST_BE,'yes',3),
         Constraint("loocv",MUST_BE,'no',3),
         Constraint("classify_alg",MUST_BE,'svm',4),
         Constraint("actual_label",MUST_BE,'no',4),
         Constraint("loocv",MUST_BE,'yes',4),
         Constraint("classify_alg",MUST_BE,'svm',5),
         Constraint("actual_label",MUST_BE,'yes',5),
         Constraint("loocv",MUST_BE,'no',5),
         Constraint("classify_alg",MUST_BE,'weighted_voting',6),
         Constraint("actual_label",MUST_BE,'yes',6),
         Constraint("loocv",MUST_BE,'no',6),
         Constraint("classify_alg",MUST_BE,'weighted_voting',7),
         Constraint("actual_label",MUST_BE,'no',7),
         Constraint("loocv",MUST_BE,'yes',7),
         Constraint("classify_alg",MUST_BE,'weighted_voting',8),
         Constraint("actual_label",MUST_BE,'yes',8),
         Constraint("loocv",MUST_BE,'no',8),
         Constraint("classify_alg",MUST_BE,'weighted_voting',9),
         Constraint("actual_label",MUST_BE,'no',9),
         Constraint("loocv",MUST_BE,'yes',9),
         Constraint("classify_alg",MUST_BE,'weighted_voting',10),
         Constraint("actual_label",MUST_BE,'yes',10),
         Constraint("loocv",MUST_BE,'no',10),
         Consequence('report_type',SET_TO,'classify'),
         help="make classification report"),
    Module(
        'make_heatmap_report',
        ClusterFile_rule.Heatmap,ReportFile,
        Constraint("cluster_alg",MUST_BE,'no_cluster_alg'),
        Consequence("report_type",SET_TO,'heatmap'),
        help="make heatmap report"),
    Module(
        'make_geneset_report',
        [GenesetAnalysis_rule.GenesetAnalysis,
         GenesetAnalysis_rule.GenesetPlot],ReportFile,
         Consequence("report_type",SET_TO,'geneset'),
        help="make geneset report"),
        
    Module(
        'make_diffgenes_report',
        [DiffExprFile_rule.DiffExprFile,DiffExprFile_rule.DiffExprFile,
         ClusterFile_rule.Heatmap,GatherFile_rule.GatherFile,
         GseaFile_rule.GseaFile],ReportFile,
         OptionDef("hm_width",20),
         OptionDef("hm_height",1),
         Constraint("gene_order",MUST_BE,'diff_ttest',0),
         Constraint("gene_order",SAME_AS,0,3),
         Constraint("contents",MUST_BE,'unspecified',0),
         Constraint("contents",MUST_BE,'unspecified',1),
         Constraint("gene_order",MUST_BE,'diff_sam',1),
         Constraint("cluster_alg",MUST_BE,'no_cluster_alg',2),
         Consequence("report_type",SET_TO,'diffgenes')),
    Module(
        'make_batch_effect_report',
        [SignalFile_rule.SignalFile,
         PcaAnalysis_rule.PcaPlot,
         
         SignalFile_rule.SignalFile,
         PcaAnalysis_rule.PcaPlot,
         
         SignalFile_rule.SignalFile,
         PcaAnalysis_rule.PcaPlot,
         
         SignalFile_rule.SignalFile,
         PcaAnalysis_rule.PcaPlot,
         
         SignalFile_rule.SignalFile,
         PcaAnalysis_rule.PcaPlot,
         
         SignalFile_rule.SignalFile,
         PcaAnalysis_rule.PcaPlot
         
         ],ReportFile,
         Constraint("quantile_norm",MUST_BE,'no',0),
         Constraint("quantile_norm",SAME_AS,0,1),
        
         Constraint("quantile_norm",MUST_BE,'yes',2),
         Constraint("quantile_norm",SAME_AS,2,3),
        
         Constraint("quantile_norm",MUST_BE,'yes',4),
         Constraint("dwd_norm",MUST_BE,'yes',4),
         Constraint("quantile_norm",SAME_AS,4,5),
         Constraint("dwd_norm",SAME_AS,4,5),
        
         Constraint("quantile_norm",MUST_BE,'yes',6),
         Constraint("bfrm_norm",MUST_BE,'yes',6),
         Constraint("quantile_norm",SAME_AS,6,7),
         Constraint("bfrm_norm",SAME_AS,6,7),
        
         Constraint("quantile_norm",MUST_BE,'yes',8),
         Constraint("shiftscale_norm",MUST_BE,'yes',8),
         Constraint("quantile_norm",SAME_AS,8,9),
         Constraint("shiftscale_norm",SAME_AS,8,9),
        
         Constraint("quantile_norm",MUST_BE,'yes',10),
         Constraint("combat_norm",MUST_BE,'yes',10),
         Constraint("quantile_norm",SAME_AS,10,11),
         Constraint("combat_norm",SAME_AS,10,11),
        
         Consequence("report_type",SET_TO,'batch_effect_remove'),
         help="make batch effect remove report")

        ]
  
        
