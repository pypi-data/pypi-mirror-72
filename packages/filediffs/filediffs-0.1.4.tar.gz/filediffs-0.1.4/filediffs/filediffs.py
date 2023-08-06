from filediffs.filediffs_cy import file_diffs_cy


def file_diffs(filename_1,
               filename_2,
               outpath_lines_present_in_both_files="lines_present_in_both_files.txt",
               outpath_lines_present_only_in_file1="lines_present_only_in_file1.txt",
               outpath_lines_present_only_in_file2="lines_present_only_in_file2.txt",
               verbose=True):
    # call cython function
    lines_only_in_file_1, lines_only_in_file_2 = file_diffs_cy(
        filename_1=bytes(filename_1, "utf-8"), filename_2=bytes(filename_2, "utf-8"),
        outpath_lines_present_in_both_files=bytes(outpath_lines_present_in_both_files, "utf-8"),
        outpath_lines_present_only_in_file1=bytes(outpath_lines_present_only_in_file1, "utf-8"),
        outpath_lines_present_only_in_file2=bytes(outpath_lines_present_only_in_file2, "utf-8"),
        verbose=verbose
    )

    return lines_only_in_file_1, lines_only_in_file_2
