% sam_file.pl

:- set_prolog_flag(toplevel_print_options,
             [quoted(true), portray(true), max_depth(0)]).

:-dynamic bam_file/2.
:-dynamic sam_file/2.
:-dynamic fastq_file/2.
:-dynamic input_sam_file/2.

/*-------------------------------------------------------------------------*/
% Output interface
% The parameters in output can be any length and it will trace to the full length one
% for the parameter which is not provide, will be a variable
sam_file(Parameters,Modules):-
    % Conditions: the Parameters is not full length
    get_desire_parameters_sam(Parameters,NewParameters1),
    length(NewParameters1,N),
    get_length(n_sam,N1),
    N<N1,
    % Input:sam_file with full length parameters
    convert_parameters_variable_sam(Parameters,NewParameters),
    %write(NewParameters),nl,
    sam_file(NewParameters,Modules).
    
/*-------------------------------------------------------------------------*/

% Input interface
% given a input_sam_file,generate sam_file that will have a full length of parameters
% the parameter which is not provided is in default value
sam_file(NewParameters,Modules):-
    input_sam_file(OldParameters,Modules),
     convert_parameters_sam(OldParameters,NewParameters).
/*-------------------------------------------------------------------------*/
%generate sam_file from sai_file.
sam_file(Parameters,Modules):-
      get_desire_parameters_sam(Parameters,NewParameters1),
      length(NewParameters1,N),
      get_length(n_sam,N1),
      N=N1,
      get_value(Parameters,contents,[unknown],Contents),
      get_value(Parameters,format,sam,Format),
      Format=sam,
	get_value(Parameters,sorted,no_sorted,Sorted),
      Sorted=no_sorted,
	get_value(Parameters,duplicates_marked,no_marked,Marked),
      Marked=no_marked,
      get_value(Parameters,recalibration,no_recalibration,Recalibration),
      Recalibration=no_recalibration,
	get_value(Parameters,has_header,no_fixed,Has_header),
      Has_header=no_fixed,
      get_value(Parameters,read,single,Read),
	get_value(Parameters,ref,human,Ref),
      (Read=single,
	% Input:sai_file
	sai_file([contents,Contents,format,sai,read,single,ref,Ref],Past_Modules);
      Read=pair,
      sai_file([contents,Contents,format,sai,read,pair1,ref,Ref],Past_Modules1),
      sai_file([contents,Contents,format,sai,read,pair2,ref,Ref],Past_Modules2),
      append(Past_Modules1,Past_Modules2,Past_Modules)),
      % Module: generate_alignment_sam   
      %Output parameters:full length sam_file parameters
      Newadd=[generate_alignment_sam,Parameters],
      append(Past_Modules,Newadd,Modules).

/*-------------------------------------------------------------------------*/
%sort sam_file.
sam_file(Parameters,Modules):-
      length(Parameters,N),
      get_length(n_sam,N1),
      N=N1,
      get_value(Parameters,format,sam,Format),
      Format=bam,
      get_value(Parameters,sorted,no_sorted,Sorted),
      Sorted=yes_sorted,
      % Input:sam_file with no_sorted,
      OldSorted = no_sorted,
      set_value(Parameters,sorted,OldSorted,OldParameters1),
      set_value(OldParameters1,format,sam,OldParameters),
	sam_file(OldParameters,Past_Modules),
      % Module: sort_sam _file
      %Output parameters:full length parameters of sam_file
      Newadd=[sort_sam_file,Parameters],
      append(Past_Modules,Newadd,Modules).

/*-------------------------------------------------------------------------*/
%mark duplicates.
sam_file(Parameters,Modules):-
      length(Parameters,N),
      get_length(n_sam,N1),
      N=N1,
	get_value(Parameters,sorted,no_sorted,Sorted),
      Sorted=yes_sorted,
      get_value(Parameters,duplicates_marked,no_marked,Duplicates_marked),
      Duplicates_marked=yes_marked,
	% Input:sam_file
      OldMarked = no_marked,
      set_value(Parameters,duplicates_marked,OldMarked,OldParameters),
	sam_file(OldParameters,Past_Modules),
      % Module: mark_duplicates
      %Output parameters:full length parameters of sam_file
      Newadd=[mark_duplicates,Parameters],
      append(Past_Modules,Newadd,Modules).
