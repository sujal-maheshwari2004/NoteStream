from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(youtube_url):
    """Extracts video ID from a YouTube URL."""
    parsed_url = urlparse(youtube_url)
    if parsed_url.hostname == 'youtu.be':  # Shortened URL
        return parsed_url.path[1:]
    elif parsed_url.hostname in ['www.youtube.com', 'youtube.com']:  # Regular or embed URL
        if 'v' in parse_qs(parsed_url.query):
            return parse_qs(parsed_url.query)['v'][0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        elif parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    raise ValueError(f"Could not extract video ID from URL: {youtube_url}")

def get_transcript(video_id):
    """Fetches the transcript for the given video ID."""
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_text = ' '.join([entry['text'] for entry in transcript])
    return full_text

def save_transcript_to_file(transcript, file_name):
    """Saves the transcript text to a file."""
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(transcript)

# Streamlit App Functions
def process_youtube_url(youtube_url):
    """Processes the YouTube URL to fetch and save the transcript."""
    try:
        video_id = get_video_id(youtube_url)
        transcript = get_transcript(video_id)
        return transcript
    except Exception as e:
        return f"Error: {e}"
