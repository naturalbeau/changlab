/*comparison_report.pl*/

% Determine if the First is before the Second in Modules
comes_before(Modules,First,Second):-
    not(Second=none),
    nth0(N,Modules,First),
    nth0(N1,Modules,Second),
    N<N1;
    Second=none,
    member(First,Modules).
/*-------------------------------------------------------------------*/
% 
make_batch_report(Parameters,Modules):-
    % Conditions: desire batch methods and order
    member((Options,First,Second),[([quantile,yes_quantile,dwd,no_dwd,combat,no_combat,bfrm,no_bfrm,shiftscale,no_shiftscale],quantile,none),
([quantile,yes_quantile,dwd,yes_dwd,combat,no_combat,bfrm,no_bfrm,shiftscale,no_shiftscale],quantile,dwd),
([quantile,yes_quantile,shiftscale,yes_shiftscale,combat,no_combat,bfrm,no_bfrm,dwd,no_dwd],quantile,shiftscale),
([bfrm,yes_bfrm,quantile,no_quantile,shiftscale,no_shiftscale,combat,no_combat,dwd,no_dwd],bfrm_normalize,none),
([quantile,yes_quantile,combat,yes_combat,shiftscale,no_shiftscale,dwd,no_dwd,bfrm,no_bfrm],quantile,combat)]),
     %Input1: signal_norm1 with created and desired batch methods
     convert_parameters_clean_out(Parameters,NewParameters1),

     (First=bfrm_normalize,
     get_options(Parameters,[num_factors],[],Options3),
     append(NewParameters1,Options3,NewParameters4);
     not(First=bfrm_normalize),
     NewParameters4=NewParameters1),

     get_value(Parameters,status,created,Status),
     Status=created,
     append(NewParameters4,Options,NewParameters),
     signal_norm1(NewParameters,Modules1),
     comes_before(Modules1,First,Second),

     %Input2: pca_plot_out 
     get_options(Parameters,[pca_gene_num],[],Options2),
     append(NewParameters,Options2,NewParameters2),
     append(NewParameters2,[objecttype,pca_plot_out],NewParameters3),
     Newadd=[pca_plot,NewParameters3],
     append(Modules1, Newadd, Modules2),

     % Input3: pca_plot_in
     pca_plot_in(NewParameters2,Modules3),

     Modules=[Modules1,Modules2,Modules3].
/*-------------------------------------------------------------------*/

make_diffgenes_report(Parameters,Modules):-
    % Conditions: Parameters has pcl,logged,no_order,created
    convert_parameters_file(Parameters,NewParameters),
    get_value(NewParameters,format,unknown_format,Format),
    Format=pcl,
    get_value(NewParameters,is_logged,unknown_logged,Is_Logged),
    Is_Logged=logged,
    get_value(NewParameters,gene_order,no_order,Gene_Order),
    Gene_Order=no_order,
    get_value(NewParameters,status,created,Status),
    Status=created,
    % Input1: gsea
    member(OldStatus,[given,jointed,splited,created]),
    set_value(NewParameters,status,OldStatus,NewParameters1),

    set_value(NewParameters1,format,gct,NewParameters2),
    gsea(NewParameters2,Modules1),

    % Input2: differential_expressed_genes with t_test
    append(NewParameters1,[diff_expr,t_test],NewParameters3),
    differential_expressed_genes(NewParameters3,Modules2),
    
    % Input3: differential_expressed_genes with sam
    append(NewParameters1,[diff_expr,sam],NewParameters4),
    differential_expressed_genes(NewParameters4,Modules3),
    
    % Input4: gather with t_test_p
    set_value(NewParameters1,gene_order,t_test_p,NewParameters5),
    gather(NewParameters5,Modules4),
    
    Modules = [Modules1,Modules2,Modules3,Modules4].
/*-------------------------------------------------------------------*/
make_cluster_report(Parameters,Modules):-
    % Input1: cluster_file 
    convert_cluster_parameters(Parameters,NewParameters1),
    cluster_file(NewParameters1,Past_Modules1),
    append(NewParameters1,[filetype,cluster_file],NewParameters2),
    % Module: annot_file
    % Output parameters:the full length parameters of cluster_file and [filetype,cluster_file]
    append(Past_Modules1,[annot_file,NewParameters2],Past_Modules2),

    % Input2: cluster_heatmap
    get_options(Parameters,[hm_width,hm_height,color],[],Options),
    append(NewParameters2,Options,NewParameters3),
    cluster_heatmap(NewParameters3,Past_Modules3),

    Modules = [Past_Modules2,Past_Modules3].
/*-------------------------------------------------------------------*/
make_classify_report(Parameters,Modules):-
    % Input1: svm_predictions
    convert_parameters_classify(Parameters,NewParameters),
    svm_predictions(NewParameters,Past_Modules1),
    set_value(NewParameters,format,gct,NewParameters3),

    % Input2: weightedVoting
    weightedVoting(NewParameters3,Past_Modules2),

    % loocv with svm
    append(NewParameters,[classification,svm],NewParameters1),
    loocv(NewParameters1,Past_Modules3),

    % loocv with weightedvoting
    append(NewParameters3,[classification,weightedvoting],NewParameters2),
    loocv(NewParameters2,Past_Modules4),

    Modules=[Past_Modules1,Past_Modules2,Past_Modules3,Past_Modules4].
/*-------------------------------------------------------------------*/
make_normalize_report(Parameters,Modules):-
    % Input1: signal_file
    convert_parameters_file(Parameters,NewParameters),
    signal_file(NewParameters,Past_Modules1),
    % Module: annot_file
    % Output parameters:full length parameters of signal_file and [filetype,signal_file]
    append(NewParameters,[filetype,signal_file],NewParameters0),
    append(Past_Modules1,[annot_file,NewParameters0],Modules1),
    
    % Input2: pca_plot_in
    get_options(Parameters,[pca_gene_num],[],Options),
    append(NewParameters,Options,NewParameters1),
    pca_plot_in(NewParameters1,Modules2),

    % Input3: pca_plot_out
    set_value(NewParameters,format,pcl,NewParameters2),
    get_options(Parameters,[pca_gene_num],[],Options),
    append(NewParameters2,Options,NewParameters3),
    pca_plot_out(NewParameters3,Modules3),

    % Input4: intensity_plot
    intensity_plot(NewParameters,Modules4),
    
    % Conditions: if preprocess is illumina
    get_value(Parameters,preprocess,unknown_preprocess,Preprocess),
    (Preprocess=illumina, 
    convert_parameters_raw(Parameters,NewParameters4), 
    set_value(NewParameters4,is_logged,no_logged,NewParameters5),
    set_value(NewParameters5,format,gct,NewParameters6),
    set_value(NewParameters6,has_missing_value,unknown_missing,NewParameters7),

    % Input5: control_file
    control_file(NewParameters7,Modules8),

    % Input6: biotin_plot
    biotin_plot(NewParameters,Modules5),

    % Input7: actb_plot
    actb_plot(NewParameters,Modules6),

    % Input8: hyb_bar_plot
    hyb_bar_plot(NewParameters,Modules7),

    Modules=[Modules1,Modules2,Modules3,Modules4,Modules8,Modules5,Modules6,Modules7];
    not(member(Preprocess,[illumina])),
    Modules=[Modules1,Modules2,Modules3,Modules4]).