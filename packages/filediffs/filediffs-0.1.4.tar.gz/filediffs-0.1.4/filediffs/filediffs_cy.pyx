# distutils: language=c++

"""
Copied from https://www.splinter.com.au/reconcilingcomparing-huge-data-sets-with-c/
This compares the contents of two files to find any records
that are in one file but not in the other file.
Note that the order of the records in the files is immaterial.

A positive value in the integer part of the dictionary
signifies that the record is found in file A
A negative value means file B
"""

from libc.stdio cimport FILE, fopen, fprintf, fclose, perror, fgets
from libcpp.string cimport string
from cpython cimport bool

cpdef file_diffs_cy(char*filename_1,
                 char*filename_2,
                 char*outpath_lines_present_in_both_files="lines_present_in_both_files.txt",
                 char*outpath_lines_present_only_in_file1="lines_present_only_in_file1.txt",
                 char*outpath_lines_present_only_in_file2="lines_present_only_in_file2.txt",
                 bool verbose=True):
    cdef FILE *fp
    cdef FILE *fp2
    cdef char ln_str[6000]
    cdef dict comparer_dict = {}
    cdef Py_ssize_t error_return = -1
    cdef Py_ssize_t v
    cdef bytes k
    cdef string progress_report = b"Compared lines from each file: "

    # /* opening file 1 for reading */
    fp = fopen(filename_1, "r")
    if fp == NULL:
        perror(bytes("Error opening " + str(filename_1), "utf-8"))
        return error_return

    # /* opening file 2 for reading */
    fp2 = fopen(filename_2, "r")
    if fp2 == NULL:
        perror(bytes("Error opening " + str(filename_2), "utf-8"))
        return error_return

    fp_both = fopen(outpath_lines_present_in_both_files, "w")
    if fp_both == NULL:
        perror("Error opening " + str(outpath_lines_present_in_both_files) + " that contains lines present in both files'")
        return error_return

    fp1_only = fopen(outpath_lines_present_only_in_file1, "w")
    if fp1_only == NULL:
        perror("Error opening " + str(outpath_lines_present_only_in_file1) + " that contains lines present only in" +
               str(filename_1))
        return error_return

    fp2_only = fopen(outpath_lines_present_only_in_file2, "w")
    if fp2_only == NULL:
        perror("Error opening " + str(outpath_lines_present_only_in_file2) + " that contains lines present only in" +
               str(filename_2))
        return error_return

    cdef Py_ssize_t i = 0
    cdef Py_ssize_t j = 0
    cdef Py_ssize_t m = 0

    # process first file
    while fgets(ln_str, 600, fp):
        i = i + 1
        if ln_str not in comparer_dict:
            comparer_dict[ln_str] = 1
        else:
            comparer_dict[ln_str] = comparer_dict[ln_str] + 1
        # if 5.000.000 rows were processed, consolidate the dict using the first 5.000.000 rows of the 2nd file
        if (i % 5000000) == 0:
            while fgets(ln_str, 6000, fp2):
                j = j + 1
                # if we saw the line, write it to file and erase it from the dict
                if ln_str in comparer_dict:
                    m = m + 1
                    # write to file
                    fprintf(fp_both, ln_str, m)
                    del comparer_dict[ln_str]
                else:
                    comparer_dict[ln_str] = -1
                if (j % 5000000) == 0:
                    if verbose:
                        if (j % 25000000) == 0:
                            progress_report.append(bytes(str(j), "utf-8"))
                    break

    # after the processing of all lines in file 1 ended, read the remaining lines of file 2
    else:
        while fgets(ln_str, 6000, fp2):
            j = j + 1
            if ln_str in comparer_dict:
                m = m + 1
                fprintf(fp_both, ln_str, m)
                del comparer_dict[ln_str]
            else:
                comparer_dict[ln_str] = -1

    # closing file connections
    fclose(fp)
    fclose(fp2)
    fclose(fp_both)

    # split dict into lines only in file 1 and only in file 2
    lines_only_in_file_1 = []
    lines_only_in_file_2 = []
    cdef Py_ssize_t n = 0
    cdef Py_ssize_t o = 0

    for k, v in comparer_dict.items():
        if v > 0:
            n = n + 1
            fprintf(fp1_only, k, n)
            lines_only_in_file_1.append(k)
        else:
            o = o + 1
            fprintf(fp2_only, k, o)
            lines_only_in_file_2.append(k)
    fclose(fp1_only)
    fclose(fp2_only)
    if verbose:
        pystring1 = "Saved lines present in both files to: " + str(outpath_lines_present_in_both_files) + "\n"
        print(pystring1)
        pystring2 = "Saved lines present in file 1 only to: " + str(outpath_lines_present_only_in_file1) + "\n"
        print(pystring2)
        pystring3 = "Saved lines present in file 2 only to: " + str(outpath_lines_present_only_in_file2) + "\n"
        print(pystring3)

    return lines_only_in_file_1, lines_only_in_file_2
