# GPT_stories: Scripts to generate and analyse stories for 236 nationalities using gpt-4o-mini 

By Hermann Wigers and Jill Walker Rettberg

[![DOI](https://zenodo.org/badge/650551217.svg)](https://doi.org/10.5281/zenodo.14938999)

## Introduction
This repository contains python scripts that generate stories by calling the GPT-API and for analysing them using different methods. The scripts and dataset were developed as part of the research project AI STORIES: Narrative Archetypes for Artificial Intelligence, which has received funding from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (Grant agreement No. 101142306). The project is also supported by the Center for Digital Narrative which is funded by the Research Council of Norway through its Centres of Excellence scheme, project number 332643.

## Setup
Ensure you have **Python installed** before running the scripts.  
You can check if Python is installed by running:

```
python --version
```
or
```
python3 --version
```
If Python is not installed, download it from python.org and follow the installation instructions.

---------------------------

We will be using the terminal to setup and run the scripts:
- First, navigate to the GPT_stories directory:
    - `cd ~/path/to/directory/GPT_Stories`
    - Verify your location with the `pwd` command. It should output 'GPT_Stories'
- Install the required libraries by running the command `pip install -r requirements.txt`.
    - There is a chance that the versions in requirements.txt are outdated. If you have any issues installing the dependencies using requirements.txt, it can also be done manually by writing `pip (or pip3) install openai`, `pip (or pip3) install pandas` etc. You'll also need Spacy's English language model, which can be downloaded with `python -m spacy download en_core_web_sm`
- Set up your OpenAI API.
    - You need an API key from OpenAI. 
    - If you do not already have one, create an account here https://openai.com/api/. When you are logged in, click on "Dashboard" in the top right corner of the OpenAI platform homepage, and then locate "API keys" in the menu on the left side of the screen (NOTE: The layout might change).
    - New users get some free credit; after that is used up you have to pay. You should make sure the spending limit on your OpenAI account is set to an amount that you can afford.
    - Create a .env file inside the repository and input the line: OPENAI_API_KEY="YOUR_API_KEY" where YOUR_API_KEY will be the key you created on OpenAIs website (NOTE: the .env file is mentioned in the .gitignore file and should not be uploaded to GitHub. If it's uploaded by mistake it will be deactivated immediately and you will have to generate a new one).
## Overview
*Go straight to 'Using the scripts' section below to see examples of running the code.*
- There are 7 scripts and 1 csv file in the GPT_Stories/script folder:
    - `country_codes.csv` Contains the country codes, demonyms, and country names for all 253 countries, including a line for default represented by the code 'XX'   
    - `story_cli.py` Runs all the other scripts
    - `generate_stories.py` Generates stories based on specified countries. 
    - `generate_summaries.py` Creates 50 word summaries for the stories
    - `name_extraction.py` Extracts the name of the protagonist for each story
    - `sentiment_analysis.py` Uses a transformer model to analyze the sentiment for each story
    - `noun_phrases.py` Extracts noun phrases from the stories
    - `word_freq.py` Counts word frequencies
- `story_cli.py` is the main script which will run all the other scripts using a Click interface. This script gives us two commands in the terminal:
    - `generate` which will generate the stories. This command takes two arguments and one option.
        - ARGUMENTS: `countries` (which countries we want to generate stories for, and `num_story_per_topic` (how many stories per country)
        - OPTIONS: `-s` or `startfrom`. You can choose which country to start from when generating for all the countries. This can be useful if the program was terminated before generating for all the countries.
    - `analyze` which takes the stories of your chosen countries and runs them through your 'analysis' of choice. `analyze` has one command and two options:
        - ARGUMENT: `countries` (which countries will be analyzed)
        - OPTIONS: `-a` or `analysis`. Type of analysis to run. 'all' for all types of analysis or specify one or more from this list: 'summaries', 'names', 'words', 'nouns',  'sentiments'. `-s` or `startfrom`. You can choose which country to start from when analysing all the countries.
          
- All output files will be stored in GPT_Stories/data (This directory will be created with the first generated story). Each country will have it's own directory where the alpha-2 code of the country will be the name of directory. 

### IMPORTANT NOTES: 
- `name_extraction.py` has to be run before `word_freq.py` since the list of names are used to remove the names from the word frequency lists. 
- `generate_summaries.py` has to be run before `sentiment_huggingface.py` since the sentiment analysis use the summaries instead of the full stories. This is because of the 512 token limit for the model used in this script.

## Using the scripts
- Navigate to the script folder `cd script`
- Generating stories:
    - Examples:
        - `python3 story_cli.py generate PS FR 1`            # this command will generate 1 story for Palestine and 1 story for France
        - `python3 story_cli.py generate all 50`          # this command will generate 50 stories for all countries
        - `python3 story_cli.py generate all 50 -s DK`    # this command will generate 50 stories for all countries, starting with Denmark
- Analyze stories
    - Examples:
        - `python3 story_cli.py analyze all -a all`       # this command will do all the analysis on all the countries
        - `python3 story_cli.py analyze all -a summary -a sentiment -s DK` # this command will generate summaries and do sentiment analysis on all countries starting with Denmark


