# genesearch


An experimental program created at the **9th Microbes & Food Safety Bioinformatics Hackathon** to summarise the literature for a particular gene using Chat-GPT


The algorithm searches PubMed for literature on a particular gene within a species. It then uses Chat-GPT to generate summaries in a hierarchical manner first for each paragraph, then each paper and finally for the set of papers.


The program requires OpenAI and Google search API's that must be supplied by the user.




### Installation


The easiest way to install the program is to clone the GitHub repository and install using pip. To include the API's create a file called `api_keys.yaml` and place it in the folder `genesearch/genesearch/`. The file should be formatted as 


```
google_api_key: "your google API key"
google_engine_id: "your google search engine ID"
openai_api_key: "your openAI API key"
```

Alternatively you can set environment variables by running

```
export GOOGLE_API_KEY="your google API key"
export GOOGLE_ENGINE_ID="your google search engine ID"
export OPENAI_API_KEY="your openAI API key"
```

The program can then be installed by running

```
cd genesearch
pip install .
```


### Running the program


After installation the program can be run by specifying the gene and species as


```
genesearch -g "gene name" -s "species name"
```


### Options


```
usage: genesearch [-h] -g GENE -s SPECIES [-n NUMBER_PAPERS] [--quiet]
                  [--version]


genesearch: A tool to summarise the literature for a particular gene in a
species.


optional arguments:
  -h, --help            show this help message and exit
  --quiet               suppress additional output
  --version             show program's version number and exit


Input/output:
  -g GENE, --gene GENE  The gene name.
  -s SPECIES, --species SPECIES
                        The species name.
  -n NUMBER_PAPERS, --num-papers NUMBER_PAPERS
                        Number of papers to summarise (default=3)
```



