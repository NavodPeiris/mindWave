
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import CTransformers
import sys
import os

from text_to_speech import text_to_speech

def document_query(query):

    # Check if folder exists, if not create it
    if not os.path.exists('summaries'):
        os.makedirs('summaries')

    # Step 1: Load the Text Files from Data Path
    loader=DirectoryLoader('summaries/',
                        glob="*.txt")

    documents=loader.load()

    #***Step 2: Split Text into Chunks***
    text_splitter=RecursiveCharacterTextSplitter(
                                                chunk_size=500,
                                                chunk_overlap=50)

    text_chunks=text_splitter.split_documents(documents)

    #**Step 3: Load the Embedding Model***
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device':'cpu'})

    #**Step 4: Convert the Text Chunks into Embeddings and Create a FAISS Vector Store***
    vector_store=FAISS.from_documents(text_chunks, embeddings)

    llm=CTransformers(model="llama2\llama-2-7b-chat.ggmlv3.q4_0.bin",
                    model_type="llama",
                    config={'max_new_tokens':128,
                            'temperature':0.01})

    template="""Use the following pieces of information to answer the user's question.
    user ask for a summary of information about a mental health patient's activities during a specific day. please return list of moods patient had during day, number of times screamed, number of times patient repeated same word, average response time, number of times patient did not respond is ?, number of times patient give a related answer, number of times patient give an unrelated answer.
    If you dont know the answer just say you don't know, don't try to make up an answer.

    Context:{context}
    Question:{question}

    Only return the helpful answer below and nothing else
    Helpful answer
    """

    qa_prompt=PromptTemplate(template=template, input_variables=['context', 'question'])

    chain = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type='stuff',
                                    retriever=vector_store.as_retriever(search_kwargs={'k': 2}),
                                    return_source_documents=True,
                                    chain_type_kwargs={'prompt': qa_prompt})

    response=chain({'query': query})
    result = response['result']
    print("Alice Says: ", result)
    return result

'''
res = document_query("give me summary about patient number 4 on 4th of october 2023")
#text_to_speech(res)
'''


