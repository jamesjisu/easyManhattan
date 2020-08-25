<<<<<<< HEAD
import random
=======
>>>>>>> f0680097e2a0c1640ffc1c8bbcc3defb72adc17a
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

<<<<<<< HEAD
def single_manhattan(filenames, chr_col, pos_col, p_col, variant_col, label_vec, color_vec, x_size, y_size, y_scale_break, y_scale_padding, p_threshold, y_label_vec, title_str, locus_labels, output_path):
=======
def single_manhattan(filenames, label_vec, color_vec, x_size, y_size, y_scale_break, y_scale_padding, p_threshold, y_label_vec, title_str, output_path):
>>>>>>> f0680097e2a0c1640ffc1c8bbcc3defb72adc17a
    f,ax = plt.subplots(1,1,sharex=True, facecolor='w', gridspec_kw={'hspace': 0})
    f.set_size_inches(x_size, y_size)
    all_max = 0
    trait_num = 0
    for filename in filenames:
        df = pd.read_csv(filename, sep = "\t")
<<<<<<< HEAD
        df['log_p'] = -np.log10(df[p_col])
        if variant_col != None:
            chr_col = 'CHR'
            pos_col = 'POS'
            df[chr_col] = df[variant_col].apply(lambda x: 23 if x.split(":")[0] == "X" else int(x.split(":")[0]))
            df[pos_col] = df[variant_col].apply(lambda x: int(x.split(":")[1]))
=======
        df['log_p'] = -np.log10(df.pval)
        df['CHR'] = df['variant'].apply(lambda x: 23 if x.split(":")[0] == "X" else int(x.split(":")[0]))
        df['LOC'] = df['variant'].apply(lambda x: int(x.split(":")[1]))
>>>>>>> f0680097e2a0c1640ffc1c8bbcc3defb72adc17a
        
        if trait_num == 0:
            x_labels = []
            x_labels_pos = []
            chrom_offset = {}
            chrom_start = {}
            chrom_offset_num = 0
            for chrom in range(1,23):
                chrom_offset[chrom] = chrom_offset_num
<<<<<<< HEAD
                chrom_start[chrom] = min(df[df[chr_col] == chrom][pos_col])
                x_labels.append(str(chrom))
                x_labels_pos.append(chrom_offset_num + (float(max(df[df[chr_col] == chrom][pos_col])) 
                                                        - float(min(df[df[chr_col] == chrom][pos_col])))/2)
                chrom_offset_num += max(df[df[chr_col] == chrom][pos_col]) - min(df[df[chr_col] == chrom][pos_col])
        
        if len(filenames) > 1:
            trait_max = single_plot_multi(ax, df, chr_col, pos_col, chrom_offset, chrom_start, color_vec, label_vec, trait_num)
=======
                chrom_start[chrom] = min(df[df['CHR'] == chrom]['LOC'])
                x_labels.append(str(chrom))
                x_labels_pos.append(chrom_offset_num + (float(max(df[df['CHR'] == chrom]['LOC'])) 
                                                        - float(min(df[df['CHR'] == chrom]['LOC'])))/2)
                chrom_offset_num += max(df[df['CHR'] == chrom]['LOC']) - min(df[df['CHR'] == chrom]['LOC'])
        
        if len(filenames) > 1:
            trait_max = single_plot_multi(ax, df, chrom_offset, chrom_start, color_vec, label_vec, trait_num)
>>>>>>> f0680097e2a0c1640ffc1c8bbcc3defb72adc17a
            if all_max < trait_max:
                all_max = trait_max
            if trait_num == 0:
                master_df = df
            else:
                master_df = pd.concat([master_df,df])
        else:
<<<<<<< HEAD
            all_max = single_plot_single(ax, df, chr_col, pos_col, chrom_offset, chrom_start, color_vec, trait_num)
=======
            all_max = single_plot_single(ax, df, chrom_offset, chrom_start, color_vec, trait_num)
