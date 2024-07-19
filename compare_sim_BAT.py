import pandas as pd
import argparse
import matplotlib.pyplot as plt

# Define the column headers for the first file
columns1 = [
    "run_number", "event", "trigger", "peakIndex", 
    "L", "L_std", "x", "x_std", "y", "y_std"
]

# Define the column headers for the second file
columns2 = ["X", "Y"]

# Function to read the first TSV file using pandas
def read_tsv_file1(file_path):
    return pd.read_csv(file_path, sep='\t', header=None, names=columns1)

# Function to read the second TSV file using pandas
def read_tsv_file2(file_path):
    return pd.read_csv(file_path, sep='\t', header=None, names=columns2)

# Function to compare X and Y values and plot the results
def compare_and_plot(df1, df2):
    # Ensure both dataframes have the same length
    if len(df1) != len(df2):
        print("The two files have different numbers of rows.")
        return

    # Extract X and Y values from both dataframes
    x1 = df1['x']
    y1 = df1['y']
    x2 = df2['X']
    y2 = df2['Y']

    # Plot the results
    lines = plt.figure(1, figsize=(10, 5))

    # Plot X comparison
    plt.subplot(1, 2, 1)
    plt.plot(x1)
    plt.plot(x2)
    plt.xlabel('MC X')
    plt.ylabel('Fitted X')
    plt.title('Comparison of X Values')
    plt.legend()

    # Plot Y comparison
    plt.subplot(1, 2, 2)
    plt.plot(y1)
    plt.plot(y2)
    plt.xlabel('MC Y')
    plt.ylabel('Fitted Y')
    plt.title('Comparison of Y Values')
    plt.legend()

    plt.tight_layout()
    lines.show()

    ## --------------------------------------------------------------------

    # Compute differences
    diff_x = x1 - x2
    diff_y = y1 - y2

    # Plot histograms of the differences
    hists = plt.figure(2, figsize=(10, 5))

    # Histogram of X differences
    plt.subplot(1, 2, 1)
    plt.hist(diff_x, bins=50, alpha=0.7, color='blue')
    plt.xlabel('(X) Fit - MC [cm]')
    plt.ylabel('Frequency')
    plt.title('Histogram of X Differences')

    # Histogram of Y differences
    plt.subplot(1, 2, 2)
    plt.hist(diff_y, bins=50, alpha=0.7, color='green')
    plt.xlabel('(Y) Fit - MC [cm]')
    plt.ylabel('Frequency')
    plt.title('Histogram of Y Differences')

    plt.tight_layout()
    hists.show()

    input()

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Read two TSV files, compare their X and Y values, and plot histograms of the differences.")
    parser.add_argument("file1_path", type=str, help="Path to the first TSV file")
    parser.add_argument("file2_path", type=str, help="Path to the second TSV file")
    args = parser.parse_args()

    df1 = read_tsv_file1(args.file1_path)
    df2 = read_tsv_file2(args.file2_path)

    compare_and_plot(df1, df2)

if __name__ == "__main__":
    main()
