import json
import os
import whisperx
import torch
import threading
from ingestion_service import ingestion_service


def process_transcript(transcript):
    """
    Process a transcript creating a full script
    
    Parameters:
        transcript (list): The transcript to process.

    Returns:
        list: The processed transcript.
    """
    try:
        # Define the Seek Interval, in seconds
        script = ""
        
        # Go through each line in the transcript
        for line in transcript:
            script += line['text'] 

        return script

    except Exception as e:
        raise Exception(f"Error processing transcript: {e}")

def create_transcript_whisperx(audio_path,  model_name="base", batch_size=4, compute_type="int8", device="cpu"):
    """
    Transcribe an audio file using WhisperX and save the transcript to a JSON file.
    Rapidly transcribes audio files using WhisperX with word alignments and eventually adds speaker labels.
    
    Parameters:
        audio_path (str): The path to the audio file to transcribe. Required.
        model_name (str): The name of the WhisperX model to use. Default is "base".
        batch_size (int): The batch size to use for transcription. Default is 4.
        compute_type (str): The compute type to use for transcription. Default is "int8".
        device (str): The device to use for transcription. Default is "cpu".
        
    Returns:
        None    
    
    """
    try:
        print('------------ Creating WhisperX Transcript ------------')

        print(f'Creating transcript using WhisperX for {audio_path}')

        ext = audio_path.split('.')[-1]

        # Get the file name
        file_name = audio_path.split(f'.{ext}')[0]

        # Define the transcript file path
        transcript_file_path = f'{file_name}.txt'
        
        video_id = file_name.split('/')[-1]
        
        # Check if the transcript file already exists
        if os.path.isfile(transcript_file_path):
            return
        
        if not os.path.isfile(audio_path):
            print("Audio File Does not Exist")
            return
        # Define the status file path
        status_file_path = f'{file_name}_status.txt'

        # Create a status file to indicate that the transcription is in progress
        with open(status_file_path, 'w') as f:
            f.write('In progress')
            f.close()

        print(f'Creating transcript using WhisperX for {audio_path}')

        # Check for CUDA, otherwise use CPU
        if torch.cuda.is_available():
            device = "cuda"
            compute_type = "float16"

        print(f"Device: {device}\n Batch Size: {batch_size}\n Compute Type: {compute_type}\n")

        # Load the model
        model = whisperx.load_model(model_name, device, compute_type=compute_type)
        
        print(audio_path)
        # Transcribe the audio file
        audio = whisperx.load_audio(audio_path)
        result = model.transcribe(audio, batch_size=batch_size)
        
        print(result)
        with open(transcript_file_path, 'w') as f:
            f.write(process_transcript(result["segments"]))
            f.close()
                
        os.remove(status_file_path)

        print('------------ WhisperX Transcript Created ------------')
        
        
        # After Generating Transcript start the Ingestion Process
        ingestion_thread  = threading.Thread(target=ingestion_service,args=(video_id,))
        ingestion_thread.start()

    except Exception as e:
        # If an error occurs, update the status file with the error message
        print(f"Error: {e}")
        with open(status_file_path, 'w') as f:
            f.write('Error\n')
            f.write(str(e))
            f.close()
            
    