# import requests
# import openai
# from bs4 import BeautifulSoup
# from flask import Flask, request, jsonify , render_template
# import requests
# import openai

# # to runt he HTML script successful locally please use
# # python -m http.server
# #http://localhost:8000

# # THIS HERE IS THE CONNECTION TO THE SERVER
# # <script async src="https://cse.google.com/cse.js?cx=832500dcf903c4b58">
# # </script>
# # <div class="gcse-search"></div>


# # pkill -f 'python -m http.server'


# # keys and shit
# openapi_key = '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'
# API_KEY = 'AIzaSyCw61Bkr1FDCh6axJm6wPU9mM8k4nNNuxE'
# CSE_ID = '832500dcf903c4b58'

# DEBUG_URL = 'https://en.wikipedia.org/wiki/Cattle'


# import requests
# import openai

# # openai.api_key = openapi_key
# # def google_search(query, num_results=5):
# #     """Perform a Google Custom Search and return the top URLs."""
# #     try:
# #         response = requests.get(
# #             'https://www.googleapis.com/customsearch/v1',
# #             params={
# #                 'key': API_KEY,
# #                 'cx': CSE_ID,
# #                 'q': query,
# #                 'num': num_results
# #             }
# #         )
# #         response.raise_for_status()  # Raises an exception for HTTP errors
# #         search_results = response.json()

# #         urls = [item['link'] for item in search_results.get('items', [])]
# #         return urls
# #     except Exception as e:
# #         print(f"An error occurred during Google Custom Search: {e}")
# #         return []

# # def get_response_from_openai_api(urls):
# #     """Generate a blog post using OpenAI's GPT based on the provided URLs."""

# #     prompt_text = "Write a detailed blog post about the following topics and reference these websites: " + ', '.join(urls)

# #     try:
# #         response = openai.ChatCompletion.create(
# #             model='gpt-4',
# #             messages=[ 
# #                 {"role": "system", "content": "check prompt"},
# #                 {"role": "user", "content": prompt_text}
# #             ]
# #         )
# #         return response['choices'][0]['message']['content'] if response['choices'][0]['message'] else "No content received from API."

# #     except Exception as e:
# #         return f"An error occurred: {e}"

# # # Main function to execute the script
# # def main():
# #     query = "puppies"  # Example query
# #     urls = google_search(query)
# #     if urls:
# #         blog_content = get_response_from_openai_api(urls)
# #         print("Generated Blog Post:\n", blog_content)
# #         print("\nReferences:")
# #         for url in urls:
# #             print(url)
# #     else:
# #         print("No URLs were found for the query.")

# # if __name__ == '__main__':
# #     main()

# # # Below is the Flask app code, commented out for future use.
# # '''
# # from flask import Flask, jsonify, request

# # app = Flask(__name__)1ç

# # @app.route('/search-to-blog', methods=['POST'])
# # def search_to_blog():
# #     # Your Flask app code here for future use
# #     pass

# # if __name__ == '__main__':
# #     app.run(debug=True)
# # '''







# # Import necessary libraries
# from flask import send_from_directory
# import requests
# import openai

# openai.api_key = openapi_key
# app = Flask(__name__)
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
#         response.raise_for_status() 
#         search_results = response.json()
#         response.raise_for_status() 
        
#         urls = [item['link'] for item in search_results.get('items', [])]
#         return urls
#     except Exception as e:
#         print(f"An error occurred during Google Custom Search: {e}")
#         return []

# @app.route('/pdfs/<filename>')
# def serve_pdf(filename):
#     directory = "/Users/panoskolyvakis/Vsprojects/blogGenerator/docs/"
#     return send_from_directory(directory, filename)
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

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/search-to-blog', methods=['POST'])
# def search_to_blog():
#     data = request.get_json()
#     query = data.get('query')
#     if not query:
#         return jsonify({"error": "No query provided"}), 400

#     urls = google_search(query)
#     if urls:
#         blog_content = get_response_from_openai_api(urls)
#         return jsonify({'blog_post': blog_content, 'references': urls})
#     else:
#         return jsonify({"error": "No URLs were found for the query."}), 404

# if __name__ == '__main__':
#     app.run(debug=True)
# #
# #
# #
# #
# #


import requests
import json
import os
from configuration import Config

config = Config()

def get_response_from_ai_latex_generator(urls, template_number):
    # Configuration
    api_key = config.openapi_key
    endpoint = config.ai_latex_generator_endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Payload
    payload = {
        "template_id": template_number,
        "urls": urls
    }
    
    # Make the request
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        # Assuming the API returns the LaTeX content directly
        latex_content = response.text
        # Specify where to save the LaTeX file
        file_path = "/Users/panoskolyvakis/Vsprojects/BlogGenerator/docs/response.tex"
        # Write the LaTeX content to a file
        with open(file_path, 'w') as file:
            file.write(latex_content)
        print(f"LaTeX content written to {file_path}")
    else:
        print(f"Failed to get response: {response.status_code}, {response.text}")

# Example usage
urls = ["https://en.wikipedia.org/wiki/Elizabeth_Maitland,_Duchess_of_Lauderdale"]
template_number = 1
get_response_from_ai_latex_generator(urls, template_number)







# import requests

# # Assuming you've set these values in your config.py
# import config

# api_key = config.ai_latex_generator_api_key
# endpoint = config.ai_latex_generator_endpoint

# headers = {
#     "Authorization": f"Bearer {api_key}",
#     "Content-Type": "application/json"
# }

# payload = {
#     "template_id": "1",
#     "urls": ["https://example.com"]
# }

# response = requests.post(endpoint, headers=headers, json=payload)

# if response.status_code == 200:
#     print("Success:", response.json())
# else:
#     print("Error:", response.status_code, response.text)
