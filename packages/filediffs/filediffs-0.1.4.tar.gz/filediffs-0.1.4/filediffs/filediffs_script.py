import argparse

from filediffs.filediffs import file_diffs


def main():
    # Argument Parsing
    parser = argparse.ArgumentParser("Compare files for differences. Example usage:\n"
                                     "filediffs filediffs/tests/data/file_1.txt filediffs/tests/data/file_2.txt \n"
                                     "filediffs filediffs/tests/data/file_1.txt filediffs/tests/data/file_2.txt "
                                     "--out_filename_both out_both.txt "
                                     "--out_filename_only_in_file1 out_file1_only "
                                     "--out_filename_only_in_file2 out_file2_only")
    parser.add_argument("file_name_1", help="Specify the first filename.")
    parser.add_argument("file_name_2", help="Specify the second filename.")
    parser.add_argument("--out_filename_both", help="Specify filename to save rows present in both files.")
    parser.add_argument("--out_filename_only_in_file1", help="Specify filename to save rows present only in file 1.")
    parser.add_argument("--out_filename_only_in_file2", help="Specify filename to save rows present only in file 2.")

    # process cli arguments
    args = parser.parse_args()

    kwargs = {}
    kwargs["filename_1"] = args.file_name_1
    kwargs["filename_2"] = args.file_name_2
    kwargs["outpath_lines_present_in_both_files"] = args.out_filename_both or "lines_present_in_both_files.txt"
    kwargs["outpath_lines_present_only_in_file1"] = args.out_filename_only_in_file1 or "lines_present_only_in_file1.txt"
    kwargs["outpath_lines_present_only_in_file2"] = args.out_filename_only_in_file2 or "lines_present_only_in_file2.txt"

    lines_only_in_file_11, lines_only_in_file_22 = file_diffs(verbose=True, **kwargs)
