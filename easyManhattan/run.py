import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    double_manhattan(args.filenames1, args.filenames2, args.label_vec, args.color_vec, args.x_size, args.y_size, args.y_scale_break, args.y_scale_padding, args.p_threshold, args.y_label_vec, args.title_str, args.output_path)




def double_manhattan(filenames1, filenames2, label_vec, color_vec, x_size, y_size, y_scale_break, y_scale_padding, p_threshold, y_label_vec, title_str, output_path):
    f,(ax,ax2) = plt.subplots(2,1,sharex=True, facecolor='w', gridspec_kw={'hspace': 0})
    f.set_size_inches(x_size, y_size)
    all_max = 0
    trait_num = 0
    for pair in zip(filenames1, filenames2):
        df1 = pd.read_csv(pair[0], sep = "\t") 
        df2 = pd.read_csv(pair[1], sep = "\t") 
        df1['log_p1'] = -np.log10(df1.pval)
        df2['log_p2'] = np.log10(df2.pval)
        df = pd.merge(df1, df2, on = 'variant').dropna()
        df['CHR'] = df['variant'].apply(lambda x: 23 if x.split(":")[0] == "X" else int(x.split(":")[0]))
        df['LOC'] = df['variant'].apply(lambda x: int(x.split(":")[1]))
        
        if trait_num == 0:
            x_labels = []
            x_labels_pos = []
            chrom_offset = {}
            chrom_start = {}
            chrom_offset_num = 0
            for chrom in range(1,23):
                chrom_offset[chrom] = chrom_offset_num
                chrom_start[chrom] = min(df[df['CHR'] == chrom]['LOC'])
                x_labels.append(str(chrom))
                x_labels_pos.append(chrom_offset_num + (float(max(df[df['CHR'] == chrom]['LOC'])) 
                                                        - float(min(df[df['CHR'] == chrom]['LOC'])))/2)
                chrom_offset_num += max(df[df['CHR'] == chrom]['LOC']) - min(df[df['CHR'] == chrom]['LOC'])
        
        if len(filenames1) > 1:
            trait_max = double_plot_multi(ax, ax2, df, chrom_offset, chrom_start, color_vec, label_vec, trait_num)
            if all_max < trait_max:
                all_max = trait_max
            if trait_num == 0:
                master_df = df
            else:
                master_df = pd.concat([master_df,df])
        else:
            all_max = double_plot_single(ax, ax2, df, chrom_offset, chrom_start, color_vec, label_vec, trait_num)
            master_df = df
        trait_num += 1

    ax.set_xlim([0, chrom_offset_num])
    ax2.set_xlim([0, chrom_offset_num])
    ax.set_ylim([y_scale_break, all_max + y_scale_padding])
    ax2.set_ylim([-all_max - y_scale_padding, -y_scale_break])
    ax.set_ylabel(y_label_vec[0])
    ax2.set_ylabel(y_label_vec[1])
    ax2.set_xlabel('Chromosome')
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)

    #Set chromosome labels
    ax2.set_xticks(x_labels_pos)
    ax2.set_xticklabels(x_labels)
    if len(filenames1) > 1: #Chromosome labels when color is used for multiple traits
        for chrom in range(1,23):
            ax.vlines(chrom_offset[chrom], ymin = 0, ymax = all_max + 2, linestyles = 'dotted', linewidth = 1)
            ax2.vlines(chrom_offset[chrom], ymin = -all_max - 2, ymax = 0, linestyles = 'dotted', linewidth = 1)
        ax.legend(loc = 'upper left', bbox_to_anchor= (1.01, 1.01))

    #Horizontal cutoff lines
    if p_threshold != 0:
        ax.hlines(y=-np.log(p_threshold), xmin = 0, xmax = chrom_offset_num, linewidth = 1)
        ax2.hlines(y=np.log(p_threshold), xmin = 0, xmax = chrom_offset_num, linewidth = 1)

    f.suptitle(title_str)
    
    #plt.show()
    plt.savefig(output_path, format = 'pdf', dpi = 400)

def double_plot_multi(ax, ax2, df, chrom_offset, chrom_start, color_vec, label_vec, trait_num):
    df['offset_num'] = df['CHR'].map(chrom_offset) - df['CHR'].map(chrom_start)
    df['IND'] = df['LOC'] + df['offset_num']
    ax.scatter(x = df['IND'], y = df['log_p1'], color = color_vec[trait_num], s = 3, label = label_vec[trait_num], rasterized = True)
    ax2.scatter(x = df['IND'], y = df['log_p2'], color = color_vec[trait_num], s = 3, rasterized = True)

    return max(max(df['log_p1'].tolist()), -min(df['log_p2'].tolist()))

def double_plot_single(ax, ax2, df, chrom_offset, chrom_start, color_vec, label_vec, trait_num):
    df['offset_num'] = df['CHR'].map(chrom_offset) - df['CHR'].map(chrom_start)
    df['IND'] = df['LOC'] + df['offset_num']
    for chrom in range(1,23):
        tempdf = df[df['CHR'] == chrom]
        ax.scatter(x = tempdf['IND'], y = tempdf['log_p1'], color = color_vec[chrom%2], s = 3, rasterized = True)
        ax2.scatter(x = tempdf['IND'], y = tempdf['log_p2'], color = color_vec[chrom%2], s = 3, rasterized = True)

    return max(max(df['log_p1'].tolist()), -min(df['log_p2'].tolist()))

main()