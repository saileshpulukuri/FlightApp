import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os
import pickle
import joblib

# -------------------------------------------------------------------------
# Streamlit Page Config
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="Flight Delay Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# Dark Mode CSS (Always Applied - No Toggle)
# -------------------------------------------------------------------------
dark_mode_css = """
<style>
/* Dark Mode Styles - Always Active */
.stApp {
    background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
    color: #e0e0e0;
}
.stSidebar {
    background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%) !important;
}
.stSidebar .css-1d391kg {
    background-color: transparent !important;
}
.stSidebar [data-testid="stSidebar"] {
    background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%) !important;
}
/* Sidebar navigation - match main background */
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%) !important;
}
section[data-testid="stSidebar"] > div {
    background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%) !important;
}
.stSidebar * {
    color: #e0e0e0 !important;
}
.stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar label {
    color: #ffffff !important;
}
/* Radio button labels in sidebar */
.stSidebar [data-testid="stRadio"] label {
    color: #ffffff !important;
}
.stSidebar [data-testid="stRadio"] [role="radiogroup"] label {
    color: #ffffff !important;
}
.stSidebar [data-testid="stRadio"] [role="radiogroup"] [data-baseweb="radio"] {
    color: #ffffff !important;
}
/* Sidebar title */
.stSidebar h1 {
    color: #ffffff !important;
}
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}
p, span, div, label {
    color: #e0e0e0 !important;
}
.stMetric {
    background: rgba(45, 45, 68, 0.6);
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
.stMetric label {
    color: #b0b0b0 !important;
}
.stMetric [data-testid="stMetricValue"] {
    color: #ffffff !important;
}
[data-testid="stForm"] {
    background: rgba(45, 45, 68, 0.4);
    padding: 1.5rem;
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
[data-testid="stSelectbox"], [data-testid="stNumberInput"], [data-testid="stSlider"] {
    background-color: rgba(45, 45, 68, 0.6);
}
[data-testid="stSelectbox"] label, [data-testid="stNumberInput"] label, [data-testid="stSlider"] label {
    color: #e0e0e0 !important;
}
/* Dropdown text visibility */
[data-testid="stSelectbox"] select, [data-testid="stSelectbox"] option {
    background-color: rgba(45, 45, 68, 0.9) !important;
    color: #ffffff !important;
}
[data-baseweb="select"] {
    background-color: rgba(45, 45, 68, 0.9) !important;
}
/* Selected value in dropdown - dark background with white text */
[data-baseweb="select"] > div[role="combobox"] {
    background-color: rgba(45, 45, 68, 0.9) !important;
    color: #ffffff !important;
}
[data-baseweb="select"] > div[role="combobox"] > div {
    background-color: rgba(45, 45, 68, 0.9) !important;
    color: #ffffff !important;
}
[data-baseweb="select"] > div[role="combobox"] span {
    color: #ffffff !important;
}
/* Selectbox input field */
[data-baseweb="select"] input {
    background-color: rgba(45, 45, 68, 0.9) !important;
    color: #ffffff !important;
}
[data-baseweb="select"] [role="option"] {
    background-color: rgba(45, 45, 68, 0.9) !important;
    color: #ffffff !important;
}
[data-baseweb="popover"] {
    background-color: rgba(45, 45, 68, 0.95) !important;
}
[data-baseweb="popover"] [role="option"] {
    background-color: rgba(45, 45, 68, 0.95) !important;
    color: #ffffff !important;
}
[data-baseweb="popover"] [role="option"]:hover {
    background-color: rgba(99, 102, 241, 0.5) !important;
    color: #ffffff !important;
}
/* Selectbox value text - ensure visibility */
div[data-baseweb="select"] > div {
    color: #ffffff !important;
}
/* All text inside selectbox */
[data-baseweb="select"] * {
    color: #ffffff !important;
}
/* Specific styling for the displayed value */
[data-baseweb="select"] [id*="bui"] {
    color: #ffffff !important;
}
/* Streamlit selectbox container */
.stSelectbox > div > div {
    background-color: rgba(45, 45, 68, 0.9) !important;
    color: #ffffff !important;
}
.stSelectbox > div > div > div {
    background-color: rgba(45, 45, 68, 0.9) !important;
    color: #ffffff !important;
}
.stSelectbox > div > div > div > div {
    color: #ffffff !important;
}
.stSelectbox span {
    color: #ffffff !important;
}
.stButton>button {
    background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
}
[data-testid="stSuccess"], [data-testid="stError"], [data-testid="stWarning"], [data-testid="stInfo"] {
    background: rgba(45, 45, 68, 0.6);
    border-radius: 10px;
}
.stExpander {
    background: rgba(45, 45, 68, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
}
/* Chat message visibility in dark mode */
[data-testid="stChatMessage"] {
    color: #e0e0e0 !important;
}
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] div {
    color: #e0e0e0 !important;
}
[data-testid="stChatMessage"] .stMarkdown {
    color: #e0e0e0 !important;
}
[data-testid="stChatMessage"] .stMarkdown p {
    color: #e0e0e0 !important;
}
/* User message styling - White background with black text */
[data-testid="stChatMessage"][data-message-role="user"] {
    background: #ffffff !important;
}
[data-testid="stChatMessage"][data-message-role="user"] p,
[data-testid="stChatMessage"][data-message-role="user"] div,
[data-testid="stChatMessage"][data-message-role="user"] .stMarkdown,
[data-testid="stChatMessage"][data-message-role="user"] .stMarkdown p {
    color: #000000 !important;
}
/* Assistant message styling */
[data-testid="stChatMessage"][data-message-role="assistant"] {
    background: rgba(45, 45, 68, 0.6) !important;
}
[data-testid="stChatMessage"][data-message-role="assistant"] p {
    color: #ffffff !important;
}
/* Smooth page transitions */
.main .block-container {
    animation: fadeIn 0.4s ease-in;
    padding-top: 1rem !important;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
/* Hide default Streamlit header spacing */
header[data-testid="stHeader"] {
    display: none;
}
/* Radio button styling for dark mode */
[data-testid="stRadio"] label {
    color: #e0e0e0 !important;
}
[data-testid="stRadio"] [role="radiogroup"] {
    color: #e0e0e0 !important;
}
/* Text input styling - Chatbot input box (white background, black text) */
[data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
}
[data-testid="stTextInput"] label {
    color: #e0e0e0 !important;
}
/* Chatbot specific input styling */
input[type="text"][placeholder*="Why is my flight delayed"], 
input[type="text"][placeholder*="What is the average delay"] {
    background-color: #ffffff !important;
    color: #000000 !important;
}
</style>
"""

st.markdown(dark_mode_css, unsafe_allow_html=True)

# -------------------------------------------------------------------------
# Load Data Efficiently
# -------------------------------------------------------------------------
@st.cache_data
def load_data():
    """
    Load data from data/dashboard_sample.parquet.
    Handles both:
      - a directory with multiple parquet part files
      - a single parquet file
    """
    try:
        parquet_path = "data/dashboard_sample.parquet"

        # Case 1: Folder with multiple parquet files
        if os.path.isdir(parquet_path):
            parquet_files = glob.glob(os.path.join(parquet_path, "*.parquet"))
            if parquet_files:
                df_list = []
                # Read first few files for performance
                for file in parquet_files[:3]:
                    try:
                        df_part = pd.read_parquet(file)
                        df_list.append(df_part)
                    except Exception as e:
                        st.warning(f"Could not read {file}: {e}")
                        continue

                if df_list:
                    df = pd.concat(df_list, ignore_index=True)
                    return df
                else:
                    st.error("No parquet files could be read from folder.")
                    return pd.DataFrame()
            else:
                st.error(f"No parquet files found in folder: {parquet_path}")
                return pd.DataFrame()

        # Case 2: Single parquet file
        elif os.path.exists(parquet_path) and parquet_path.endswith(".parquet"):
            try:
                df = pd.read_parquet(parquet_path)
                return df
            except Exception as e:
                st.error(f"Error reading parquet file: {e}")
                return pd.DataFrame()

        else:
            st.error(f"Data path not found: {parquet_path}")
            return pd.DataFrame()

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


# -------------------------------------------------------------------------
# Load and Prepare Data
# -------------------------------------------------------------------------
df = load_data()

if df.empty:
    st.error("❌ No data loaded! Please check your 'data/dashboard_sample.parquet' files.")
    st.stop()


def create_hub_column_data(df_in: pd.DataFrame) -> pd.DataFrame:
    """Create ORIGIN_IS_HUB column based on known major hub airports."""
    major_hubs = [
        "ATL", "DFW", "DEN", "ORD", "LAX", "JFK", "SFO", "SEA", "MIA", "CLT",
        "PHL", "DTW", "MSP", "BOS", "LGA", "EWR", "IAH", "DCA"
    ]
    df_copy = df_in.copy()
    if "ORIGIN_AIRPORT" in df_copy.columns and "ORIGIN_IS_HUB" not in df_copy.columns:
        df_copy["ORIGIN_IS_HUB"] = df_copy["ORIGIN_AIRPORT"].isin(major_hubs).astype(int)
    return df_copy


# Add hub column to full dataframe
df = create_hub_column_data(df)

# Create a smaller sample for charts to avoid UI crashes
if len(df) > 50_000:
    chart_df = df.sample(n=50_000, random_state=42).reset_index(drop=True)
else:
    chart_df = df.copy()

# Ensure sample also has hub info
chart_df = create_hub_column_data(chart_df)

# Sidebar info (hidden for clean UI)
# st.sidebar.success(f"✅ Data loaded: {len(df):,} flights")


# -------------------------------------------------------------------------
# Helper Functions for Mappings
# -------------------------------------------------------------------------
@st.cache_data
def get_airline_name_mapping(df_in: pd.DataFrame) -> dict:
    """Create mapping of airline codes to full names if available; otherwise fallback."""
    airline_mapping = {}
    if "carrier_name" in df_in.columns and "AIRLINE" in df_in.columns:
        mapping_df = df_in[["AIRLINE", "carrier_name"]].drop_duplicates()
        airline_mapping = dict(zip(mapping_df["AIRLINE"], mapping_df["carrier_name"]))

    # Fallback mapping
    fallback_mapping = {
        "AA": "American Airlines",
        "AS": "Alaska Airlines",
        "B6": "JetBlue Airways",
        "DL": "Delta Air Lines",
        "EV": "ExpressJet Airlines",
        "F9": "Frontier Airlines",
        "HA": "Hawaiian Airlines",
        "MQ": "Envoy Air",
        "NK": "Spirit Airlines",
        "OO": "SkyWest Airlines",
        "UA": "United Airlines",
        "US": "US Airways",
        "VX": "Virgin America",
        "WN": "Southwest Airlines",
    }

    return airline_mapping if airline_mapping else fallback_mapping


def format_airline_label(code: str, mapping: dict) -> str:
    """Format airline code as 'CODE (Full Name)'."""
    full_name = mapping.get(code, code)
    return f"{code} ({full_name})"


