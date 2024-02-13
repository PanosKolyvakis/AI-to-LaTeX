
import os
import openai
from configuration import Config
import subprocess


# Initialize configuration and OpenAI API key
config = Config()
openai.api_key = config.openapi_key

# This function gets the response from the OpenAI API and saves it as a .tex file
def get_response_from_openai_api(urls):
    # Construct the prompt text
    prompt_text = "Write a detailed blog post about the following topic and reference these websites. The LaTeX Format should be used in your whole answer (do not include anything like 'this should be written in the .tex file ---> JUST return The .tex file') and please do not use or reference any pictures as your response will be directly fed into a .tex document. The output from this GPT-API call will directly be fed into a .tex file and then converted into a .pdf file so your answer should compile correctly without any editing from a human: " + ', '.join(urls)
    
    # Corrected file path to save the .tex document
    tex_file_path = 'static/docs/response.tex'
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
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(tex_file_path), exist_ok=True)
        
        # Write content to the .tex file
        with open(tex_file_path, 'w') as file:
            file.write(final)
        print('GPT response written in directory')
    
    except Exception as e:
        print(f"An error occurred: {e}")

# This function compiles the .tex document into a .pdf file
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
    subprocess.run(["open" , pdf_filename])
    print(f"PDF generated: {pdf_filename}")


# template = r"""\documentclass[11pt]{article}
# \usepackage[utf8]{inputenc}
# \usepackage{geometry}
# \geometry{a4paper}
# \usepackage{graphicx}
# \usepackage{booktabs}
# \usepackage{array}
# \usepackage{verbatim}
# \usepackage{subfig}
# \usepackage{fancyhdr}
# \usepackage{amsmath}
# \usepackage{cite}
# \usepackage{hyperref}
# \usepackage{float}
# \usepackage{natbib}
# \usepackage{doi}

# \title{Insert Your Title Here}
# \author{Author Name\\
# \small Institution Name}
# \date{\today}

# \begin{document}
# \maketitle

# \begin{abstract}
# Your abstract text goes here.
# \end{abstract}

# \section{Introduction}
# \label{sec:introduction}
# Your introduction text goes here.

# \section{Related Work}
# \label{sec:relatedwork}
# Discussion of related work in your area of research.

# \section{Methodology}
# \label{sec:methodology}
# Describe your research methods here.

# \section{Results}
# \label{sec:results}
# Present and discuss your research results here.

# \section{Discussion}
# \label{sec:discussion}
# Discuss the implications of your findings here.

# \section{Conclusion}
# \label{sec:conclusion}
# Your conclusion text goes here.

# \bibliographystyle{unsrtnat}
# \bibliography{references}

# \end{document}"""