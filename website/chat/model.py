import torch
import numpy as np
import pandas as pd
from sentence_transformers import util, SentenceTransformer
from time import perf_counter as timer
import textwrap
from openai import OpenAI
import os
import sys

OPENAI_API_KEY="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"

def print_wrapped(text, wrap_length=80):
    wrapped_text = textwrap.fill(text, wrap_length)
    print(wrapped_text)

def retrieve_relevant_resources(query: str,
                                embeddings: torch.tensor,
                                model: SentenceTransformer,
                                n_resources_to_return: int=5,
                                print_time: bool=True):
    """
    Embeds a query with model and returns top k scores and indices from embeddings.
    """

    # Embed the query
    query_embedding = model.encode(query,
                                   convert_to_tensor=True)

    # Get dot product scores on embeddings
    start_time = timer()
    dot_scores = util.dot_score(query_embedding, embeddings)[0]
    end_time = timer()

    if print_time:
        print(f"[INFO] Time taken to get scores on {len(embeddings)} embeddings: {end_time-start_time:.5f} seconds.")

    scores, indices = torch.topk(input=dot_scores,
                                 k=n_resources_to_return)

    return scores, indices

def print_top_results_and_scores(query: str,
                                 embeddings: torch.tensor,
                                 model,
                                 pages_and_chunks: list[dict],
                                 n_resources_to_return: int=5,
                                 verbose: bool=False):
    """
    Takes a query, retrieves most relevant resources and prints them out in descending order.

    Note: Requires pages_and_chunks to be formatted in a specific way (see above for reference).
    """

    text_final = ''
    
    scores, indices = retrieve_relevant_resources(query=query,model=model,
                                                  embeddings=embeddings,
                                                  n_resources_to_return=n_resources_to_return, print_time=verbose)
    if verbose:
        print(f"Query: {query}\n")
        print("Results:")
    # Loop through zipped together scores and indicies
    for score, index in zip(scores, indices):
        text_final += pages_and_chunks[index]["sentence_chunk"]
        if verbose:
            print(f"Score: {score:.4f}")
            # Print relevant sentence chunk (since the scores are in descending order, the most relevant chunk will be first)
            print_wrapped(pages_and_chunks[index]["sentence_chunk"])
            # Print the page number too so we can reference the textbook further and check the results
            print(f"Page number: {pages_and_chunks[index]['page_number']}")
            print("\n")
        
    return text_final

def get_answer_from_query(model, query: str,
                    embeddings: torch.tensor,
                    pages_and_chunks: list[dict],
                    n_resources_to_return: int=5,
                    verbose: bool=False):

    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Get just the scores and indices of top related results
    # scores, indices = retrieve_relevant_resources(query=query,
    #                                             embeddings=embeddings)
 
    # Print out the texts of the top scores
    chunks = print_top_results_and_scores(query=query,
                                embeddings=embeddings, model=model, pages_and_chunks=pages_and_chunks)

    #prompt =  'Answer this question: \"\"' + query + '\"\" based on the information below. If the question is not relevant, answer: """Not relevant. How can I help you?""" \\"\"\"' + chunks + '\"\"\"'

    messages = [
        {"role": "system", "content": query + ' Use the information below and give a detailed answer, but do not mention the text. If the question is not relevant, answer: I do not have an answer to this question. How can I help you? \ \n'},
        {"role": "user", "content": chunks}
    ]

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages)
    
    if verbose:
        print(messages)
        print("")
        print("")
        print("")
        print("QUESTION:\n", query)
        print("RESPONSE:")
        print(response.choices[0].message.content)
        
    return response.choices[0].message.content

