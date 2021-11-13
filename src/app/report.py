from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile


def generate_report(**kwargs):
    temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', mode='w+b', delete=False)

    HTML(string=render_to_string('report.html', kwargs)).write_pdf(target=temp_file.name)

    return temp_file
