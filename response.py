
import os
import openai
from configuration import Config
import subprocess

class Config:
    def __init__(self):
        self.response_path = '/Users/panoskolyvakis/vsprojects/BlogGenerator/docs/response.tex'
        self.openapi_key = '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'
        self.google_API_KEY = 'AIzaSyCw61Bkr1FDCh6axJm6wPU9mM8k4nNNuxE'
        self.google_CSE_ID = '832500dcf903c4b58'
        self.DEBUG_URL = 'https://en.wikipedia.org/wiki/Cattle'
        self.html_template= '/Users/panoskolyvakis/vsprojects/blogGenerator/templates'


config = Config()

file_path = config.response_path
openai.api_key = config.openapi_key



''''this function gets the response from the API'''
def get_response_from_openai_api(urls):
    global file_path

    # Construct the prompt text
    prompt_text = "Write a detailed blog post about the following topic and reference these websites. The LaTeX Format should be used in your whole answer and please do not use or reference any pictures as your response will be directly fed into a .tex document. the output from this GPT- API call will directly be fed into a .tex file and then converted into a .pdf file so your answer should compile correctly without any editing from a human: " + ', '.join(urls)
    
    # Specify the file path (change according to your environment)
    file_path = config.response_path
    
    try:
        # Actual OpenAI API call
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {"role": "system", "content": "check prompt"},
                {"role": "user", "content": prompt_text}
            ]
        )
        
        final = response['choices'][0]['message']['content'] if response['choices'][0]['message'] else "No content received from API."
        
        # Debugging: Print the content to be written to the file
        print("Content to be written to the file:")
        print(final)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write content to the file
        with open(file_path, 'w') as file:
            file.write(final)
        print('GPT response written in directory')
    
    except Exception as e:

        print(f"An error occurred: {e}")




def compile_latex_to_pdf(tex_file):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(tex_file), exist_ok=True)

        # Construct PDF filename
        pdf_filename = tex_file.replace('.tex', '.pdf')

        # Delete existing PDF file if it exists
        if os.path.exists(pdf_filename):
            os.remove(pdf_filename)
            print(f"Existing PDF file deleted: {pdf_filename}")

        # Change to the directory of the tex_file to ensure pdflatex runs correctly
        os.chdir(os.path.dirname(tex_file))
        
        # Run pdflatex command with nonstopmode option to ignore errors
        subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file])
        
        # Verify PDF generation
        if os.path.exists(pdf_filename):
            print(f"PDF successfully generated: {pdf_filename}")
            return pdf_filename
        else:
            return "PDF file was not generated. Check LaTeX compilation errors."
    except Exception as e:
        return f"An error occurred during LaTeX compilation: {e}"



if __name__ == '__main__':

    urls = ['https://www.visitgreece.gr']
    get_response_from_openai_api(urls)
    file_path = config.response_path
    pdf_filename = compile_latex_to_pdf(file_path)

    print(f"PDF generated: {pdf_filename}")


#     1 Introduction
# The renowned philosopher Socrates once said, ”An unexamined life is not worth living.” An extension of this notion would propose that an unexamined world is not worth inhabiting. One of the numerous facets of this world that merit their thorough examination is the unparalleled beauty of Greece. Thankfully, website such as VisitGreece.gr have made this task notably easier, and that’s what we will be exploring throughout this blog post.
