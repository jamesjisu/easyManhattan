# easyManhattan
![Logo](https://raw.githubusercontent.com/jamesjisu/easyManhattan/master/logo.png)

easyManhattan is an easy-to-use Python package to generate a variety of Manhattan plots, including double Manhattan plots, which can be used to explore differences in sex or other paired attributes

## Installation
You can install easyManhattan using `pip install easyManhattan`, or alternatively, by cloning this repository to your working directory. The following dependencies are required:
* numpy
* pandas
* matplotlib

## Usage
### Commands
To use easyManhattan on the command line, you can make use of the `easyManhattan` command. If installed using `pip`, you can use `python -m easyManhattan`; alternatively, if you cloned the repository, you can use `python path_to_cloned_repository/easyManhattan/easyManhattan`. The arguments are as follows: <br />   
`run.py [-h] --filenames FILENAMES1 [FILENAMES1 ...] [--double-filenames [FILENAMES2 [FILENAMES2 ...]]] --names LABEL_VEC [LABEL_VEC ...] --colors COLOR_VEC [COLOR_VEC ...] [--width X_SIZE] [--height Y_SIZE] [--y-break Y_SCALE_BREAK] [--y-padding Y_SCALE_PADDING] [--p-threshold P_THRESHOLD] [--y-labels Y_LABEL_VEC [Y_LABEL_VEC ...]] [--plot-title TITLE_STR] [--locus-labels LOCUS_LABELS] [--output-path OUTPUT_PATH]` <br />
where the arguments are <br />
*  `--filenames` List of summary statistic file paths 
*  `--double-filenames` List of second summary statistic file paths 
*  `--names` List of summary statistic trait names 
*  `--colors` List of marker colors for multiple traits, or list of 2 colors for alternating chromosome marker colors (choose color codes from [here](https://matplotlib.org/3.1.0/gallery/color/named_colors.html))
*  `--width` Desired width of the plot (in inches) 
*  `--height` Desired height of the plot (in inches) 
*  `--y-break` Y-axis break, to increase readability of the plot 
*  `--y-padding` Y-scale maximum padding, value added to y-axis maximum on plot scale 
*  `--p-threshold` Specify p-value threshold to plot a horizontal line (5e-8 usually used) 
*  `--y-labels` Labels for y-axis (1 for single Manhattan plot, 2 for double Manhattan plot) 
*  `--plot-title` Name of the plot 
*  `--locus-labels` Path to a tab-delimited file containing loci to be labeled (see formatting below)
*  `--output-path` Desired output path of plot <br />
The following arguments are also available using `easyManhattan -h` 

### Input Format
#### Summary Statistics
The summary statistics can take a variety of formats--the only required columns are a chromosome column, a position column, and a p-value.

#### Locus Labels
easyManhattan also has a simple labelling function as well, using matplotlib's `annotate` function. The labels must be specified in a file following the following format: <br />

**Single Manhattan Plot** <br />
Tab-delimited with 5 columns: CHR    Starting Position of Locus    Ending Position of Locus    Label    matplotlib Color Code <br />
Single-position loci can be specified by using the same position for the starting and ending position. <br />
Example: <br />
`1    123456    123456    GENE1    b` <br />
`5    2345678   2445678   GENE2    g` <br />
`13   456789    457789    GENE3    r` <br />
`20   123456    123456    GENE4    y` <br />

**Double Manhattan Plot** <br />
Tab-delimited with 6 columns: CHR    Starting Position of Locus    Ending Position of Locus    Label    matplotlib Color Code    Top or Bottom Plot (1 for top, 2 for bottom) <br />
Single-position loci can be specified by using the same position for the starting and ending position. <br />
Example: <br />
`1    123456    123456    GENE1    b    1` <br />
`5    2345678   2445678   GENE2    g    2` <br />
`13   456789    457789    GENE3    r    2` <br />
`20   123456    123456    GENE4    y    1` <br />

**Note: Locus label input files do NOT take a header line**



## Tutorial 
### Download
To begin, clone the easyManhattan repository with `git clone https://github.com/jamesjisu/easyManhattan.git` or by downloading from GitHub. You can run easyManhattan directly from this cloned repository or by installing the package with `pip install easyManhattan`

### Try Making a Plot
You can try making an example Manhattan plot using the provided `example.txt` summary statistics. Navigate to the top level of the repository, and use the following command `python -m easyManhattan --filenames example.txt --p-col pval --variant-col variant --names test1 --colors black grey --plot-title easyManhattan --output-path test.pdf`
. This will create the example plot as `example.pdf` in the top directory of the repository.