@st.cache_data
def get_airport_name_mapping(df_in: pd.DataFrame) -> dict:
    """
    Create airport code -> full name mapping if columns exist
    (e.g., AIRPORT + airport_name).
    """
    airport_mapping = {}
    if "airport_name" in df_in.columns and "AIRPORT" in df_in.columns:
        mapping_df = df_in[["AIRPORT", "airport_name"]].drop_duplicates()
        airport_mapping = dict(zip(mapping_df["AIRPORT"], mapping_df["airport_name"]))
    return airport_mapping


def format_airport_label(code, mapping: dict) -> str:
    """Format airport label as 'CODE (Name)' if mapping is available."""
    if pd.isna(code) or code == "":
        return str(code)
    code_str = str(code)
    full_name = mapping.get(code_str, None)
    if full_name:
        # if full_name looks like "Airport Name: City, State", take just left side
        name_part = str(full_name).split(":")[0].strip()
        return f"{code_str} ({name_part})"
    return code_str


airline_mapping = get_airline_name_mapping(df)
airport_mapping = get_airport_name_mapping(df)


# -------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------
st.sidebar.title(" Flight Dashboard")

menu = st.sidebar.radio(
    "Navigate",
    [
        "Home Overview",
        "Airline Analysis",
        "Airport Analysis",
        "Routes & Distance",
        "Time Trends",
        "Delay Relationships",
        "Delay Prediction",
    ]
)

# -------------------------------------------------------------------------
# HOME OVERVIEW
# -------------------------------------------------------------------------
if menu == "Home Overview":
    st.title(" Flight Delay Overview")

    total_flights = len(df)

    # Choose main delay column
    delay_col = None
    if "TOTAL_DELAY" in df.columns:
        delay_col = "TOTAL_DELAY"
    elif "ARRIVAL_DELAY" in df.columns:
        delay_col = "ARRIVAL_DELAY"

    if delay_col:
        avg_delay = df[delay_col].mean()
        median_delay = df[delay_col].median()
        delay_60_pct = (df[delay_col] > 60).mean() * 100
    else:
        avg_delay = median_delay = delay_60_pct = 0.0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Flights", f"{total_flights:,}")
    col2.metric("Avg Total Delay", f"{avg_delay:.2f} min")
    col3.metric("Median Total Delay", f"{median_delay:.2f} min")
    col4.metric("Flights with delay > 60 mins", f"{delay_60_pct:.2f}%")

    st.subheader("Distribution of Total Flight Delays")
    if delay_col and delay_col in chart_df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))

        # clip to focus on -50 to 300 like in notebook
        mask = chart_df[delay_col].between(-50, 300)
        filtered_df = chart_df[mask].copy()

        sns.histplot(
            data=filtered_df,
            x=delay_col,
            bins=50,
            kde=True,
            color="skyblue",
            ax=ax,
        )
        ax.set_title("Distribution of Total Flight Delays", fontsize=14, pad=15)
        ax.set_xlabel("Total Delay (minutes)", fontsize=12)
        ax.set_ylabel("Number of Flights", fontsize=12)
        ax.set_xlim(-50, 300)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Delay column not found in data.")


# -------------------------------------------------------------------------
# AIRLINE ANALYSIS
# -------------------------------------------------------------------------
elif menu == "Airline Analysis":
    st.title(" Airline Delay Analysis")

    if "AIRLINE" not in df.columns:
        st.error("AIRLINE column not found in data.")
    else:
        # ---------------- Chart 1: Average Arrival Delay by Airline ----------------
        st.subheader("Average Arrival Delay by Airline")

        if "ARRIVAL_DELAY" in df.columns:
            airline_delay = (
                df.groupby("AIRLINE")["ARRIVAL_DELAY"]
                .mean()
                .sort_values(ascending=False)
                .reset_index()
            )

            if len(airline_delay) > 0:
                airline_delay["Airline_Label"] = airline_delay["AIRLINE"].apply(
                    lambda x: format_airline_label(x, airline_mapping)
                )

                fig, ax = plt.subplots(figsize=(10, 6))
                colors = [
                    "blue" if x >= 0 else "red"
                    for x in airline_delay["ARRIVAL_DELAY"]
                ]
                ax.barh(
                    airline_delay["Airline_Label"],
                    airline_delay["ARRIVAL_DELAY"],
                    color=colors,
                    alpha=0.7,
                )
                ax.axvline(x=0, color="black", linestyle="--", linewidth=1)
                ax.set_xlabel("Average Arrival Delay (minutes)", fontsize=12)
                ax.set_ylabel("Airline", fontsize=12)
                ax.set_title("Average Arrival Delay by Airline", fontsize=14, pad=15)
                ax.grid(True, alpha=0.3, axis="x")
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.warning("No airline delay data available.")
        else:
            st.warning("ARRIVAL_DELAY column not found.")

        # ---------------- Chart 2: Distribution of Total Delays by Airline (Boxplot) ----------------
        st.subheader("Distribution of Total Delays by Airline")

        delay_col = None
        if "TOTAL_DELAY" in chart_df.columns:
            delay_col = "TOTAL_DELAY"
        elif "ARRIVAL_DELAY" in chart_df.columns:
            delay_col = "ARRIVAL_DELAY"

        if delay_col and "AIRLINE" in chart_df.columns:
            top_airlines = chart_df["AIRLINE"].value_counts().head(10).index
            plot_df = chart_df[chart_df["AIRLINE"].isin(top_airlines)].copy()

            if len(plot_df) > 0:
                plot_df["Airline_Label"] = plot_df["AIRLINE"].apply(
                    lambda x: format_airline_label(x, airline_mapping)
                )

                fig2, ax2 = plt.subplots(figsize=(14, 6))
                sns.boxplot(
                    data=plot_df,
                    x="Airline_Label",
                    y=delay_col,
                    palette="Set2",
                    ax=ax2,
                )
                plt.xticks(rotation=45, ha="right", fontsize=9)
                plt.ylabel("Total Delay (minutes)", fontsize=12)
                plt.xlabel("Airline", fontsize=12)
                plt.title("Distribution of Total Delays by Airline", fontsize=14, pad=15)
                plt.tight_layout()
                st.pyplot(fig2)
            else:
                st.warning("Insufficient data for airline boxplot.")
        else:
            st.warning("Required columns not found for airline boxplot.")

        # ---------------- Chart 3: Proportion of Delay Causes (Donut) ----------------
        st.subheader("Proportion of Average Delay Causes")

        delay_causes = {}
        if "DEPARTURE_DELAY" in df.columns:
            delay_causes["Departure Delay"] = df["DEPARTURE_DELAY"].mean()
        if "ARRIVAL_DELAY" in df.columns:
            delay_causes["Arrival Delay"] = df["ARRIVAL_DELAY"].mean()
        if "AIR_SYSTEM_DELAY" in df.columns:
            delay_causes["Air System Delay"] = df["AIR_SYSTEM_DELAY"].fillna(0).mean()
        if "AIRLINE_DELAY" in df.columns:
            delay_causes["Airline Delay"] = df["AIRLINE_DELAY"].fillna(0).mean()
        if "nas_delay" in df.columns:
            delay_causes["NAS Delay"] = df["nas_delay"].fillna(0).mean()
        elif "NAS_DELAY" in df.columns:
            delay_causes["NAS Delay"] = df["NAS_DELAY"].fillna(0).mean()

        if delay_causes:
            cause_df = pd.DataFrame(
                list(delay_causes.items()),
                columns=["Cause", "Average Delay (minutes)"],
            )
            cause_df = cause_df[cause_df["Average Delay (minutes)"] > 0]

            if len(cause_df) > 0:
                fig3 = px.pie(
                    cause_df,
                    names="Cause",
                    values="Average Delay (minutes)",
                    hole=0.4,
                    title="Proportion of Average Delay Causes",
                )
                fig3.update_traces(textposition="inside", textinfo="percent+label")
                fig3.update_layout(title_font_size=16)
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.warning("No non-zero delay cause data available.")
        else:
            st.warning("Delay cause columns not found in data.")


