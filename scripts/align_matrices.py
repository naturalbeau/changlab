#!/usr/bin/env python

# Functions:

import os
import sys


def read_matrix(filename):
    import arrayio

    # Read the files.
    assert os.path.exists(filename), \
        "I could not find the file: %s" % filename
    fmt_module = arrayio.choose_format(filename)
    assert fmt_module, \
        "I could not figure out the format of file: %s" % filename
    x = fmt_module.read(filename)
    return x


def write_matrix(filename, matrix):
    import arrayio
    arrayio.write(matrix, open(filename, 'w'))


def write_annot(filename, annot_data):
    from genomicode import jmath
    name_order, name2annots = annot_data
    matrix = []
    for name in name_order:
        annots = name2annots[name]
        x = [name] + annots
        matrix.append(x)
    # Transpose the matrix.
    matrix = jmath.transpose(matrix)

    handle = open(filename, 'w')
    for x in matrix:
        print >>handle, "\t".join(map(str, x))


def read_annot(filename):
    from genomicode import genesetlib

    name_order = []
    name2annots = {}
    for x in genesetlib.read_tdf(
        filename, preserve_spaces=True, allow_duplicates=True):
        name, description, annots = x
        name_order.append(name)
        name2annots[name] = annots
    return name_order, name2annots


def get_sample_names(matrix):
    import arrayio
    
    name = arrayio.COL_ID
    if name not in matrix._col_names:
        name = matrix._synonyms[name]
    assert name in matrix._col_names, "I can not find the sample names."
    x = matrix.col_names(name)
    return x


def find_best_annots(name2annots, match_annots, case_insensitive):
    all_matches = []  # list of (num_matches, name, matches)
    for name, annots in name2annots.iteritems():
        matches = intersect(annots, match_annots, case_insensitive)
        x = len(matches), name, matches
        all_matches.append(x)
    all_matches = sorted(all_matches)
    x = all_matches[-1]
    x, name, matches = x
    return name, matches


def is_same_annot(x, y, case_insensitive):
    if case_insensitive:
        x, y = x.upper(), y.upper()
    return x == y


def intersect(annots1, annots2, case_insensitive):
    # Return the intersection of annots1 and annots2.  Preserves the
    # order according to annots1.

    ## TOO SLOW.
    ## in_both = []
    ## for x in annots1:
    ##     matching = False
    ##     for y in annots2:
    ##         if is_same_annot(x, y, case_insensitive):
    ##             matching = True
    ##             break
    ##     if matching:
    ##         in_both.append(x)
    ## return in_both
    
    annots1_cmp = annots1
    annots2_cmp = annots2
    if case_insensitive:
        annots1_cmp = [x.upper() for x in annots1]
        annots2_cmp = [x.upper() for x in annots2]
    annots2_cmp = {}.fromkeys(annots2_cmp)
    in_both = [
        annots1[i] for i in range(len(annots1)) if
        annots1_cmp[i] in annots2_cmp]
    return in_both



def annot_index(annot_list, annot, case_insensitive):
    for i, a in enumerate(annot_list):
        if is_same_annot(annot, a, case_insensitive):
            break
    else:
        raise AssertionError, "Missing: %s" % annot
    return i
    

def find_common_samples(matrix_data, first_annot_header, case_insensitive):
    # Initialize the list of common samples from one of the data sets.
    # Try one of the expression data files first.  If not available,
    # then use an annotation file (assuming first_annot_header is
    # provided).
    assert matrix_data
    common = None
    x = [x for x in matrix_data if x[2]]  # pull out expression files
    if x:
        # Found an expression file.
        infile, outfile, is_express_file, matrix = x[0]
        common = get_sample_names(matrix)
    else:
        # No expression files.
        assert first_annot_header, "--first_annot_header not provided."
        infile, outfile, is_express_file, annot_data = matrix_data[0]
        name_order, name2annots = annot_data
        assert first_annot_header in name2annots
        common = name2annots[first_annot_header]
    assert common

    # Make sure the common IDs are in each of the data sets.
    for x in matrix_data:
        infile, outfile, is_express_file, data = x
        if is_express_file:
            annots = get_sample_names(data)
        else:
            name_order, name2annots = annot_data
            name, annots = find_best_annots(
                name2annots, common, case_insensitive)
            assert annots, "%s has no matching annotations." % infile

        common = intersect(common, annots, case_insensitive)

    # Finally, order the annotations according to the first file given.
    assert matrix_data
    x = matrix_data[0]
    infile, outfile, is_express_file, data = x
    if is_express_file:
        samples = get_sample_names(data)
    else:
        name_order, name2annots = data
        x, samples = find_best_annots(name2annots, common, case_insensitive)
    samples = intersect(samples, common, case_insensitive)
    
    return samples


