import os
import tempfile
from django.template.loader import render_to_string
from weasyprint import HTML


def generate_report(**kwargs):
    base_path = os.path.dirname(os.path.abspath(__file__)) + '/templates/print/'
    temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', mode='w+b', delete=False)

    HTML(string=render_to_string('report.html', kwargs), base_url=f'{base_path}').write_pdf(target=temp_file.name)

    return temp_file
