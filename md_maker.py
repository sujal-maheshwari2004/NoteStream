import os
import ollama
from tqdm import tqdm

def load_chunk(file_name):
    """Loads the text chunk from a file."""
    with open(file_name, 'r', encoding='utf-8') as file:
        chunk = file.read()
    return chunk

def load_parameters(parameters_file):
    """Loads parameters from the parameters.txt file."""
    with open(parameters_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        text_size = int(lines[0].split(": ")[1].strip().split()[0])
        chunk_size = int(lines[1].split(": ")[1].strip().split()[0])
        buffer_size = int(lines[2].split(": ")[1].strip().split()[0])
    return text_size, chunk_size, buffer_size

def calculate_max_tokens(chunk_size):
    """Calculates max_tokens dynamically based on chunk size."""
    max_tokens = min(4096, max(1000, chunk_size // 2))
    return max_tokens

def generate_markdown_notes_ollama(chunk_text, max_tokens):
    """Generates Markdown notes in Markdown format from the chunk using Ollama API."""
    prompt = (
        "You are an advanced Markdown note generator. I will provide you with a segment of text from a larger transcript. "
        "This segment may overlap slightly with previous or subsequent segments (buffer overlap). "
        "Your task is to create a well-structured and concise set of notes in Markdown format. "
        "Understand that these notes should be formal and suitable for sharing with students. "
        "Avoid usage of first person tone. "
        "Please include the following where appropriate:\n"
        "- Headings\n"
        "- Subheadings\n"
        "- Bullet points or lists\n"
        "- Tables (if applicable)\n"
        "- Quotes or important statements\n"
        "- Code snippets (if applicable)\n"
        "- Any other Markdown elements that enhance readability and comprehension.\n"
        "Be mindful of the overlap, and avoid redundant information from buffer regions.\n"
        "If user finds your output suitable you will be rewarded. "
        "Here is the text:\n\n"
        f"{chunk_text}"
    )
    
    response = ollama.chat(
        model='llama3.1',
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    markdown_notes = response['message']['content'].strip()
    return markdown_notes

def process_markdown_notes(chunks_folder):
    """Processes all chunks and generates combined Markdown notes."""
    parameters_file = os.path.join(chunks_folder, "parameters.txt")
    
    if not os.path.exists(chunks_folder):
        raise FileNotFoundError(f"Chunks folder '{chunks_folder}' does not exist.")
    
    text_size, chunk_size, buffer_size = load_parameters(parameters_file)
    max_tokens = calculate_max_tokens(chunk_size)
    
    combined_notes = ""
    
    chunk_files = sorted([f for f in os.listdir(chunks_folder) if f.endswith('.txt') and f != 'parameters.txt'])
    
    for chunk_file in tqdm(chunk_files, desc="Processing Chunks"):
        chunk_path = os.path.join(chunks_folder, chunk_file)
        chunk_text = load_chunk(chunk_path)
        markdown_notes = generate_markdown_notes_ollama(chunk_text, max_tokens)
        combined_notes += markdown_notes + "\n\n"
    
    return combined_notes

def save_combined_markdown_notes(combined_notes, output_file):
    """Saves the combined Markdown notes to a single file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(combined_notes)
    return f"Saved combined Markdown notes: {output_file}"