def align_express(matrix, samples, case_insensitive):
    names = get_sample_names(matrix)
    I = []
    for n in samples:
        i = annot_index(names, n, case_insensitive)
        I.append(i)
    x = matrix.matrix(None, I)
    return x


def align_annot(name2annots, samples, case_insensitive):
    name, x = find_best_annots(name2annots, samples, case_insensitive)
    annots = name2annots[name]
    I = []
    for n in samples:
        i = annot_index(annots, n, case_insensitive)
        I.append(i)
    name2annots_new = {}
    for name, annots in name2annots.iteritems():
        x = [annots[i] for i in I]
        name2annots_new[name] = x
    return name2annots_new


def align_matrices(matrix_data, samples, case_insensitive):
    new_matrix_data = []
    for x in matrix_data:
        infile, outfile, is_express_file, data = x
        if is_express_file:
            data_new = align_express(data, samples, case_insensitive)
        else:
            name_order, name2annots = data
            x = align_annot(name2annots, samples, case_insensitive)
            data_new = name_order, x
        x = infile, outfile, is_express_file, data_new
        new_matrix_data.append(x)
    return new_matrix_data


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Align a set of matrices.  Preserve the order of the "
        "first file given.")
    parser.add_argument("outfile", nargs="+")
    
    parser.add_argument(
        "--clobber", default=False, action="store_true",
        help="Overwrite output files, if they already exist.")
    parser.add_argument(
        "--case_insensitive", default=False, action="store_true",
        help="Do a case insensitive search of sample names.")

    parser.add_argument(
        "--express_file", default=[], action="append", help="")
    parser.add_argument(
        "--annot_file", default=[], action="append", help="")

    parser.add_argument(
        "--first_annot_header", help="If only aligning annotation files, "
        "find the samples to be matched under this header in the first "
        "annotation file.")
    
    args = parser.parse_args()
    assert len(args.outfile) == len(args.express_file) + len(args.annot_file)
    for x in args.express_file + args.annot_file:
        assert os.path.exists(x), "I could not find file: %s" % x
    for x in args.outfile:
        assert args.clobber or not os.path.exists(x), "File exists: %s" % x

    # Align the outfiles to the expression and annotation files.
    express_file = args.express_file[:]
    annot_file = args.annot_file[:]
    outfile = args.outfile[:]
    matrix_data = []  # list of (infile, outfile, is_express_file)
    for arg in sys.argv:
        if arg not in ["--express_file", "--annot_file"]:
            continue
        assert outfile
        if arg == "--express_file":
            assert express_file
            x = express_file.pop(0), outfile.pop(0), True
        else:
            assert annot_file
            x = annot_file.pop(0), outfile.pop(0), False
        matrix_data.append(x)
    assert not express_file
    assert not annot_file
    assert not outfile

    # Read each of the files.
    new_matrix_data = []  # list of (infile, outfile, is_express_file, data)
    for x in matrix_data:
        infile, outfile, is_express_file = x
        if is_express_file:
            data = read_matrix(infile)
        else:
            data = read_annot(infile)
        x = infile, outfile, is_express_file, data
        new_matrix_data.append(x)
    matrix_data = new_matrix_data

    # Find the intersection of each file.
    common_samples = find_common_samples(
        matrix_data, args.first_annot_header, args.case_insensitive)
    assert common_samples, "No common samples found."

    # Align each of the matrices.
    matrix_data = align_matrices(
        matrix_data, common_samples, args.case_insensitive)

    # Write out each of the matrices.
    for x in matrix_data:
        infile, outfile, is_express_file, data = x
        if is_express_file:
            write_matrix(outfile, data)
        else:
            write_annot(outfile, data)
    

if __name__ == '__main__':
    main()
    #import cProfile as profile
    #profile.runctx("main()", globals(), locals())
