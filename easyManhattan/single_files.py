import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def single_manhattan(filenames, label_vec, color_vec, x_size, y_size, y_scale_break, y_scale_padding, p_threshold, y_label_vec, title_str, output_path):
    f,ax = plt.subplots(1,1,sharex=True, facecolor='w', gridspec_kw={'hspace': 0})
    f.set_size_inches(x_size, y_size)
    all_max = 0
    trait_num = 0
    for filename in filenames:
        df = pd.read_csv(filename, sep = "\t")
        df['log_p'] = -np.log10(df.pval)
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
        
        if len(filenames) > 1:
            trait_max = single_plot_multi(ax, df, chrom_offset, chrom_start, color_vec, label_vec, trait_num)
            if all_max < trait_max:
                all_max = trait_max
            if trait_num == 0:
                master_df = df
            else:
                master_df = pd.concat([master_df,df])
        else:
            all_max = single_plot_single(ax, df, chrom_offset, chrom_start, color_vec, trait_num)
            master_df = df
        trait_num += 1

    ax.set_xlim([0, chrom_offset_num])
    ax.set_ylim([y_scale_break, all_max + y_scale_padding])
    ax.set_ylabel(y_label_vec[0])
    ax.set_xlabel('Chromosome')
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)

    #Set chromosome labels
    ax.set_xticks(x_labels_pos)
    ax.set_xticklabels(x_labels)
    if len(filenames) > 1: #Chromosome labels when color is used for multiple traits
        for chrom in range(1,23):
            ax.vlines(chrom_offset[chrom], ymin = 0, ymax = all_max + 2, linestyles = 'dotted', linewidth = 1)
        ax.legend(loc = 'upper left', bbox_to_anchor= (1.01, 1.01))

    #Horizontal cutoff lines
    if p_threshold != 0:
        ax.hlines(y=-np.log10(p_threshold), xmin = 0, xmax = chrom_offset_num, linewidth = 1)

    f.suptitle(title_str)
    
    #plt.show()
    plt.savefig(output_path, format = 'pdf', dpi = 400)

def single_plot_multi(ax, df, chrom_offset, chrom_start, color_vec, label_vec, trait_num):
    df['offset_num'] = df['CHR'].map(chrom_offset) - df['CHR'].map(chrom_start)
    df['IND'] = df['LOC'] + df['offset_num']
    ax.scatter(x = df['IND'], y = df['log_p'], color = color_vec[trait_num], s = 3, label = label_vec[trait_num], rasterized = True)

    return max(df['log_p'].tolist())

def single_plot_single(ax, df, chrom_offset, chrom_start, color_vec, trait_num):
    df['offset_num'] = df['CHR'].map(chrom_offset) - df['CHR'].map(chrom_start)
    df['IND'] = df['LOC'] + df['offset_num']
    for chrom in range(1,23):
        tempdf = df[df['CHR'] == chrom]
        ax.scatter(x = tempdf['IND'], y = tempdf['log_p'], color = color_vec[chrom%2], s = 3, rasterized = True)

    return max(df['log_p'].tolist())