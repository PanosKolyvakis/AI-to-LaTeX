"""
This script provides functionality for generating LaTeX documents from predefined templates and compiling them into PDF files. It defines a set of LaTeX templates for different types of documents such as scientific articles, reviews, and blog posts. Each template is stored in a dictionary and can be written to a .tex file by specifying the template name. Additionally, the script includes a function to compile a .tex file into a PDF using the pdflatex command, handling directory management and compilation errors.

Features:
- Predefined LaTeX templates for various document types.
- Function to write a selected template to a .tex file, with the option to specify the output path.
- Function to compile a .tex file into a PDF, including error handling and output management.

Usage:
- To use a template, call `write_template_to_file` with the desired template name and output path.
- To compile a .tex file to PDF, call `compile_latex_to_pdf` with the path to the .tex file.

Example:
    template_name = "scientific_document"
    output_tex_path = 'output.tex'
    write_template_to_file(template_name, output_tex_path)
    compile_latex_to_pdf(output_tex_path)

Note:
This script requires a LaTeX installation on the system and access to the 'pdflatex' command.
"""

import os
import subprocess



LaTeX_templates = {
    "scientific_document": r"""
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
""",
    "newsletter": r"""\documentclass[10pt,a4paper]{article}

% Define geometry
\setlength\topmargin{-48pt}
\setlength\headheight{15pt} % Adjusted from 0pt to ensure enough space for headers
\setlength\headsep{25pt}
\setlength\marginparwidth{-20pt}
\setlength\textwidth{7.0in}
\setlength\textheight{9.5in}
\setlength\oddsidemargin{-30pt}
\setlength\evensidemargin{-30pt}

\frenchspacing % better looking spacing

% Call packages we'll need
\usepackage[english]{babel} % English language/hyphenation
\usepackage{graphicx} % Support for images
\usepackage{amssymb,amsmath} % Math packages
\usepackage{multicol} % Three-column layout
\usepackage{url} % Support for clickable links
\usepackage{marvosym} % Symbols
\usepackage{wrapfig} % Allows wrapping text around figures
\usepackage[T1]{fontenc} % Font encoding
\usepackage{charter} % Charter font for main content
\usepackage{blindtext} % Dummy text
\usepackage{datetime} % Custom date
\newdateformat{mydate}{\monthname[\THEMONTH] \THEYEAR}
\usepackage[pdfpagemode=FullScreen, colorlinks=false]{hyperref} % Links and PDF behavior

% Customize footer
\usepackage{fancyhdr}
\pagestyle{fancy}
\lfoot{\footnotesize 
    Science \& Technology Newsletter \\
    \Mundus\ \href{http://www.howtotex.com}{HowToTeX.com} \quad
    \Telefon\ 555-5555 \quad
    \Letter\ \href{mailto:frits@howtotex.com}{frits@howtotex.com}
}
\cfoot{}
\rfoot{\footnotesize ~\\ Page \thepage}
\renewcommand{\headrulewidth}{0.0pt} % No bar on top of page
\renewcommand{\footrulewidth}{0.4pt} % Bar on bottom of page

%%% Definitions for custom commands
\newcommand{\HorRule}[1]{\noindent\rule{\linewidth}{#1}}
\newcommand{\SepRule}{\noindent\begin{center}\rule{250pt}{1pt}\end{center}}
\newcommand{\JournalName}[1]{\begin{center}\Huge #1\end{center}\par\normalsize\normalfont}
\newcommand{\JournalIssue}[1]{\hfill \textsc{\mydate \today, No #1}\par\normalsize\normalfont}
\newcommand{\NewsItem}[1]{\large #1 \vspace{4pt}\par\normalsize\normalfont}
\newcommand{\NewsAuthor}[1]{\hfill by \textsc{#1} \vspace{4pt}\par\normalfont}

\begin{document}
% Your document content follows
\JournalIssue{1}
\JournalName{}
\noindent\HorRule{3pt} \\[-0.75\baselineskip]
\HorRule{1pt}

% Front article
\vspace{0.5cm}
\SepRule
\vspace{0.5cm}

\begin{center}
\begin{minipage}[h]{0.75\linewidth}
	\NewsItem{}
	\emph{}
\end{minipage}
\end{center}

% Other news (1)
\vspace{0.5cm}
\SepRule
\vspace{0.5cm}
\begin{multicols}
	\NewsItem{}
	\NewsAuthor{}
	\emph{}
\end{multicols}
\end{document}""",

    "review": r"""
\documentclass[11pt]{article}
\usepackage{times, geometry, hyperref, natbib, graphicx}
\usepackage{hyperref}
\geometry{letterpaper, margin=1in}
\title{Review Template}
\author{Author Name \\
\small Institution \\
\small \texttt{email@example.com}}
\date{\today}
\begin{document}
\maketitle
\begin{abstract}
This is a sample abstract text.
\end{abstract}
\section{Introduction}
This is the introduction section.
\section{Literature Review}
This section reviews the literature.
\section{Discussion}
Discussion of the findings.
\section{Conclusion}
Conclusions drawn from the discussion.
\section*{Acknowledgments}
Acknowledgments here.
% Uncomment and populate the .bib file for citations
%\bibliographystyle{apalike}
%\bibliography{references}
\end{document}

""",
    "blogpost": r"""
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{graphicx}

\geometry{a4paper, margin=1in}
\title{{title}}
\author{{author}}
\date{{date}}

\begin{document}
\maketitle

\begin{abstract}
{abstract}
\end{abstract}

{content}

% Example of including an image
% \begin{figure}[h]
% \centering
% \includegraphics[width=0.5\textwidth]{{path_to_image}}
% \caption{{caption}}
% \label{fig:example}
% \end{figure}

% Example of a section
% \section{Section Title}
% {section_content}

\end{document}
"""
}


