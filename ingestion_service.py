import os
import uuid
import logging
from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader


logging.basicConfig(filename='output.log', level=logging.INFO)
def ingestion_service(video_id):
    
    try:
        HF_API_KEY = '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'
        
        BASE_PATH = "./uploads"
        
        DB_BASE_PATH = "./db"
        
        status_file_path = f"./db/{video_id}.txt"
        
        logging.info("---------- Ingesting Transcript ---------")

        # check if Transcript Exist for this video
        if not os.path.exists(f'{BASE_PATH}/{video_id}.txt'):
            logging.info("Transcript for the file does not Exist")
            raise FileNotFoundError(f"Transcript Not Found")
        
        
        # Create a status file to indicate that the ingestion is in progress
        with open(status_file_path, 'w') as f:
            f.write('In progress')
            f.close()
        
        # Create the embeddings
        embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=HF_API_KEY ,model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Load the document from the Directory
        transcript_loader = DirectoryLoader(f'{BASE_PATH}/', glob=f"**/{video_id}.txt")
        loaders = [transcript_loader]
        documents = []
        for loader in loaders:
            documents.extend(loader.load())
            logging.info(f"Loaded {len(documents)} documents")
        
        
            
        # Split and process documents
        text_splitter = CharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
        documents = text_splitter.split_documents(documents)


        logging.info("Documents split into chunks")

        ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.page_content)) for doc in documents]
        unique_ids = list(set(ids))

        logging.info(f"Unique ids loaded: {len(unique_ids)}")

        seen_ids = set()

        logging.info("Removing duplicate documents")

        unique_docs = [doc for doc, id in zip(documents, ids) if id not in seen_ids and (seen_ids.add(id) or True)]
        
        logging.info(unique_docs)
        logging.info(f"Unique docs loaded: {len(unique_docs)}")    
        
        
        vectorstoreDB = Chroma.from_documents(
            unique_docs, 
            embeddings, 
            ids=unique_ids, 
            persist_directory=f"./{DB_BASE_PATH}/{video_id}_vectorstore",
            collection_name="vector_"+str(video_id)+"_store",
        )

        vectorstoreDB.persist()
        
        # Once the ingestion is done, delete the status file
        os.remove(status_file_path)
        
        logging.info("------------ Ingestion complete ------------")
    except Exception as e:
        
        # If an error occurs, update the status file with the error message
        with open(status_file_path, 'w') as f:
            f.write('Error\n')
            f.write(str(e))
            f.close()
            
         # If an error occurs, logging.info the error message to the console and raise it again
        logging.info(f"An error occurred: {e}")

if __name__ == '__main__':
    ingestion_service('5fb0e875-4935-11ef-a4e6-283a4d3fb3b6')