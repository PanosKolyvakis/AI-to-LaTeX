import requests
import openai
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify , render_template
import requests
import openai
import requests
import openai



# to runt he HTML script successful locally please use
# python -m http.server
#http://localhost:8000

# THIS HERE IS THE CONNECTION TO THE SERVER
# <script async src="https://cse.google.com/cse.js?cx=832500dcf903c4b58">
# </script>
# <div class="gcse-search"></div>


# pkill -f 'python -m http.server'




# openai.api_key = openapi_key
# def google_search(query, num_results=5):
#     """Perform a Google Custom Search and return the top URLs."""
#     try:
#         response = requests.get(
#             'https://www.googleapis.com/customsearch/v1',
#             params={
#                 'key': API_KEY,
#                 'cx': CSE_ID,
#                 'q': query,
#                 'num': num_results
#             }
#         )
#         response.raise_for_status()  # Raises an exception for HTTP errors
#         search_results = response.json()

#         urls = [item['link'] for item in search_results.get('items', [])]
#         return urls
#     except Exception as e:
#         print(f"An error occurred during Google Custom Search: {e}")
#         return []

# def get_response_from_openai_api(urls):
#     """Generate a blog post using OpenAI's GPT based on the provided URLs."""

#     prompt_text = "Write a detailed blog post about the following topics and reference these websites: " + ', '.join(urls)

#     try:
#         response = openai.ChatCompletion.create(
#             model='gpt-4',
#             messages=[ 
#                 {"role": "system", "content": "check prompt"},
#                 {"role": "user", "content": prompt_text}
#             ]
#         )
#         return response['choices'][0]['message']['content'] if response['choices'][0]['message'] else "No content received from API."

#     except Exception as e:
#         return f"An error occurred: {e}"

# # Main function to execute the script
# def main():
#     query = "puppies"  # Example query
#     urls = google_search(query)
#     if urls:
#         blog_content = get_response_from_openai_api(urls)
#         print("Generated Blog Post:\n", blog_content)
#         print("\nReferences:")
#         for url in urls:
#             print(url)
#     else:
#         print("No URLs were found for the query.")

# if __name__ == '__main__':
#     main()

# # Below is the Flask app code, commented out for future use.
# '''
# from flask import Flask, jsonify, request

# app = Flask(__name__)

# @app.route('/search-to-blog', methods=['POST'])
# def search_to_blog():
#     # Your Flask app code here for future use
#     pass

# if __name__ == '__main__':
#     app.run(debug=True)
# '''







# Import necessary libraries
import requests
import openai

openai.api_key = openapi_key
app = Flask(__name__ , template_folder='/Users/panoskolyvakis/vsprojects/blogGenerator/templates')
def google_search(query, num_results=5):
    """Perform a Google Custom Search and return the top URLs."""
    try:
        response = requests.get(
            'https://www.googleapis.com/customsearch/v1',
            params={
                'key': API_KEY,
                'cx': CSE_ID,
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

def get_response_from_openai_api(urls):
    """Generate a blog post using OpenAI's GPT based on the provided URLs."""

    prompt_text = "Write a detailed blog post about the following topic and reference these websites. The LaTex Format should be used in your whole answer: " + ', '.join(urls)

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[ 
                {"role": "system", "content": "check prompt"},
                {"role": "user", "content": prompt_text}
            ]
        )
        return response['choices'][0]['message']['content'] if response['choices'][0]['message'] else "No content received from API."

    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search-to-blog', methods=['POST'])
def search_to_blog():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    urls = google_search(query)
    if urls:
        blog_content = get_response_from_openai_api(urls)
        return jsonify({'blog_post': blog_content, 'references': urls})
    else:
        return jsonify({"error": "No URLs were found for the query."}), 404

if __name__ == '__main__':
    app.run(debug=True)
#
#
#
#
#