def write_template_to_file(template_name, output_tex_path='output.tex'):
    if template_name not in LaTeX_templates:
        return f"Template '{template_name}' not found."
    
    template = LaTeX_templates[template_name]
    directory = os.path.dirname(output_tex_path)
    if directory:  
        os.makedirs(directory, exist_ok=True)

    with open(output_tex_path, 'w') as tex_file:
        tex_file.write(template)  # Directly write the template without placeholders
    print('Template successfully saved to .tex file.')

def compile_latex_to_pdf(tex_file_path):
    try:
        if not tex_file_path.endswith('.tex'):
            return "Invalid file type. Please provide a .tex file."

        pdf_filename = tex_file_path.replace('.tex', '.pdf')
        # Ensure we're in the correct directory to include any relative paths in the LaTeX document
        os.chdir(os.path.dirname(tex_file_path) or '.')
        
        result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file_path], capture_output=True, text=True)
        
        # Check for compilation errors
        if result.returncode != 0:
            return f"PDF file was not generated due to LaTeX compilation errors. {result.stdout}\n{result.stderr}"
        
        if os.path.exists(pdf_filename):
            return f"PDF successfully generated: {pdf_filename}"
        else:
            return "PDF file was not generated. Check LaTeX compilation errors."
    except Exception as e:
        return f"An error occurred during LaTeX compilation: {e}"
    finally:
        # Ensure we always return to the original directory
        os.chdir(os.getcwd())

if __name__ == '__main__':
    def compile_latex_to_pdf(tex_file_path):
        try:
            if not tex_file_path.endswith('.tex'):
                return "Invalid file type. Please provide a .tex file."

            pdf_filename = tex_file_path.replace('.tex', '.pdf')
            # Ensure we're in the correct directory to include any relative paths in the LaTeX document
            os.chdir(os.path.dirname(tex_file_path) or '.')

            result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file_path], capture_output=True, text=True)

            # Print stdout and stderr to see the compilation messages
            print(result.stdout)
            print(result.stderr)

            # Check for compilation errors
            if result.returncode != 0:
                return f"PDF file was not generated due to LaTeX compilation errors."

            if os.path.exists(pdf_filename):
                print(f"PDF successfully generated: {pdf_filename}")
                return pdf_filename
            else:
                return "PDF file was not generated. Check LaTeX compilation errors."
        except Exception as e:
            print(f"An error occurred during LaTeX compilation: {e}")
        finally:
            # Ensure we always return to the original directory
            os.chdir(os.getcwd())

    output_tex_path = 'static/docs/response.tex'
    compile_latex_to_pdf('static/docs/response.tex')
    subprocess.run(['open' , 'response.pdf'])











