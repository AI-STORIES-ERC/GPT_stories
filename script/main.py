import click
from generate_stories import main as generate_stories
from analyze_stories import main as analyze_stories
from name_extraction import main as extract_names
from noun_phrases import main as extract_noun_phrases
from sentiment_analysis_textblob import main as tb_sentiment
from sentiment_huggingface import main as hf_sentiment
from watson_sentiment import main as watson_sentiment
from word_compare import main as word_compare
from word_freq import main as word_freq



@click.group()
@click.pass_context()
def cli(ctx):
    """CLI for story processing tasks."""
    ctx.ensure_object(dict)
    pass

@cli.command()
@click.argument('countries')
@click.argument('num_story_per_topic', type=int)
@click.pass_context()
def generate(ctx, countries, num_story_per_topic):
    """Generate stories."""
    ctx.obj['stories'] = generate_stories(countries, num_story_per_topic)

@cli.command()
@click.pass_context()
def analyze(ctx):
    """Analyze stories."""

    analyze_stories(ctx)

@cli.command()
@click.pass_context()
def extract_names(ctx):
    """Extract names from stories."""
    extract_names(ctx)

@cli.command()
@click.pass_context()
def extract_noun_phrases(ctx):
    """Extract noun phrases from stories."""
    extract_noun_phrases(ctx)

@cli.command()
@click.pass_context()
def tb_sentiment_analysis(ctx):
    """Perform sentiment analysis using TextBlob."""
    tb_sentiment(ctx)

@cli.command()
@click.pass_context()
def hf_sentiment_analysis(ctx):
    """Perform sentiment analysis using HuggingFace."""
    hf_sentiment(ctx)

# @cli.command()
# def watson_sentiment_analysis():
#     """Perform sentiment analysis using Watson."""
#     watson_sentiment()

@cli.command()
@click.pass_context()
def compare_words(ctx):
    """Compare words in stories."""
    word_compare(ctx)

@cli.command()
@click.pass_context()
def word_frequency(ctx):
    """Calculate word frequency in stories."""
    word_freq(ctx)

if __name__ == '__main__':
    cli()