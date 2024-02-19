import requests
import sys
import os
from configuration import Config
from flask import Flask, request, jsonify, render_template, send_from_directory, abort
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from configuration import Config
from response import compile_latex_to_pdf, get_response_from_openai_api , google_search , get_refined_doc
from LaTeXprocessing import LaTeX_templates


# Get the Config Correct
config = Config()

# initialize flask
app = Flask(__name__, template_folder= config.html_template)

@app.route('/search-to-blog', methods=['POST'])
def search_to_blog():
    data = request.json

    query = data['query']

    print(data)
    query = data.get('query')
    template = data.get('template')
    print(template)
    name = data.get('name')
    date = data.get('date')
    title = data.get('title')
    details = [name, date, title]
    if not query:
        return jsonify({"error": "No query provided"}), 400

    urls = google_search(query)
    print(urls if urls else 'no URL FOUND')

    if urls:
        template_to_use = LaTeX_templates[template]
        # Generate blog content for display using URLs
        get_response_from_openai_api(urls , template_to_use , details = details)
        
        # Adjust the path for saving the .tex file within 'static/docs'
        tex_filename = 'response.tex'

        file_path_tex = os.path.join(app.static_folder, 'docs', tex_filename)
        

        # Assuming compile_latex_to_pdf takes the .tex path and saves the .pdf in the same directory
        file_path_pdf = compile_latex_to_pdf(file_path_tex)


        # Return the JSON response with blog content and PDF web path
        return jsonify({'pdf_web_path': file_path_pdf, 'blog_post':'', 'references': urls})
    else:
        return jsonify({"error": "No URLs were found for the query."}), 404


@app.route('/download-pdf/<filename>')
def download_pdf(filename):
    # Serve PDFs from the 'static/docs' directory
    directory = os.path.join(app.static_folder, 'docs')
    try:
        return send_from_directory(directory, filename, as_attachment=False)
    except FileNotFoundError:
        abort(404)



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/pdf-ready/<filename>')
def pdf_ready(filename):

    pdf_path = os.path.join(app.static_folder, 'docs', filename)

    if os.path.exists(pdf_path):
        return jsonify({'ready': True})
    else:
        return jsonify({'ready': False})


@app.route('/submit-refinement', methods=['POST'])
def submit_refinement():
    data = request.json
    refinement_details = data.get('refinement_details')
    get_refined_doc(refinement_details)
    # Adjust the path for saving the .tex file within 'static/docs'
    tex_filename = 'response.tex'
    file_path_tex = os.path.join(app.static_folder, 'docs', tex_filename)
    
    # Assuming compile_latex_to_pdf takes the .tex path and saves the .pdf in the same directory
    file_path_pdf = compile_latex_to_pdf(file_path_tex)
    # Return the JSON response with blog content and PDF web path
    return jsonify({'pdf_web_path': file_path_pdf})




if __name__ == '__main__':
    app.run(debug=True)




