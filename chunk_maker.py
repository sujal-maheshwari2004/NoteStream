import os

def load_transcript(file_name):
    """Loads the transcript from a text file."""
    with open(file_name, 'r', encoding='utf-8') as file:
        transcript = file.read()
    return transcript

def determine_chunk_and_buffer_size(text_length):
    """Determines chunk size and buffer size based on the text length."""
    if text_length <= 2000:
        chunk_size = 500
        buffer_size = 50
    elif text_length <= 10000:
        chunk_size = 1000
        buffer_size = 100
    elif text_length <= 50000:
        chunk_size = 5000
        buffer_size = 250
    elif text_length <= 100000:
        chunk_size = 10000
        buffer_size = 500
    else:
        chunk_size = 20000
        buffer_size = 1000
    
    return chunk_size, buffer_size

def split_text_into_chunks(text, chunk_size, buffer_size):
    """Splits the text into chunks with buffer overlap."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - buffer_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        
        if i + chunk_size >= len(words):
            break
    
    return chunks

def save_chunks(chunks, output_folder):
    """Saves each chunk to a separate text file in the output folder."""
    os.makedirs(output_folder, exist_ok=True)
    
    for i, chunk in enumerate(chunks):
        file_name = os.path.join(output_folder, f"chunk_{i + 1}.txt")
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(chunk)
        
        print(f"Saved: {file_name}")

def save_parameters(output_folder, text_size, chunk_size, buffer_size):
    """Saves the parameters to a text file."""
    parameters_file = os.path.join(output_folder, "parameters.txt")
    
    with open(parameters_file, 'w', encoding='utf-8') as file:
        file.write(f"Text Size: {text_size} words\n")
        file.write(f"Chunk Size: {chunk_size} words\n")
        file.write(f"Buffer Size: {buffer_size} words\n")
    
    print(f"Parameters saved: {parameters_file}")

# Streamlit App Functions
def process_transcript(file_name, output_folder):
    """Processes the transcript: splits it into chunks and saves them."""
    transcript = load_transcript(file_name)
    transcript_length = len(transcript.split())
    chunk_size, buffer_size = determine_chunk_and_buffer_size(transcript_length)
    chunks = split_text_into_chunks(transcript, chunk_size, buffer_size)
    save_chunks(chunks, output_folder)
    save_parameters(output_folder, transcript_length, chunk_size, buffer_size)
    return f"Processing complete. {len(chunks)} chunks saved."

