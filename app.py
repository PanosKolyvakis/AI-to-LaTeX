import requests
import openai
from flask import Flask, request, jsonify , render_template
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from configuration import Config
from response import compile_latex_to_pdf , get_response_from_openai_api



# to runt he HTML script successful locally please u
#http://localhost:8000
# python -m http.server
# THIS HERE IS THE CONNECTION TO THE SERVER
# <script async src="https://cse.google.com/cse.js?cx=832500dcf903c4b58">
# </script>
# <div class="gcse-search"></div>


# pkill -f 'python -m http.server'


# keys and shit


# Initialize Flask app

config = Config()

app = Flask(__name__, template_folder=config.html_template)

# Function to perform Google Custom Search and return URLs
def google_search(query, num_results=5):
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
        response.raise_for_status() 
        
        urls = [item['link'] for item in search_results.get('items', [])]
        return urls
    except Exception as e:
        print(f"An error occurred during Google Custom Search: {e}")
        return []

            

# Function to compile LaTeX to PDF
def compile_latex_to_pdf_alternative():
    try:
        os.system("pdflatex response.tex")  
        return "response.pdf"  
    except Exception as e:
        return f"An error occurred during LaTeX compilation: {e}"

# Function to delete files // not used
def cleanup_files(*file_paths):
    for path in file_paths:
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted {path}")

# Index route
@app.route('/')

def index():
    return render_template('index.html')



# Search to blog route
@app.route('/search-to-blog', methods=['POST'])
def search_to_blog():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    urls = google_search(query)
    if urls:
        # Generate blog content for display using URLs
        blog_content = get_response_from_openai_api(urls) 

        file_path = config.response_path
        pdf_filename = compile_latex_to_pdf(file_path)

        print(f"PDF generated: {pdf_filename}")

        
        return jsonify({'blog_post': blog_content, 'pdf_filename': pdf_filename, 'references': urls})
    else:
        return jsonify({"error": "No URLs were found for the query."}), 404

# Driver Code
if __name__ == '__main__':
    app.run(debug=True)

    


