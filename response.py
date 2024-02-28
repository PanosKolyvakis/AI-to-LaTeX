"""
This script is part of a web application that generates LaTeX documents based on user queries, compiles them into PDFs, and allows for document refinement through OpenAI's GPT API. It interfaces with Google's Custom Search Engine (CSE) to perform searches based on user queries and uses the results to generate content for LaTeX documents. The script supports refining these documents based on further user input and compiles the LaTeX into PDFs using a local LaTeX installation.

Dependencies:
- Flask 3.0.2: Used for the web server and handling HTTP requests.
- requests 2.25.1: Used for making HTTP requests to Google's Custom Search API.
- openai 0.28.0: Used for generating and refining document content with GPT models.

Features:
- Performs Google searches via the Custom Search JSON API and extracts URLs from the results.
- Generates LaTeX document content by submitting prompts to the OpenAI API, incorporating search results.
- Refines existing LaTeX documents based on user input using the OpenAI API.
- Compiles LaTeX documents into PDF format.

The script is designed to be a part of a larger Flask web application, interacting with frontend components for user input and displaying generated documents. It is structured to be easily integrated into web routes or background tasks within the Flask app.

Usage:
- The script is not intended to be run as a standalone program. Functions within the script are called by the Flask app in response to user actions (e.g., submitting a search query, requesting document refinement).
- Configuration parameters (e.g., API keys, file paths) are loaded from a separate `configuration.py` module.

Note:
- Ensure all non-standard dependencies are installed in your environment.
- A valid OpenAI API key and Google CSE setup are required for full functionality.
"""

import os
import openai
from configuration import Config
import subprocess
import requests
import subprocess
import os


# Initialize configuration and OpenAI API key
config = Config()
openai.api_key = config.openapi_key
tex_file_path = 'static/docs/response.tex'


def google_search(query, num_results=5):
    print('Google Search initated')
    try:
        response = requests.get(
            'https://www.googleapis.com/customsearch/v1',
            params={
                'key': config.google_API_KEY,
                'cx': config.google_CSE_ID,
                'q': query,
                'num': num_results
            }
        )
        response.raise_for_status()
        search_results = response.json()
        
        urls = [item['link'] for item in search_results.get('items', [])]
        print(urls)
        return urls
    except Exception as e:
        print(f"An error occurred during Google Custom Search: {e}")
        return []

# This function gets the response from the OpenAI API and saves it as a .tex file
# Populate {LaTex_temps[1]} and return 
def get_response_from_openai_api(urls , template , details):
    # Joining URLs with LaTeX newline for clarity in the prompt.
    formatted_urls = " \\\\ ".join(urls)  # LaTeX newline between URLs for clarity.
    
    # Construct the prompt text for the GPT API call.
    prompt_text = (
        "Generate a complete LaTeX document article on a specified topic. "
        "The document should include a title, an abstract, sections for introduction, main content (with sub-sections as necessary), and a conclusion. "
        "Incorporate references to the following URLs appropriately within the text, formatted according to LaTeX bibliography standards. "
        "The output should be in valid .tex format, ready for direct compilation into PDF without any human editing. "
        "Do not include any images or external dependencies not covered in basic LaTeX packages. \\usepackage{polyglossia} to write in other languages "
        "Here are the URLs to reference: " + formatted_urls + "\n\n"
        "Please ensure the document starts with the \\documentclass{} command, followed by necessary \\usepackage commands, and is structured correctly for compilation. "
        "End the document with \\end{document}. "
        f"use the template: {template} and substitute the following details {details}"
        "Note: The output will be directly used to generate a PDF; it must be fully compliant with LaTeX syntax and conventions."
        

    )
    print(prompt_text)
    # Corrected file path to save the .tex document
    try:
        # Actual OpenAI API call
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "check prompt"},
                {"role": "user", "content": prompt_text}
            ]
        )
        
        final = response.choices[0].message.content if response.choices[0].message else "No content received from API."
        
        # # Ensure the directory exists
        # os.makedirs(os.path.dirname(tex_file_path), exist_ok=True)
        
        

        # Write content to the .tex file
        with open(tex_file_path, 'w') as file:
            file.write(final)
        print('GPT response written in directory')
    
    except Exception as e:
        print(f"An error occurred: {e}")





def get_refined_doc( user_input):

    tex_file_path = 'static/docs/response.tex'
    with open(tex_file_path, 'r') as tex_file:
        tex_file = tex_file.read()
        
    # Construct the prompt text for the GPT API call.
    prompt_text = (
        f"Refine the following {tex_file} accirding to the following '{user_input}'"        
        "The output should be in valid .tex format, ready for direct compilation into PDF without any human editing. "
        "Do not include any images or external dependencies not covered in basic LaTeX packages."
        "Please ensure the document starts with the \\documentclass{} command, followed by necessary \\usepackage commands, and is structured correctly for compilation. "
        "begin the document with \\begin{document}. "
        "End the document with \\end{document}. "
        "Note: The output will be directly used to generate a PDF from tex; it must be fully compliant with LaTeX syntax and conventions and should not contain any delimeters (remove any that the user input may contain such as ```latex)."
        

    )
    print('prompt fed into GPT:' + f'{prompt_text}')
    # Corrected file path to save the .tex document
    try:
        # Actual OpenAI API call
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "check prompt"},
                {"role": "user", "content": prompt_text}
            ]
        )
        final = response.choices[0].message.content if response.choices[0].message else "No content received from API."
        
        # # Ensure the directory exists
        # os.makedirs(os.path.dirname(tex_file_path), exist_ok=True)
        tex_file_path = 'static/docs/response.tex'
        # Write content to the .tex file
        with open(tex_file_path, 'w') as file:
            file.write(final)
        print('GPT response written in directory')
    
    except Exception as e:
        print(f"An error occurred: {e}")




def compile_latex_to_pdf(tex_file_relative_path='static/docs/response.tex'):
    try:
        # Get the absolute path of the directory where the script is located
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the .tex file
        tex_file_path = os.path.join(base_dir, tex_file_relative_path)

 
        if not tex_file_path.endswith('.tex'):
            return "Invalid file type. Please provide a .tex file."

        # Construct PDF filename
        pdf_filename = tex_file_path.replace('.tex', '.pdf')

        # Save current directory
        current_dir = os.getcwd()

        # Change to the directory of the tex_file to ensure pdflatex runs correctly
        os.chdir(os.path.dirname(tex_file_path) or '.')

        # Run pdflatex command with nonstopmode option to ignore errors
        result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file_path], capture_output=True, text=True)

        # Change back to the original directory
        os.chdir(current_dir)

        # Check the subprocess result for errors
        if result.returncode != 0:
            print(f"LaTeX compilation errors:\n{result.stdout}\n{result.stderr}")
            return "PDF file was not generated due to LaTeX compilation errors."

        # Verify PDF generation
        if os.path.exists(pdf_filename):
            print(f"PDF successfully generated: {pdf_filename}")
            return pdf_filename
        else:
            return "PDF file was not generated. Check LaTeX compilation errors."
    except Exception as e:
        # Change back to the original directory in case of exception
        os.chdir(current_dir)
        return f"An error occurred during LaTeX compilation: {e}"


if __name__ == '__main__':

    urls = google_search('lion')

    get_response_from_openai_api(urls)

    compile_latex_to_pdf()
