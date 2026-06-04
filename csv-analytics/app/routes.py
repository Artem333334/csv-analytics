import os
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
from flask import Blueprint, render_template, request, redirect

from analysis import build_chart

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'app/static/uploads'

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload():

    file = request.files['file']

    if file:

        path = os.path.join(UPLOAD_FOLDER, file.filename)

        file.save(path)

        df = pd.read_csv(path)
rows = len(df)
cols = len(df.columns)

missing = df.isnull().sum().sum()

stats = {
    "rows": rows,
    "columns": cols,
    "missing": missing
}
        table = df.head(20).to_html(classes='table table-striped')

        chart = build_chart(df)

        return render_template(
            'table.html',
            table=table,
            chart=chart,
            stats=stats
        )

    return redirect('/')
@main.route('/pdf')
def pdf():

    pdf_file = "report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = [
        Paragraph("CSV Analytics Report", styles['Title']),
        Paragraph("Generated automatically", styles['BodyText'])
    ]

    doc.build(content)

    return send_file(pdf_file, as_attachment=True)
