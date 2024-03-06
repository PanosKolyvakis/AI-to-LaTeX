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
from WebScrapper import read_url
import logging

config = Config()

# Setup logging
logging.basicConfig(level=logging.INFO, filename="app_logs.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Initialize configuration and OpenAI API key
openai.api_key = config.openapi_key
global tex_file_path
tex_file_path = 'static/docs/response.tex'

def google_search(query, num_results=3):
    logger.info('Google Search initiated')
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
        logger.info(f'Search URLs: {urls}')
        return urls
    except Exception as e:
        print(f"An error occurred during Google Custom Search: {e}")
        logger.error(f"Google Custom Search error: {e}")
        return []

def get_response_from_openai_api(urls , template , details):
    print('____________EXECUTING NORMAL RESPONSE FUNCTION___________')
    logger.info('Executing normal response function')
    formatted_urls = " \\\\ ".join(urls)
    
    prompt_text = (
        "Generate a complete LaTeX document article on a specified topic. "
        "The document should include a title, an abstract, sections for introduction, main content (with sub-sections as necessary), and a conclusion. "
        "Incorporate references to the following URLs appropriately within the text, formatted according to LaTeX bibliography standards. "
        "The output should be in valid .tex format, ready for direct compilation into PDF without any human editing. "
        "Do not include any images or external dependencies not covered in basic LaTeX packages. \\usepackage{polyglossia} , \\usepackage{fontspec} and \\setmainlanguage{greek} to write in other languages "
        "Here are the URLs to reference: " + formatted_urls + "\n\n"
        "Please ensure the document starts with the \\documentclass{} command (not ```tex), followed by necessary \\usepackage commands, and is structured correctly for compilation. "
        "End the document with \\end{document}. "
        f"use the template: {template} and substitute the following details {details}"
        "Note: The output will be directly used to generate a PDF; it must be fully compliant with LaTeX syntax and conventions."
        
    )
    print(prompt_text)
    logger.info(f'Prompt text: {prompt_text}')
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "check prompt"},
                {"role": "user", "content": prompt_text}
            ]
        )
        
        final = response.choices[0].message.content if response.choices[0].message else "No content received from API."
        os.makedirs(os.path.dirname(tex_file_path), exist_ok=True)
        
        with open(tex_file_path, 'w') as file:
            file.write(final)
        print('GPT response written in directory')
        logger.info('GPT response successfully written to directory')
    
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"Error during OpenAI API call: {e}")


def get_response_from_web_scrape(urls, template):
    print('____________EXECUTING WEB SCRAPE FUNCTION___________')
    logger.info('Executing web scrape function')
    webscrapped_text = ''

    for url in urls:
        webscrapped_text += read_url(url) if read_url(url) else ' '
    print(f'____________this is the webscraped text ----------> ___________{webscrapped_text}')
    logger.info(f'Web scraped text: {webscrapped_text}')

    prompt_text = ("Generate a complete LaTeX document article on a specified topic. "
        " please add recent dates from the webscrapped_text any date that the article was written at as a reference"
        "The document should include a title, an abstract, sections for introduction, main content (with sub-sections as necessary), and a conclusion. "
        "Incorporate references to the following URLs appropriately within the text, formatted according to LaTeX bibliography standards. "
        "The output should be in valid .tex format, ready for direct compilation into PDF without any human editing. "
        "Do not include any images or external dependencies not covered in basic LaTeX packages. \\usepackage{polyglossia} , \\usepackage{fontspec} and \\setmainlanguage{greek} to write in other languages "
        "here is the web- scrapped recent script that you need to format nicely within the template " "\n\n"
        "Please ensure the document starts with the \\documentclass{} command (not ```tex), followed by necessary \\usepackage commands, and is structured correctly for compilation. "
        "start with \\begin{document} End the document with \\end{document}. "
        f"use the template: {template} and substitute/summarize the following details {webscrapped_text}"
        "Note: The output will be directly used to generate a PDF; it must be fully compliant with LaTeX syntax and conventions."
        )
    print(prompt_text)
    logger.info(f'Prompt text for web scrape: {prompt_text}')
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "check prompt"},
                {"role": "user", "content": prompt_text}
            ]
        )
        
        final = response.choices[0].message.content if response.choices[0].message else "No content received from API."
        print('----------------->FINAL MESSAGE RETRIEVED FROM GPT ------------------> {}'.format(final))
        logger.info(f'Final message from GPT (web scrape): {final}')

        cleaned_content = final.strip("`")
        os.makedirs(os.path.dirname(tex_file_path), exist_ok=True)
        
        with open(tex_file_path, 'w') as file:
            file.write(cleaned_content)
        print('GPT response written in directory')
        logger.info('GPT response from web scrape successfully written to directory')
    
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"Error during web scrape response generation: {e}")


