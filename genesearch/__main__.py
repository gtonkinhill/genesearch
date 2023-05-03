from .summarise import *
from .search import *
import yaml
import importlib
from importlib.metadata import version
import sys
import os
import argparse
import logging


def get_options(args):

    description = 'genesearch: A tool to summarise the literature for a particluar gene in a species.'

    parser = argparse.ArgumentParser(description=description,
                                     prog='genesearch')

    search_opts = parser.add_argument_group('Input/output')
    search_opts.add_argument(
        "-g",
        "--gene",
        dest="gene",
        required=True,
        help="The gene name.",
        type=str)

    search_opts.add_argument(
        "-s",
        "--species",
        dest="species",
        required=True,
        help="The species name.",
        type=str)

    search_opts.add_argument("-n",
                         "--num-papers",
                         dest="number_papers",
                         help="Number of papers to summarise (default=3)",
                         default=3,
                         type=int)

     # Other options
    parser.add_argument('-l', '--loglevel', type=str.upper,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='INFO', help='Set the logging threshold.')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + version("genesearch"))

    args = parser.parse_args(args)
    return (args)





def main():

    # Load arguments
    args = get_options(sys.argv[1:])

    # set logging up
    logging.basicConfig(level=args.loglevel,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

    # Load API Keys
    apis = {}
    apis['google_api_key'] = os.getenv('GOOGLE_API_KEY')
    apis['google_engine_id'] = os.getenv('GOOGLE_ENGINE_ID')
    apis['openai_api_key'] = os.getenv('OPENAI_API_KEY')

    if None in apis.values()
        with importlib.resources.as_file(importlib.resources.files("genesearch").joinpath("api_keys.yaml")) as yaml_path:
            with open(yaml_path) as yaml_file:
                try:
                    apis = yaml.safe_load(yaml_file)
                except yaml.YAMLError as error:
                    print(f"Error reading YAML file: {error}")

    openai.api_key = apis['openai_api_key']

    # Define your search query
    query = f'"{args.gene}" {args.species}'

    # Call the custom Google Search API
    results = call_google_search_api(apis['google_api_key'], apis['google_engine_id'], query)

    # Download the text of the first 10 results
    texts = download_text_from_search_results(results, args.number_papers)
    texts = [text for text in texts if args.gene.lower() in " ".join(text).lower()]

    # split into chuncks and recursively summarise using GPT-3
    paper_summaries = []
    for paper in texts:
        paper_summaries.append(divide_and_conquer_cgpt(paper, args.gene))

    relevant_summaries = []
    for summary in paper_summaries:
        if is_species(summary, args.species):
            relevant_summaries.append(summary)

    if len(relevant_summaries)>1:
        logging.info("Merging paper summaries")
        final_summary = divide_and_conquer_cgpt(relevant_summaries, args.gene)
    elif len(relevant_summaries)==1:
        logging.info("Only a sinlge paper has been summaried.")
        final_summary = relevant_summaries[0]
    else:
        logging.warning("No relevant paper summaries found!")
        sys.exit(1)

    print(final_summary)

    return



if __name__ == '__main__':
    main()