# template i am trying to incorporate

# \documentclass[10pt,a4paper]{article}

# % Define geometry
# \setlength\topmargin{-48pt}
# \setlength\headheight{15pt} % Adjusted from 0pt to ensure enough space for headers
# \setlength\headsep{25pt}
# \setlength\marginparwidth{-20pt}
# \setlength\textwidth{7.0in}
# \setlength\textheight{9.5in}
# \setlength\oddsidemargin{-30pt}
# \setlength\evensidemargin{-30pt}

# \frenchspacing % better looking spacing

# % Call packages we'll need
# \usepackage[english]{babel} % English language/hyphenation
# \usepackage{graphicx} % Support for images
# \usepackage{amssymb,amsmath} % Math packages
# \usepackage{multicol} % Three-column layout
# \usepackage{url} % Support for clickable links
# \usepackage{marvosym} % Symbols
# \usepackage{wrapfig} % Allows wrapping text around figures
# \usepackage[T1]{fontenc} % Font encoding
# \usepackage{charter} % Charter font for main content
# \usepackage{blindtext} % Dummy text
# \usepackage{datetime} % Custom date
# \newdateformat{mydate}{\monthname[\THEMONTH] \THEYEAR}
# \usepackage[pdfpagemode=FullScreen, colorlinks=false]{hyperref} % Links and PDF behavior

# % Customize footer
# \usepackage{fancyhdr}
# \pagestyle{fancy}
# \lfoot{\footnotesize 
#     Science \& Technology Newsletter \\
#     \Mundus\ \href{http://www.howtotex.com}{HowToTeX.com} \quad
#     \Telefon\ 555-5555 \quad
#     \Letter\ \href{mailto:frits@howtotex.com}{frits@howtotex.com}
# }
# \cfoot{}
# \rfoot{\footnotesize ~\\ Page \thepage}
# \renewcommand{\headrulewidth}{0.0pt} % No bar on top of page
# \renewcommand{\footrulewidth}{0.4pt} % Bar on bottom of page

# %%% Definitions for custom commands
# \newcommand{\HorRule}[1]{\noindent\rule{\linewidth}{#1}}
# \newcommand{\SepRule}{\noindent\begin{center}\rule{250pt}{1pt}\end{center}}
# \newcommand{\JournalName}[1]{\begin{center}\Huge #1\end{center}\par\normalsize\normalfont}
# \newcommand{\JournalIssue}[1]{\hfill \textsc{\mydate \today, No #1}\par\normalsize\normalfont}
# \newcommand{\NewsItem}[1]{\large #1 \vspace{4pt}\par\normalsize\normalfont}
# \newcommand{\NewsAuthor}[1]{\hfill by \textsc{#1} \vspace{4pt}\par\normalfont}

# \begin{document}
# % Your document content follows
# \JournalIssue{1}
# \JournalName{Science \& Technology}
# \noindent\HorRule{3pt} \\[-0.75\baselineskip]
# \HorRule{1pt}

# % Front article
# \vspace{0.5cm}
# \SepRule
# \vspace{0.5cm}

# \begin{center}
# \begin{minipage}[h]{0.75\linewidth}
# 	\NewsItem{News on Gaza: Latest Updates}
# 	\emph{Lorem ipsum dolor sit amet, consectetur adipiscing elit...}
# \end{minipage}
# \end{center}

# % Other news (1)
# \vspace{0.5cm}
# \SepRule
# \vspace{0.5cm}
# \begin{multicols}{3}
# 	\NewsItem{Another Perspective on Gaza Crisis}
# 	\NewsAuthor{John Doe}
# 	\emph{Sed ac tellus in tortor luctus efficitur...}
# \end{multicols}
# \end{document}