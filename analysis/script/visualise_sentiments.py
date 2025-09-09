import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from adjustText import adjust_text  # Prevent overlapping labels

#note: requires installing adjustText package
#pip install adjustText

def make_boxplot():
    df = pd.read_csv("analysis/data/all_countries_sentiments.csv")

    # Calculate sentiment counts
    sentiment_counts = calculate_sentiment_counts(df)

    # Convert the sentiment counts to a DataFrame suitable for boxplot
    sentiment_counts = sentiment_counts.stack().reset_index()
    sentiment_counts.columns = ['group_by', 'sentiment', 'count']

    # Ensure sentiment order is preserved
    sentiment_order = ['anger', 'fear', 'joy', 'love', 'sadness', 'surprise']
    sentiment_counts['sentiment'] = pd.Categorical(sentiment_counts['sentiment'], categories=sentiment_order, ordered=True)

    # Assign numerical codes AFTER sorting
    sentiment_counts = sentiment_counts.sort_values('sentiment')
    sentiment_counts['sentiment_code'] = sentiment_counts['sentiment'].cat.codes

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Boxplot with aligned labels
    sentiment_counts.boxplot(column='count', by='sentiment_code', grid=False, patch_artist=True, ax=ax,
                             flierprops=dict(marker='o', markersize=8, markerfacecolor='red', markeredgecolor='black'))

    # Set colors for the boxes
    colors = ['#A6CEE3', '#1F78B4', '#B2DF8A', '#33A02C', '#FB9A99', '#E31A1C']
    for box, color in zip(ax.patches[:len(colors)], colors):  # Ensure coloring works
        box.set_facecolor(color)
        box.set_alpha(0.6)  # Semi-transparent fill

    ax.set_title("Sentiment Counts by Sentiment", fontsize=14)
    ax.set_ylabel("Count", fontsize=12)
    ax.set_xlabel("Sentiment", fontsize=12)

    # **Ensure x-axis labels align correctly**
    box_positions = ax.get_xticks()  # Get actual tick positions
    ax.set_xticks(box_positions)  # Ensure proper positioning
    ax.set_xticklabels(sentiment_order, rotation=30, ha="right")  # Apply correct sentiment labels

    # **Fix outlier label placement using actual tick positions**
    texts = []
    for i, sentiment in enumerate(sentiment_order):
        sentiment_data = sentiment_counts[sentiment_counts['sentiment'] == sentiment]
        outlier_threshold = sentiment_data['count'].quantile(0.99)  # Select only extreme outliers
        outliers = sentiment_data[sentiment_data['count'] > outlier_threshold]
        
        for _, row in outliers.iterrows():
            text = ax.text(box_positions[i], row['count'], row['group_by'], fontsize=9, ha='center', va='bottom', color='black')
            texts.append(text)

    # Adjust text to prevent overlap
    adjust_text(texts, arrowprops=dict(arrowstyle="-", color='gray', alpha=0.5))

    plt.show()








def make_scatterplot():
    
    df = pd.read_csv("analysis/data/all_countries_sentiments.csv")

    # Create a scatter plot of the sentiment confidence scores
    df.plot.scatter(x='sentiment', y='confidence')
    plt.title("Sentiment by Confidence")
    plt.ylabel("Confidence")
    plt.xlabel("Sentiment")

    # Add labels for outliers
    for i, row in df.iterrows():
        if row['confidence'] > df['confidence'].quantile(0.95):  # Adjust the threshold as needed
            plt.text(row['sentiment'], row['confidence'], row['country_name'], fontsize=8, ha='right')

    plt.show()



def calculate_sentiment_counts(df, group_by="country_name", region=None, sub_region=None, country_list=None):
    """
    Aggregates sentiment counts based on the selected grouping level.

    Parameters:
    - df (DataFrame): The dataset containing sentiment labels.
    - group_by (str): "country", "region", or "sub-region".
    - region (str, optional): If specified, filters data to this specific region.
    - sub_region (str, optional): If specified, filters data to this specific sub-region.
    - country_list (list, optional): If specified, filters data to these specific countries.

    Returns:
    - DataFrame with sentiment counts aggregated by the grouping level.
    """

    # Apply filters
    if region:
        df = df[df["region"] == region]
    if sub_region:
        df = df[df["sub-region"] == sub_region]
    if country_list:
        df = df[df["country_name"].isin(country_list)]

    #rename country_names United States of America (the) to USA, Korea (the Republic of) to South Korea, Korea (the Democratic People's Republic of) to North Korea, United Kingdom of Great Britain and Northern Ireland (the) to United Kingdom, Bolivia (Plurinational State of) to Bolivia
    df['country_name'] = df['country_name'].replace({
        "United States of America (the)": "USA",
        "Korea (the Republic of)": "South Korea",
        "Korea (the Democratic People's Republic of)": "North Korea",
        "United Kingdom of Great Britain and Northern Ireland (the)": "United Kingdom",
        "Bolivia (Plurinational State of)": "Bolivia",
        "Taiwan (Province of China)": "Taiwan",
        "Russian Federation (the)": "Russia",
        "Iran (Islamic Republic of)": "Iran",
        "Venezuela (Bolivarian Republic of)": "Venezuela",
    })

    # Aggregate sentiment counts by the chosen group level
    return df.groupby([group_by, "sentiment"]).size().unstack(fill_value=0)


