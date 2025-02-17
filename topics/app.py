import streamlit as st
import pandas as pd
import numpy as np

st.title("StreamLit")

st.write("This is a simple text.")

df = pd.DataFrame({
    "column A": [1, 2, 3, 4, 5],
    "column B": [10, 20, 30, 40, 50]
}
)

st.write(df)

st.write("-----------------------------")

chart_data = pd.DataFrame(
    np.random.randn(20, 3), columns=['a', 'b', 'c']
)
st.line_chart(chart_data)
