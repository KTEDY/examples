import streamlit as st
import pandas as pd
import requests

import plotly.graph_objects as go

from datetime import datetime
from dateutil.relativedelta import relativedelta


def date_time(delta):
    time = datetime.today() - relativedelta(months=delta)
    return time.strftime("%Y-%m-%d")


def tga_requests():
    time_delta = 12
    size = time_delta * 31

    base_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
    end_point = "/v1/accounting/dts/dts_table_1"
    field = f"?fields=record_date, open_today_bal&" \
            f"sort=record_date&" \
            f"filter=account_type:in:(Treasury General Account (TGA) Closing Balance),record_date:gte:{date_time(time_delta)}&" \
            f"format=json&page[size]={size}"

    req = requests.get(base_url + end_point + field).json()

    df = pd.DataFrame(req["data"]).astype({"open_today_bal": "int"})
    return df
# df.set_index("record_date", inplace=True)
# {open_today_bal=154808, record_date=2023-05-10}


def streamlit_run():
    df = tga_requests()

    st.write("TGA_Daily streamlit visualize example")

    fig = go.Figure([go.Scatter(x=df["record_date"], y=df["open_today_bal"])])
    st.plotly_chart(fig)

    with st.expander("show raw data"):
        st.table(df)


if __name__ == "__main__":
    streamlit_run()
