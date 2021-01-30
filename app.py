import streamlit as st
import pandas as pd
from data_prep import sax
from PIL import Image

st.title("SAX Showcase")

dataset = st.sidebar.selectbox("Select dataset:", ["shampoo sales", "sunspots", "temperatures", "daily female births"])

dataset_paths = {
    "shampoo sales": "data/shampoo.csv",
    "sunspots": "data/monthly-sunspots.csv",
    "temperatures": "data/daily-min-temperatures.csv",
    "daily female births": "data/daily-total-female-births.csv"
}

univar_ts = pd.read_csv(dataset_paths[dataset], index_col="index")
col_name = univar_ts.columns[0]

possible_frames = [i for i in range(1, 27) if len(univar_ts) % i == 0]
frame_selection = st.sidebar.slider("Granularity:", 1, len(possible_frames))
number_frames = possible_frames[frame_selection-1]

st.markdown("### Original Time Series")
st.dataframe(univar_ts)
st.line_chart(univar_ts[col_name])
st.markdown("### Piecewise Aggregate Approximation")
st.write(f"Selected number of frames: {number_frames}")

univar_ts = univar_ts.sort_values(col_name)
sax_col, paa_col = sax(univar_ts[col_name], number_frames)
univar_ts["sax"] = sax_col
univar_ts["paa"] = paa_col
univar_ts = univar_ts.sort_index()
st.line_chart(univar_ts[[col_name, "paa"]])

st.markdown("### Symbolic Aggregate Approximation")
result_sax = ""
for i in univar_ts.sax:
    result_sax += i
st.markdown("```" + result_sax + "```")

sax_summary = pd.DataFrame(set(list(zip(sax_col, paa_col)))).sort_values(1).reset_index(drop=True)
sax_summary.columns = ["sax", "mean_of_frame"]
st.write("Mean of the original time series' values in each frame:")
st.write(sax_summary)

frequencies = {}
for i in set(sax_col):
    frequencies[i] = [sax_col.count(i)]
st.write("Frequency of SAX symbols:")
st.write(pd.DataFrame(frequencies))
    
image = Image.open('lisa_sax.gif')
st.image(image)

st.markdown("### Further Information:")
st.markdown("http://www.cs.ucr.edu/~eamonn/SAX.htm")
st.markdown("https://jmotif.github.io/sax-vsm_site/morea/algorithm/SAX.html")
st.markdown("### Python Implementation:")
st.markdown("by Pavel Senin: https://github.com/seninp/saxpy")