/*-------------------------------------------------------------------------*/
%fix header
sam_file(Parameters,Modules):-
      length(Parameters,N),
      get_length(n_sam,N1),
      N=N1,
	get_value(Parameters,sorted,no_sorted,Sorted),
      Sorted=yes_sorted,
      get_value(Parameters,duplicates_marked,no_marked,Duplicates_marked),
      Duplicates_marked=yes_marked,
      
      get_value(Parameters,recalibration,no_recalibration,Recalibration),
      Recalibration=no_recalibration,

      %get_value(Parameters,ref,human,Ref),
      %(Ref=human,
      %Recalibration=yes_recalibration;
      %Ref=fly,
      %Recalibration=no_recalibration),

	get_value(Parameters,has_header,no_fixed,Has_header),
      Has_header=yes_fixed,
	% Input:sam_file
      OldFixheader = no_fixed,
      set_value(Parameters,has_header,OldFixheader,OldParameters),
	sam_file(OldParameters,Past_Modules),
      % Module: fix_header_GATK
      %Output parameters:full length parameters of sam_file
      Newadd=[fix_header_GATK,Parameters],
      append(Past_Modules,Newadd,Modules).

/*-------------------------------------------------------------------------*/
%base quality score recalibration .
sam_file(Parameters,Modules):-
      length(Parameters,N),
      get_length(n_sam,N1),
      N=N1,
	get_value(Parameters,ref,human,Ref),
      Ref=human,
	get_value(Parameters,sorted,no_sorted,Sorted),
      Sorted=yes_sorted,
      get_value(Parameters,has_header,no_fixed,Has_header),
      Has_header=yes_fixed,
      get_value(Parameters,duplicates_marked,no_marked,Duplicates_marked),
      Duplicates_marked=yes_marked,
      get_value(Parameters,recalibration,no_recalibration,Recalibration),
      Recalibration=yes_recalibration,
	% Input:sam_file
      OldRecalibration = no_recalibration,
      set_value(Parameters,recalibration,OldRecalibration,OldParameters),
	sam_file(OldParameters,Past_Modules),
      % Module: base_quality_score_recalibration
      %Output parameters:full length parameters of sam_file
      Newadd=[base_quality_score_recalibration,Parameters],
      append(Past_Modules,Newadd,Modules).


/*-------------------------------------------------------------------------*/
% convert the Parameters to a full length Parameters for sam_file, for the parameter which
% is not specified, will assign a default value
convert_parameters_sam(Parameters,NewParameters):-
    
    get_value(Parameters,contents,[unknown],Contents),
    NewParameters0=[contents,Contents],
 
    get_value(Parameters,format,unknown_format,Format),
    member(Format,[sam,bam]),
    append(NewParameters0,[format,Format],NewParameters1),
     
    get_value(Parameters,sorted,no_sorted,Sorted),
    member(Sorted,[no_sorted,yes_sorted]),
    append(NewParameters1,[sorted,Sorted],NewParameters2),
    
    get_value(Parameters,duplicates_marked,no_marked,Duplicates_marked),
    member(Duplicates_marked,[no_marked,yes_marked]),
    append(NewParameters2,[duplicates_marked,Duplicates_marked],NewParameters3),
    
    get_value(Parameters,recalibration,no_recalibration,Recalibration),
    member(Recalibration,[no_recalibration,yes_recalibration]),
    append(NewParameters3,[recalibration,Recalibration],NewParameters4),

    get_value(Parameters,has_header,no_fixed,Has_header),
    member(Has_header,[no_fixed,yes_fixed]),
    append(NewParameters4,[has_header,Has_header],NewParameters5),

    get_value(Parameters,read,single,Read),
    member(Read,[single,pair]),
    append(NewParameters5,[read,Read],NewParameters6),
  
    get_value(Parameters,ref,human,Ref),
    member(Ref,[human,fly]),
    append(NewParameters6,[ref,Ref],NewParameters).
 
    