>>>>>>> f0680097e2a0c1640ffc1c8bbcc3defb72adc17a
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
<<<<<<< HEAD
            ax.vlines(chrom_offset[chrom], ymin = 0, ymax = all_max + y_scale_padding, linestyles = 'dotted', linewidth = 1)
=======
            ax.vlines(chrom_offset[chrom], ymin = 0, ymax = all_max + 2, linestyles = 'dotted', linewidth = 1)
>>>>>>> f0680097e2a0c1640ffc1c8bbcc3defb72adc17a
        ax.legend(loc = 'upper left', bbox_to_anchor= (1.01, 1.01))

    #Horizontal cutoff lines
    if p_threshold != 0:
        ax.hlines(y=-np.log10(p_threshold), xmin = 0, xmax = chrom_offset_num, linewidth = 1)
<<<<<<< HEAD
        
    #Add SNP labels
    if locus_labels != None:
        locus_labels_list = []
        label_file = open(locus_labels, 'r')
        for line in label_file:
            locus_labels_list.append(line.rsplit('\t'))
        add_locus_labels(ax, master_df, chr_col, pos_col, locus_labels_list, all_max + y_scale_padding, p_threshold)
=======
>>>>>>> f0680097e2a0c1640ffc1c8bbcc3defb72adc17a

    f.suptitle(title_str)
    
    if output_path == None:
        plt.show()
    else:
        plt.savefig(output_path, format = 'pdf', dpi = 400)

<<<<<<< HEAD
def single_plot_multi(ax, df, chr_col, pos_col, chrom_offset, chrom_start, color_vec, label_vec, trait_num):
    df['offset_num'] = df[chr_col].map(chrom_offset) - df[chr_col].map(chrom_start)
    df['IND'] = df[pos_col] + df['offset_num']
    ax.scatter(x = df['IND'], y = df['log_p'], color = color_vec[trait_num], s = 3, label = label_vec[trait_num], rasterized = True)
    return max(df['log_p'].tolist())

def single_plot_single(ax, df, chr_col, pos_col, chrom_offset, chrom_start, color_vec, trait_num):
    df['offset_num'] = df[chr_col].map(chrom_offset) - df[chr_col].map(chrom_start)
    df['IND'] = df[pos_col] + df['offset_num']
    for chrom in range(1,23):
        tempdf = df[df[chr_col] == chrom]
        ax.scatter(x = tempdf['IND'], y = tempdf['log_p'], color = color_vec[chrom%2], s = 3, rasterized = True)
    return max(df['log_p'].tolist())

def add_locus_labels(ax, master_df, chr_col, pos_col, locus_labels_list, all_max, p_threshold):
    horiz_align = ['left', 'right']
    locus_ind = 0
    vert_offset = -np.log10(p_threshold) + np.dot((all_max + np.log10(p_threshold))/len(locus_labels_list), range(0,len(locus_labels_list)))
    random.shuffle(vert_offset)
    for locus in locus_labels_list:
        df_temp = master_df[(master_df[chr_col] == int(locus[0])) & (master_df[pos_col] >= int(locus[1])) & (master_df[pos_col] <= int(locus[2]))]
        df_ind = df_temp['log_p'].argmax()
        point_coord = [int(df_temp.iloc[[df_ind]]['IND']),float(df_temp.iloc[[df_ind]]['log_p'])]
        label_coord = [int(df_temp.iloc[[df_ind]]['IND']),vert_offset[locus_ind] + (all_max + np.log10(p_threshold))/(2*len(locus_labels_list))]
        if int(locus[0]) == 1 : alignment = 'left'
        elif int(locus[0]) >= 20: alignment = 'right'
        else: alignment = horiz_align[locus_ind % 2]
        ax.annotate(locus[3].rstrip(), xy=(point_coord), xytext=(label_coord), horizontalalignment = alignment, 
                    arrowprops=dict(arrowstyle="->"), color = locus[4].rstrip())
        locus_ind += 1
=======
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
>>>>>>> f0680097e2a0c1640ffc1c8bbcc3defb72adc17a
