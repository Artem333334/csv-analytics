import os
import pandas as pd

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

        table = df.head(20).to_html(classes='table table-striped')

        chart = build_chart(df)

        return render_template(
            'table.html',
            table=table,
            chart=chart
        )

    return redirect('/')