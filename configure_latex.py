import os
path = '/Users/panoskolyvakis/vsprojects/BlogGenerator/test.tex'

def compile_latex_to_pdf(tex_file):
    try:

        os.system(f"pdflatex {tex_file}")  # Compile LaTeX to PDF
        pdf_filename = tex_file.replace('.tex', '.pdf')  # Assuming tex_file ends with .tex
        return pdf_filename  
    except Exception as e:
        return f"An error occurred during LaTeX compilation: {e}"

if __name__ == '__main__':
    tex_file = path  
    pdf_filename = compile_latex_to_pdf(tex_file)
    print(f"PDF generated: {pdf_filename}")