# -------------------------------------------------------------------------
# AIRPORT ANALYSIS
# -------------------------------------------------------------------------
elif menu == "Airport Analysis":
    st.title("Airport Delay Analysis")

    delay_col = None
    if "TOTAL_DELAY" in df.columns:
        delay_col = "TOTAL_DELAY"
    elif "ARRIVAL_DELAY" in df.columns:
        delay_col = "ARRIVAL_DELAY"

    if delay_col is None:
        st.error("No suitable delay column found in data.")
    else:
        # ---------------- Chart 1: Hub vs Non-Hub Comparison ----------------
        st.subheader("Average Delay at Hub vs Non-Hub Airports")

        if "ORIGIN_IS_HUB" in df.columns:
            hub_comparison = (
                df.groupby("ORIGIN_IS_HUB")[delay_col]
                .mean()
                .reset_index()
            )
            hub_comparison["ORIGIN_IS_HUB"] = hub_comparison["ORIGIN_IS_HUB"].astype(int)

            if len(hub_comparison) > 0:
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.barplot(
                    data=hub_comparison,
                    x="ORIGIN_IS_HUB",
                    y=delay_col,
                    palette="coolwarm",
                    ax=ax,
                )
                ax.set_xlabel("Hub Status (0 = Non-Hub, 1 = Hub)", fontsize=12)
                ax.set_ylabel("Average Delay (minutes)", fontsize=12)
                ax.set_title("Average Delay at Hub vs Non-Hub Airports", fontsize=14, pad=15)
                ax.grid(True, alpha=0.3, axis="y")
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.warning("No hub comparison data available.")
        else:
            st.info("ORIGIN_IS_HUB column not found - skipping hub vs non-hub chart.")

        # ---------------- Chart 2: Top 10 Origin Airports by Departure Delay ----------------
        st.subheader("Top 10 Origin Airports by Average Departure Delay")

        if "ORIGIN_AIRPORT" in df.columns and "DEPARTURE_DELAY" in df.columns:
            df_clean = df.copy()
            df_clean["ORIGIN_AIRPORT"] = df_clean["ORIGIN_AIRPORT"].astype(str)

            df_clean = df_clean[
                df_clean["ORIGIN_AIRPORT"].str.len().between(3, 4)
                & df_clean["ORIGIN_AIRPORT"].str.match(r"^[A-Z0-9]+$", na=False)
            ]

            top_origin = (
                df_clean.groupby("ORIGIN_AIRPORT")["DEPARTURE_DELAY"]
                .mean()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            if len(top_origin) > 0:
                top_origin["Airport_Label"] = top_origin["ORIGIN_AIRPORT"].apply(
                    lambda x: format_airport_label(x, airport_mapping)
                )

                fig2 = px.bar(
                    top_origin,
                    x="DEPARTURE_DELAY",
                    y="Airport_Label",
                    orientation="h",
                    title="Top 10 Origin Airports by Average Departure Delay",
                    color="DEPARTURE_DELAY",
                    color_continuous_scale="viridis",
                    labels={
                        "DEPARTURE_DELAY": "Average Delay (minutes)",
                        "Airport_Label": "Origin Airport",
                    },
                )
                fig2.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("No origin airport data available after cleaning.")
        else:
            st.warning("ORIGIN_AIRPORT or DEPARTURE_DELAY column not found.")

        # ---------------- Chart 3: Top 10 Destination Airports by Arrival Delay ----------------
        st.subheader("Top 10 Destination Airports by Average Arrival Delay")

        if "DESTINATION_AIRPORT" in df.columns and "ARRIVAL_DELAY" in df.columns:
            df_clean = df.copy()
            df_clean["DESTINATION_AIRPORT"] = df_clean["DESTINATION_AIRPORT"].astype(str)

            df_clean = df_clean[
                df_clean["DESTINATION_AIRPORT"].str.len().between(3, 4)
                & df_clean["DESTINATION_AIRPORT"].str.match(r"^[A-Z0-9]+$", na=False)
            ]

            top_dest = (
                df_clean.groupby("DESTINATION_AIRPORT")["ARRIVAL_DELAY"]
                .mean()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            if len(top_dest) > 0:
                top_dest["Airport_Label"] = top_dest["DESTINATION_AIRPORT"].apply(
                    lambda x: format_airport_label(x, airport_mapping)
                )

                fig3 = px.bar(
                    top_dest,
                    x="ARRIVAL_DELAY",
                    y="Airport_Label",
                    orientation="h",
                    title="Top 10 Destination Airports by Average Arrival Delay",
                    color="ARRIVAL_DELAY",
                    color_continuous_scale="plasma",
                    labels={
                        "ARRIVAL_DELAY": "Average Delay (minutes)",
                        "Airport_Label": "Destination Airport",
                    },
                )
                fig3.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.warning("No destination airport data available after cleaning.")
        else:
            st.warning("DESTINATION_AIRPORT or ARRIVAL_DELAY column not found.")

        # ---------------- Chart 4: Average Total Delay by Hub Airport ----------------
        st.subheader("Average Total Delay by Hub Airport")

        if "ORIGIN_IS_HUB" in df.columns and "ORIGIN_AIRPORT" in df.columns:
            hub_df = df[df["ORIGIN_IS_HUB"] == 1].copy()

            if len(hub_df) > 0:
                hub_df["ORIGIN_AIRPORT"] = hub_df["ORIGIN_AIRPORT"].astype(str)
                hub_df_clean = hub_df[
                    hub_df["ORIGIN_AIRPORT"].str.len().between(3, 4)
                    & hub_df["ORIGIN_AIRPORT"].str.match(r"^[A-Z0-9]+$", na=False)
                ].copy()

                avg_delay_hub = (
                    hub_df_clean.groupby("ORIGIN_AIRPORT")[delay_col]
                    .mean()
                    .sort_values(ascending=False)
                    .reset_index()
                )

                if len(avg_delay_hub) > 0:
                    avg_delay_hub["Airport_Label"] = avg_delay_hub["ORIGIN_AIRPORT"].apply(
                        lambda x: format_airport_label(x, airport_mapping)
                    )

                    fig4 = px.bar(
                        avg_delay_hub,
                        x=delay_col,
                        y="Airport_Label",
                        orientation="h",
                        title="Average Total Delay by Hub Airport",
                        color=delay_col,
                        color_continuous_scale="viridis",
                        labels={
                            delay_col: "Average Delay (minutes)",
                            "Airport_Label": "Hub Airport",
                        },
                    )
                    fig4.update_layout(yaxis={"categoryorder": "total ascending"})
                    st.plotly_chart(fig4, use_container_width=True)
                else:
                    st.info("No cleaned hub airport data found.")
            else:
                st.info("No flights from hub airports in the dataset.")
        else:
            st.info("Hub airport column not found; skipping hub delay chart.")


# -------------------------------------------------------------------------
# ROUTES & DISTANCE
# -------------------------------------------------------------------------
elif menu == "Routes & Distance":
    st.title("Route & Distance Impact on Delays")

    # ---------------- Chart 1: Top 10 Most Delay-Prone Routes ----------------
    st.subheader("Top 10 Most Delay-Prone Routes")

    delay_col = None
    if "ARRIVAL_DELAY" in df.columns:
        delay_col = "ARRIVAL_DELAY"
    elif "TOTAL_DELAY" in df.columns:
        delay_col = "TOTAL_DELAY"

    if delay_col and "ORIGIN_AIRPORT" in df.columns and "DESTINATION_AIRPORT" in df.columns:
        df_routes = df.copy()
        df_routes["ORIGIN_AIRPORT"] = df_routes["ORIGIN_AIRPORT"].astype(str)
        df_routes["DESTINATION_AIRPORT"] = df_routes["DESTINATION_AIRPORT"].astype(str)

        valid_pattern = r"^[A-Z][A-Z0-9]{1,3}$"
        df_routes = df_routes[
            df_routes["ORIGIN_AIRPORT"].str.len().between(3, 4)
            & df_routes["DESTINATION_AIRPORT"].str.len().between(3, 4)
            & df_routes["ORIGIN_AIRPORT"].str.match(valid_pattern, na=False, case=False)
            & df_routes["DESTINATION_AIRPORT"].str.match(valid_pattern, na=False, case=False)
        ].copy()

        route_delay = (
            df_routes.groupby(["ORIGIN_AIRPORT", "DESTINATION_AIRPORT"])[delay_col]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        if len(route_delay) > 0:
            route_delay = route_delay[route_delay[delay_col] > 0].copy()
            route_delay[delay_col] = route_delay[delay_col].astype(float)

            route_delay["Origin_Label"] = route_delay["ORIGIN_AIRPORT"].apply(
                lambda x: format_airport_label(x, airport_mapping)
            )
            route_delay["Destination_Label"] = route_delay["DESTINATION_AIRPORT"].apply(
                lambda x: format_airport_label(x, airport_mapping)
            )
            route_delay["Route"] = (
                route_delay["ORIGIN_AIRPORT"] + " → " + route_delay["DESTINATION_AIRPORT"]
            )
            route_delay["Route_Label"] = (
                route_delay["Origin_Label"] + " → " + route_delay["Destination_Label"]
            )

            # sort again by delay just to be safe
            route_delay = route_delay.sort_values(delay_col, ascending=False).head(10).copy()
            route_delay[delay_col] = pd.to_numeric(route_delay[delay_col], errors="coerce")
            route_delay = route_delay.dropna(subset=[delay_col])

            if len(route_delay) > 0:
                min_delay_val = float(route_delay[delay_col].min())
                max_delay_val = float(route_delay[delay_col].max())
                min_delay = max(0, min_delay_val - 10)
                max_delay = max_delay_val + 30

                # Sort by delay descending for display
                route_delay_display = route_delay.sort_values(delay_col, ascending=False).copy()

                fig, ax = plt.subplots(figsize=(14, 8))

                # Use Route_Label for y-axis (shows Origin → Destination)
                routes = route_delay_display["Route_Label"].values
                y_pos = np.arange(len(routes))

                # Generate distinct colors for each route
                colors_list = plt.cm.Set3(np.linspace(0, 1, len(routes)))
                
                # Create bar chart with different color for each route
                for i, (idx, row) in enumerate(route_delay_display.iterrows()):
                    delay_val = float(row[delay_col])
                    route_label = row["Route_Label"]
                    
                    # Use distinct color for each route
                    bar_color = colors_list[i]
                    ax.barh(i, delay_val, color=bar_color, alpha=0.8, edgecolor='black', linewidth=1.5)
                    ax.text(
                        delay_val + 2,
                        i,
                        f"{delay_val:.1f} min",
                        va="center",
                        fontsize=10,
                        fontweight="bold",
                    )

                ax.set_yticks(y_pos)
                ax.set_yticklabels(routes, fontsize=10)
                ax.set_xlabel("Average Arrival Delay (minutes)", fontsize=12, fontweight='bold')
                ax.set_ylabel("Route (Origin → Destination)", fontsize=12, fontweight='bold')
                ax.set_title("Top 10 Most Delay-Prone Routes", fontsize=14, fontweight='bold', pad=15)
                ax.set_xlim(min_delay, max_delay)
                ax.grid(True, axis="x", alpha=0.3, linestyle="--")
                plt.tight_layout()
                st.pyplot(fig)

                with st.expander("📋 View Route Details"):
                    display_df = route_delay[["Route_Label", delay_col]].copy()
                    display_df.columns = ["Route", "Avg Delay (minutes)"]
                    display_df["Avg Delay (minutes)"] = display_df["Avg Delay (minutes)"].round(1)
                    display_df = display_df.sort_values("Avg Delay (minutes)", ascending=False)
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
            else:
                st.warning("No valid route data after filtering.")
        else:
            st.warning("No route data available after grouping.")
    else:
        st.warning("Required columns (ORIGIN_AIRPORT, DESTINATION_AIRPORT, delay) not found.")

    # ---------------- Chart 2: Delay vs Flight Distance ----------------
    st.subheader("Delay vs Flight Distance")

    delay_col_scatter = None
    if "TOTAL_DELAY" in chart_df.columns:
        delay_col_scatter = "TOTAL_DELAY"
    elif "ARRIVAL_DELAY" in chart_df.columns:
        delay_col_scatter = "ARRIVAL_DELAY"

    if delay_col_scatter and "DISTANCE" in chart_df.columns:
        if len(chart_df) > 10_000:
            scatter_sample = chart_df.sample(n=10_000, random_state=42)
        else:
            scatter_sample = chart_df.copy()

        if len(scatter_sample) > 0:
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            sns.scatterplot(
                data=scatter_sample,
                x="DISTANCE",
                y=delay_col_scatter,
                alpha=0.4,
                ax=ax2,
            )
            ax2.set_xlabel("Flight Distance (miles)", fontsize=12)
            ax2.set_ylabel("Total Delay (minutes)", fontsize=12)
            ax2.set_title("Delay vs Flight Distance", fontsize=14, pad=15)
            ax2.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig2)
        else:
            st.warning("Insufficient data for distance scatter plot.")
    else:
        st.warning("DISTANCE or delay column not found in data.")


# -------------------------------------------------------------------------
# TIME TRENDS
# -------------------------------------------------------------------------
elif menu == "Time Trends":
    st.title(" Time-Based Delay Trends")

    delay_col = None
    if "TOTAL_DELAY" in df.columns:
        delay_col = "TOTAL_DELAY"
    elif "ARRIVAL_DELAY" in df.columns:
        delay_col = "ARRIVAL_DELAY"

    # ---------------- Chart 1: Delay by Month ----------------
    st.subheader("Average Total Delay by Month")

    if "MONTH" in df.columns and delay_col:
        df_month = df.copy()
        df_month["MONTH"] = pd.to_numeric(df_month["MONTH"], errors="coerce")
        df_month = df_month[df_month["MONTH"].between(1, 12)]
        df_month[delay_col] = df_month[delay_col].fillna(0)

        month_delay = (
            df_month.groupby("MONTH")[delay_col]
            .mean()
            .reset_index()
            .sort_values("MONTH")
        )

        month_names = {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
            5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
            9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
        }
        month_delay["Month_Name"] = month_delay["MONTH"].map(month_names)

        if len(month_delay) > 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(month_delay["MONTH"], month_delay[delay_col], marker="o", color="teal")
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels([month_names[i] for i in range(1, 13)])
            ax.set_xlabel("Month", fontsize=12)
            ax.set_ylabel("Average Delay (minutes)", fontsize=12)
            ax.set_title("Average Total Delay by Month", fontsize=14, pad=15)
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("No month data available.")
    else:
        st.warning("MONTH or delay column not found for monthly trends.")

    # ---------------- Chart 2: Delay by Hour of Day ----------------
    st.subheader("Average Total Delay by Hour of Day")

    if "SCHEDULED_DEPARTURE" in df.columns and delay_col:
        df_hour = df.copy()
        df_hour["HOUR"] = pd.to_numeric(df_hour["SCHEDULED_DEPARTURE"], errors="coerce") // 100
        df_hour = df_hour[df_hour["HOUR"].between(0, 23)]
        df_hour[delay_col] = df_hour[delay_col].fillna(0)

        hour_delay = (
            df_hour.groupby("HOUR")[delay_col]
            .mean()
            .reset_index()
            .sort_values("HOUR")
        )

        if len(hour_delay) > 0:
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.plot(hour_delay["HOUR"], hour_delay[delay_col], marker="o", color="blue")
            ax2.set_xticks(range(0, 24, 2))
            ax2.set_xlabel("Hour of Day", fontsize=12)
            ax2.set_ylabel("Average Delay (minutes)", fontsize=12)
            ax2.set_title("Average Total Delay by Hour of Day", fontsize=14, pad=15)
            ax2.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig2)
        else:
            st.warning("No hourly data available.")
    else:
        st.info("SCHEDULED_DEPARTURE or delay column not found – cannot compute hourly trends.")


# -------------------------------------------------------------------------
# DELAY RELATIONSHIPS
# -------------------------------------------------------------------------
elif menu == "Delay Relationships":
    st.title(" Delay Relationships & Correlations")

    # ---------------- Chart 1: Correlation Heatmap ----------------
    st.subheader("Correlation Between Different Delay Types")

    possible_delay_cols = [
        "DEPARTURE_DELAY",
        "ARRIVAL_DELAY",
        "AIR_SYSTEM_DELAY",
        "AIRLINE_DELAY",
        "TOTAL_DELAY",
        "nas_delay",
        "NAS_DELAY",
    ]

    delay_cols = [col for col in possible_delay_cols if col in chart_df.columns]

    # de-duplicate NAS delay if both versions exist
    if "NAS_DELAY" in delay_cols and "nas_delay" in delay_cols:
        delay_cols.remove("nas_delay")

    if len(delay_cols) >= 2:
        corr = chart_df[delay_cols].corr()
        if not corr.empty:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(
                corr,
                annot=True,
                cmap="coolwarm",
                fmt=".2f",
                ax=ax,
                square=True,
                linewidths=0.5,
                cbar_kws={"shrink": 0.8},
            )
            ax.set_title("Correlation Between Different Delay Types", fontsize=14, pad=20)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("Could not calculate correlation matrix (empty).")
    else:
        st.warning(f"Need at least 2 delay-related numeric columns. Found: {delay_cols}")

    # ---------------- Chart 2: Departure vs Arrival Delay Scatter ----------------
    st.subheader("Relationship Between Departure and Arrival Delays")

    if "DEPARTURE_DELAY" in chart_df.columns and "ARRIVAL_DELAY" in chart_df.columns:
        scatter_df = chart_df[["DEPARTURE_DELAY", "ARRIVAL_DELAY"]].dropna()

        if len(scatter_df) > 10_000:
            scatter_df = scatter_df.sample(n=10_000, random_state=42)

        if len(scatter_df) > 0:
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            sns.scatterplot(
                data=scatter_df,
                x="DEPARTURE_DELAY",
                y="ARRIVAL_DELAY",
                alpha=0.4,
                color="lightblue",
                ax=ax2,
            )
            ax2.set_xlabel("Departure Delay (minutes)", fontsize=12)
            ax2.set_ylabel("Arrival Delay (minutes)", fontsize=12)
            ax2.set_title("Relationship Between Departure and Arrival Delays", fontsize=14, pad=15)
            ax2.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig2)
        else:
            st.warning("Insufficient data for departure vs arrival scatter plot.")
    else:
        st.warning("DEPARTURE_DELAY or ARRIVAL_DELAY column not found.")

    # ---------------- Key Delay Statistics ----------------
    if "TOTAL_DELAY" in df.columns:
        st.markdown("---")
        st.subheader("Key Delay Statistics")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Total Delay", f"{df['TOTAL_DELAY'].mean():.2f} minutes")
        with col2:
            st.metric("Median Total Delay", f"{df['TOTAL_DELAY'].median():.2f} minutes")
        with col3:
            st.metric(
                "Flights with delay > 60 mins",
                f"{(df['TOTAL_DELAY'] > 60).mean() * 100:.2f}%",
            )


