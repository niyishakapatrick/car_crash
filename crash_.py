import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objs as go

# st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="Crash Dashboard", page_icon="🚧", layout="wide")
st.header("ROAD CRASH ANALYTICS DASHBOARD")
st.markdown("Data: Rwanda Road Traffic Crashes 2013", unsafe_allow_html=True)

# Load crash dataset
df = pd.read_csv('crash_data.csv')  # Make sure this file exists in your project

# Ensure necessary columns exist
if 'hour_crash' not in df.columns:
    st.error("Missing 'hour_crash' column in the dataset!")
    st.stop()

# Sidebar filters
st.sidebar.image("data/ur_aceds.png", caption="")
vehicle_type = st.sidebar.multiselect("Select Vehicle Type", options=df["type_vehicle"].dropna().unique(), default=df["type_vehicle"].dropna().unique())
road_type = st.sidebar.multiselect("Select Road Type", options=df["road_type"].dropna().unique(), default=df["road_type"].dropna().unique())
condition = st.sidebar.multiselect("Select Road Condition", options=df["road_condition"].dropna().unique(), default=df["road_condition"].dropna().unique())

# Filtered Data
df_selection = df.query("type_vehicle == @vehicle_type and road_type == @road_type and road_condition == @condition")

if df_selection.empty:
    st.warning("No data available for selected filters. Please adjust your filter options.")
    st.stop()

# Metrics & Summary
def Home():
    with st.expander("📋 VIEW CRASH DATASET"):
        columns_to_show = st.multiselect(
            "Select columns to display",
            options=df_selection.columns.tolist(),  # Convert Index to list
            default=df_selection.columns.tolist()   # Convert Index to list
        )

        st.dataframe(df_selection[columns_to_show], use_container_width=True)

    total_crashes = len(df_selection)
    avg_age = df_selection['age'].mean()
    min_age = df_selection['age'].min()
    max_age = df_selection['age'].max()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Crashes", total_crashes)
    col2.metric("Average Age", f"{avg_age:.1f}")
    col3.metric("Min Age", f"{min_age:.1f}")
    col4.metric("Max Age", f"{max_age:.1f}")
    
    style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")

    with st.expander("📊 AGE DISTRIBUTION"):
        df_selection['age'].hist(bins=20, color='skyblue')
        st.pyplot()

# Charts
def graphs():
    # Bar chart: Crashes by Vehicle Type
    vehicle_crash_count = df_selection["type_vehicle"].value_counts()
    fig_bar = px.bar(vehicle_crash_count, x=vehicle_crash_count.index, y=vehicle_crash_count.values,
                     labels={"x": "Vehicle Type", "y": "Number of Crashes"},
                     title="Crashes by Vehicle Type", color_discrete_sequence=["#0083B8"])

    # Crashes by Hour (Horizontal Bar Chart)
    crash_by_hour = df_selection["hour_crash"].value_counts().sort_index()
    fig_hbar = px.bar(crash_by_hour, y=crash_by_hour.index, x=crash_by_hour.values,
                      labels={"y": "Hour of Crash", "x": "Count"},
                      title="Crashes by Hour", orientation="h", color_discrete_sequence=["#0083B8"])

    left, right = st.columns(2)
    left.plotly_chart(fig_bar, use_container_width=True)
    right.plotly_chart(fig_hbar, use_container_width=True)

    with st.expander("📍 Pie Chart: Gender Distribution"):
        fig_pie = px.pie(df_selection, names="gender", title="Crash Distribution by Gender")
        st.plotly_chart(fig_pie, use_container_width=True)

