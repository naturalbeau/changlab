from Module import AbstractModule

class Module(AbstractModule):
    def __init__(self):
        AbstractModule.__init__(self)

    def run(
        self, network, antecedents, out_attributes, user_options, num_cores,
        out_path):
        import os
        from genomicode import parallel
        from genomicode import filelib
        from genomicode import alignlib
        from Betsy import module_utils as mlib

        fastq_node, sample_node, orient_node, reference_node = antecedents
        fastq_files = mlib.find_merged_fastq_files(
            sample_node.identifier, fastq_node.identifier)
        ref = alignlib.create_reference_genome(reference_node.identifier)
        assert os.path.exists(ref.fasta_file_full)
        orient = mlib.read_orientation(orient_node.identifier)
        filelib.safe_mkdir(out_path)

        metadata = {}
        metadata["tool"] = "bowtie1 %s" % alignlib.get_bowtie1_version()

        # With low alignment percentages, might want to play around with:
        # - insert size
        # - maximum mismatch

        # Make a list of the jobs to run.
        jobs = []
        for x in fastq_files:
            sample, pair1, pair2 = x
            sam_filename = os.path.join(out_path, "%s.sam" % sample)
            log_filename = os.path.join(out_path, "%s.log" % sample)
            x = sample, pair1, pair2, sam_filename, log_filename
            jobs.append(x)
        
        # Generate bowtie1 commands for each of the files.
        attr2orient = {
            "single" : None,
            "paired_fr" : "fr",
            "paired_rf" : "rf",
            "paired_ff" : "ff",
            }
        orientation = attr2orient[orient.orientation]
        #x = sample_node.data.attributes["orientation"]
        #orientation = attr2orient[x]

        sq = parallel.quote
        commands = []
        for x in jobs:
            sample, pair1, pair2, sam_filename, log_filename = x
            nc = max(1, num_cores/len(jobs))
            x = alignlib.make_bowtie1_command(
                ref.fasta_file_full, sam_filename, pair1, fastq_file2=pair2,
                orientation=orientation, num_threads=nc)
            x = "%s >& %s" % (x, sq(log_filename))
            commands.append(x)
        metadata["commands"] = commands
        parallel.pshell(commands, max_procs=num_cores)

        # Make sure the analysis completed successfully.
        for x in jobs:
            sample, pair1, pair2, sam_filename, log_filename = x
            # Make sure sam file created.
            assert filelib.exists_nz(sam_filename), \
                   "Missing: %s" % sam_filename
            # Make sure there are some alignments.
            x = open(log_filename).read()
            assert x.find("No alignments") < 0, "No alignments"

        return metadata


    def name_outfile(self, antecedents, user_options):
        return "alignments.bowtie"
