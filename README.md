
# NoteStream

NoteStream is a Streamlit-based application designed to help users generate concise and structured Markdown notes from YouTube video transcripts. This tool is perfect for students, educators, and professionals looking to save time by automatically transforming long video courses into manageable notes.

## Features

- **Transcript Extraction**: Fetch transcripts directly from YouTube videos.
- **Chunk Management**: Automatically process long transcripts into smaller, manageable chunks with buffer overlap for context.
- **Markdown Notes Generation**: Convert transcript chunks into structured Markdown notes using advanced AI models.
- **Downloadable Output**: Download the generated notes as a Markdown file for easy sharing and editing.

---

## How to Use

1. **Enter the YouTube Video Link**:  
   Paste the URL of the YouTube video from which you want to generate notes.

2. **Fetch and Process Transcript**:  
   The app will fetch the transcript of the video and process it into smaller chunks.

3. **Generate Markdown Notes**:  
   The processed chunks will be converted into structured notes in Markdown format.

4. **Download Your Notes**:  
   Once processing is complete, download the notes in Markdown format with a single click.

---

## Installation

### Prerequisites

- Python 3.7 or higher
- `pip` package manager

### Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/sujal-maheshwari2004/NoteStream.git
   cd NoteStream
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Access the app in your browser at `http://localhost:8501`.


## Files and Structure

- **`/app.py`**: Main Streamlit application file. Handles the UI and workflow.
- **`/chunk_maker.py`**: Manages transcript chunking and file operations.
- **`/md_maker.py`**: Processes chunks to generate Markdown notes using AI models.
- **`/transcript_extractor.py`**: Handles transcript fetching and pre-processing.
- **`/requirements.txt`**: Lists all the dependencies required for the project.

---

## Technologies Used

- **[Streamlit](https://streamlit.io/)**: For building the user interface.
- **[YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/)**: For fetching video transcripts.
- **[Ollama](https://ollama.ai/)**: AI-powered note generation.
- **Python Libraries**: 
  - `tqdm`: Progress bar for processing chunks.
  - `markdown2`: Conversion to Markdown format.
  - `pdfkit`: (Optional) Convert Markdown notes to PDF.