def make_proportional_stacked_barchart(df, 
                                       group_by="country_name", 
                                       region=None, 
                                       sub_region=None, 
                                       country_list=None,
                                       filename="unnamed"):
    """
    Creates a proportional stacked bar chart of sentiment distribution.
    
    Parameters:
    - df (DataFrame): The dataset containing sentiment data.
    - group_by (str): Aggregation level, "country", "region", or "sub-region".
    - region (str, optional): If specified, filters data to this specific region.
    - sub_region (str, optional): If specified, filters data to this specific sub-region.
    - country_list (list, optional): If specified, filters data to these specific countries.
    
    Returns:
    - A stacked bar chart showing proportional sentiment distribution.
    """

    # Filter by region if specified
    if region:
        df = df[df["region"] == region]
    
    # Filter by sub-region if specified
    if sub_region:
        df = df[df["sub-region"] == sub_region]
    
    # Filter by country list if specified
    if country_list:
        df = df[df["country_name"].isin(country_list)]

    # Calculate sentiment counts based on grouping level
    sentiment_counts = calculate_sentiment_counts(df, group_by=group_by)

    # Define fixed colours for each sentiment
    sentiment_colours = {
        "sadness": "blue",
        "love": "red",
        "anger": "brown",
        "joy": "lightgreen",
        "surprise": "pink",
        "fear": "orange"
    }
    
    # Convert to proportions
    sentiment_proportions = sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0)

    # Ensure the colours are applied in the correct order
    available_sentiments = sentiment_proportions.columns.tolist()
    colours = [sentiment_colours[sent] for sent in available_sentiments if sent in sentiment_colours]

    # Plot
    plt.figure(figsize=(14, 7))
    sentiment_proportions.plot(kind="bar", 
                               stacked=True, 
                               figsize=(14, 7),
                               color=colours)

    # Title and labels
    title = "Proportional Sentiment Distribution"
    if region:
        title += f" in {region}"
    if sub_region:
        title += f" in {sub_region}"
    if country_list:
        title += f" for Selected Countries"
    
    plt.title(title)
    plt.ylabel("Proportion of Sentiments")
    plt.xlabel(group_by.replace("_", " ").title())
    plt.xticks(rotation=45, ha="right")  # Ensure country names are readable
    plt.legend(title="Sentiment", bbox_to_anchor=(1, 1), loc='upper left')
    plt.tight_layout()  # Adjust layout to fit labels
    plt.show()

        # Save the plot

    output_path=(f"analysis/figures/sentiments_{filenmae}.png")

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.show()  # Show the plot for interactive environments

# def make_boxplot(df):

#     df_melted = df.melt(
#     id_vars=["sentiment"], 
#     value_vars=["country_name"], 
#     var_name="Country", 
#     value_name="Frequency")
#     print(df_melted)    

#     plt.figure(figsize=(14, 6))

#     # Create a box plot with visible outliers
#     ax = sns.boxplot(data=df, x="")
#     plt.show()



def sort_sentiments(sentiment, df, group_by="country", region=None, country_list=None):
    """
    Sorts the DataFrame by the specified sentiment in descending order.
    
    Parameters:
    - df (pd.DataFrame): The DataFrame to sort.
    - sentiment (str): The sentiment column to sort by.
    
    Returns:
    - The sorted DataFrame.
    """
    sentiment_counts = calculate_sentiment_counts(df, group_by=group_by, region=region, country_list=country_list)
    
    # Convert to proportions
    sentiment_proportions = sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0)

    sorted_sentiments = sentiment_proportions.sort_values(by=sentiment, ascending=False)
    print(sorted_sentiments.head(20))

if __name__ == "__main__":
    # Load the dataset
    df = pd.read_csv("analysis/data/all_countries_sentiments.csv")

    # Example usage of make_proportional_stacked_barchart function
    #make_boxplot(df="analysis/data/all_countries_sentiments.csv")

    # Uncomment the following lines to generate other visualizations or analyses

    # Generate proportional stacked bar chart by country
    #make_proportional_stacked_barchart(df, group_by="country_name")

    # Generate proportional stacked bar chart by sub-region
    #make_proportional_stacked_barchart(df, group_by="sub-region")

    # Generate proportional stacked bar chart for  region
    #make_proportional_stacked_barchart(df, group_by="country_name", region="Asia", filename="Asia")


    # Generate proportional stacked bar chart for a specific list of countries
    #make_proportional_stacked_barchart(df, group_by="country_name", country_list=["USA", "United Kingdom", "North Korea", "Austria"])

    # Sort sentiments by 'fear' for each country
    sort_sentiments("fear", df, group_by="region", region="Asia")
    #print(sort_sentiments("sadness", df, group_by="country_name")) #only shows european countriess???

    #make_proportional_stacked_barchart(df, group_by="sub-region")

    