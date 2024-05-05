# ChatGPT-like website with RAG model for legal documents in banking

_Toro Rosso Project HackITall 2024 April. This project has been presented in a hackathon._

## RAG model

### Detailed diagram
![alt text](/model_training/assets/simple-local-rag-workflow-flowchart.png)

### General Usage

`Modifed_RAG_with_sentence_transformer.ipynb` generates the word embedding file `text_chunks_and_embeddings_df.csv`. It requires a relatively strong computing power to run the `all-mpnet-base-v2` word embedding model from sentence_transformer, thus Google Colab can be a good idea. 

The `model.py` uses the word_embeddings previously generated to answer questions. It can be run in CLI or it can be imported to another file. It uses the OpenAI API to translate the queries into Romanian, to retrieve the top k most relevant contexts from the `.csv` file, uses `gpt-3.5-turbo` 
model from OpenAI to generate a coherent answer using information from the retrieved contexts, and later translates it back to Romanian. 

### Documents Database and Word Embeddings

See [General Business Terms](/pdfs/General-business-terms-and-conditions-for-legal-entities-and-self-employed-individuals-version-no-25-5-May-2023.pdf) to see an example of a pre-processed document. Multiple chunks(contexts) excerpted from these kinds of documents are projected onto the word embedding vector space (two word embedding of closely related chunks in meaning are close in the vector space). When a query is processed, it is projected onto the vector space and the top k nearest embeddings in the vector space are the most relevant chunks of text. 

![](/model_training/assets/images.jpeg)

## Flask Server and API calls
After the model was prepared, it was connected to a Flask backend.  
For the fronted we were inspired by BCR's George and ChatGPT. Thus we choose a this modern and clean design.
![alt text](/website/assets/georgeta.jpeg)

The user has feedback for every question. Also, we there is local history on the left of the page.

All the messages are saved locally, on the session. After the page is reloaded, all the answers are deleted
![alt text](/website/assets/georgeta_more_questions.jpeg)

#### Endpoints

- `POST /execute-python-script`: Here, the answer from the RAG is returned.

## Run
We created an automated script to run the server. See [run.sh]("/website/chat/run.sh"). 


