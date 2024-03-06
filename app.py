"""
This Flask web application interfaces with various services and tools to facilitate the creation of blog posts from search queries, leveraging LaTeX for document preparation and PDF generation. The application allows users to submit search queries, select templates, and automatically generate blog content, which is then compiled into a LaTeX document and rendered as a PDF. It features several endpoints to handle different aspects of the workflow, including submitting search queries, downloading generated PDFs, and refining document content.

Features:
- Accepts search queries and template preferences via a web interface.
- Uses the provided query to perform a Google search and retrieves relevant URLs.
- Processes these URLs to generate blog content, utilizing OpenAI's API for content generation and refinement.
- Supports LaTeX document preparation and PDF compilation.
- Provides endpoints for downloading the generated PDFs and refining the document content based on user feedback.

Endpoints:
- `/search-to-blog`: POST endpoint to accept search queries and template preferences, generates blog content, and compiles it into a PDF.
- `/download-pdf/<filename>`: GET endpoint to download the generated PDF document.
- `/`: Default endpoint that serves the application's main interface.
- `/pdf-ready/<filename>`: GET endpoint to check if the PDF is ready for download.
- `/submit-refinement`: POST endpoint to accept refinements for the generated document content.

Usage:
- Run the application and navigate to the main page to submit a search query and template preference.
- The application will generate a blog post based on the query, compile it into a PDF, and provide a link to download the document.
- Users can also submit refinements to the generated content, which the application will process and use to update the document.

Note:
This application requires an external configuration for its operation, specified in `configuration.py`, and utilizes external APIs and LaTeX for document processing and PDF generation. Ensure all dependencies are installed and configured before running.
"""

#import statements
import logging
from configuration import Config
from flask import Flask, request, jsonify, render_template, send_from_directory, abort
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from response import compile_latex_to_pdf, get_response_from_openai_api, google_search, get_refined_doc, get_response_from_web_scrape
from LaTeXprocessing import LaTeX_templates

# Configure logging


#opens on http://127.0.0.1:5000
with open('app_logs.log', 'w'): # opening to make sure the log clears up
    pass

# Configure logging to print to both file and terminal
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    handlers=[
                        logging.FileHandler('app_logs.log'),
                        logging.StreamHandler(sys.stdout)
                    ])
# getting the config details correct
config = Config()

# initializing Flask object
app = Flask(__name__, template_folder=config.html_template)

# methods;
@app.route('/search-to-blog', methods=['POST'])
def search_to_blog():
    data = request.json
    logging.info('Received /search-to-blog request: %s', data)

    query = data.get('query')
    template = data.get('template')
    name = data.get('name')
    date = data.get('date')
    title = data.get('title')
    need_web_scrapping = bool(data.get('enableWebScraping', False))

    if not query:
        logging.error('No query provided in /search-to-blog')
        return jsonify({"error": "No query provided"}), 400

    logging.info('Processing query: %s with template: %s', query, template)
    urls = google_search(query)

    if urls:
        logging.info('URLs retrieved for query: %s', urls)
        template_to_use = LaTeX_templates[template]

        if not need_web_scrapping:
            logging.info('Generating content without web scraping for: %s', query)
            get_response_from_openai_api(urls, template_to_use, details=[name, date, title])
        else:
            logging.info('Generating content with web scraping for: %s', query)
            get_response_from_web_scrape(urls, template_to_use)

        tex_filename = 'response.tex'
        file_path_tex = os.path.join(app.static_folder, 'docs', tex_filename)
        file_path_pdf = compile_latex_to_pdf(file_path_tex)
        logging.info('PDF generated and available at: %s', file_path_pdf)

        return jsonify({'pdf_web_path': file_path_pdf, 'blog_post': '', 'references': urls})
    else:
        logging.error('No URLs found for query: %s', query)
        return jsonify({"error": "No URLs were found for the query."}), 404


@app.route('/download-pdf/<filename>')
def download_pdf(filename):
    directory = os.path.join(app.static_folder, 'docs')
    try:
        logging.info('Downloading PDF: %s', filename)
        return send_from_directory(directory, filename, as_attachment=True)
    except FileNotFoundError:
        logging.error('PDF file not found: %s', filename)
        abort(404)


@app.route('/')
def index():
    logging.info('Serving the index page')
    return render_template('index.html')


@app.route('/pdf-ready/<filename>')
def pdf_ready(filename):
    pdf_path = os.path.join(app.static_folder, 'docs', filename)
    if os.path.exists(pdf_path):
        logging.info('PDF is ready for download: %s', filename)
        return jsonify({'ready': True})
    else:
        logging.info('PDF not ready for download: %s', filename)
        return jsonify({'ready': False})


@app.route('/submit-refinement', methods=['POST'])
def submit_refinement():
    data = request.json
    logging.info('Received refinement details: %s', data)
    refinement_details = data.get('refinement_details')
    get_refined_doc(refinement_details)
    tex_filename = 'response.tex'
    file_path_tex = os.path.join(app.static_folder, 'docs', tex_filename)
    file_path_pdf = compile_latex_to_pdf(file_path_tex)
    logging.info('Document refined and PDF recompiled: %s', file_path_pdf)
    return jsonify({'pdf_web_path': file_path_pdf})


@app.route('/submit-edited-tex', methods=['POST'])
def submit_edited_tex():
    
    data = request.json
    tex_content = data.get('texContent', '')
    logging.info('Received TeX content for recompilation')

    with open('static/docs/response.tex', 'w') as tex_file:
        tex_file.write(tex_content)
    compile_latex_to_pdf('static/docs/response.tex')
    logging.info('TeX content updated and document recompiled successfully')
    return jsonify({"message": "TeX content updated and document recompiled successfully"})

if __name__ == '__main__':
    print('Initializing flask in local IP : http://127.0.0.1:5000')
    app.run(debug=True)




