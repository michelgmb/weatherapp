from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

variable = "Hello"
df = pd.read_csv("data/stations.txt",skiprows=17)
table = df[['STAID', 'STANAME                                 ',]]
htmlCode = table.to_html()
@app.route("/")
def home():
    return render_template("home.html", data=htmlCode)


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    date = int(date)
    station = f"data/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(station, skiprows=20)

    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

    return {
        "Station": station,
        "Date": date,
        "Temperature": temperature

    }


# print(about(1, 18600105))
if __name__ == "__main__":
    app.run(debug=True, port=5022)  # if you have 2 app give the other app a new port app.run(debug=True, port=5001)