def get_embeddings_from_file(filename:str = "text_chunks_and_embeddings_df.csv"):
    # Import texts and embedding df
    text_chunks_and_embedding_df = pd.read_csv(filename)

    # Convert embedding column back to np.array (it got converted to string when it got saved to CSV)
    text_chunks_and_embedding_df["embedding"] = text_chunks_and_embedding_df["embedding"].apply(lambda x: np.fromstring(x.strip("[]"), sep=" "))

    # Convert texts and embedding df to list of dicts
    pages_and_chunks = text_chunks_and_embedding_df.to_dict(orient="records")   

    # Convert embeddings to torch tensor and send to device (note: NumPy arrays are float64, torch tensors are float32 by default)
    embeddings = torch.tensor(np.array(text_chunks_and_embedding_df["embedding"].tolist()), dtype=torch.float32).to("cpu")

    return embeddings, pages_and_chunks

def get_answer_from_RAG(query:str):

    embedding_model = SentenceTransformer(model_name_or_path="all-mpnet-base-v2", device="cpu") # choose the device to load the model to (note: GPU will often be *much* faster than CPU)

    embeddings, pages_and_chunks = get_embeddings_from_file()
    response = get_answer_from_query(query=query, embeddings=embeddings, pages_and_chunks=pages_and_chunks, model=embedding_model)
    
    return response 

def translate_to_english(query:str):
    client = OpenAI(api_key=OPENAI_API_KEY)
    messages = [
        {"role": "system", "content": "Translate into English the following sentence:  " +query}
    ]

    response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=messages)
        
    return response.choices[0].message.content

def translate_to_romanian(query:str):
    client = OpenAI(api_key=OPENAI_API_KEY)
    messages = [
        {"role": "system", "content": "Translate into Romanian the following sentence:  " + query}
    ]

    response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=messages)
        
    return response.choices[0].message.content

def get_answer_from_RAG_romanian(query:str):

    embedding_model = SentenceTransformer(model_name_or_path="all-mpnet-base-v2", device="cpu") # choose the device to load the model to (note: GPU will often be *much* faster than CPU)

    embeddings, pages_and_chunks = get_embeddings_from_file()
    
    query = translate_to_english(query=query)
    response = get_answer_from_query(query=query, embeddings=embeddings, pages_and_chunks=pages_and_chunks, model=embedding_model)
    response = translate_to_romanian(query=response)
    
    return response 


if __name__=="__main__":
    # query = "what is the maximum amount of money guaranteed by the europeean union?"
    query = "care este suma maximă de bani garantată de uniunea europeană?"

    print("QUERY: ")
    print_wrapped(query)
    response = get_answer_from_RAG_romanian(query)
    print("RESPONSE:")
    print_wrapped(response)

# get_answer_from_RAG_romanian(sys.argv[1])












# query = "is the bcr technical support 24/7?"
# query = "what is the maximum amount of money you can send in the app?"
# query = "what is the procedure for getting a loan?" # prost
# query = "what is the interest rates for deposits at BCR bank?"
# query = "what is the interest rate for deposits for 12 months deposit for RON?" # prost ~ prea multe numere
# query = "what is the maximum amount of money guaranteed by the europeean union?"
# query = "why do i have a fee for a money transfer to another bank?"
# query = "what have you eaten today?"
# print("QUESTION:\n", query)

# # Get just the scores and indices of top related results
# scores, indices = retrieve_relevant_resources(query=query,
#                                               embeddings=embeddings)
# # scores, indices

# # Print out the texts of the top scores
# chunks = print_top_results_and_scores(query=query,
#                              embeddings=embeddings)

# #prompt =  'Answer this question: \"\"' + query + '\"\" based on the information below. If the question is not relevant, answer: """Not relevant. How can I help you?""" \\"\"\"' + chunks + '\"\"\"'

# messages = [
#     {"role": "system", "content": query + '  based on the information below. If the question is not relevant, answer: I do not have an answer to this question. How can I help you? \ \n'},
#     {"role": "user", "content": chunks}
#   ]

# print(messages)
# print("")
# print("")
# print("")

# response = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=messages
# )
# print("QUESTION:\n", query)
# print("RESPONSE:")
# print(response.choices[0].message.content)