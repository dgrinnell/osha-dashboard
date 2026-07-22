"""OSHA Severe Injury & Fatality Dashboard."""

import streamlit as st
import time

from src.data_loader import load_severe_injuries, load_fatalities, clean_data
from src.charts import (
    create_trend_chart,
    create_severity_trend_chart,
    create_state_choropleth,
    create_naics_bar_chart,
    create_body_part_chart,
    create_injury_type_pie,
    create_event_bar_chart
)

# Page configuration
st.set_page_config(
    page_title="OSHA Injury Dashboard",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
REFRESH_INTERVAL = 300  # 5 minutes in seconds


def apply_filters(df, filters):
    """Apply sidebar filters to the dataframe."""
    df_filtered = df.copy()

    # Date range filter
    if filters['date_range'] and len(filters['date_range']) == 2:
        start_date, end_date = filters['date_range']
        df_filtered = df_filtered[
            (df_filtered['EventDate'].dt.date >= start_date) &
            (df_filtered['EventDate'].dt.date <= end_date)
        ]

    # State filter
    if filters['states']:
        df_filtered = df_filtered[df_filtered['State'].isin(filters['states'])]

    # Injury type filter
    if filters['injury_types']:
        df_filtered = df_filtered[df_filtered['NatureTitle'].isin(filters['injury_types'])]

    # Industry filter
    if filters['industries']:
        df_filtered = df_filtered[df_filtered['Primary NAICS'].isin(filters['industries'])]

    return df_filtered


def render_sidebar(df):
    """Render sidebar with filters and return filter values."""
    with st.sidebar:
        st.header("Filters")

        # Auto-refresh toggle
        auto_refresh = st.checkbox("Auto-refresh (5 min)", value=False)

        st.divider()

        # Date range filter
        min_date = df['EventDate'].min()
        max_date = df['EventDate'].max()

        if min_date is not None and max_date is not None:
            date_range = st.date_input(
                "Date Range",
                value=(min_date.date(), max_date.date()),
                min_value=min_date.date(),
                max_value=max_date.date()
            )
        else:
            date_range = None

        # State filter
        states = sorted([s for s in df['State'].dropna().unique() if s and s != 'nan'])
        selected_states = st.multiselect(
            "States",
            options=states,
            default=None,
            placeholder="All States"
        )

        # Injury type filter
        injury_types = sorted([t for t in df['NatureTitle'].dropna().unique() if t and t != 'nan'])
        selected_types = st.multiselect(
            "Injury Types",
            options=injury_types,
            default=None,
            placeholder="All Types"
        )

        # Industry filter (top 30 most common)
        top_industries = df['Primary NAICS'].value_counts().head(30).index.tolist()
        selected_industries = st.multiselect(
            "Industry (NAICS)",
            options=top_industries,
            default=None,
            placeholder="All Industries"
        )

        return {
            'auto_refresh': auto_refresh,
            'date_range': date_range,
            'states': selected_states,
            'injury_types': selected_types,
            'industries': selected_industries
        }


def render_kpi_metrics(df, df_fatalities):
    """Render top row of KPI metrics."""
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Total Severe Injuries",
            value=f"{len(df):,}"
        )

    with col2:
        hosp = int(df['Hospitalized'].sum())
        st.metric(
            label="Hospitalizations",
            value=f"{hosp:,}"
        )

    with col3:
        amp = int(df['Amputation'].sum())
        st.metric(
            label="Amputations",
            value=f"{amp:,}"
        )

    with col4:
        # Calculate hospitalization rate
        hosp_rate = (df['Hospitalized'].sum() / len(df) * 100) if len(df) > 0 else 0
        st.metric(
            label="Hospitalization Rate",
            value=f"{hosp_rate:.1f}%"
        )

    with col5:
        st.metric(
            label="Total Fatalities",
            value=f"{len(df_fatalities):,}"
        )


def main():
    """Main application."""
    # Header
    st.title("⚠️ OSHA Severe Injury & Fatality Dashboard")

    # Load data
    with st.spinner("Loading data..."):
        df_injuries = load_severe_injuries()
        df_injuries = clean_data(df_injuries)
        df_fatalities = load_fatalities()

    min_date = df_injuries['EventDate'].min()
    max_date = df_injuries['EventDate'].max()
    st.caption(
        f"OSHA severe injury reports (federal jurisdiction), "
        f"{min_date.strftime('%B %Y')} – {max_date.strftime('%B %Y')}"
    )

    # Sidebar filters
    filters = render_sidebar(df_injuries)

    # Apply filters
    df_filtered = apply_filters(df_injuries, filters)

    # Display record count
    st.caption(f"Showing {len(df_filtered):,} of {len(df_injuries):,} records")

    # KPI Metrics row
    render_kpi_metrics(df_filtered, df_fatalities)

    st.divider()

    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📈 Trends", "🗺️ Geography", "📊 Analysis"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                create_trend_chart(df_filtered),
                use_container_width=True
            )

        with col2:
            st.plotly_chart(
                create_severity_trend_chart(df_filtered),
                use_container_width=True
            )

    with tab2:
        st.plotly_chart(
            create_state_choropleth(df_filtered),
            use_container_width=True
        )

        # State breakdown table
        with st.expander("View State Breakdown"):
            state_summary = df_filtered.groupby('State').agg({
                'ID': 'count',
                'Hospitalized': 'sum',
                'Amputation': 'sum'
            }).reset_index()
            state_summary.columns = ['State', 'Total Injuries', 'Hospitalizations', 'Amputations']
            state_summary = state_summary.sort_values('Total Injuries', ascending=False)
            st.dataframe(state_summary, use_container_width=True, hide_index=True)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                create_naics_bar_chart(df_filtered),
                use_container_width=True
            )

        with col2:
            st.plotly_chart(
                create_injury_type_pie(df_filtered),
                use_container_width=True
            )

        col3, col4 = st.columns(2)

        with col3:
            st.plotly_chart(
                create_body_part_chart(df_filtered),
                use_container_width=True
            )

        with col4:
            st.plotly_chart(
                create_event_bar_chart(df_filtered),
                use_container_width=True
            )

    # Raw data view
    st.divider()
    with st.expander("📋 View Raw Data"):
        # Limit to 1000 rows for performance
        display_df = df_filtered.head(1000).copy()

        # Format for display
        if 'EventDate' in display_df.columns:
            display_df['EventDate'] = display_df['EventDate'].dt.strftime('%Y-%m-%d')

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # Download button
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data (CSV)",
            data=csv,
            file_name="osha_filtered_data.csv",
            mime="text/csv"
        )

    # Auto-refresh logic
    if filters['auto_refresh']:
        # Initialize session state for refresh tracking
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = time.time()

        elapsed = time.time() - st.session_state.last_refresh

        # Show countdown in sidebar
        with st.sidebar:
            remaining = max(0, REFRESH_INTERVAL - elapsed)
            st.caption(f"Next refresh in {int(remaining)}s")

        # Trigger refresh if interval passed
        if elapsed >= REFRESH_INTERVAL:
            st.session_state.last_refresh = time.time()
            st.cache_data.clear()
            st.rerun()


if __name__ == "__main__":
    main()
