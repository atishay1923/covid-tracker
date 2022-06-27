def find_top_confirmed(n = 15):

    import pandas as pd
    corona_df=pd.read_csv(r"C:\Users\91724\Desktop\Corona\covid-19-dataset-2.csv")
    by_country = corona_df.groupby('Country_Region').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
    cdf = by_country.nlargest(n, 'Confirmed')
    cdf1=cdf.filter(['Confirmed',  'Recovered'])
    return cdf1


cdf=find_top_confirmed()
pairs=[(country,confirmed,recovery) for country,confirmed,recovery in zip(cdf.index,cdf['Confirmed'],cdf['Recovered'])]


from textwrap import fill
from turtle import color, fillcolor
import folium
import pandas as pd
corona_df = pd.read_csv(r"C:\Users\91724\Desktop\Corona\covid-19-dataset-2.csv")
corona_df=corona_df[['Lat','Long_','Confirmed']]
corona_df=corona_df.dropna()

m=folium.Map(location=[23.2599,77.4126],
            tiles="stamen toner",
            zoom_start=12)

def circle_maker(x):
    folium.Circle(location=[x[0],x[1]],
                 radius=float(x[2]),
                 color='orangered',
            
                 popup='confirmed cases:{}'.format(x[2])).add_to(m)
corona_df.apply(lambda x:circle_maker(x),axis=1)

html_map=m._repr_html_()
from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html",table=cdf, cmap=html_map,pairs=pairs)

if __name__=="__main__":
    app.run(debug=True)