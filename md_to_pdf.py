import os
import pdfkit
import markdown2

def md_to_html(md_file):
    """Converts Markdown content to HTML."""
    with open(md_file, 'r', encoding='utf-8') as file:
        md_content = file.read()
    html_content = markdown2.markdown(md_content)
    return html_content

def save_html_as_pdf(html_content, pdf_file):
    """Converts HTML content to a PDF file."""
    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
    }
    pdfkit.from_string(html_content, pdf_file, options=options)
    return f"PDF saved as: {pdf_file}"

# Streamlit App Functions
def convert_md_to_pdf(md_file, pdf_file):
    """Converts a Markdown file to a PDF."""
    html_content = md_to_html(md_file)
    result_message = save_html_as_pdf(html_content, pdf_file)
    return result_message
