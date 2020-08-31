from flask import Flask, render_template
import os
from utils.gsheet import extract_sheet

app = Flask(__name__)
global dic_df


@app.route("/")
def home():
    return render_template("index.html.j2")

@app.route('/oauth2callback')
def callback():
  dic_df = extract_sheet()
  df = dic_df['A']
  return render_template("df.html.j2", length = len(df), dataframe=df.to_html())


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 
