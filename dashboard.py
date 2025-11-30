import streamlit as st
import pandas as pd
import json
from kafka import KafkaConsumer
import time
import plotly.express as px

st.set_page_config(layout="wide", page_title="Real-Time Traffic AI")
st.title("🚦 Real-Time Traffic Analysis")

def get_consumer():
    try:
        return KafkaConsumer(
            'traffic_data',
            bootstrap_servers=['kafka:29092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='latest'
        )
    except:
        return None

consumer = get_consumer()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Live Speed (km/h)")
    speed_metric = st.empty()
    speed_chart = st.empty()

with col2:
    st.subheader("Traffic Condition")
    condition_box = st.empty()
    raw_data_table = st.empty()

data_buffer = []

if consumer:
    for message in consumer:
        new_data = message.value
        data_buffer.append(new_data)
        if len(data_buffer) > 20: data_buffer.pop(0)
        
        df = pd.DataFrame(data_buffer)
        
        current_speed = new_data['current_speed']
        free_flow = new_data['free_flow_speed']
        
        speed_metric.metric("Current Speed", f"{current_speed} km/h", f"{current_speed - free_flow} km/h")
        
        if current_speed < (free_flow * 0.5):
            condition_box.error("🚨 HEAVY CONGESTION")
        elif current_speed < (free_flow * 0.8):
            condition_box.warning("⚠️ MODERATE TRAFFIC")
        else:
            condition_box.success("✅ FREE FLOW")

        fig = px.line(df, x='timestamp', y='current_speed', title='Speed Trend')
        speed_chart.plotly_chart(fig, use_container_width=True)
        raw_data_table.dataframe(df.tail(5))
else:
    st.info("Waiting for data stream... (App is starting)")
    time.sleep(2)
    st.rerun()