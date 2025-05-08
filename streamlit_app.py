
import streamlit as st
from viz import *
from get_data import *
from config import *
from load_data import load_data
import warnings
warnings.filterwarnings("ignore")
from xlsxwriter import Workbook

@st.cache_data(ttl=3600)  # Atualiza os dados a cada 3600 segundos (1 hora)
def get_data_cached():
    return load_data()

#################################################### BUILD DASHBOARD ############################################

st.set_page_config(page_title=dashboard_main_title, layout="wide")
# white Logo
st.markdown(f'''
    <div style="text-align: center;">
        <img src="{travel_logo_url}" alt="Logo" style="width: 30%;">
    </div>
    ''', unsafe_allow_html=True)
# app title
st.markdown(
    f"<h1 style='color:{default_color1}; text-align: center;'>{dashboard_main_title}</h1>",
    unsafe_allow_html=True
)


df_benchmarks, df_hpi, df_aux_cppi, df_greed_fear, df_warren_buff, df_vix, df_ipc_pt, df_eur, df_fx, df_key_ecb_ir, df_ir_str = get_data_cached()


tab0, tab1, tab4, tab5, tab7, tab8, tab9 = st.tabs(sidebar_indicators2)


with tab0:
    st.markdown(f"<div style='text-align: center;'><h2>Fear & Greed (CNN index)</h2></div>", unsafe_allow_html=True)
    with st.expander("Show and download raw data", expanded=False):
        if st.checkbox("Show raw data",  key="raw_data_tab0"):
            st.markdown(f"<h6 style='color:{default_color1};'>Raw data</h6>", unsafe_allow_html=True)
            st.dataframe(df_greed_fear, hide_index=True)

            st.download_button(label="Download in xlsx format",
                            data=convert_df_to_excel(df_greed_fear),
                            file_name='greed_fear.xlsx',
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        
    with st.expander("Greed & Fear index", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            fear_greed_plot(df_greed_fear)
        with col2:
            st.markdown("#")
            st.markdown(fear_greed_str, unsafe_allow_html=True)
            st.write("**Source:** https://edition.cnn.com/markets/fear-and-greed?utm_source=hp")
        
    with st.expander("Fear and Greed evolution and anomalies over time", expanded=True):    
        if st.checkbox("Show anomalies", key="show_anomalies_tab0"):
            st.markdown(f"<h6 style='color:{default_color1};'>Anomalies</h6>", unsafe_allow_html=True)
            method = st.selectbox("Select anomaly detection method", options=["isolation_forest", "HMM", "zscore"])

            col3, col4 = st.columns(2)
            with col3:
                plot_anomalies(df_greed_fear, 'Rating', method)
            with col4:
                plot_interactive_time_series(df_greed_fear[['Date', 'Rating']], option_to_choose_variables='no')
        else: 
            plot_interactive_time_series(df_greed_fear[['Date', 'Rating']], option_to_choose_variables='no')

with tab1:
    st.markdown(f"<div style='text-align: center;'><h2>Stock Market Indicators</h2></div>", unsafe_allow_html=True)

    col6, col7 = st.columns(2)

    with col6:
        st.markdown(f"<div style='text-align: center; color: #179297;'><h2>VIX - Volatility index</h2></div>", unsafe_allow_html=True)

        with st.expander('Show and download raw data', expanded=False):
            st.markdown(f"<h6 style='color:{default_color1};'>Raw data</h6>", unsafe_allow_html=True)
            st.dataframe(df_vix, hide_index=True)

            st.download_button(label="Download in xlsx format",
                            data=convert_df_to_excel(df_vix),
                            file_name='vix.xlsx',
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with st.expander("VIX evolution over time", expanded=True):
            plot_interactive_time_series(df_vix, option_to_choose_variables='no')

        with st.expander('Times anomaly detection', expanded=False):
            method = st.selectbox("Select anomaly detection method", options=["isolation_forest", "HMM", "zscore"], key="anom_tab1")
            plot_anomalies(df_vix, 'VIX', method)

        st.write("**Source:** https://finance.yahoo.com/quote/%5EVIX/")
        st.markdown(vix_str, unsafe_allow_html=True)

    with col7:
        st.markdown(f"<div style='text-align: center; color: #179297'><h2>Warren Buffett indicator - Marketcap to GDP</h2></div>", unsafe_allow_html=True)

        with st.expander('Show and download raw data', expanded=False):
            st.markdown(f"<h6 style='color:{default_color1};'>Raw data</h6>", unsafe_allow_html=True)
            st.dataframe(df_warren_buff, hide_index=True)

            st.download_button(label="Download in xlsx format",
                            data=convert_df_to_excel(df_warren_buff),
                            file_name='warren_buffett_index.xlsx',
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with st.expander("Warren Buffett index over time", expanded=True):
            plot_interactive_time_series(df_warren_buff[['Date', 'Indicador de Warren Buffett (%)']], option_to_choose_variables='no')

        with st.expander('Times anomaly detection', expanded=False):
            method = st.selectbox("Select anomaly detection method", options=["isolation_forest", "HMM", "zscore"], key='anom_tab2')
            plot_anomalies(df_warren_buff, 'Indicador de Warren Buffett (%)', method)

        #st.write("**Source:** https://edition.cnn.com/markets/fear-and-greed?utm_source=hp")
        st.markdown(warren_str, unsafe_allow_html=True)
    
    st.divider()

    col8, col9 = st.columns(2)

    with col8:
        st.markdown(f"<div style='text-align: center; color: #179297'><h2>Benchmark Indexs</h2></div>", unsafe_allow_html=True)

        with st.expander('Show and download raw data', expanded=False):
            st.markdown(f"<h6 style='color:{default_color1};'>Raw data</h6>", unsafe_allow_html=True)
            st.dataframe(df_benchmarks, hide_index=True)
        
            st.download_button(label="Download in xlsx format",
                            data=convert_df_to_excel(df_benchmarks),
                            file_name='benchmarks.xlsx',
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        with st.expander("Stock market benchmarks", expanded=True):
            normalize = st.checkbox("Normalize variables", key="normalize_benchmarks")
            
            if normalize:
                # Normalizando as variáveis (excluindo a coluna 'Date')
                df_benchmarks_normalized = df_benchmarks.copy()
                for col in df_benchmarks_normalized.columns[1:]:
                    df_benchmarks_normalized[col] = (df_benchmarks_normalized[col] - df_benchmarks_normalized[col].min()) / (df_benchmarks_normalized[col].max() - df_benchmarks_normalized[col].min())
                plot_interactive_time_series(df_benchmarks_normalized)
            else:
                plot_interactive_time_series(df_benchmarks)

        with st.expander('Times anomaly detection', expanded=False):
            column = st.selectbox("Select column to analyze anomalies", options=df_benchmarks.columns[1:], index=0)
            method = st.selectbox("Select anomaly detection method", options=["isolation_forest", "HMM", "zscore"], key="stock_market_bench")
            plot_anomalies(df_benchmarks, column, method)

        st.write("**Source:** Yahoo Finance")
        st.markdown(index_str, unsafe_allow_html=True)

    with col9:

        fig = correlation_matrix2(df_benchmarks)

        # Mostrar no Streamlit
        st.plotly_chart(fig, use_container_width=True)
        #correlation_matrix2(df_benchmarks, "Correlation matrix")

with tab4:

    col20, col21 = st.columns(2)

    with col20:
        st.markdown(f"<div style='text-align: center; color: #179297'><h2>Euribor rates</h2></div>", unsafe_allow_html=True)

        if st.checkbox("Show raw data",  key="raw_data_tab4"):
            st.markdown(f"<h6 style='color:{default_color1};'>Raw data</h6>", unsafe_allow_html=True)
            st.dataframe(df_eur, hide_index=True)

            st.download_button(label="Download in xlsx format",
                            data=convert_df_to_excel(df_eur),
                            file_name='euribors.xlsx',
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        plot_interactive_time_series(df_eur)
        st.write("**Source:** Yahoo Finance")
        st.markdown(euribor_str, unsafe_allow_html=True)

    with col21:
        with st.expander("What is the likelihood that the Fed will change the Federal target rate at upcoming FOMC meetings, according to interest rate traders?", expanded=False):
            st.markdown(f"<div style='text-align: center;'><h2>CME FedWatch Tool</h2></div>", unsafe_allow_html=True)
            st.markdown(cme_tool_str, unsafe_allow_html=True)
            st.markdown(md_botao_cme, unsafe_allow_html=True)


        with st.expander('Euro short-term rate (€STR)', expanded=True):
            st.markdown(f"<div style='text-align: center; color: #179297'><h2>Euro short-term rate (€STR)</h2></div>", unsafe_allow_html=True)

            if st.checkbox("Show raw data", key="raw_data_tab9"):
                st.markdown(f"<h6 style='color:{default_color1};'>Raw data</h6>", unsafe_allow_html=True)
                st.dataframe(df_ir_str, hide_index=True)

                st.download_button(label="Download in xlsx format",
                                data=convert_df_to_excel(df_ir_str),
                                file_name='short_term_rates.xlsx',
                                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            plot_interactive_time_series(df_ir_str, option_to_choose_variables='no')

            st.write("**Source:** https://bpstat.bportugal.pt/dados/series?mode=graphic&svid=6698&series=12559714")
            st.markdown(ir_str_str, unsafe_allow_html=True)


        with st.expander('Key ECB interest rates', expanded=True):
            st.markdown(f"<div style='text-align: center; color: #179297'><h2>Key ECB interest rates</h2></div>", unsafe_allow_html=True)

            if st.checkbox("Show raw data", key="raw_data_tab10"):
                st.markdown(f"<h6 style='color:{default_color1};'>Raw data</h6>", unsafe_allow_html=True)
                st.dataframe(df_key_ecb_ir, hide_index=True)

                st.download_button(label="Download in xlsx format",
                                data=convert_df_to_excel(df_key_ecb_ir),
                                file_name='key_ecb_ir.xlsx',
                                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            plot_interactive_time_series(df_key_ecb_ir)

            st.write("**Source:**  https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.pt.html")
            st.markdown(key_ecb_str, unsafe_allow_html=True)



with tab5:
    st.markdown(f"<div style='text-align: center;'><h3>Property prices - Portugal and Euro Area</h3></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div style='text-align: center; color: #179297'><h3>Commercial Property prices - Portugal and Euro Area</h3></div>", unsafe_allow_html=True)

        with st.expander("Show and download raw data", expanded=False):
            if st.checkbox("Show raw data",  key="raw_data_tab5"):
                st.markdown(f"<h6 style='color:{default_color1};'>Raw data</h6>", unsafe_allow_html=True)
                st.dataframe(df_aux_cppi, hide_index=True)

                st.download_button(label="Download in xlsx format",
                                data=convert_df_to_excel(df_aux_cppi),
                                file_name='cppi.xlsx',
                                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                
        with st.expander("Plot Commercial Property prices data", expanded=True):
            normalizey = st.checkbox("Normalize variables", key="normalize_cppi")
    
            if normalizey:
                # Normalizando as variáveis (excluindo a coluna 'Date')
                df_aux_cppi_normalized = df_aux_cppi.copy()
                for col in df_aux_cppi_normalized.columns[1:]:
                    df_aux_cppi_normalized[col] = (df_aux_cppi_normalized[col] - df_aux_cppi_normalized[col].min()) / (df_aux_cppi_normalized[col].max() - df_aux_cppi_normalized[col].min())
                plot_interactive_time_series_years(df_aux_cppi_normalized)
            else:
                plot_interactive_time_series_years(df_aux_cppi)
            st.write("**Source:** ECB & BIS")
            st.markdown(cpp_str, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div style='text-align: center; color: #179297'><h3>Residential Property prices - Portugal and Euro Area</h3></div>", unsafe_allow_html=True)
        with st.expander("Show and download raw data", expanded=False):
            if st.checkbox("Show raw data",  key="raw_data_tab6"):
                st.markdown(f"<h6 style='color:{default_color1};'>Raw data</h6>", unsafe_allow_html=True)
                st.dataframe(df_hpi, hide_index=True)

                st.download_button(label="Download in xlsx format",
                                data=convert_df_to_excel(df_hpi),
                                file_name='residential_price_index.xlsx',
                                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with st.expander("Plot Residential Property prices data", expanded=True):
            normalizex = st.checkbox("Normalize variables", key="normalize_hpi")

            if normalizex:
                # Normalizando as variáveis (excluindo a coluna 'Date')
                df_hpi_normalized = df_hpi.copy()
                for col in df_hpi_normalized.columns[1:]:
                    df_hpi_normalized[col] = (df_hpi_normalized[col] - df_hpi_normalized[col].min()) / (df_hpi_normalized[col].max() - df_hpi_normalized[col].min())
                plot_interactive_time_series(df_hpi_normalized)
            else:
                plot_interactive_time_series(df_hpi)

        with st.expander("Time series anomaly detection"):
            if st.checkbox("Show anomalies", key="show_anomalies_tab6"):
                column = st.selectbox("Select column to analyze anomalies", options=df_hpi.columns[1:], index=0)
                method = st.selectbox("Select anomaly detection method", options=["isolation_forest", "HMM", "zscore"])
                plot_anomalies(df_hpi, column, method)

        st.write("**Source:** ECB")
        st.markdown(resi_str, unsafe_allow_html=True)

with tab7:
    st.markdown(f"<div style='text-align: center; color: #179297'><h2>Inflation (CPI) - Portugal</h2></div>", unsafe_allow_html=True)

    if st.checkbox("Show raw data",  key="raw_data_tab7"):
        st.markdown(f"<h6 style='color:{default_color1};'>Raw data</h6>", unsafe_allow_html=True)
        st.dataframe(df_ipc_pt, hide_index=True)

        st.download_button(label="Download in xlsx format",
                           data=convert_df_to_excel(df_ipc_pt),
                           file_name='inflation_portugal.xlsx',
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    plot_interactive_time_series(df_ipc_pt, option_to_choose_variables='no')
    st.write("**Source:** https://bpstat.bportugal.pt/serie/5721524")
    st.markdown(inflation_str, unsafe_allow_html=True)

with tab8:
    st.markdown(f"<div style='text-align: center;'><h2>Currency exchange rates</h2></div>", unsafe_allow_html=True)

    if st.checkbox("Show raw data",  key="raw_data_tab8"):
        st.markdown(f"<h6 style='color:{default_color1};'>Raw data</h6>", unsafe_allow_html=True)
        st.dataframe(df_fx, hide_index=True)

        st.download_button(label="Download in xlsx format",
                           data=convert_df_to_excel(df_fx),
                           file_name='fx_rates.xlsx',
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    plot_interactive_time_series(df_fx)
    st.write("**Source:** https://finance.yahoo.com/quote/EURUSD=X/")

with tab9:
    st.markdown(f"<div style='text-align: center;'><h2>Commodities</h2></div>", unsafe_allow_html=True)
    st.write("In progress ...")




