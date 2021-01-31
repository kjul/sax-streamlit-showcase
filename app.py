import streamlit as st
import pandas as pd
import numpy as np
from data_prep import sax, cuts_for_asize
from PIL import Image
import string

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
size_of_alphabet = st.sidebar.slider("Alphabet size:", 2, 20)

sd = np.std(univar_ts)
mean = np.mean(univar_ts)
cuts = np.array(cuts_for_asize(size_of_alphabet))
sax_cuts = [i * sd + mean for i in cuts]
sax_cuts.pop(0)
alphabet = list(string.ascii_lowercase) 
for i, j in enumerate(sax_cuts):
    univar_ts["upper bound of " + alphabet.pop(0)] = int(j)
st.dataframe(univar_ts)
st.line_chart(univar_ts)

st.markdown("### Symbolic Aggregate Approximation")
univar_ts["sax"] = sax(univar_ts[col_name], size_of_alphabet)
result_sax = "".join(univar_ts.sax)
st.markdown("```" + result_sax + "```")

st.write("Frequency of SAX symbols:")
frequencies = {}
for i in set(list(result_sax)):
    frequencies[i] = [result_sax.count(i)]
st.write(pd.DataFrame(frequencies))
    
image = Image.open('lisa_sax.gif')
st.image(image)

st.markdown("### Further Information:")
st.markdown("http://www.cs.ucr.edu/~eamonn/SAX.htm")
st.markdown("https://jmotif.github.io/sax-vsm_site/morea/algorithm/SAX.html")
st.markdown("### Python Implementation:")
st.markdown("by Pavel Senin: https://github.com/seninp/saxpy")
