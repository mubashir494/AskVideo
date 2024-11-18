import os
import logging
from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_groq import ChatGroq




logging.basicConfig(filename='output.log', level=logging.INFO)

def chat(video_id, prompt):
    """
    Starts a chat with the given prompt and returns the response.

    Args:
        podcast_id (str): The id of the podcast.
        episode_id (str): The id of the episode.
        prompt (str): The prompt to start the chat with.

    Raises:
        Exception: If an error occurs during the chat process.

    Returns:
        str: The response from the chat.
    """
    try:
        logging.info("------------ Starting chat ------------")

        prompt = str(prompt)

        DB_BASE_DIR = './db'
        HF_API_KEY = 'hf_qGGgLOoPJVtyHxxTBCkhFSZnLJcvGFM'
        GROQ_API_KEY = 'gsk_fGkvDnIOiDTypeO2lVFiWGdyb3FYr0fhV57wPr92gVrxiIpWm'
        
        
        if not HF_API_KEY:
            raise ValueError("HF_API_KEY not found in environment variables")
        
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        persist_directory = f"{DB_BASE_DIR}/{video_id}_vectorstore"

        if not os.path.exists(persist_directory):
            raise FileNotFoundError(f"Vectorstore not found at {persist_directory}")

        collection_name = f"vector_{video_id}_store"

        # Create the language model and embeddings

        embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=HF_API_KEY ,model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        #embeddings = OpenAIEmbeddings()

        # Access the vectorstore
        vectorstore = Chroma(embedding_function=embeddings, persist_directory=persist_directory, collection_name=collection_name)

        retriever = vectorstore.as_retriever()

        general_system_template = r""" 
        You have access to a podcast transcript. Assume you are the host answering the question the user asks you.
        ----
        {context}
        ---
        {question}
        ----
        """

        general_user_template = "Question:```{question}```"
        
        messages = [
            SystemMessagePromptTemplate.from_template(general_system_template),
            HumanMessagePromptTemplate.from_template(general_user_template)
        ]

        qa_prompt = ChatPromptTemplate.from_messages(messages)
        
        
        llm = ChatGroq(temperature=0.2, groq_api_key=GROQ_API_KEY, max_tokens=200, model_name="mixtral-8x7b-32768")
        
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, callbacks=[StreamingStdOutCallbackHandler()], verbose=True,)

        prompt = f"{prompt} (answer with a maximum of 200 tokens)"

        logging.info(f"Prompt: {prompt}")

        response  = qa.run(prompt, callbacks=[StreamingStdOutCallbackHandler()])

        logging.info("------------ Chat ended ------------")
        return response
    except Exception as e:
        logging.info(f"An error occurred: {e}")
        raise e

if __name__ == '__main__':
    chat('0c47c267-4981-11ef-8fbd-283a4d3fb3b6',"What is this about?")
