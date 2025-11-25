import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_top_words_boxplot(csv_path="..analysis/data/filtered_word_freq.csv", 
                           num_words=20, 
                           output_path="../analysis/figures/top_words_boxplot.png"):
    """
    Reads a CSV file containing word frequencies by country, selects the top N words globally,
    and generates a boxplot of their frequency distribution across countries.

    Parameters:
    - csv_path (str): Path to the CSV file containing the data.
    - num_words (int): Number of top words to include in the analysis.
    - output_path (str): Path to save the generated plot.
    """

    # Load data
    df = pd.read_csv(csv_path)

    # Identify country columns (excluding metadata)
    country_columns = [col for col in df.columns if col not in ["Word", "global_freq", "num_countries"]]

    # Identify the top N most used words based on global frequency
    top_words = df.nlargest(num_words, "global_freq")["Word"]

    # Filter dataset to only include the top words
    #df_top = df[df["Word"].isin(top_words)]
    ## **** NOTE TESTING HERE REMOVE IF DOESNT WORK ****
    df_top = df[df["Word"].isin(["fight", "protest","clash","soldier","war"])]

    # Sort words by global frequency in descending order
    df_top_sorted = df_top.sort_values(by="global_freq", ascending=False)

    # Melt the DataFrame for visualization
    df_melted = df_top_sorted.melt(id_vars=["Word"], value_vars=country_columns, var_name="Country", value_name="Frequency")
    print(df_melted)
    # Set up the figure
    plt.figure(figsize=(14, 6))

    # Create a box plot with visible outliers
    ax = sns.boxplot(data=df_melted, x="Word", y="Frequency", showfliers=True, order=df_top_sorted["Word"])

    # Annotate key outliers
    for i, word in enumerate(df_top_sorted["Word"]):
        word_data = df_melted[df_melted["Word"] == word]

        # Find the country with the highest frequency for each word
        max_freq_row = word_data.loc[word_data["Frequency"].idxmax()]

        # Find the 90th percentile as an additional threshold for outliers
        q90 = word_data["Frequency"].quantile(0.90)
        high_outliers = word_data[word_data["Frequency"] >= q90]

        # Annotate max frequency country with jitter
        ax.text(
            x=i,
            y=max_freq_row["Frequency"] + 20,  # Offset label
            s=max_freq_row["Country"],
            horizontalalignment='center',
            verticalalignment='bottom',
            fontsize=12,
            color='red',
            fontweight='bold'
        )

    # Customize plot appearance
    plt.ylim(bottom=0, top=max(df_melted["Frequency"]))  # Adjust y-axis
    plt.title(f"Top {num_words} Most Used Words - Frequency Distribution Across Countries", fontsize=14)
    plt.xlabel("Word", fontsize=10)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(rotation=90, fontsize=12)
    plt.yticks(fontsize=12)

    # Save the plot
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.show()  # Show the plot for interactive environments

# Example usage:
# plot_top_words_boxplot()

plot_top_words_boxplot("analysis/data/regional_word_freq.csv", 
20, "analysis/figures/regional_top_words_boxplot.png")