# Progress Bar
def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""", unsafe_allow_html=True)
    target = 100  # Replace with a real KPI if needed
    current = len(df_selection)
    percent = round((current / target) * 100)
    mybar = st.progress(0)

    if percent > 100:
        st.success("Target Achieved 🎯")
    else:
        st.write(f"You have {percent}% of the crash data target ({target} entries)")
        for i in range(percent):
            time.sleep(0.01)
            mybar.progress(i + 1, text="Processing Crash Records")

# Menu Navigation
def sideBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Progress"],
            icons=["house", "graph-up"],
            menu_icon="menu-up",
            default_index=0
        )
    if selected == "Home":
        Home()
        graphs()
    elif selected == "Progress":
        Progressbar()
        graphs()

sideBar()

# Boxplot
st.subheader("🚘 VEHICLE TYPE BY AGE DISTRIBUTION")
feature_y = st.selectbox("Select Quantitative Feature", df_selection.select_dtypes(include='number').columns)
fig2 = go.Figure(
    data=[go.Box(x=df_selection['type_vehicle'], y=df_selection[feature_y], name='')],
    layout=go.Layout(
        title="Vehicle Type by Age Distribution (Boxplot)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
        font=dict(color='black')
    )
)
st.plotly_chart(fig2, use_container_width=True)

# Hide Streamlit Footer
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)





# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from streamlit_option_menu import option_menu
# from numerize.numerize import numerize
# import time
# from streamlit_extras.metric_cards import style_metric_cards
# import plotly.graph_objs as go

# st.set_option('deprecation.showPyplotGlobalUse', False)
# st.set_page_config(page_title="Crash Dashboard", page_icon="🚧", layout="wide")
# st.header("ROAD CRASH ANALYTICS DASHBOARD")

# # Load crash dataset
# df = pd.read_csv('crash_data.csv')  # Make sure this file exists in your project

# # Sidebar filters
# st.sidebar.image("data/ur_aceds.png", caption="")
# vehicle_type = st.sidebar.multiselect("Select Vehicle Type", options=df["type_vehicle"].dropna().unique(), default=df["type_vehicle"].dropna().unique())
# road_type = st.sidebar.multiselect("Select Road Type", options=df["road_type"].dropna().unique(), default=df["road_type"].dropna().unique())
# condition = st.sidebar.multiselect("Select Road Condition", options=df["road_condition"].dropna().unique(), default=df["road_condition"].dropna().unique())

# # Filtered Data
# df_selection = df.query("type_vehicle == @vehicle_type and road_type == @road_type and road_condition == @condition")

# if df_selection.empty:
#     st.warning("No data available for selected filters. Please adjust your filter options.")
#     st.stop()
# # Metrics & Summary
# def Home():
#     with st.expander("📋 VIEW CRASH DATASET"):
#         columns_to_show = st.multiselect(
#     "Select columns to display",
#     options=df_selection.columns.tolist(),  # Convert Index to list
#     default=df_selection.columns.tolist()   # Convert Index to list
#     )

#         st.dataframe(df_selection[columns_to_show], use_container_width=True)

#     total_crashes = len(df_selection)
#     avg_age = df_selection['age'].mean()
#     min_age = df_selection['age'].min()
#     max_age = df_selection['age'].max()

#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Total Crashes", total_crashes)
#     col2.metric("Average Age", f"{avg_age:.1f}")
#     col3.metric("Min Age", f"{min_age:.1f}")
#     col4.metric("Max Age", f"{max_age:.1f}")
    
#     style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")

#     with st.expander("📊 AGE DISTRIBUTION"):
#         df_selection['age'].hist(bins=20, color='skyblue')
#         st.pyplot()

# # Charts
# def graphs():
#     # Bar chart: Crashes by Vehicle Type
#     vehicle_crash_count = df_selection["type_vehicle"].value_counts()
#     fig_bar = px.bar(vehicle_crash_count, x=vehicle_crash_count.index, y=vehicle_crash_count.values,
#                      labels={"x": "Vehicle Type", "y": "Number of Crashes"},
#                      title="Crashes by Vehicle Type", color_discrete_sequence=["#0083B8"])
    
#     # Line chart: Crashes by Hour
#     crash_by_hour = df_selection["hour_crash"].value_counts().sort_index()
#     fig_line = px.line(x=crash_by_hour.index, y=crash_by_hour.values,
#                        labels={"x": "Hour of Crash", "y": "Count"},
#                        title="Crashes by Hour", markers=True)

#     left, right = st.columns(2)
#     left.plotly_chart(fig_bar, use_container_width=True)
#     right.plotly_chart(fig_line, use_container_width=True)

#     with st.expander("📍 Pie Chart: Gender Distribution"):
#         fig_pie = px.pie(df_selection, names="gender", title="Crash Distribution by Gender")
#         st.plotly_chart(fig_pie, use_container_width=True)

# # Progress Bar
# def Progressbar():
#     st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""", unsafe_allow_html=True)
#     target = 100  # Replace with a real KPI if needed
#     current = len(df_selection)
#     percent = round((current / target) * 100)
#     mybar = st.progress(0)

#     if percent > 100:
#         st.success("Target Achieved 🎯")
#     else:
#         st.write(f"You have {percent}% of the crash data target ({target} entries)")
#         for i in range(percent):
#             time.sleep(0.01)
#             mybar.progress(i + 1, text="Processing Crash Records")

# # Menu Navigation
# def sideBar():
#     with st.sidebar:
#         selected = option_menu(
#             menu_title="Main Menu",
#             options=["Home", "Progress"],
#             icons=["house", "graph-up"],
#             menu_icon="menu-up",
#             default_index=0
#         )
#     if selected == "Home":
#         Home()
#         graphs()
#     elif selected == "Progress":
#         Progressbar()
#         graphs()

# sideBar()

# # Boxplot
# st.subheader("🚘 VEHICLE TYPE BY AGE DISTRIBUTION")
# feature_y = st.selectbox("Select Quantitative Feature", df_selection.select_dtypes(include='number').columns)
# fig2 = go.Figure(
#     data=[go.Box(x=df_selection['type_vehicle'], y=df_selection[feature_y], name='')],
#     layout=go.Layout(
#         title="Vehicle Type by Age Distribution (Boxplot)",
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
#         yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
#         font=dict(color='black')
#     )
# )
# st.plotly_chart(fig2, use_container_width=True)

# # Hide Streamlit Footer
# st.markdown("""
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}
# </style>
# """, unsafe_allow_html=True)


