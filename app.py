import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi
from transcript_extractor import get_video_id, get_transcript, save_transcript_to_file
from chunk_maker import load_transcript, determine_chunk_and_buffer_size, split_text_into_chunks, save_chunks, save_parameters
from md_maker import load_chunk, load_parameters, calculate_max_tokens, generate_markdown_notes_ollama, save_combined_markdown_notes

def cleanup_files(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def main():
    st.sidebar.title("NoteStream")
    st.sidebar.subheader("Effortless Study Notes from YouTube Courses")
    
    # Adding guide to the sidebar
    st.sidebar.markdown(
        """
        ### How to Use This App
        1. **Enter the YouTube Video Link**:
            - Paste the URL of the YouTube video from which you want to generate notes.
        2. **Fetch and Process Transcript**:
            - The app will automatically fetch the transcript of the video.
            - It will then process the transcript into manageable chunks.
        3. **Generate Notes**:
            - The app will convert these chunks into well-structured Markdown notes.
        4. **Download Your Notes**:
            - Once the processing is complete, a download button will appear for you to download your notes in Markdown format.
        """
    )
    
    # Adding 15 blank lines for spacing
    for _ in range(15):
        st.sidebar.write("")
    
    # Adding "Developed by" heading and information section
    st.sidebar.markdown("### Developed by")
    st.sidebar.markdown("**Sujal Maheshwari**")
    st.sidebar.markdown(
        """
        <div style="text-align: center;">
            <a href="https://github.com/sujal-maheshwari2004" target="_blank">
                <img src="https://img.shields.io/badge/GitHub-000000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
            </a>
            <a href="https://www.linkedin.com/in/sujal-maheshwari/" target="_blank">
                <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
            </a>
            <a href="https://drive.google.com/file/d/10SAzKkTQ0ulPPCKj1GUy8VlWC0UDJLnc/view?usp=sharing" target="_blank">
                <img src="https://img.shields.io/badge/Resume-000000?style=for-the-badge&logo=pdf&logoColor=white" alt="Resume"/>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.title("hour long course's notes in minutes")

    youtube_url = st.text_input("Enter the YouTube video link:")

    if youtube_url:
        try:
            st.write("Fetching transcript...")
            video_id = get_video_id(youtube_url)
            transcript = get_transcript(video_id)
            transcript_file = 'transcript.txt'
            save_transcript_to_file(transcript, transcript_file)

            st.write("Processing transcript into chunks...")
            output_folder = 'transcript_chunks'
            transcript_length = len(transcript.split())
            chunk_size, buffer_size = determine_chunk_and_buffer_size(transcript_length)
            chunks = split_text_into_chunks(transcript, chunk_size, buffer_size)
            save_chunks(chunks, output_folder)
            save_parameters(output_folder, transcript_length, chunk_size, buffer_size)

            st.write("Generating Markdown notes...")
            parameters_file = os.path.join(output_folder, "parameters.txt")
            text_size, chunk_size, buffer_size = load_parameters(parameters_file)
            max_tokens = calculate_max_tokens(chunk_size)

            combined_notes = ""
            chunk_files = sorted([f for f in os.listdir(output_folder) if f.endswith('.txt') and f != 'parameters.txt'])
            
            progress_bar = st.progress(0)
            num_chunks = len(chunk_files)

            for i, chunk_file in enumerate(chunk_files):
                chunk_path = os.path.join(output_folder, chunk_file)
                chunk_text = load_chunk(chunk_path)
                markdown_notes = generate_markdown_notes_ollama(chunk_text, max_tokens)
                combined_notes += markdown_notes + "\n\n"
                
                progress = (i + 1) / num_chunks
                progress_bar.progress(progress)
            
            save_combined_markdown_notes(combined_notes, 'combined_notes.md')

            st.write("Download your Markdown notes:")
            with open('combined_notes.md', "rb") as file:
                st.download_button(
                    label="Download Markdown Notes",
                    data=file,
                    file_name='combined_notes.md',
                    mime="text/markdown"
                )

            # Clean up intermediate files
            cleanup_files([transcript_file] + [os.path.join(output_folder, f) for f in chunk_files])
            if os.path.exists(output_folder):
                os.rmdir(output_folder)

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
