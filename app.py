import pandas as pd
import scipy.stats
import streamlit as st
import time

# Initialize session state variables
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

st.header('Lanzar una moneda')

# Initialize an empty list to hold the chart data
chart_data = []

# Create a line chart
chart = st.line_chart(chart_data)

def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0
    global chart_data

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no

        # Append new mean value to chart_data
        chart_data.append(mean)
        chart.line_chart(chart_data)  # Update the line chart with new data
        time.sleep(0.05)

    return mean

# Streamlit widgets
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iterations', 'mean'])
        ],
        axis=0
    ).reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])
