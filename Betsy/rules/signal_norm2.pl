%signal_norm2.pl

:- set_prolog_flag(toplevel_print_options,
             [quoted(true), portray(true), max_depth(0)]).
/*-------------------------------------------------------------------------*/
% Output interface
% The parameters in output can be any length and it will trace to the full length one
% for the parameter which is not provide, will be in no_gene_center/no_gene_normalize

signal_norm2(DatasetId,Contents,Parameters,Modules):-
    get_desire_parameters_norm2(Parameters,NewParameters1),
    length(NewParameters1,N),
    get_length(n_norm2,N1),
    N<N1,
    convert_parameters_norm2(NewParameters1,NewParameters),
    signal_norm2(DatasetId,Contents,NewParameters,Modules).
/*-------------------------------------------------------------------------*/
% Input interface
% generate signal_norm2 from signal_norm1 with no_gene_center/no_gene_normalize

signal_norm2(DatasetId,Contents,Parameters,Modules):-
   length(Parameters,N),
   get_length(n_norm2,N1),
   N=N1,
   get_value(Parameters,gene_center,no_gene_center,Gene_Center),
   Gene_Center=no_gene_center,
   get_value(Parameters,gene_normalize,no_gene_normalize,Gene_Normalize),
   Gene_Normalize=no_gene_normalize,
   get_desire_parameters_norm1(Parameters,NewParameters),
   signal_norm1(DatasetId,Contents,NewParameters,Modules).

/*-------------------------------------------------------------------------*/
%gene-center the signal file
signal_norm2(DatasetId,Contents,Parameters, Modules):-
    get_value(Parameters,status,created,Status),
    Status=created,
    member(OldStatus,[given,created,jointed,splited]),
    get_value(Parameters,gene_center,no_gene_center,Gene_Center),
    member(Gene_Center,[mean,median]),
    OldGene_center=no_gene_center,
    get_value(Parameters,gene_normalize,no_gene_normalize,Gene_Normalize),
    Gene_Normalize=no_gene_normalize,
    set_value(Parameters,status,OldStatus,OldParameters1),
    set_value(OldParameters1,gene_center,OldGene_center,OldParameters),
    signal_norm2(DatasetId, Contents,OldParameters,Past_Modules),
    append(['DatasetId',
            DatasetId,'Contents',Contents],Parameters,Write_list),
    Newadd=[centering,Write_list],
    append(Past_Modules, Newadd, Modules).
/*-------------------------------------------------------------------------*/
%gene_normalize the signal file
signal_norm2(DatasetId,Contents,Parameters, Modules):-
    get_value(Parameters,status,created,Status),
    Status=created,
    member(OldStatus,[given,created,jointed,splited]),
    get_value(Parameters,gene_normalize,no_gene_normalize,Gene_Normalize),
    member(Gene_Normalize, [variance, sum_of_squares]),
    OldGene_normalize=no_gene_normalize,
    set_value(Parameters,status,OldStatus,OldParameters1),
    set_value(OldParameters1,gene_normalize,OldGene_normalize,OldParameters),
     signal_norm2(DatasetId, Contents,OldParameters,Past_Modules),
    append(['DatasetId',
            DatasetId,'Contents',Contents],Parameters,Write_list),
    Newadd=[normalize,Write_list],
    append(Past_Modules, Newadd, Modules).

