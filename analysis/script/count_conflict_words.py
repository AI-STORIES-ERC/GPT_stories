import pandas as pd

# Load the filtered word frequency file
word_freq = pd.read_csv("../data/filtered_word_freq.csv")

# Which words
conflict_words = [
    "battle", "clash", "conflict", "fight",
    "protest", "soldier", "violence", "war", "warrior",
    "gun", "sword", "knife", "weapon", "army", "military"
]

supernatural_words = ["magic", "guardian", "ghost", "spirit", "ritual", "curse",
                      "fairy"]

#words = conflict_words

# The following two lines look for words in the word_freq doc that match
# wikidata items that are instances of mythical creatures. The ONLY match is
# "beast" - showing that these culturally specific mythical creatures are not
# present in the stories. Another confounding factor is that many mythical
# creatures have multi-word labels.
#
#mythical_creatures_data = pd.read_csv("../data/wikidata_instance_of_mythical_creatures.csv")
#words = mythical_creatures_data["itemLabel"].tolist()


# Extract relevant rows
data = word_freq[word_freq["Word"].isin(words)].set_index("Word")

# Get only the columns that are country codes (ISO alpha-2)
country_cols = [c for c in word_freq.columns if len(c) == 2 and c.isupper()]

# Prepare dictionary of top 10 tables
tables = {}
for word in words:
    if word in data.index:
        counts = data.loc[word, country_cols].sort_values(ascending=False)
        top10 = counts.head(10).reset_index()
        top10.columns = ["Country", "Count"]
        tables[word] = top10

print(tables)

# Example: show top 10 for "war"



#print(tables["war"])
