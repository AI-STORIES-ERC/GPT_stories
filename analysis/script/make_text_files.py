import pandas as pd
import os
#from docx import Document

def make_text_files(country, num_stories):
    """
    Create .txt and .docx files from a CSV file containing stories.
    
    Parameters:
    - country: The country code for the file (e.g. "AU").
    - num_stories: The number of stories to process.
    """
    input_path = f"../../data/{country}/{country}_stories.csv"
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The file {input_path} does not exist.")
    
    df = pd.read_csv(input_path)

    if num_stories > len(df):
        raise ValueError(f"Requested {num_stories} stories, but only {len(df)} available.")
    
    df = df.head(num_stories)

    output_dir = "../data/story_texts"
    os.makedirs(output_dir, exist_ok=True)

    for row in df.itertuples(index=False):
        story_id = row.Story_ID
        story_text = row.Story

        # Save as text file
        txt_path = os.path.join(output_dir, f"{story_id}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(story_text)

        # Save as Word document
        #doc = Document()
        #doc.add_heading(story_id, level=1)
        #doc.add_paragraph(story_text)
        #doc_path = os.path.join(output_dir, f"{story_id}.docx")
        #doc.save(doc_path)

    print(f"{num_stories} stories saved to {output_dir} as .txt")

if __name__ == "__main__":

    # Use this line to convert stories to txt for a single country
    make_text_files("AU", 50)

    '''
    # Use this to do all countries
    if __name__ == "__main__":
        # Path to CSV file with alpha-2 codes for each country
        country_csv = "/Users/jill.walker.rettberg/data_analysis/GPT_stories/support_data/country_data.csv"

        # Number of stories you want to convert to text per country
        NUM_STORIES = 20

        # Load the CSV
        countries_df = pd.read_csv(country_csv)

        # Loop through each alpha-2 code
        for code in countries_df["alpha-2"].dropna().astype(str):
            code = code.strip().upper()
            try:
                print(f"\nProcessing {code}…")
                make_text_files(code, NUM_STORIES)
            except Exception as e:
                print(f"❌ Error for {code}: {e}")
    '''