# -------------------------------------------------------------------------
# DELAY PREDICTION
# -------------------------------------------------------------------------
elif menu == "Delay Prediction":
    st.title(" Flight Delay Prediction")
    st.markdown("Enter flight details below to predict whether your flight will be delayed.")

    # Try to load model
    @st.cache_resource
    def load_prediction_model():
        """Load the trained model from Models folder"""
        model_path = None
        model_type = None
        
        # Check for Spark model
        spark_model_path = "Models/best_spark_model"
        if os.path.exists(spark_model_path):
            try:
                # Try importing PySpark
                from pyspark.ml import PipelineModel
                from pyspark.sql import SparkSession
                
                # Create Spark session
                spark = SparkSession.builder.appName("FlightDelayPrediction").getOrCreate()
                
                # Load model
                model = PipelineModel.load(spark_model_path)
                return model, "spark", spark
            except ImportError:
                # PySpark warning (hidden for clean UI)
                # st.warning("⚠️ PySpark not available. Install with: pip install pyspark")
                pass
            except Exception as e:
                # Spark model loading error (hidden for clean UI)
                # st.warning(f"⚠️ Could not load Spark model: {e}")
                pass
        
        # Check for scikit-learn models (common formats)
        # Prioritize flight_delay_model.pkl
        model_files = [
            "Models/flight_delay_model.pkl",
            "Models/flight_delay_model.joblib",
        ]
        
        encoder_files = [
            "Models/airline_encoder.pkl",
            "Models/airline_encoder.joblib",
        ]
        
        # Try to load the main model
        for model_path in model_files:
            if os.path.exists(model_path):
                try:
                    # Try joblib first (better for scikit-learn)
                    if model_path.endswith('.pkl') or model_path.endswith('.joblib'):
                        model = joblib.load(model_path)
                    else:
                        with open(model_path, 'rb') as f:
                            model = pickle.load(f)
                    
                    # Try to load encoder if it exists
                    encoder = None
                    for enc_path in encoder_files:
                        if os.path.exists(enc_path):
                            try:
                                if enc_path.endswith('.pkl') or enc_path.endswith('.joblib'):
                                    encoder = joblib.load(enc_path)
                                else:
                                    with open(enc_path, 'rb') as f:
                                        encoder = pickle.load(f)
                                break
                            except Exception as e:
                                continue
                    
                    return model, "sklearn", encoder
                except Exception as e:
                    # Model loading error (hidden for clean UI)
                    # st.warning(f"⚠️ Could not load model from {model_path}: {e}")
                    continue
        
        # Fallback: try any .pkl or .joblib in Models folder
        sklearn_patterns = [
            "Models/*.pkl",
            "Models/*.joblib",
            "models/*.pkl",
            "models/*.joblib",
        ]
        
        for pattern in sklearn_patterns:
            files = glob.glob(pattern)
            # Skip encoder files
            files = [f for f in files if 'encoder' not in os.path.basename(f).lower()]
            if files:
                model_path = files[0]
                try:
                    if model_path.endswith('.pkl') or model_path.endswith('.joblib'):
                        model = joblib.load(model_path)
                    else:
                        with open(model_path, 'rb') as f:
                            model = pickle.load(f)
                    return model, "sklearn", None
                except Exception as e:
                    # Model loading error (hidden for clean UI)
                    # st.warning(f"⚠️ Could not load model from {model_path}: {e}")
                    pass
        
        return None, None, None

    # Load model
    model, model_type, encoder_or_spark = load_prediction_model()
    encoder = encoder_or_spark if model_type == "sklearn" else None
    spark_session = encoder_or_spark if model_type == "spark" else None
    
    # Model status (hidden for clean UI)
    # if model is None:
    #     st.warning("⚠️ ML Model not loaded. Using statistical prediction based on historical data.")
    #     st.info("💡 To use ML model: Place a scikit-learn model (.pkl/.joblib) in the 'Models' folder.")
    # else:
    #     model_info = f"✅ ML Model loaded successfully! (Type: {model_type})"
    #     if encoder is not None:
    #         model_info += " | Encoder loaded"
    #     st.success(model_info)
    
    # Create prediction form (always show, even without model)
    with st.form("prediction_form"):
        st.subheader(" Enter Flight Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Get unique airlines from data
            if "AIRLINE" in df.columns:
                airlines = sorted(df["AIRLINE"].dropna().unique().tolist())
            else:
                airlines = ["AA", "AS", "B6", "DL", "EV", "F9", "HA", "MQ", "NK", "OO", "UA", "US", "VX", "WN"]
            
            airline = st.selectbox(
                " Airline",
                options=airlines,
                help="Select the airline carrier"
            )
            
            # Get unique origin airports
            if "ORIGIN_AIRPORT" in df.columns:
                origins = sorted(df["ORIGIN_AIRPORT"].dropna().astype(str).unique().tolist())
                origins = [o for o in origins if len(str(o)) >= 3 and str(o).isalpha()][:100]  # Limit for performance
            else:
                origins = ["ATL", "DFW", "DEN", "ORD", "LAX", "JFK", "SFO", "SEA", "MIA", "CLT"]
            
            origin_airport = st.selectbox(
                " Origin Airport",
                options=origins,
                help="Select the departure airport code"
            )
            
            # Get unique destination airports
            if "DESTINATION_AIRPORT" in df.columns:
                destinations = sorted(df["DESTINATION_AIRPORT"].dropna().astype(str).unique().tolist())
                destinations = [d for d in destinations if len(str(d)) >= 3 and str(d).isalpha()][:100]
            else:
                destinations = ["ATL", "DFW", "DEN", "ORD", "LAX", "JFK", "SFO", "SEA", "MIA", "CLT"]
            
            destination_airport = st.selectbox(
                " Destination Airport",
                options=destinations,
                help="Select the arrival airport code"
            )
            
            # Month
            month = st.slider(
                " Month",
                min_value=1,
                max_value=12,
                value=6,
                help="Select the month (1=January, 12=December)"
            )
        
        with col2:
            # Day of Week
            day_of_week = st.selectbox(
                " Day of Week",
                options=[1, 2, 3, 4, 5, 6, 7],
                format_func=lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][x-1],
                help="Select the day of the week"
            )
            
            # Scheduled Departure Time (HHMM format)
            st.markdown(" ** Scheduled Departure Time** ")
            time_col1, time_col2 = st.columns(2)
            with time_col1:
                hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12, step=1)
            with time_col2:
                minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0, step=15)
            
            scheduled_departure = hour * 100 + minute
            
            # Distance
            if "DISTANCE" in df.columns:
                min_dist = int(df["DISTANCE"].min()) if not df["DISTANCE"].isna().all() else 100
                max_dist = int(df["DISTANCE"].max()) if not df["DISTANCE"].isna().all() else 5000
                avg_dist = int(df["DISTANCE"].mean()) if not df["DISTANCE"].isna().all() else 1000
            else:
                min_dist, max_dist, avg_dist = 100, 5000, 1000
            
            distance = st.number_input(
                " Flight Distance (miles)",
                min_value=min_dist,
                max_value=max_dist,
                value=avg_dist,
                step=50,
                help="Enter the flight distance in miles"
            )
            
            # Is Origin a Hub (auto-filled based on origin)
            major_hubs = ['ATL', 'DFW', 'DEN', 'ORD', 'LAX', 'JFK', 'SFO', 'SEA', 'MIA', 'CLT', 
                         'PHL', 'DTW', 'MSP', 'BOS', 'LGA', 'EWR', 'IAH', 'DCA']
            is_hub = 1 if origin_airport in major_hubs else 0
            st.info(f" Origin is Hub: {'Yes' if is_hub == 1 else 'No'} (Auto-detected)")
        
        # Submit button
        submitted = st.form_submit_button(" Predict Delay", use_container_width=True)
        
        if submitted:
            try:
                # Store the original airline selected by user (for chatbot context)
                selected_airline = airline
                
                # Prepare input data
                input_data = {
                    "AIRLINE": selected_airline,  # Always show user's selected airline
                    "ORIGIN_AIRPORT": origin_airport,
                    "DESTINATION_AIRPORT": destination_airport,
                    "MONTH": month,
                    "DAY_OF_WEEK": day_of_week,
                    "SCHEDULED_DEPARTURE": scheduled_departure,
                    "DISTANCE": distance,
                    "ORIGIN_IS_HUB": is_hub,
                }
                
                # Make prediction based on model type
                if model is None:
                    # Fallback: Statistical prediction using historical data
                    st.info("📊 Using statistical prediction based on historical flight data...")
                    
                    # Filter data based on inputs
                    filtered_df = df.copy()
                    
                    # Filter by airline if column exists
                    if "AIRLINE" in filtered_df.columns:
                        filtered_df = filtered_df[filtered_df["AIRLINE"] == airline]
                    
                    # Filter by origin if column exists
                    if "ORIGIN_AIRPORT" in filtered_df.columns:
                        filtered_df = filtered_df[filtered_df["ORIGIN_AIRPORT"].astype(str) == str(origin_airport)]
                    
                    # Filter by destination if column exists
                    if "DESTINATION_AIRPORT" in filtered_df.columns:
                        filtered_df = filtered_df[filtered_df["DESTINATION_AIRPORT"].astype(str) == str(destination_airport)]
                    
                    # Filter by month if column exists
                    if "MONTH" in filtered_df.columns:
                        filtered_df = filtered_df[filtered_df["MONTH"] == month]
                    
                    # Filter by day of week if column exists
                    if "DAY_OF_WEEK" in filtered_df.columns:
                        filtered_df = filtered_df[filtered_df["DAY_OF_WEEK"] == day_of_week]
                    
                    # Use delay column
                    delay_col = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in filtered_df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in filtered_df.columns else None
                    
                    if delay_col and len(filtered_df) > 0:
                        # Calculate probability of delay (delay > 0)
                        delay_rate = (filtered_df[delay_col] > 0).mean()
                        avg_delay_when_delayed = filtered_df[filtered_df[delay_col] > 0][delay_col].mean()
                        
                        # If not enough data, use broader filters
                        if len(filtered_df) < 10:
                            # Relax filters - use airline and month only
                            filtered_df = df.copy()
                            if "AIRLINE" in filtered_df.columns:
                                filtered_df = filtered_df[filtered_df["AIRLINE"] == airline]
                            if "MONTH" in filtered_df.columns:
                                filtered_df = filtered_df[filtered_df["MONTH"] == month]
                            
                            if delay_col and len(filtered_df) > 0:
                                delay_rate = (filtered_df[delay_col] > 0).mean()
                                avg_delay_when_delayed = filtered_df[filtered_df[delay_col] > 0][delay_col].mean()
                            else:
                                # Use overall statistics
                                delay_rate = (df[delay_col] > 0).mean() if delay_col in df.columns else 0.3
                                avg_delay_when_delayed = df[df[delay_col] > 0][delay_col].mean() if delay_col in df.columns else 30
                        else:
                            avg_delay_when_delayed = avg_delay_when_delayed if not pd.isna(avg_delay_when_delayed) else 30
                        
                        prob_delayed = delay_rate if not pd.isna(delay_rate) else 0.3
                        is_delayed = prob_delayed > 0.5
                        estimated_delay = prob_delayed * avg_delay_when_delayed if is_delayed else 0
                    
                    else:
                        # Use overall statistics
                        delay_col = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in df.columns else None
                        if delay_col:
                            delay_rate = (df[delay_col] > 0).mean()
                            avg_delay_when_delayed = df[df[delay_col] > 0][delay_col].mean()
                        else:
                            delay_rate = 0.3
                            avg_delay_when_delayed = 30
                        
                        prob_delayed = delay_rate if not pd.isna(delay_rate) else 0.3
                        is_delayed = prob_delayed > 0.5
                        estimated_delay = prob_delayed * avg_delay_when_delayed if is_delayed else 0
                
                elif model_type == "spark":
                    # Spark model prediction
                    from pyspark.sql import Row
                    input_row = Row(**input_data)
                    input_df = spark_session.createDataFrame([input_row])
                    predictions = model.transform(input_df)
                    
                    # Extract prediction (Spark returns probability and prediction)
                    prediction_row = predictions.collect()[0]
                    
                    # Check if model has probability column
                    if "probability" in predictions.columns:
                        prob = prediction_row["probability"]
                        if isinstance(prob, (list, tuple)):
                            prob_delayed = float(prob[1]) if len(prob) > 1 else float(prob[0])
                        else:
                            prob_delayed = float(prob)
                    else:
                        prob_delayed = 0.5
                    
                    prediction = prediction_row["prediction"]
                    is_delayed = int(prediction) == 1
                    
                    # Estimate delay minutes for Spark model
                    if is_delayed:
                        if "ARRIVAL_DELAY" in df.columns:
                            avg_delay = df[df["ARRIVAL_DELAY"] > 0]["ARRIVAL_DELAY"].mean()
                            estimated_delay = prob_delayed * avg_delay if not pd.isna(avg_delay) else prob_delayed * 30
                        else:
                            estimated_delay = prob_delayed * 30
                    else:
                        estimated_delay = 0
                    
                elif model_type == "sklearn":
                    # Scikit-learn model prediction
                    try:
                        # Prepare features based on model's expected input
                        # Model expects: ['AIRLINE_ENC', 'MONTH', 'DAY', 'DISTANCE']
                        
                        # Encode airline using the encoder
                        airline_enc = 0
                        if encoder is not None:
                            try:
                                # Try to encode the airline code
                                if airline in encoder.classes_:
                                    airline_enc = encoder.transform([airline])[0]
                                else:
                                    # If airline not in encoder, use default (first class)
                                    # Warning hidden for clean UI
                                    # st.warning(f"⚠️ Airline '{airline}' not in encoder. Using default encoding.")
                                    airline_enc = 0
                            except Exception as e:
                                # Error encoding warning hidden for clean UI
                                # st.warning(f"⚠️ Error encoding airline: {e}")
                                airline_enc = 0
                        
                        # Prepare feature array in the exact order the model expects
                        # Based on model.feature_names_in_: ['AIRLINE_ENC', 'MONTH', 'DAY', 'DISTANCE']
                        features = np.array([[
                            airline_enc,      # AIRLINE_ENC (encoded airline)
                            month,            # MONTH
                            day_of_week,      # DAY (using day_of_week input)
                            distance          # DISTANCE
                        ]])
                        
                        # Make prediction
                        if hasattr(model, "predict_proba"):
                            proba = model.predict_proba(features)[0]
                            # Assuming class 1 is "delayed" and class 0 is "on time"
                            prob_delayed = proba[1] if len(proba) > 1 else proba[0]
                            prediction = model.predict(features)[0]
                        else:
                            prediction = model.predict(features)[0]
                            # Default probability if no predict_proba
                            prob_delayed = 0.7 if prediction == 1 else 0.3
                        
                        is_delayed = int(prediction) == 1
                        
                        # Estimate delay minutes based on probability and historical data
                        if is_delayed:
                            if "ARRIVAL_DELAY" in df.columns:
                                avg_delay = df[df["ARRIVAL_DELAY"] > 0]["ARRIVAL_DELAY"].mean()
                                estimated_delay = prob_delayed * avg_delay if not pd.isna(avg_delay) else prob_delayed * 30
                            else:
                                estimated_delay = prob_delayed * 30
                        else:
                            estimated_delay = 0
                        
                    except Exception as e:
                        st.error(f"Error with sklearn model prediction: {str(e)}")
                        # Fallback to statistical method
                        st.info(" Falling back to statistical prediction...")
                        # Use the statistical prediction code from above
                        filtered_df = df.copy()
                        if "AIRLINE" in filtered_df.columns:
                            filtered_df = filtered_df[filtered_df["AIRLINE"] == airline]
                        if "MONTH" in filtered_df.columns:
                            filtered_df = filtered_df[filtered_df["MONTH"] == month]
                        delay_col = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in df.columns else None
                        if delay_col and len(filtered_df) > 0:
                            delay_rate = (filtered_df[delay_col] > 0).mean()
                            avg_delay_when_delayed = filtered_df[filtered_df[delay_col] > 0][delay_col].mean()
                            prob_delayed = delay_rate if not pd.isna(delay_rate) else 0.3
                            is_delayed = prob_delayed > 0.5
                            estimated_delay = prob_delayed * avg_delay_when_delayed if is_delayed else 0
                        else:
                            prob_delayed = 0.3
                            is_delayed = False
                            estimated_delay = 0
                    
                    # Store prediction results in session state so they persist across reruns
                    st.session_state.prediction_results = {
                        "is_delayed": is_delayed,
                        "prob_delayed": prob_delayed,
                        "estimated_delay": estimated_delay,
                        "input_data": input_data,
                        "model_type": model_type if model else "statistical",
                        "data_points": len(filtered_df) if 'filtered_df' in locals() and 'delay_col' in locals() and delay_col and len(filtered_df) > 0 else None
                    }
                    
                    # Store prediction context for chatbot
                    st.session_state.last_prediction_context = {
                        "airline": selected_airline,
                        "origin": origin_airport,
                        "destination": destination_airport,
                        "month": month,
                        "day": day_of_week,
                        "distance": distance,
                        "is_delayed": is_delayed,
                        "prob_delayed": prob_delayed,
                        "estimated_delay": estimated_delay
                    }
                    
            except Exception as e:
                st.error(f" Error making prediction: {str(e)}")
                st.exception(e)
    
    # Display prediction results (persist across reruns)
    if st.session_state.get("prediction_results"):
        results = st.session_state.prediction_results
        st.markdown("---")
        st.subheader(" Prediction Results")
        
        result_col1, result_col2 = st.columns(2)
        
        with result_col1:
            if results["is_delayed"]:
                st.error(" **Prediction: DELAYED**")
                st.metric("Delay Probability", f"{results['prob_delayed'] * 100:.1f}%")
            else:
                st.success(" **Prediction: ON TIME**")
                st.metric("On-Time Probability", f"{(1 - results['prob_delayed']) * 100:.1f}%")
        
        with result_col2:
            if results["is_delayed"]:
                st.info(f" **Estimated Delay: {results['estimated_delay']:.0f} minutes**")
            else:
                st.info(" **Estimated Delay: 0 minutes**")
        
        # Show input summary
        with st.expander(" View Input Summary"):
            st.json(results["input_data"])
        
        # Show data used for prediction (if statistical method)
        if results["model_type"] == "statistical" and results.get("data_points"):
            with st.expander(" Prediction Method"):
                st.info("This prediction is based on historical flight data matching your criteria. For more accurate predictions, install PySpark and use the ML model.")
                st.write(f" **Data Points Used:** {results['data_points']:,} historical flights")
    
    # Chatbot Assistant Section (OUTSIDE the form to avoid st.button() error)
    if st.session_state.get("last_prediction_context"):
        st.markdown("---")
        st.subheader("💬 Flight Delay Chatbot Assistant")
        st.markdown("Ask me anything about your flight delay prediction! I can explain delay reasons, statistics, and more.")
        
        # Initialize chat history in session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Helper function to analyze delay reasons and patterns
        def get_delay_reasons_stats(airline=None, origin=None, dest=None, month=None, day=None):
            """Get delay reason statistics and patterns for given filters"""
            filtered_df = df.copy()
            
            if airline and "AIRLINE" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["AIRLINE"] == airline]
            if origin and "ORIGIN_AIRPORT" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["ORIGIN_AIRPORT"].astype(str) == str(origin)]
            if dest and "DESTINATION_AIRPORT" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["DESTINATION_AIRPORT"].astype(str) == str(dest)]
            if month and "MONTH" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["MONTH"] == month]
            if day and "DAY_OF_WEEK" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["DAY_OF_WEEK"] == day]
            
            delay_reasons = {}
            patterns = {}
            
            # Check for various delay reason column names
            delay_cols = {
                "Weather": ["WEATHER_DELAY", "weather_delay", "Weather_Delay"],
                "Carrier": ["CARRIER_DELAY", "carrier_delay", "AIRLINE_DELAY", "airline_delay"],
                "NAS": ["NAS_DELAY", "nas_delay", "AIR_SYSTEM_DELAY"],
                "Security": ["SECURITY_DELAY", "security_delay"],
                "Late Aircraft": ["LATE_AIRCRAFT_DELAY", "late_aircraft_delay"]
            }
            
            for reason, col_names in delay_cols.items():
                for col in col_names:
                    if col in filtered_df.columns:
                        avg_delay = filtered_df[col].fillna(0).mean()
                        if avg_delay > 0:
                            delay_reasons[reason] = avg_delay
                        break
            
            # Analyze patterns even without specific delay reason columns
            if len(filtered_df) > 0:
                delay_col = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in filtered_df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in filtered_df.columns else None
                
                if delay_col:
                    patterns["avg_delay"] = filtered_df[delay_col].mean()
                    patterns["median_delay"] = filtered_df[delay_col].median()
                    patterns["delay_rate"] = (filtered_df[delay_col] > 0).mean() * 100
                    patterns["avg_when_delayed"] = filtered_df[filtered_df[delay_col] > 0][delay_col].mean() if len(filtered_df[filtered_df[delay_col] > 0]) > 0 else 0
                    
                    # Analyze by month if available
                    if "MONTH" in filtered_df.columns:
                        month_delays = filtered_df.groupby("MONTH")[delay_col].mean()
                        patterns["worst_month"] = month_delays.idxmax() if len(month_delays) > 0 else None
                        patterns["best_month"] = month_delays.idxmin() if len(month_delays) > 0 else None
                    
                    # Analyze by day of week if available
                    if "DAY_OF_WEEK" in filtered_df.columns:
                        day_delays = filtered_df.groupby("DAY_OF_WEEK")[delay_col].mean()
                        patterns["worst_day"] = day_delays.idxmax() if len(day_delays) > 0 else None
                        patterns["best_day"] = day_delays.idxmin() if len(day_delays) > 0 else None
                    
                    # Analyze by distance if available
                    if "DISTANCE" in filtered_df.columns:
                        # Categorize by distance
                        filtered_df["distance_category"] = pd.cut(
                            filtered_df["DISTANCE"],
                            bins=[0, 500, 1000, 2000, float('inf')],
                            labels=["Short (<500mi)", "Medium (500-1000mi)", "Long (1000-2000mi)", "Very Long (>2000mi)"]
                        )
                        distance_delays = filtered_df.groupby("distance_category")[delay_col].mean()
                        patterns["distance_analysis"] = distance_delays.to_dict() if len(distance_delays) > 0 else {}
            
            return delay_reasons, len(filtered_df), patterns
        
        # Helper function to process user questions
        def process_question(question, context=None):
            """Process user question and generate answer"""
            question_lower = question.lower()
            
            # Check if question is off-topic (not about flights/airlines/delays)
            flight_keywords = ["flight", "airline", "airport", "delay", "route", "departure", "arrival", 
                             "aircraft", "plane", "ticket", "booking", "travel", "journey", "trip",
                             "hub", "carrier", "destination", "origin", "miles", "distance", "time"]
            is_flight_related = any(keyword in question_lower for keyword in flight_keywords)
            
            if not is_flight_related:
                return "I'm specifically trained to help with flight delay predictions and airline-related questions! I can help you understand delays, analyze routes, compare airlines, and explain your flight predictions. Feel free to ask me anything about flight delays, airlines, or your specific flight prediction!"
            
            # Extract context if available
            airline = context.get("airline") if context else None
            origin = context.get("origin") if context else None
            dest = context.get("destination") if context else None
            month = context.get("month") if context else None
            day = context.get("day") if context else None
            distance = context.get("distance") if context else None
            is_delayed = context.get("is_delayed") if context else None
            prob_delayed = context.get("prob_delayed") if context else None
            estimated_delay = context.get("estimated_delay") if context else None
            
            # Get scheduled departure time from prediction results if available
            scheduled_departure = None
            if st.session_state.get("prediction_results"):
                pred_data = st.session_state.prediction_results.get("input_data", {})
                scheduled_departure = pred_data.get("SCHEDULED_DEPARTURE")
            if scheduled_departure is None:
                scheduled_departure = context.get("SCHEDULED_DEPARTURE") if context else None
            
            # Question: Why is my flight delayed / delay reasons
            if any(word in question_lower for word in ["reason", "why", "cause", "what causes", "why delayed", "what could be the reason"]):
                delay_reasons, num_flights, patterns = get_delay_reasons_stats(airline, origin, dest, month, day)
                
                # Start with a natural, conversational response
                if is_delayed and estimated_delay:
                    if estimated_delay > 60:
                        answer = f"Your flight from {origin} to {dest} with {airline} is likely to be delayed by around {estimated_delay:.0f} minutes. "
                    elif estimated_delay > 30:
                        answer = f"Your flight from {origin} to {dest} with {airline} might experience a delay of about {estimated_delay:.0f} minutes. "
                    else:
                        answer = f"Your flight from {origin} to {dest} with {airline} could have a small delay, around {estimated_delay:.0f} minutes. "
                    
                    answer += "Here are the possible reasons for your delay:\n\n"
                    
                    # Add detailed delay reasons - provide multiple reasons
                    if delay_reasons:
                        sorted_reasons = sorted(delay_reasons.items(), key=lambda x: x[1], reverse=True)
                        
                        reason_count = 0
                        for reason, delay_val in sorted_reasons:
                            if delay_val > 0 and reason_count < 4:  # Show up to 4 reasons
                                if reason == "Weather":
                                    answer += f"🌧️ **Weather Conditions**: Weather delays average {delay_val:.0f} minutes on this route. "
                                    if month:
                                        month_names = ["", "January", "February", "March", "April", "May", "June", 
                                                      "July", "August", "September", "October", "November", "December"]
                                        if month in [12, 1, 2]:
                                            answer += f"Winter weather in {month_names[month]} can definitely be a factor. "
                                        elif month in [6, 7, 8]:
                                            answer += f"Summer thunderstorms in {month_names[month]} are common. "
                                    answer += "\n\n"
                                    
                                elif reason == "Carrier":
                                    answer += f" **Airline Operations**: {airline if airline else 'The airline'} sometimes faces operational challenges like aircraft maintenance, crew scheduling, or ground handling issues, averaging {delay_val:.0f} minutes when they occur. "
                                    answer += "\n\n"
                                    
                                elif reason == "NAS":
                                    answer += f"🏢 **Airport Congestion**: Air traffic control congestion at {dest if dest else 'the destination airport'} can cause delays, especially during peak hours. This typically adds about {delay_val:.0f} minutes. "
                                    # Check if it's a peak time
                                    if scheduled_departure:
                                        hour = scheduled_departure // 100 if scheduled_departure else 12
                                        if 6 <= hour <= 9:
                                            answer += f"Your morning departure (around {hour}:00) is during peak rush hour. "
                                        elif 16 <= hour <= 19:
                                            answer += f"Your evening departure (around {hour}:00) is during the busy evening rush. "
                                    answer += "\n\n"
                                    
                                elif reason == "Late Aircraft":
                                    answer += f" **Late Arriving Aircraft**: When your plane arrives late from another flight, it can push your departure back by around {delay_val:.0f} minutes. "
                                    if origin:
                                        major_hubs = ['ATL', 'DFW', 'DEN', 'ORD', 'LAX', 'JFK', 'SFO', 'SEA', 'MIA', 'CLT', 
                                                     'PHL', 'DTW', 'MSP', 'BOS', 'LGA', 'EWR', 'IAH', 'DCA']
                                        if origin in major_hubs:
                                            answer += f"This is common at busy hub airports like {origin}. "
                                    answer += "\n\n"
                                    
                                elif reason == "Security":
                                    answer += f" **Security Delays**: Security screening can sometimes cause delays, typically adding about {delay_val:.0f} minutes when they occur. "
                                    answer += "\n\n"
                                
                                reason_count += 1
                        
                        # If no specific delay reasons found, provide contextual reasons
                        if reason_count == 0:
                            answer += "Based on your flight details, here are the likely reasons:\n\n"
                            
                            # Month-based reasons
                            if month:
                                month_names = ["", "January", "February", "March", "April", "May", "June", 
                                              "July", "August", "September", "October", "November", "December"]
                                if month in [12, 1, 2]:
                                    answer += f"❄️ **Winter Weather**: Traveling in {month_names[month]} means winter weather conditions (snow, ice, storms) can cause delays. "
                                    answer += "\n\n"
                                elif month in [6, 7, 8]:
                                    answer += f"⛈️ **Summer Storms**: {month_names[month]} often brings thunderstorms that can disrupt flight schedules. "
                                    answer += "\n\n"
                            
                            # Time-based reasons
                            if scheduled_departure:
                                hour = scheduled_departure // 100 if scheduled_departure else 12
                                if 6 <= hour <= 9:
                                    answer += f"🌅 **Peak Morning Rush**: Your departure at {hour}:00 is during peak morning hours when airports are busiest, increasing delay likelihood. "
                                    answer += "\n\n"
                                elif 16 <= hour <= 19:
                                    answer += f"🌆 **Peak Evening Rush**: Your departure at {hour}:00 is during peak evening hours when congestion is highest. "
                                    answer += "\n\n"
                            
                            # Hub-based reasons
                            if dest:
                                major_hubs = ['ATL', 'DFW', 'DEN', 'ORD', 'LAX', 'JFK', 'SFO', 'SEA', 'MIA', 'CLT', 
                                             'PHL', 'DTW', 'MSP', 'BOS', 'LGA', 'EWR', 'IAH', 'DCA']
                                if dest in major_hubs:
                                    answer += f"🏢 **Hub Airport Congestion**: {dest} is a major hub airport, which means it handles many flights and can get congested, especially during peak times. "
                                    answer += "\n\n"
                            
                            # Airline-based reasons
                            if airline:
                                airline_df = df[df["AIRLINE"].astype(str) == str(airline)].copy()
                                if len(airline_df) > 0:
                                    delay_col_airline = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in airline_df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in airline_df.columns else None
                                    if delay_col_airline:
                                        airline_avg = airline_df[delay_col_airline].mean()
                                        if airline_avg > 15:
                                            answer += f" **Airline Operations**: {airline} flights on similar routes average {airline_avg:.0f} minutes delay, suggesting operational factors may be involved. "
                                            answer += "\n\n"
                            
                            # Day-based reasons
                            if day:
                                day_names = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                                if day in [1, 2, 3, 4, 5]:  # Weekdays
                                    answer += f" **Weekday Travel**: {day_names[day]}s are typically busier with business travelers, which can increase airport congestion. "
                                    answer += "\n\n"
                            
                            # Distance-based reasons
                            if distance:
                                if distance > 2000:
                                    answer += f" **Long-Haul Flight**: Your {distance}-mile flight is long-haul, which means more opportunities for delays to accumulate. "
                                    answer += "\n\n"
                        
                        # Add a summary
                        answer += "These factors can combine to cause delays, so it's good to plan ahead!"
                    else:
                        # Provide multiple possible reasons when specific delay data isn't available
                        answer += "Based on your flight details, here are the possible reasons for delays:\n\n"
                        
                        # Month-based reasons
                        if month:
                            month_names = ["", "January", "February", "March", "April", "May", "June", 
                                          "July", "August", "September", "October", "November", "December"]
                            if month in [12, 1, 2]:
                                answer += f" **Winter Weather**: Traveling in {month_names[month]} means winter weather conditions (snow, ice, storms) can cause delays. "
                                answer += "\n\n"
                            elif month in [6, 7, 8]:
                                answer += f" **Summer Storms**: {month_names[month]} often brings thunderstorms that can disrupt flight schedules. "
                                answer += "\n\n"
                            elif patterns.get("worst_month") and month == patterns["worst_month"]:
                                answer += f" **Peak Travel Month**: {month_names[month]} tends to be the worst month for delays on this route, often due to weather or increased travel volume. "
                                answer += "\n\n"
                        
                        # Time-based reasons
                        if scheduled_departure:
                            hour = scheduled_departure // 100 if scheduled_departure else 12
                            if 6 <= hour <= 9:
                                answer += f" **Peak Morning Rush**: Your departure at {hour}:00 is during peak morning hours when airports are busiest, increasing delay likelihood. "
                                answer += "\n\n"
                            elif 16 <= hour <= 19:
                                answer += f" **Peak Evening Rush**: Your departure at {hour}:00 is during peak evening hours when congestion is highest. "
                                answer += "\n\n"
                            elif 10 <= hour <= 14:
                                answer += f" **Midday Travel**: Midday flights like yours (around {hour}:00) are usually less crowded, but delays can still happen due to airport operations. "
                                answer += "\n\n"
                        
                        # Hub-based reasons
                        if dest:
                            major_hubs = ['ATL', 'DFW', 'DEN', 'ORD', 'LAX', 'JFK', 'SFO', 'SEA', 'MIA', 'CLT', 
                                         'PHL', 'DTW', 'MSP', 'BOS', 'LGA', 'EWR', 'IAH', 'DCA']
                            if dest in major_hubs:
                                answer += f" **Hub Airport Congestion**: {dest} is a major hub airport, which means it handles many flights and can get congested, especially during peak times. "
                                answer += "\n\n"
                        
                        if origin:
                            major_hubs = ['ATL', 'DFW', 'DEN', 'ORD', 'LAX', 'JFK', 'SFO', 'SEA', 'MIA', 'CLT', 
                                         'PHL', 'DTW', 'MSP', 'BOS', 'LGA', 'EWR', 'IAH', 'DCA']
                            if origin in major_hubs:
                                answer += f" **Hub Departure**: Departing from {origin}, a major hub, means your aircraft might arrive late from another flight, causing cascading delays. "
                                answer += "\n\n"
                        
                        # Airline-based reasons
                        if airline:
                            airline_df = df[df["AIRLINE"].astype(str) == str(airline)].copy()
                            if len(airline_df) > 0:
                                delay_col_airline = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in airline_df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in airline_df.columns else None
                                if delay_col_airline:
                                    airline_avg = airline_df[delay_col_airline].mean()
                                    if airline_avg > 15:
                                        answer += f" **Airline Operations**: {airline} flights on similar routes average {airline_avg:.0f} minutes delay, suggesting operational factors like maintenance, crew scheduling, or ground handling may be involved. "
                                        answer += "\n\n"
                        
                        # Day-based reasons
                        if day:
                            day_names = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                            if day in [1, 2, 3, 4, 5]:  # Weekdays
                                answer += f" **Weekday Travel**: {day_names[day]}s are typically busier with business travelers, which can increase airport congestion and delays. "
                                answer += "\n\n"
                            elif patterns.get("worst_day") and day == patterns["worst_day"]:
                                answer += f"**Peak Travel Day**: {day_names[day]}s can be tricky for this route, often because airports are busier. "
                                answer += "\n\n"
                        
                        # Distance-based reasons
                        if distance:
                            if distance > 2000:
                                answer += f"**Long-Haul Flight**: Your {distance}-mile flight is long-haul, which means more opportunities for delays to accumulate along the way. "
                                answer += "\n\n"
                        
                        # Delay rate insights
                        if patterns.get("delay_rate"):
                            delay_rate = patterns["delay_rate"]
                            if delay_rate > 50:
                                answer += f" **High Delay Frequency**: This route sees delays in about {delay_rate:.0f}% of flights, so multiple factors can contribute. "
                                answer += "\n\n"
                        
                        answer += "These factors can combine to cause delays, so it's good to plan ahead!"
                    
                    # Add route-specific context
                    if origin and dest:
                        answer += f"You're flying from {origin} to {dest}, "
                    if airline:
                        answer += f"with {airline}. "
                    if month:
                        month_names = ["", "January", "February", "March", "April", "May", "June", 
                                      "July", "August", "September", "October", "November", "December"]
                        answer += f"You're traveling in {month_names[month]}, "
                    if day:
                        day_names = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                        answer += f"on a {day_names[day]}. "
                    
                    # Add friendly recommendations
                    if estimated_delay > 60:
                        answer += "I'd definitely suggest getting to the airport earlier than usual and having a backup plan, just to be safe."
                    elif estimated_delay > 30:
                        answer += "You might want to add some extra time to your schedule, just in case."
                    else:
                        answer += "It's not a huge delay, but worth keeping in mind when planning your day."
                else:
                    # On-time response (already good, keeping it)
                    answer = f"Great news! Your flight from {origin} to {dest} with {airline} is predicted to be on time. "
                    answer += f"No delays expected, so you should be good to go! "
                    if month:
                        month_names = ["", "January", "February", "March", "April", "May", "June", 
                                      "July", "August", "September", "October", "November", "December"]
                        answer += f"You're traveling in {month_names[month]}, "
                    if day:
                        day_names = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                        answer += f"on a {day_names[day]}. "
                    if distance:
                        if distance < 500:
                            answer += f"It's a short flight ({distance} miles), so even if there's a delay, it shouldn't be too disruptive."
                        elif distance < 2000:
                            answer += f"It's a {distance}-mile flight, so plan accordingly."
                        else:
                            answer += f"It's a long flight ({distance} miles), so any delays could impact your schedule more."
                
                return answer
            
            # Question: Average delay time
            elif any(word in question_lower for word in ["average", "avg", "mean", "how long", "how much time", "typical delay"]):
                delay_reasons, num_flights, patterns = get_delay_reasons_stats(airline, origin, dest, month, day)
                
                # Natural, conversational response
                if patterns and patterns.get("avg_delay") is not None:
                    avg_delay = patterns["avg_delay"]
                    
                    if avg_delay < 5:
                        answer = f"Flights on this route are usually on time. The average delay is just {avg_delay:.0f} minutes, so you're looking good! "
                    elif avg_delay < 15:
                        answer = f"Most flights run pretty smoothly here. You can expect delays around {avg_delay:.0f} minutes on average. "
                    elif avg_delay < 30:
                        answer = f"This route sees some delays, typically around {avg_delay:.0f} minutes. "
                    else:
                        answer = f"Delays are common on this route, averaging about {avg_delay:.0f} minutes. "
                    
                    # Add context about when delays happen
                    if patterns.get("avg_when_delayed") and patterns["avg_when_delayed"] > 0:
                        when_delayed = patterns["avg_when_delayed"]
                        if patterns.get("delay_rate"):
                            delay_rate = patterns["delay_rate"]
                            if delay_rate < 30:
                                answer += f"When delays do happen, they're usually around {when_delayed:.0f} minutes, but that's pretty rare. "
                            else:
                                answer += f"When there are delays, they tend to be around {when_delayed:.0f} minutes. "
                    
                    # Your specific flight
                    if estimated_delay is not None:
                        if estimated_delay == 0:
                            answer += f"For your specific flight, it looks like you'll be on time - no delays expected!"
                        elif estimated_delay < 15:
                            answer += f"Your flight might have a small delay of about {estimated_delay:.0f} minutes, but nothing major."
                        elif estimated_delay < 30:
                            answer += f"Your flight could be delayed by around {estimated_delay:.0f} minutes, so plan accordingly."
                        else:
                            answer += f"Your flight is likely to be delayed by about {estimated_delay:.0f} minutes, so I'd suggest building in some extra time."
                else:
                    # Fallback to prediction data
                    if estimated_delay is not None:
                        if estimated_delay == 0:
                            answer = "Your flight is usually on time with no delays expected. You should be good to go!"
                        else:
                            answer = f"Your flight typically experiences delays of around {estimated_delay:.0f} minutes. "
                            if is_delayed:
                                answer += "So you'll want to plan for that."
                            else:
                                answer += "But your specific flight looks like it might be okay."
                    else:
                        # Draw conclusions from available context even without route data
                        answer = f"Based on your flight details, "
                        if airline:
                            airline_df = df[df["AIRLINE"].astype(str) == str(airline)].copy()
                            if len(airline_df) > 0:
                                delay_col_airline = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in airline_df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in airline_df.columns else None
                                if delay_col_airline:
                                    airline_avg = airline_df[delay_col_airline].mean()
                                    if airline_avg < 10:
                                        answer += f"{airline} typically has good on-time performance with minimal delays. "
                                    else:
                                        answer += f"{airline} flights sometimes experience delays averaging {airline_avg:.0f} minutes. "
                        if month:
                            month_df = df[df["MONTH"] == month].copy()
                            if len(month_df) > 0:
                                delay_col_month = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in month_df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in month_df.columns else None
                                if delay_col_month:
                                    month_avg = month_df[delay_col_month].mean()
                                    month_names = ["", "January", "February", "March", "April", "May", "June", 
                                                  "July", "August", "September", "October", "November", "December"]
                                    answer += f"Traveling in {month_names[month]} generally shows delays around {month_avg:.0f} minutes on average. "
                        if distance:
                            if distance < 500:
                                answer += f"Since it's a short {distance}-mile flight, delays are typically minimal. "
                            elif distance < 1500:
                                answer += f"For a {distance}-mile flight, moderate delays can occur. "
                            else:
                                answer += f"Long-haul flights like your {distance}-mile journey may experience more significant delays. "
                        answer += "Your prediction indicates you should be on time!"
                
                return answer
            # Question: About this specific prediction
            elif any(word in question_lower for word in ["my flight", "this flight", "my prediction", "this prediction"]):
                if context and is_delayed is not None:
                    if is_delayed:
                        if estimated_delay > 60:
                            answer = f"Your flight from {origin} to {dest} with {airline} is likely to be delayed by around {estimated_delay:.0f} minutes. "
                            answer += f"That's a pretty significant delay, so I'd definitely recommend getting to the airport early and maybe having a backup plan. "
                        elif estimated_delay > 30:
                            answer = f"Your flight looks like it might be delayed by about {estimated_delay:.0f} minutes. "
                            answer += f"Not terrible, but you'll want to add some buffer time to your schedule. "
                        else:
                            answer = f"Your flight could have a small delay of around {estimated_delay:.0f} minutes. "
                            answer += f"Nothing too serious, but worth keeping in mind. "
                        
                        # Add route context
                        if origin and dest:
                            answer += f"You're flying from {origin} to {dest}, "
                        if airline:
                            answer += f"with {airline}. "
                    else:
                        answer = f"Great news! Your flight from {origin} to {dest} with {airline} is predicted to be on time. "
                        answer += f"No delays expected, so you should be good to go! "
                    
                    # Add timing context
                    if month:
                        month_names = ["", "January", "February", "March", "April", "May", "June", 
                                      "July", "August", "September", "October", "November", "December"]
                        answer += f"You're traveling in {month_names[month]}, "
                    if day:
                        day_names = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                        answer += f"on a {day_names[day]}. "
                    
                    if distance:
                        if distance < 500:
                            answer += f"It's a short flight ({distance} miles), so even if there's a delay, it shouldn't be too disruptive."
                        elif distance < 2000:
                            answer += f"It's a {distance}-mile flight, so plan accordingly."
                        else:
                            answer += f"It's a long flight ({distance} miles), so any delays could impact your schedule more."
                else:
                    answer = "I'd love to help, but I need you to make a prediction first! Fill out the form above and click 'Predict Delay', then I can tell you all about your specific flight."
                
                return answer
            
            # Question: Route-specific
            elif any(word in question_lower for word in ["route", "from", "to", "between"]):
                if origin and dest:
                    route_df = df[
                        (df["ORIGIN_AIRPORT"].astype(str) == str(origin)) &
                        (df["DESTINATION_AIRPORT"].astype(str) == str(dest))
                    ].copy()
                    
                    if len(route_df) > 0:
                        delay_col = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in route_df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in route_df.columns else None
                        
                        if delay_col:
                            avg_delay = route_df[delay_col].mean()
                            delay_rate = (route_df[delay_col] > 0).mean() * 100
                            
                            if avg_delay < 5:
                                answer = f"The route from {origin} to {dest} is usually pretty reliable. "
                                answer += f"Most flights run on time, with delays averaging just {avg_delay:.0f} minutes when they do happen. "
                            elif avg_delay < 15:
                                answer = f"Flights from {origin} to {dest} generally run smoothly. "
                                answer += f"You might see delays of around {avg_delay:.0f} minutes sometimes, but it's not too bad. "
                            elif avg_delay < 30:
                                answer = f"This route from {origin} to {dest} does see some delays, typically around {avg_delay:.0f} minutes. "
                            else:
                                answer = f"The route from {origin} to {dest} tends to have delays, averaging about {avg_delay:.0f} minutes. "
                            
                            if delay_rate < 30:
                                answer += f"Delays aren't super common though - only about {delay_rate:.0f}% of flights get delayed. "
                            elif delay_rate < 50:
                                answer += f"About {delay_rate:.0f}% of flights on this route experience delays. "
                            else:
                                answer += f"Delays happen fairly often - about {delay_rate:.0f}% of flights get delayed. "
                            
                            if estimated_delay is not None:
                                if estimated_delay == 0:
                                    answer += f"For your specific flight, it looks like you'll be on time!"
                                else:
                                    answer += f"Your flight might be delayed by around {estimated_delay:.0f} minutes."
                        else:
                            # Draw insights from available data
                            answer = f"Looking at flights from {origin} to {dest}, "
                            
                            # Analyze by origin airport
                            origin_df = df[df["ORIGIN_AIRPORT"].astype(str) == str(origin)].copy()
                            if len(origin_df) > 0:
                                delay_col_origin = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in origin_df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in origin_df.columns else None
                                if delay_col_origin:
                                    origin_avg = origin_df[delay_col_origin].mean()
                                    answer += f"departures from {origin} typically see delays averaging {origin_avg:.0f} minutes. "
                            
                            # Analyze by destination
                            dest_df = df[df["DESTINATION_AIRPORT"].astype(str) == str(dest)].copy()
                            if len(dest_df) > 0:
                                delay_col_dest = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in dest_df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in dest_df.columns else None
                                if delay_col_dest:
                                    dest_avg = dest_df[delay_col_dest].mean()
                                    answer += f"Arrivals at {dest} average around {dest_avg:.0f} minutes delay. "
                            
                            if estimated_delay is not None:
                                if estimated_delay == 0:
                                    answer += f"Your prediction shows you should be on time!"
                                else:
                                    answer += f"Your prediction suggests a delay of about {estimated_delay:.0f} minutes."
                            else:
                                answer += "Based on these patterns, your flight should be manageable."
                    else:
                        # Draw insights from available data even without exact route match
                        answer = f"Looking at the {origin} to {dest} route, "
                        
                        # Analyze by origin airport
                        if origin:
                            origin_df = df[df["ORIGIN_AIRPORT"].astype(str) == str(origin)].copy()
                            if len(origin_df) > 0:
                                delay_col_origin = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in origin_df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in origin_df.columns else None
                                if delay_col_origin:
                                    origin_avg = origin_df[delay_col_origin].mean()
                                    answer += f"flights departing from {origin} typically experience delays averaging {origin_avg:.0f} minutes. "
                        
                        # Analyze by destination airport
                        if dest:
                            dest_df = df[df["DESTINATION_AIRPORT"].astype(str) == str(dest)].copy()
                            if len(dest_df) > 0:
                                delay_col_dest = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in dest_df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in dest_df.columns else None
                                if delay_col_dest:
                                    dest_avg = dest_df[delay_col_dest].mean()
                                    answer += f"Flights arriving at {dest} see delays around {dest_avg:.0f} minutes on average. "
                        
                        # Add airline context
                        if airline:
                            airline_df = df[df["AIRLINE"].astype(str) == str(airline)].copy()
                            if len(airline_df) > 0:
                                delay_col_airline = "ARRIVAL_DELAY" if "ARRIVAL_DELAY" in airline_df.columns else "TOTAL_DELAY" if "TOTAL_DELAY" in airline_df.columns else None
                                if delay_col_airline:
                                    airline_avg = airline_df[delay_col_airline].mean()
                                    answer += f"{airline} flights generally have delays averaging {airline_avg:.0f} minutes. "
                        
                        # Add prediction context
                        if estimated_delay is not None:
                            if estimated_delay == 0:
                                answer += f"Based on your prediction, your flight should be on time!"
                            else:
                                answer += f"Your prediction suggests a delay of about {estimated_delay:.0f} minutes for this flight."
                        else:
                            answer += "Based on these patterns, your flight should be manageable."
                else:
                    answer = "I'd be happy to tell you about a specific route! Just let me know which airports you're flying between."
                
                return answer
            
            # Question: General help
            elif any(word in question_lower for word in ["help", "what can you", "what do you", "how can you"]):
                answer = """I can help you understand your flight delay prediction! Here's what I can answer:

📊 **About Your Prediction:**
• "Tell me about my flight prediction"
• "Why is my flight delayed?"
• "What is the average delay for my route?"

🔍 **Delay Reasons:**
• "What causes delays for my flight?"
• "What is the main reason for delays on this route?"

📈 **Statistics:**
• "What is the average delay for [airline/route]?"
• "How much is this airline delayed on average?"

💡 **Tip:** I use your prediction details to give you personalized answers!"""
                
                return answer
            
            # Default response
            else:
                    return """I can help you understand your flight delay prediction! Try asking:

• "Why is my flight delayed?"
• "What is the average delay for my route?"
• "Tell me about my flight prediction"
• "What causes delays for my flight?"

Or type "help" to see all available questions!"""
                    
        # Clear chat button (prominent, always visible when there's chat history)
        if st.session_state.chat_history:
            col_clear_header, col_clear_btn = st.columns([4, 1])
            with col_clear_header:
                st.markdown("**Ask me anything about flight delays, your prediction, or delay statistics:**")
            with col_clear_btn:
                if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.session_state.chat_input_counter = 0  # Reset input counter too
                    st.rerun()
        else:
            st.markdown("**Ask me anything about flight delays, your prediction, or delay statistics:**")
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input using text_input and button (similar to Credit Risk chatbot)
        col_input, col_button = st.columns([5, 1])
        with col_input:
            # Use a counter to force widget reset when needed
            if "chat_input_counter" not in st.session_state:
                st.session_state.chat_input_counter = 0
            
            # Create unique key that changes when we want to clear
            input_key = f"chat_input_{st.session_state.chat_input_counter}"
            
            user_question = st.text_input(
                "Ask me about your flight delay prediction...",
                key=input_key,
                label_visibility="collapsed",
                placeholder="e.g., Why is my flight delayed? What is the average delay for my route?"
            )
        with col_button:
            send_button = st.button("Send", type="primary", use_container_width=True)
        
        # Process question when button is clicked
        if send_button and user_question:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            
            # Get context from last prediction
            context = st.session_state.last_prediction_context if st.session_state.last_prediction_context else {}
            
            # Process question and get answer
            answer = process_question(user_question, context)
            
            # Add assistant response to history
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            
            # Increment counter to force widget reset (creates new key, clearing the input)
            st.session_state.chat_input_counter += 1
            
            # Rerun to update chat display
            st.rerun()
        
        # Tips section
        with st.expander("💡 Tip: Ask me questions like"):
            st.markdown("""
            - "Why is my flight delayed?" (after submitting your prediction)
            - "What is the average delay for my route?"
            - "What causes delays for my flight?"
            - "Tell me about my flight prediction"
            - "How much is this airline delayed on average?"
            """)