/*signature_analysis*/

gsea(Parameters,Modules):-
   convert_parameters_file(Parameters,NewParameters),
   % Conditions:gct,logged,created
   get_value(NewParameters,format,unknown_format,Format),
   Format=gct,
   get_value(NewParameters,is_logged,unknown_logged,Is_Logged),
   Is_Logged=logged,
   get_value(NewParameters,status,created,Status),
   Status=created,
   % Input: class_label_file and signal_file
   get_value(NewParameters,contents,[unknown],Contents),
   get_value(NewParameters,preprocess,unknown_preprocess,Preprocess),
   class_label_file([contents,Contents,preprocess,Preprocess,status,_],Past_Modules_1),
   member(OldStatus,[given,jointed,splited,created]),
   set_value(NewParameters,status,OldStatus,NewParameters1),
   signal_file(NewParameters1,Past_Modules_2),
   append(Past_Modules_1,Past_Modules_2,Past_Modules),
   % Module:gsea
   % Output parameters: update the parameters to full length
   Newadd=[gsea,NewParameters],
   append(Past_Modules,Newadd,Modules).


signature_score(Parameters,Modules):-
   convert_parameters_file(Parameters,NewParameters),
   % Conditions: pcl,logged,created,'HG_U133A'
   get_value(NewParameters,format,unknown_format,Format),
   Format=pcl,
   get_value(NewParameters,is_logged,unknown_logged,Is_Logged),
   Is_Logged=logged,
   get_value(NewParameters,status,created,Status),
   Status=created,
   get_value(Parameters,platform,unknown_platform,Platform),
   Platform='HG_U133A',
   member(OldStatus,[given,jointed,splited,created]),
   set_value(NewParameters,status,OldStatus,NewParameters2),
   get_value(Parameters,preprocess,unknown_preprocess,Preprocess),
   % conditions: if preprocess is rma or mas5
   (member(Preprocess,[rma,mas5]),
   set_value(NewParameters2,preprocess,rma,NewParameters3),
   set_value(NewParameters2,preprocess,mas5,NewParameters4),
   % Input: signal_file with rma and signal_file with mas5
   signal_file(NewParameters3,Past_Modules_1),
   signal_file(NewParameters4,Past_Modules_2),
   append(Past_Modules_2,Past_Modules_1,Past_Modules),
   append([pre1,rma,pre2,mas5],NewParameters,Write_list);
   % Conditions: if preprocess is illumina
   Preprocess=illumina,
   % Input: signal_file with illumina
   signal_file(NewParameters2,Past_Modules),
   append([pre1,Preprocess,pre2,Preprocess],NewParameters,Write_list)),
   % Module: run_scoresig
   % Output parameters: the parameters include the pre1 and pre2
   Newadd=[run_scoresig,Write_list],
   append(Past_Modules,Newadd,Modules).

