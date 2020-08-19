# easyManhattan
easyManhattan is an easy-to-use Python package to generate a variety of Manhattan plots, including double Manhattan plots, which can be used to explore differences in sex or other paired attributes

## Installation
You can install easyManhattan using `pip install easyManhattan`, or alternatively, by cloning this repository to your working directory. The following dependencies are required:
* numpy
* pandas
* matplotlib

## Usage
To use easyManhattan on the command line, you can make use of the `easyManhattan` command.  
`run.py [-h] --filenames FILENAMES1 [FILENAMES1 ...] [--double-filenames [FILENAMES2 [FILENAMES2 ...]]] --names LABEL_VEC [LABEL_VEC ...] --colors COLOR_VEC [COLOR_VEC ...] [--width X_SIZE] [--height Y_SIZE] [--y-break Y_SCALE_BREAK] [--y-padding Y_SCALE_PADDING] [--p-threshold P_THRESHOLD] [--y-labels Y_LABEL_VEC [Y_LABEL_VEC ...]] [--plot-title TITLE_STR] --output-path OUTPUT_PATH` <br />
where the arguments are <br />
*  `--filenames FILENAMES1 [FILENAMES1 ...]` List of summary statistic file paths 
*  `--double-filenames [FILENAMES2 [FILENAMES2 ...]]` List of second summary statistic file paths 
*  `--names LABEL_VEC [LABEL_VEC ...]` List of summary statistic trait names 
*  `--colors COLOR_VEC [COLOR_VEC ...]` List of marker colors for multiple traits, or list of 2 colors for alternating chromosome marker colors 
*  `--width X_SIZE` Desired width of the plot (in inches) 
*  `--height Y_SIZE` Desired height of the plot (in inches) 
*  `--y-break Y_SCALE_BREAK` Y-axis break, to increase readability of the plot 
*  `--y-padding Y_SCALE_PADDING` Y-scale maximum padding, value added to y-axis maximum on plot scale 
*  `--p-threshold P_THRESHOLD` Specify p-value threshold to plot a horizontal line (5e-8 usually used) 
*  `--y-labels Y_LABEL_VEC [Y_LABEL_VEC ...]` Labels for y-axis (1 for single Manhattan plot, 2 for double Manhattan plot) 
*  `--plot-title TITLE_STR` Name of the plot 
*  `--output-path OUTPUT_PATH` Desired output path of plot <br />
The following arguments are also available using `easyManhattan -h` 


## Tutorial
