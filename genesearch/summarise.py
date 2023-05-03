import openai
import logging


def call_openai_chat_api(prompt, model="gpt-3.5-turbo"):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return completion.choices[0].message.content


def divide_and_conquer_cgpt(paragraphs, gene, max_para=100):
    summaries = paragraphs

    while len(summaries) > 1:
        paragraphs = summaries
        summaries = []
        i = 0
        for p in paragraphs:
            gene_mentioned = gene.lower() in p.lower()
            response_text = ""
            has_appended = False

            if i >= 2 and not gene_mentioned:
                continue
            if i > max_para: continue
            # if not gene_mentioned: continue

            # Define your prompt (message)
            prompt = f'Please summarise the following paragraph in less than 200 words: "{p}".'
            if gene_mentioned:
                prompt += (
                    f" Focus on the description of the gene {gene} in the paragraph."
                )

            # Call the OpenAI Chat API
            response_text = call_openai_chat_api(prompt)

            if i % 2 == 1:
                summaries.append(prev + " " + response_text)
                has_appended = True
            else:
                prev = response_text

            i += 1

            logging.info(f"Summarising paragraph: {i}")

        if not has_appended:
            summaries[-1] = summaries[-1] + " " + response_text

    prompt = f'Please summarise the description of gene {gene} in the following paragraph: "{summaries[0]}".'

    # Call the OpenAI Chat API
    response_text = call_openai_chat_api(prompt)

    logging.info("Final paper summary:")
    logging.info(response_text)

    return response_text


def is_species(text, species):
    prompt = f'Does this paragraph focus on the species {species}? "'

    prompt += text

    prompt += '" Only answer with the words "Yes" or "No" and nothing else'

    # Call the OpenAI Chat API
    response_text = call_openai_chat_api(prompt)
    rtlower = response_text.lower()
    print(response_text)

    if "no" in rtlower:
        return False
    elif "yes" in rtlower:
        return True
    else:
        print("Did not answer with yes or no!")
        sys.exit(1)

    return None
