import altair as alt
import pandas as pd
import streamlit as st

# Configuration
st.set_page_config(
    page_title="Employment Ratio Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom UI Styling
st.markdown(
    """
    <style>
    /* New Global App Background */
    .stApp {
        background-color: #f0fdf4;
    }
    
    /* New Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* Custom Header Color */
    h1, h2, h3 {
        color: #166534 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Data loading
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_employment_ratio.csv")
    df.columns = df.columns.str.strip()
    df["Year"] = df["Year"].astype(int)
    return df


@st.cache_data
def convert_df_to_csv(data_frame):
    return data_frame.to_csv(index=False).encode("utf-8")


df = load_data()

# Data Validation
required_columns = ["Area", "Year", "Total", "Male", "Female", "Gap"]
missing_cols = [c for c in required_columns if c not in df.columns]
if missing_cols:
    st.error(f"Missing required dataset columns: {', '.join(missing_cols)}")
    st.stop()


#sidebar and Filters
with st.sidebar:
    st.title("Control Panel")
    st.markdown("---")

    countries = sorted(df["Area"].dropna().unique().tolist())
    selected_countries = st.multiselect(
        "Select Countries",
        options=countries,
        default=countries[:5] if len(countries) >= 5 else countries,
    )

    min_yr, max_yr = int(df["Year"].min()), int(df["Year"].max())
    year_range = st.slider(
        "Year Range",
        min_value=min_yr,
        max_value=max_yr,
        value=(min_yr, max_yr),
    )

    metric = st.selectbox(
        "Primary Chart Metric", ["Total", "Male", "Female", "Gap"]
    )


# Fitering
filtered = df[
    (df["Area"].isin(selected_countries))
    & (df["Year"].between(year_range[0], year_range[1]))
].sort_values(["Area", "Year"])

if filtered.empty:
    st.warning("No data found matching your selected filter criteria.")
    st.stop()

# UI setup
st.title("Global Employment & Gender Ratio Analysis")
st.caption(
    "Explore trends, gender distribution, and gaps across global employment data."
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Selected Countries", len(selected_countries))
col2.metric("Avg Total Employment", f"{filtered['Total'].mean():.1f}%")
col3.metric("Avg Male Employment", f"{filtered['Male'].mean():.1f}%")
col4.metric("Avg Gender Gap", f"{filtered['Gap'].mean():.1f} pts")

st.markdown("<br>", unsafe_allow_html=True)

#Gender gap
country_gap_stats = (
    filtered.groupby("Area")["Gap"]
    .mean()
    .sort_values(ascending=False)
)

max_gap_country = country_gap_stats.index[0]
max_gap_val = country_gap_stats.iloc[0]

min_gap_country = country_gap_stats.index[-1]
min_gap_val = country_gap_stats.iloc[-1]

gap_col1, gap_col2 = st.columns(2)

with gap_col1:
    st.error(
        f"**Highest Gender Gap:** **{max_gap_country}**\n\n"
        f"Averaged **{max_gap_val:.1f} percentage points** gap between male and female employment in the selected period."
    )

with gap_col2:
    st.success(
        f"**Lowest Gender Gap (Closest to Parity):** **{min_gap_country}**\n\n"
        f"Averaged **{min_gap_val:.1f} percentage points** gap between male and female employment in the selected period."
    )

st.markdown("<br>", unsafe_allow_html=True)


#Navigation
tab_trends, tab_gender, tab_explorer = st.tabs(
    ["Time Series Trends", "Gender Parity Analysis", "Data Explorer"]
)

#Tab 1
with tab_trends:
    st.subheader('Total Ratio by Year and Country')

with st.container(border=True):

    highlight = alt.selection_point(
        fields=['Area'],
        on='mouseover',
        empty='all'
    )

    bar_chart = (
        alt.Chart(filtered)
        .mark_bar(
            cornerRadiusTopLeft=4,
            cornerRadiusTopRight=4
        )
        .encode(
            x=alt.X(
                'Year:O',
                title='Year'
            ),

            y=alt.Y(
                'Total:Q',
                title='Total Ratio (%)'
            ),

            xOffset='Area:N',

            color=alt.Color(
                'Area:N',
                title='Country'
            ),

            opacity=alt.condition(
                highlight,
                alt.value(1),
                alt.value(0.25)
            ),

            tooltip=[
                alt.Tooltip(
                    'Area:N',
                    title='Country'
                ),
                alt.Tooltip(
                    'Year:O',
                    title='Year'
                ),
                alt.Tooltip(
                    'Total:Q',
                    title='Total Ratio',
                    format='.2f'
                )
            ]
        )
        .add_params(highlight)
        .properties(
            height=450
        )
    )

    st.altair_chart(
        bar_chart,
        use_container_width=True
    )

    st.subheader("Gender Gap Disparity Trend")

    with st.container(border=True):
        gap_chart = (
            alt.Chart(filtered)
            .mark_line(point=True, strokeWidth=2)
            .encode(
                x=alt.X("Year:N", title="Year"),
                y=alt.Y("Gap:Q", title="Gender Gap (pts)"),
                color=alt.Color("Area:N", title="Country"),
                tooltip=[
                    alt.Tooltip("Area:N", title="Country"),
                    alt.Tooltip("Year:N", title="Year"),
                    alt.Tooltip("Gap:Q", title="Gap", format=".2f"),
                ],
            )
            .properties(height=350)
            .interactive()
        )

        st.altair_chart(gap_chart, use_container_width=True)

#Tab 2
with tab_gender:
    st.subheader("Male vs Female Employment Ratio")

    with st.container(border=True):
        avail_years = sorted(filtered["Year"].unique(), reverse=True)
        scatter_year = st.selectbox(
            "Select Benchmark Year for Scatter Plot", avail_years, key="scatter_year"
        )

        scatter_data = filtered[filtered["Year"] == scatter_year].copy()

        dots = (
            alt.Chart(scatter_data)
            .mark_circle(size=120, opacity=0.85)
            .encode(
                x=alt.X(
                    "Male:Q",
                    title="Male Ratio (%)",
                    scale=alt.Scale(zero=False),
                ),
                y=alt.Y(
                    "Female:Q",
                    title="Female Ratio (%)",
                    scale=alt.Scale(zero=False),
                ),
                color=alt.Color("Area:N", title="Country"),
                size=alt.Size("Gap:Q", title="Gender Gap"),
                tooltip=[
                    alt.Tooltip("Area:N", title="Country"),
                    alt.Tooltip("Male:Q", title="Male (%)", format=".2f"),
                    alt.Tooltip("Female:Q", title="Female (%)", format=".2f"),
                    alt.Tooltip("Gap:Q", title="Gap (pts)", format=".2f"),
                ],
            )
        )

        parity_line = (
            alt.Chart(pd.DataFrame({"x": [0, 100], "y": [0, 100]}))
            .mark_line(color="gray", strokeDash=[4, 4])
            .encode(x="x:Q", y="y:Q")
        )

        combined_scatter = (
            (parity_line + dots).properties(height=480).interactive()
        )

        st.altair_chart(combined_scatter, use_container_width=True)

# Tab 3
with tab_explorer:
    st.subheader("Filtered Dataset")

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        st.download_button(
            label="📥 Export Filtered CSV",
            data=convert_df_to_csv(filtered),
            file_name="employment_ratio_filtered.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.dataframe(
        filtered[required_columns],
        use_container_width=True,
        hide_index=True,
        height=500,
    )