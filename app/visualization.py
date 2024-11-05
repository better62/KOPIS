import streamlit as st
import pandas as pd

def date_visual(result):
    result = [item for sublist in result for item in sublist]
    df = pd.DataFrame(result, columns=['항목', '내용'])
    df = df.sort_values(by="항목")
    st.table(df.set_index('항목'))

def region_visual(result):
    result = [item for sublist in result for item in sublist]
    df = pd.DataFrame(result, columns=['항목', '내용'])
    df = df.sort_values(by="항목")
    st.table(df.set_index('항목'))

def genre_visual(result):
    result = [item for sublist in result for item in sublist]
    df = pd.DataFrame(result, columns=['항목', '내용'])
    df = df.sort_values(by="항목")
    st.table(df.set_index('항목'))


def performance_visual(result):
    result = [item for sublist in result for item in sublist]
    df = pd.DataFrame(result, columns=['항목', '내용'])
    df = df.sort_values(by="항목")
    st.table(df.set_index('항목'))


def facility_visual(result):
    result = [item for sublist in result for item in sublist]
    df = pd.DataFrame(result, columns=['항목', '내용'])
    df['내용'] = df['내용'].replace({"N":"없음", "Y":'있음'})
    df = df.sort_values(by="항목")
    st.table(df.set_index('항목'))




