#python compare_sim_BAT_v2.py fitted_dx_XXX.txt dx_XXX_mc_truth.txt fitted_dx_YYY.txt /dx_YYY_mc_truth.txt ...

import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np

# Define the column headers for the first file
columns1 = [
    "run_number", "event", "trigger", "peakIndex", 
    "L", "L_std", "x", "x_std", "y", "y_std"
]

# Define the column headers for the subsequent files
columns2 = ["X", "Y"]

# Function to read the first TSV file using pandas
def read_tsv_file1(file_path):
    return pd.read_csv(file_path, sep='\t', header=None, names=columns1)

# Function to read subsequent TSV files using pandas
def read_tsv_file2(file_path):
    return pd.read_csv(file_path, sep='\t', header=None, names=columns2)

# Function to compare X and Y values and plot the results
def compare_and_plot(pairs, bins, args):
    # Get the legend labels from the file names
    legend_labels = [file_path.split('/')[-1].split('.')[0].split('_')[-1] for file_path in args.file_paths[::2]]

    plt.subplot(1, 2, 1)
    for i, (df1, df2) in enumerate(pairs):
        diff_x = df1['x'] - df2['X']

        if legend_labels[i] == "0833":
            plt.hist(diff_x, bins=bins, alpha=0.5, label= "DX = -" + legend_labels[i],stacked=True)
        else:
            plt.hist(diff_x, bins=bins, alpha=0.5, label= "DX = " + legend_labels[i], stacked=True)
    plt.xlabel('Difference (x1 - x2)')
    plt.ylabel('Frequency')
    plt.title('Histogram of X Differences')
    plt.legend()



    # Plot histograms of the Y differences
    plt.subplot(1, 2, 2)
    for i, (df1, df2) in enumerate(pairs):
        diff_y = df1['y'] - df2['Y']

        if legend_labels[i] == "0833":
            plt.hist(diff_y, bins=bins, alpha=0.4, label= "DX = -" + legend_labels[i], stacked=True)
        else:
            plt.hist(diff_y, bins=bins, alpha=0.4, label= "DX = " + legend_labels[i], stacked=True)

    plt.xlabel('Difference (y1 - y2)')
    plt.ylabel('Frequency')
    plt.title('Histogram of Y Differences')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Read multiple TSV files in pairs, compare their X and Y values, and plot overlaid histograms of the differences.")
    parser.add_argument("file_paths", type=str, nargs='+', help="Paths to the TSV files to compare in pairs")
    parser.add_argument("--bins", type=int, default=30, help="Number of bins for the histogram")
    args = parser.parse_args()

    # Ensure an even number of file paths is provided
    if len(args.file_paths) % 2 != 0:
        print("Please provide an even number of file paths.")
        return

    # Read the files in pairs
    pairs = []
    for i in range(0, len(args.file_paths), 2):
        df1 = read_tsv_file1(args.file_paths[i])
        df2 = read_tsv_file2(args.file_paths[i+1])
        pairs.append((df1, df2))

    compare_and_plot(pairs, args.bins,args)

if __name__ == "__main__":
    main()
