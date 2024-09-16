"""
    Calls the OpenAI API to generate short plot summaries and 
    save them to a csv file.

    The OpenAI API key must be saved as the first line of a plain text file 
    called key.txt. The first two lines after the libraries are imported reads
    the first line of key.txt, strips any whitespace, and sets it as the API 
    key. If you fork this repo, make sure never to commit your key.txt file to
    GitHub or a public repository - it should be in your .gitignore file. You
    should also make sure to set your maximum usage of tokens at the OpenAI site
    to an amount you can afford.

    The generate_stories function sends prompts to the OpenAI and requests a 
    plot summary as many times as specified.

    Only one prompt is sent to the model at a time, and no history is retained.
    This means that each story iteration is generated as though from a blank 
    slate, without knowledge of previous prompts or previously generated stories.

    [more explanation of the module]
 
    """
import os
import openai
import pandas as pd
from dotenv import load_dotenv
import csv




        
def load_api_key():
    """
    Loads the OpenAI API key from environment variables.

    This function uses python-dotenv to load environment variables from a .env file,
    retrieves the OPENAI_API_KEY, and sets it for the OpenAI client. If the API key
    is not found, it raises a ValueError.

    Raises:
    -------
    ValueError
        If the API key is not found in the environment variables.

    """
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("API Key not found. Please check your .env file or environment variables.")
    
    openai.api_key = api_key


# Load the API key when the module is imported
load_api_key()
    

def generate_stories(topics: list[str], number_of_stories_per_topic: int):
    """
    Generates a prompt for each item in the topics list, then sends each
    prompt to the OpenAI API to generate a plot summary as many times as
    specified by the number_of_stories_per_topic parameter.

    The basic structure of the prompt is "Write a 50 word plot summary for a
    potential [topic] children's novel." The generated plot summaries are saved to a pandas
    dataframe.

    I use the term "story" instead of "plot" in the code to avoid confusion with the
    plotting of data.

    Parameters
    ----------
    topics : list[str]
        A list of topics, e.g. cultures or countries. A prompt will be
        generated for each item in the list.
    number_of_stories_per_topic : int
        The number of plots to generate for each topic.

    Returns !!!!FINISH THIS LATER!!!!
    -------
    int
        A pandas dataframe containing the generated plots.

    Examples
    --------
    >>> generate_plots(["Native American", "Asian American"], 2)

    >>> generate_plots(["Norwegian", "Australian"], 3)

    """
    messages = [{"role": "system", "content": ""}]
    prompts = make_prompts(topics)
    stories = []


    # prints a statement about how many prompts are sent to the model and how many stories per prompt are generated by the model
    prompt_init_print(prompts, number_of_stories_per_topic)

    
    for prompt_number in range(len(prompts)):

        # prints the current prompt and how many prompts are given
        prompt_counter_print(prompts, prompt_number)

        for story_iteration in range(number_of_stories_per_topic):
            messages.append({"role": "user", "content": prompts[prompt_number]})
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.8,
                n=1,
            )
            # Extract the generated story from the response
            story = response.choices[0].message.content
            # create unique identifier for each story   
            story_id = f"{topics[prompt_number]}_{story_iteration+1}"
            stories.append((story_id, story, prompts[prompt_number], topics[prompt_number]))
            # Print the version and story
            print(f"\nVersion {story_iteration+1}: {story}")

    return stories

# create a csv file with the stories, prompts, and topics   
def create_dataset(stories):
    """
    Creates a CSV file with the generated stories, prompts, and topics.

    Parameters:
    -----------
    stories : list of tuples
        Each tuple contains (story, prompt, topic)

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the stories, prompts, and topics
    """
    # Create a DataFrame from the stories list
    df = pd.DataFrame(stories, columns=['Story ID', 'Story', 'Prompt', 'Topic'])

    # Generate a unique filename
    filename = input("\n---------------------\n\nEnter a filename for the dataset: ")+".csv"

    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False, quoting=csv.QUOTE_ALL)

    print(f"Dataset saved to {filename}")

    return df



def make_prompts(topics):
    """
    Makes a prompt for the story generation.
    """
    prompts = []
    try:
        for topic in topics:
            prompt = f"Write a 50 word plot summary for a potential {topic} children's novel."
            prompts.append(prompt)
        print("\n", len(prompts), "unique prompts generated.\n")
    except:
        print("Error: topics must be a list of strings.")
    return prompts









def prompt_init_print(prompts, number_of_stories_per_topic):
    # Print the number of unique prompts being sent to the OpenAI API
    # and the number of stories being generated for each prompt
    print(
        "Sending",
        len(prompts),
        "unique prompts to the OpenAI API, and generating",
        number_of_stories_per_topic,
        "stories for each prompt.",
    )

def prompt_counter_print(prompts, prompt_number):
    # Get the number of prompts
    num_of_prompts = len(prompts)
    
    # Iterate through each prompt and print its details
    print(
            "\n---------------------------------\n\nPrompt",
            prompt_number + 1,
            "of",
            num_of_prompts,
            ":",
            prompts[prompt_number],
        )



# ----- TESTS -----#


def test_make_prompts():
    topics = ["Native American", "Asian American"]
    prompts = make_prompts(topics)
    assert (
        prompts[0]
        == "Write a 50 word plot summary for a potential Native American children's novel."
    )
    assert (
        prompts[1]
        == "Write a 50 word plot summary for a potential Asian American children's novel."
    )


# ----- END OF TESTS -----#

if __name__ == "__main__":
    cultures = ["Native American", "Asian American"]
    
    countries = [
        "Norwegian", 
        "Japanese",
        "Australian",
        "American"
    ]

    
    
    stories = generate_stories(["Australian"], 100)
    dataset = create_dataset(stories)
    
