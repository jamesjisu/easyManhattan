import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

def double_manhattan(filenames1, filenames2, chr_col, pos_col, p_col, variant_col, label_vec, color_vec, x_size, y_size, y_scale_break, y_scale_padding, p_threshold, y_label_vec, title_str, locus_labels, output_path):
    f,(ax,ax2) = plt.subplots(2,1,sharex=True, facecolor='w', gridspec_kw={'hspace': 0})
    f.set_size_inches(x_size, y_size)
    all_max = 0
    trait_num = 0
    for pair in zip(filenames1, filenames2):
        df1 = pd.read_csv(pair[0], sep = "\t") 
        df2 = pd.read_csv(pair[1], sep = "\t") 
        df1['log_p1'] = -np.log10(df1[p_col])
        df2['log_p2'] = np.log10(df2[p_col])
        if variant_col != None:
            df = pd.merge(df1, df2, on = variant_col).dropna()
            chr_col = 'CHR'
            pos_col = 'POS'
            df[chr_col] = df[variant_col].apply(lambda x: 23 if x.split(":")[0] == "X" else int(x.split(":")[0]))
            df[pos_col] = df[variant_col].apply(lambda x: int(x.split(":")[1]))
        else:
            df1[variant_col] = str(df1[chr_col]) + ':' + str(df1['pos_col'])
            df2[variant_col] = str(df2[chr_col]) + ':' + str(df2['pos_col'])
            df = pd.merge(df1, df2, on = variant_col).dropna()
        
        if trait_num == 0:
            x_labels = []
            x_labels_pos = []
            chrom_offset = {}
            chrom_start = {}
            chrom_offset_num = 0
            for chrom in range(1,23):
                chrom_offset[chrom] = chrom_offset_num
                chrom_start[chrom] = min(df[df[chr_col] == chrom][pos_col])
                x_labels.append(str(chrom))
                x_labels_pos.append(chrom_offset_num + (float(max(df[df[chr_col] == chrom][pos_col])) 
                                                        - float(min(df[df[chr_col] == chrom][pos_col])))/2)
                chrom_offset_num += max(df[df[chr_col] == chrom][pos_col]) - min(df[df[chr_col] == chrom][pos_col])
        
        if len(filenames1) > 1:
            trait_max = double_plot_multi(ax, ax2, df, chr_col, pos_col, chrom_offset, chrom_start, color_vec, label_vec, trait_num)
            if all_max < trait_max:
                all_max = trait_max
            if trait_num == 0:
                master_df = df
            else:
                master_df = pd.concat([master_df,df])
        else:
            all_max = double_plot_single(ax, ax2, df, chr_col, pos_col, chrom_offset, chrom_start, color_vec, trait_num)
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
        ax.hlines(y=-np.log10(p_threshold), xmin = 0, xmax = chrom_offset_num, linewidth = 1)
        ax2.hlines(y=np.log10(p_threshold), xmin = 0, xmax = chrom_offset_num, linewidth = 1)
    
    #Add SNP labels
    if locus_labels != None:
        locus_labels_1 = []
        locus_labels_2 = []
        label_file = open(locus_labels, 'r')
        for line in label_file:
            if line.rsplit('\t')[5].rstrip() == '1':
                locus_labels_1.append(line.rsplit('\t'))
            else:
                locus_labels_2.append(line.rsplit('\t'))
        add_locus_labels(ax, master_df, chr_col, pos_col, locus_labels_1, all_max + y_scale_padding, p_threshold, 1)
        add_locus_labels(ax2, master_df, chr_col, pos_col, locus_labels_2, all_max + y_scale_padding, p_threshold, 2)

    f.suptitle(title_str)
    
    if output_path == None:
        plt.show()
    else:
        plt.savefig(output_path, format = 'pdf', dpi = 400)

def double_plot_multi(ax, ax2, df, chr_col, pos_col, chrom_offset, chrom_start, color_vec, label_vec, trait_num):
    df['offset_num'] = df[chr_col].map(chrom_offset) - df[chr_col].map(chrom_start)
    df['IND'] = df[pos_col] + df['offset_num']
    ax.scatter(x = df['IND'], y = df['log_p1'], color = color_vec[trait_num], s = 3, label = label_vec[trait_num], rasterized = True)
    ax2.scatter(x = df['IND'], y = df['log_p2'], color = color_vec[trait_num], s = 3, rasterized = True)

    return max(max(df['log_p1'].tolist()), -min(df['log_p2'].tolist()))

def double_plot_single(ax, ax2, df, chr_col, pos_col, chrom_offset, chrom_start, color_vec, trait_num):
    df['offset_num'] = df[chr_col].map(chrom_offset) - df[chr_col].map(chrom_start)
    df['IND'] = df[pos_col] + df['offset_num']
    for chrom in range(1,23):
        tempdf = df[df[chr_col] == chrom]
        ax.scatter(x = tempdf['IND'], y = tempdf['log_p1'], color = color_vec[chrom%2], s = 3, rasterized = True)
        ax2.scatter(x = tempdf['IND'], y = tempdf['log_p2'], color = color_vec[chrom%2], s = 3, rasterized = True)

    return max(max(df['log_p1'].tolist()), -min(df['log_p2'].tolist()))

def add_locus_labels(ax, master_df, chr_col, pos_col, locus_labels_list, all_max, p_threshold, ax_num):
    horiz_align = ['left', 'right']
    locus_ind = 0
    vert_offset = -np.log10(p_threshold) + np.dot((all_max + np.log10(p_threshold))/len(locus_labels_list), range(0,len(locus_labels_list)))
    random.shuffle(vert_offset)
    for locus in locus_labels_list:
        df_temp = master_df[(master_df[chr_col] == int(locus[0])) & (master_df[pos_col] >= int(locus[1])) & (master_df[pos_col] <= int(locus[2]))]
        if ax_num == 1:
            df_ind = df_temp['log_p1'].argmax()
            point_coord = [int(df_temp.iloc[[df_ind]]['IND']),float(df_temp.iloc[[df_ind]]['log_p1'])]
            label_coord = [int(df_temp.iloc[[df_ind]]['IND']),vert_offset[locus_ind] + (all_max + np.log10(p_threshold))/(2*len(locus_labels_list))]
            if int(locus[0]) == 1 : alignment = 'left'
            elif int(locus[0]) >= 20: alignment = 'right'
            else: alignment = horiz_align[locus_ind % 2]
            ax.annotate(locus[3].rstrip(), xy=(point_coord), xytext=(label_coord), horizontalalignment = alignment, 
                        arrowprops=dict(arrowstyle="->"), color = locus[4].rstrip())
        else:
            df_ind = df_temp['log_p2'].argmin()
            point_coord = [int(df_temp.iloc[[df_ind]]['IND']),float(df_temp.iloc[[df_ind]]['log_p2'])]
            label_coord = [int(df_temp.iloc[[df_ind]]['IND']), - vert_offset[locus_ind] - (all_max + np.log10(p_threshold))/(2*len(locus_labels_list))]
            if int(locus[0]) == 1 : alignment = 'left'
            elif int(locus[0]) >= 20: alignment = 'right'
            else: alignment = horiz_align[locus_ind % 2]
            ax.annotate(locus[3].rstrip(), xy=(point_coord), xytext=(label_coord), horizontalalignment = alignment, 
                        arrowprops=dict(arrowstyle="->"), color = locus[4].rstrip())
        locus_ind += 1