def get_refined_doc(user_input):
    print('Prompt for refining document')
    logger.info('Refining document with user input')
    tex_file_path = 'static/docs/response.tex'
    with open(tex_file_path, 'r') as tex_file:
        tex_file = tex_file.read()
    
    prompt_text = (
        f"Refine the following {tex_file} according to the following '{user_input}'"        
        "The output should be in valid .tex format, ready for direct compilation into PDF without any human editing. "
        "Do not include any images or external dependencies not covered in basic LaTeX packages."
        "Please ensure the document starts with the \\documentclass{} command, followed by necessary \\usepackage commands, and is structured correctly for compilation. "
        "begin the document with \\begin{document} . "
        "End the document with \\end{document}."
        "Note: The output will be directly used t o generate a PDF from tex; it must be fully compliant with LaTeX syntax and conventions and should not contain any delimeters (remove any that the user input may contain such as ```latex)."
        

    )
    print(prompt_text)
    logger.info(f'Prompt for document refinement: {prompt_text}')
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "check prompt"},
                {"role": "user", "content": prompt_text}
            ]
        )
        final = response.choices[0].message.content if response.choices[0].message else "No content received from API."
        with open(tex_file_path, 'w') as file:
            file.write(final)
        print('Refined GPT response written in directory')
        logger.info('Refined document successfully written to directory')
    
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"Error during document refinement: {e}")




def compile_latex_to_pdf(tex_file_relative_path='static/docs/response.tex'):
    print('Compiling LaTeX to PDF')
    logger.info('Compiling LaTeX document to PDF')
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        tex_file_path = os.path.join(base_dir, tex_file_relative_path)
 
        if not tex_file_path.endswith('.tex'):
            print("Invalid file type. Please provide a .tex file.")
            logger.error("Invalid LaTeX file type for compilation")
            return "Invalid file type."

        pdf_filename = tex_file_path.replace('.tex', '.pdf')
        current_dir = os.getcwd()
        os.chdir(os.path.dirname(tex_file_path) or '.')

        result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file_path], capture_output=True, text=True)
        os.chdir(current_dir)

        if result.returncode != 0:
            print(f"LaTeX compilation errors:\n{result.stdout}\n{result.stderr}")
            logger.error(f"LaTeX compilation errors: {result.stderr}")
            return "PDF file was not generated due to LaTeX compilation errors."

        if os.path.exists(pdf_filename):
            print(f"PDF successfully generated: {pdf_filename}")
            logger.info(f"PDF successfully generated: {pdf_filename}")
            return pdf_filename
        else:
            print("PDF file was not generated. Check LaTeX compilation errors.")
            logger.error("PDF not generated due to LaTeX compilation errors.")
            return "PDF not generated."
    except Exception as e:
        os.chdir(current_dir) 
        print(f"An error occurred during LaTeX compilation: {e}")
        logger.error(f"LaTeX compilation error: {e}")
        return f"Compilation error: {e}"




if __name__ == '__main__':

    urls = google_search('israel-Gaza war')

    template = r"""
        \documentclass[twocolumn]{article}
        \usepackage{lipsum, hyperref, graphicx}
        \usepackage{hyperref}
        \title{Sample Two Column Article}
        \author{Author Name}
        \date{\today}
        \begin{document}
        \maketitle
        \begin{abstract}
        This is a sample abstract text.
        \end{abstract}
        This is sample content. \lipsum[1-3]
        \end{document}
    """
    get_response_from_web_scrape(urls , template )


