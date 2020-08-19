import argparse
import double_files
import single_files

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
                        default = 3,
                        type = float,
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
                        nargs = '+',
                        dest = 'y_label_vec',
                        help = 'Labels for y-axis (1 for single Manhattan plot, 2 for double Manhattan plot)')
    parser.add_argument('--plot-title', 
                        default = 'Manhattan Plot',
                        dest = 'title_str',
                        help = 'Name of the plot')
    parser.add_argument('--output-path',
                        required = True,
                        dest = 'output_path',
                        help = 'Desired output path of plot')

    args = parser.parse_args()

    if args.filenames2 == None:
        single_files.single_manhattan(args.filenames1, args.label_vec, args.color_vec, args.x_size, args.y_size, args.y_scale_break, args.y_scale_padding, args.p_threshold, args.y_label_vec, args.title_str, args.output_path)
    else:
        double_files.double_manhattan(args.filenames1, args.filenames2, args.label_vec, args.color_vec, args.x_size, args.y_size, args.y_scale_break, args.y_scale_padding, args.p_threshold, args.y_label_vec, args.title_str, args.output_path)
    

main()