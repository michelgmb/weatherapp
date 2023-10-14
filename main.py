from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

variable = "Hello"
df = pd.read_csv("data/stations.txt", skiprows=17)
table = df[['STAID', 'STANAME                                 ', ]]
htmlCode = table.to_html()


@app.route("/")
def home():
    return render_template("home.html", data=htmlCode)


# URL Endpoints for satation Particular day temperature
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


# URL Endpoints for all Date, Temperature of a station
@app.route("/api/v1/<station>")
def all_temperature(station):
    station = f"data/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(station, skiprows=20, parse_dates=['    DATE'])
    dict_df = df.to_dict(orient="records")

    return dict_df




@app.route("/api/yearly/v1/<station>/<year>")
def all_year(station, year):
    station = f"data/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(station, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)

    all_year_temp = df.loc[df['    DATE'].str.startswith(str(year))]
    all_year_temp = all_year_temp.to_dict(orient="records")
    return all_year_temp



# print(about(1, 18600105))
if __name__ == "__main__":
    app.run(debug=True, port=5000)  # if you have 2 app give the other app a new port app.run(debug=True, port=5001)