/*-------------------------------------------------------------------------*/
%get the parameters list for sam_file
get_desire_parameters_sam(Parameters,NewParameters):-

    get_value(Parameters,contents,[unknown],Contents),
    append([],[contents,Contents],NewParameters0),
   
    (member(format,Parameters),
    get_value_variable(Parameters,format,Format),
    append(NewParameters0,[format,Format],NewParameters1);
    not(member(format,Parameters)),
    NewParameters1=NewParameters0),

    (member(sorted,Parameters),
    get_value_variable(Parameters,sorted,Sorted),
    append(NewParameters1,[sorted,Sorted],NewParameters2);
    not(member(sorted,Parameters)),
    NewParameters2=NewParameters1),

    (member(duplicates_marked,Parameters),
    get_value_variable(Parameters,duplicates_marked,Duplicates_marked),
    append(NewParameters2,[duplicates_marked,Duplicates_marked],NewParameters3);
    not(member(duplicates_marked,Parameters)),
    NewParameters3=NewParameters2),
    
    (member(recalibration,Parameters),
    get_value_variable(Parameters,recalibration,Recalibration),
    append(NewParameters3,[recalibration,Recalibration],NewParameters4);
    not(member(recalibration,Parameters)),
    NewParameters4=NewParameters3),
    
    (member(has_header,Parameters),
    get_value_variable(Parameters,has_header,Has_header),
    append(NewParameters4,[has_header,Has_header],NewParameters5);
    not(member(has_header,Parameters)),
    NewParameters5=NewParameters4),
    
    (member(read,Parameters),
    get_value_variable(Parameters,read,Read),
    append(NewParameters5,[read,Read],NewParameters6);
    not(member(read,Parameters)),
    NewParameters6=NewParameters5),

    (member(ref,Parameters),
    get_value_variable(Parameters,ref,Ref),
    append(NewParameters6,[ref,Ref],NewParameters);
    not(member(ref,Parameters)),
    NewParameters=NewParameters6).

   

/*-------------------------------------------------------------------------*/
% convert the Parameters to a full length Parameters for sam_file, for the parameter which
% is not specified, will assign a variable

convert_parameters_variable_sam(Parameters,NewParameters):-
    get_value(Parameters,contents,[unknown],Contents),
    append([],[contents,Contents],NewParameters0),
    get_value_variable(Parameters,format,Format),
    member(Format,[sam,bam]),
    append(NewParameters0,[format,Format],NewParameters1),
    get_value_variable(Parameters,sorted,Sorted),
    member(Sorted,[no_sorted,yes_sorted]),
    append(NewParameters1,[sorted,Sorted],NewParameters2),
    get_value_variable(Parameters,duplicates_marked,Duplicates_marked),
    member(Duplicates_marked,[no_marked,yes_marked]),
    append(NewParameters2,[duplicates_marked,Duplicates_marked],NewParameters3),
    get_value_variable(Parameters,recalibration,Recalibration),
    member(Recalibration,[no_recalibration,yes_recalibration]),
    append(NewParameters3,[recalibration,Recalibration],NewParameters4),
    get_value_variable(Parameters,has_header,Has_header),
    member(Has_header,[no_fixed,yes_fixed]),
    append(NewParameters4,[has_header,Has_header],NewParameters5),
    get_value_variable(Parameters,read,Read),
    member(Read,[single,pair]),
    append(NewParameters5,[read,Read],NewParameters6),
    get_value_variable(Parameters,ref,Ref),
    member(Ref,[human,fly]),
    append(NewParameters6,[ref,Ref],NewParameters).
    



