# This script encapsulates the complete openCL kernels source files
# into a unique C file that is included inside the MBPL_Context.c
# source file to produce the openCL program that is loaded and build
# upon context creation

import glob

def tidyLine(l):
    l = l.replace('\n','')
    l = l.replace("\\","\\\\")
    l = l.replace('"','\\"')
    return l

cl_srcs = ["cl/gendef.cl"]+glob.glob("cl/MBPL_*.cl")

output_lines = """
/* This is an automatically generated source files from */
/* the openCL kernel source file found in cl/ */

const char *progSrc = "\\n" \\
"""
for cl_src in cl_srcs:
    srcf = open(cl_src)
    src_lines = srcf.readlines()
    srcf.close()

    for l in src_lines:
        l = tidyLine(l)
        output_lines += '"'+l+'\\n " \\\n'

output_lines += ' "\\n"; \n'

f = open("include-private/cl_srcs.c", "w")
f.write(output_lines)
f.close()

