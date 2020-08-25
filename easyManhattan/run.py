import argparse
from easyManhattan import double_files
from easyManhattan import single_files

def main():
    parser = argparse.ArgumentParser(description='Make a Manhattan plot')

    parser.add_argument('--filenames', 
                        nargs = '+', 
                        required = True,
                        help = 'List of summary statistic file paths', 
                        dest = 'filenames1')
    parser.add_argument('--double-filenames', 
                        nargs = '*', 
                        help = 'List of second summary statistic file paths', 
                        dest = 'filenames2')
    parser.add_argument('--chr-col',
                        help = 'Name of the chr-value column',
                        dest = 'chr_col')
    parser.add_argument('--pos-col',
                        help = 'Name of the pos-value column',
                        dest = 'pos_col')
    parser.add_argument('--p-col',
                        required = True,
                        help = 'Name of the p-value column',
                        dest = 'p_col')
    parser.add_argument('--variant-col',
                        help = 'Name of the variant column (formatted as CHR:POS:A1:A2)',
                        dest = 'variant_col')
    parser.add_argument('--names', 
                        nargs = '+', 
                        required = True,
                        help = 'List of summary statistic trait names', 
                        dest = 'label_vec')
    parser.add_argument('--colors',
                        nargs = '+',
                        required = True,
                        help = 'List of marker colors for multiple traits, or list of 2 colors for alternating chromosome marker colors',
                        dest = 'color_vec')
    parser.add_argument('--width', 
                        default = 8,
                        type = float,
                        dest = 'x_size',
                        help = 'Desired width of the plot (in inches)')
    parser.add_argument('--height', 
                        default = 6,
                        type = float,
                        dest = 'y_size',
                        help = 'Desired height of the plot (in inches)')
    parser.add_argument('--y-break', 
                        type = float,
                        default = 0,
                        dest = 'y_scale_break',
                        help = 'Y-axis break, to increase readability of the plot')
    parser.add_argument('--y-padding', 
                        default = 2,
                        type = float,
                        dest = 'y_scale_padding',
                        help = 'Y-scale maximum padding, value added to y-axis maximum on plot scale')
    parser.add_argument('--p-threshold',
                        default = 0,
                        type = float,
                        dest = 'p_threshold',
                        help = 'Specify p-value threshold to plot a horizontal line (5e-8 usually used)')
    parser.add_argument('--y-labels', 
                        default = ["-log(p)"],
                        nargs = '+',
                        dest = 'y_label_vec',
                        help = 'Labels for y-axis (1 for single Manhattan plot, 2 for double Manhattan plot)')
    parser.add_argument('--plot-title', 
                        default = 'Manhattan Plot',
                        dest = 'title_str',
                        help = 'Name of the plot')
    parser.add_argument('--locus-labels',
                        dest = 'locus_labels',
                        help = 'Path to a tab-delimited file with locus labels')
    parser.add_argument('--output-path',
                        dest = 'output_path',
                        help = 'Desired output path of plot')

    args = parser.parse_args()

    #Check for valid arguments
    if (args.variant_col == None) and ((args.chr_col == None) or (args.pos_col == None)):
        parser.error('Either the name of a chromosome and position column or the name of a variant column is required')

    if len(args.filenames1) > 1:
        if len(args.filenames1) != len(args.color_vec):
            raise ValueError("Number of colors specified does not match the number of summary statistics provided")
        elif len(args.filenames1) != len(args.label_vec):
            raise ValueError("Number of summary statistics and number of trait names does not match")
    else:
        if len(args.color_vec) != 2:
            raise ValueError("Please specify two colors for alternating chromosomes on the plot")

    if (args.p_threshold < 0) or (args.p_threshold > 1):
        raise ValueError("Invalid value for p-value threshold")
    elif (args.x_size <= 0) or (args.y_size <= 0):
        raise ValueError("Dimensions must be positive values")

    if args.filenames2 == None: #Single Manhattan plot case
        if args.locus_labels != None:
            loci_labels_file = open(args.locus_labels)
            for line in loci_labels_file:
                if len(line.rsplit("\t")) != 5:
                    raise ValueError("Incorrect number of columns in locus labels file (also check for any whitespace issues)")

    else: #Double Manhattan plot case
        if len(args.filenames1) != len(args.filenames2):
            raise ValueError("Number of traits in top Manhattan plot and bottom Manhattan plot do not match")    
        if args.locus_labels != None:
            loci_labels_file = open(args.locus_labels)
            for line in loci_labels_file:
                if len(line.rsplit("\t")) != 6:
                    raise ValueError("Incorrect number of columns in locus labels file (also check for any whitespace issues)")

        

    if args.filenames2 == None:
        single_files.single_manhattan(args.filenames1, args.chr_col, args.pos_col, args.p_col, args.variant_col, args.label_vec, args.color_vec, args.x_size, args.y_size, args.y_scale_break, args.y_scale_padding, args.p_threshold, args.y_label_vec, args.title_str, args.locus_labels, args.output_path)
    else:
        double_files.double_manhattan(args.filenames1, args.filenames2, args.chr_col, args.pos_col, args.p_col, args.variant_col, args.label_vec, args.color_vec, args.x_size, args.y_size, args.y_scale_break, args.y_scale_padding, args.p_threshold, args.y_label_vec, args.title_str, args.locus_labels, args.output_path)
    
if __name__ == "__main__":
    main()