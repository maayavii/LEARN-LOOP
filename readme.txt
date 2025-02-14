user Agora app to create a virtual video call
created an account and bought an id
made urls and views implimented a column


//for file convertion

    Here’s a summary of the libraries used and their roles:

    Pillow (PIL):
        Image processing, such as converting .jpg to .png.

    python-docx:
        Reading and manipulating .docx (Word) files.

    reportlab:
        Creating .pdf files programmatically.

    PyPDF2:
        Reading and writing .pdf files.

    python-pptx (for potential PowerPoint handling):
        Manipulating .pptx files.


Required Python Packages:

pdf2docx - For PDF to DOCX conversion
python-docx2pdf - For DOCX to PDF conversion
Pillow (PIL) - For image processing
PyPDF2 - For PDF manipulation
python-pptx - For PowerPoint manipulation
reportlab - For PDF generation

Django Setup:

Django app name: file_converter
Media handling setup in settings.py
MEDIA_URL and MEDIA_ROOT configuration

File Types Supported:

PDF (.pdf)
Word Documents (.docx)
PowerPoint (.pptx)
Images (.jpg, .jpeg, .png)

Frontend Technologies:

HTML5
JavaScript (Vanilla JS)
Bootstrap CSS framework
CSRF token handling for security

Project Structure:

models.py - Database models
views.py - View functions
urls.py - URL routing
utils.py - Utility functions
templates/ - HTML templates
media/ - File storage

uploads/
converted/
documents/
edited/



Key Features:

File format conversion
Document editing
Page removal
Page insertion
File preview
Download edited files