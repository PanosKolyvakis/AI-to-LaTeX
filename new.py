import os
import os
import openai


file_path = '/Users/panoskolyvakis/vsprojects/BlogGenerator/docs/response.tex'
openapi_key = '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'
openai.api_key = openapi_key



''''this function gets the response from the API'''
def get_response_from_openai_api(urls):
    global file_path

    # Construct the prompt text
    prompt_text = "Write a detailed blog post about the following topic and reference these websites. The LaTeX Format should be used in your whole answer: " + ', '.join(urls)
    
    # Specify the file path (change according to your environment)
    file_path = '/Users/panoskolyvakis/vsprojects/BlogGenerator/docs/response.tex'
    
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
        # Change to the directory of the tex_file to ensure pdflatex runs in the correct context
        os.chdir(os.path.dirname(tex_file))
        # Run pdflatex command
        os.system(f'pdflatex "{tex_file}"')
        # Construct PDF filename
        pdf_filename = tex_file.replace('.tex', '.pdf')
        # Check if PDF was generated
        if os.path.exists(pdf_filename):
            return pdf_filename
        else:
            return "PDF file was not generated. Check LaTeX compilation errors."
    except Exception as e:
        return f"An error occurred during LaTeX compilation: {e}"

if __name__ == '__main__':

    urls = ['https://openai.com']
    get_response_from_openai_api(urls)
    file_path = '/Users/panoskolyvakis/vsprojects/BlogGenerator/docs/response.tex'
    pdf_filename = compile_latex_to_pdf(file_path)

    print(f"PDF generated: {pdf_filename}")