import streamlit as st
import plotly_express as px
import pandas as pd
import numpy as np



data_sources = {
    "Champions League": './538_champions_league.csv',
    "NBA": './538_nba.csv',
    "NFL": './538_nfl.csv',
    "Premier League": './538_premier_league.csv'
    }


df_color=pd.read_csv('https://raw.githubusercontent.com/aaroncolesmith/bovada/master/color_map.csv')
trans_df = df_color[['team','primary_color']].set_index('team').T
color_map=trans_df.to_dict('index')['primary_color']

# word_freq.update({'before': 23})
del df_color
del trans_df


def app():



    st.title('538 Viz')

    # with st.form("input_form"):
    #     # st.write("Select a Sport / Competition")
    #     sel = st.radio("Select sport/competition:", list(data_sources.keys()))
    #     submit_button = st.form_submit_button(label='Submit')
    #
    # if submit_button:
    #     data = data_sources[sel]
    #     st.write(data)
    #     df=pd.read_csv(data)
    #     st.write(df.head(5))
    #
    #     columns=df.columns
    #     numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    #     num_columns = df.select_dtypes(include=numerics).columns.tolist()
    #
    #     title_columns = [x.title() for x in num_columns]
    #     title_columns = [x.replace('_',' ') for x in title_columns]
    #
    #     col_dict = dict(zip(title_columns, num_columns))
    #     a=np.insert(list(col_dict.keys()),0,'')
    #
    #     col_select=st.selectbox('Select a metric -', a)
    #
    #     if len(col_select) > 0:
    #         st.write(col_select)
    #         st.write(col_dict[col_select])




    sel = st.radio("Select sport/competition:", list(data_sources.keys()))

    data = data_sources[sel]
    d=pd.read_csv(data)

    columns=d.columns
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    num_columns = d.select_dtypes(include=numerics).columns.tolist()

    title_columns = [x.title() for x in num_columns]
    title_columns = [x.replace('_',' ') for x in title_columns]
    title_columns = [x.replace('Ucl','UCL') for x in title_columns]
    title_columns = [x.replace('Elo','ELO') for x in title_columns]
    title_columns = [x.replace('Spi','SPI') for x in title_columns]

    col_dict = dict(zip(title_columns, num_columns))
    a=np.insert(list(col_dict.keys()),0,'')

    col_select=st.selectbox('Select a metric -', a)

    if len(col_select) > 0:
        val = col_dict[col_select]
        d[val] = pd.to_numeric(d[val])

        fig=px.scatter(d,
                   x='updated',
                   y=val,
                   color='team',
                   title='Odds Over Time',
                   render_mode='svg',
                   color_discrete_map=color_map)
        fig.update_traces(mode='lines',
                            line_shape='spline',
                            opacity=.75,
                            marker=dict(size=8,line=dict(width=1,color='DarkSlateGrey')),
                            line = dict(width=4))

        if col_select in ['ELO','SPI']:
            fig.update_yaxes(title=val.replace('_',' ').title())
        else:
            fig.update_yaxes(tickformat = ',.0%',title=val.replace('_',' ').title())
        fig.update_xaxes(title='Date')
        st.plotly_chart(fig)


        d[val+'_pct_change_initial']=d.groupby('team')[val].transform(lambda x: (x-x.iloc[0]))
        fig=px.scatter(d,
                   x='updated',
                   y=val+'_pct_change_initial',
                   title='Change Vs. Initial Odds',
                   color='team',
                   color_discrete_map=color_map,
                   render_mode='svg')
        fig.update_traces(mode='lines',
                            line_shape='spline',
                            opacity=.75,
                            marker=dict(size=8,line=dict(width=1,color='DarkSlateGrey')),
                            line = dict(width=4))
        if col_select in ['ELO','SPI']:
            fig.update_yaxes(title=val.replace('_',' ').title())
        else:
            fig.update_yaxes(tickformat = ',.0%',title=val.replace('_',' ').title())
        fig.update_xaxes(title='Date')
        st.plotly_chart(fig)


        fig=px.bar(
            d.loc[pd.to_datetime(d.updated) == pd.to_datetime(d.updated).max()].sort_values(val,ascending=False),
            x='team',
            y=val,
            title='Latest Odds by Team',
            color='team',
            color_discrete_map=color_map,
            )
        if col_select in ['ELO','SPI']:
            fig.update_yaxes(title=val.replace('_',' ').title())
        else:
            fig.update_yaxes(tickformat = ',.0%',title=val.replace('_',' ').title())
        fig.update_xaxes(title='Team')

        del d[val+'_pct_change_initial']
        st.plotly_chart(fig)








if __name__ == "__main__":
    #execute
    app()
