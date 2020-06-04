import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import base64
import streamlit as st
import base64
from io import BytesIO


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'


def main():
    st.title("Yazlık Tüketim Toplamının dağılımı")
    data = pd.read_csv(r"bins.csv")
    data = data[data["Yaz_bin_min"] <=10000]
    fig = px.histogram(data, x="Yaz_bin_min", y="TESISAT_NO",
                   marginal="box", # or violin, rug
                   hover_data=data.columns,histfunc='sum')
    st.plotly_chart(fig)

    slider_yaz_tuk=st.slider("Minimum Yaz Tüketimi",0,10000, step=25)

    rel_data_2=data[data["Yaz_bin_min"]>=slider_yaz_tuk]
    fin_abone_1 = rel_data_2["TESISAT_NO"].sum()
    st.success("{} abone seçildi".format(fin_abone_1))


    st.title("Yazlık Tüketim Ratiosunun dağılımı")


    fig2 = px.histogram(rel_data_2, x="ratio_bin_min", y="TESISAT_NO",
                   marginal="box", # or violin, rug
                   hover_data=rel_data_2.columns,histfunc='sum')

    st.plotly_chart(fig2)

    slider_yaz_ratiosu = st.slider("Minimum Yaz Ratiosu", 0, 100, step=2)

    rel_data_3=rel_data_2[rel_data_2["ratio_bin_min"]>=slider_yaz_ratiosu]
    fin_abone = rel_data_3["TESISAT_NO"].sum()
    st.success("{} abone seçildi".format(fin_abone))


    if st.checkbox("Müşteri datasını indirmek istiyorum"):
        bins_w_customer=pd.read_hdf(r"bins_numbers.hdf")
        bins_w_customer=bins_w_customer[(bins_w_customer["Yaz_bin_min"]>=slider_yaz_tuk)&(bins_w_customer["ratio_bin_min"]>=slider_yaz_ratiosu)]
        x=bins_w_customer.groupby(by=["BOLGE_ADI"])["TESISAT_NO"].sum().reset_index()
        fig_pie = px.pie(x, values='TESISAT_NO', names='BOLGE_ADI')
        st.plotly_chart(fig_pie)

        st.dataframe(bins_w_customer.sort_values(by="TESISAT_NO", ascending=False))
        st.markdown(get_table_download_link(bins_w_customer), unsafe_allow_html=True)

if __name__ == '__main__':
    main()

