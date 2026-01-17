"""Chart generation functions using Plotly."""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from .utils import STATE_ABBREV, NAICS_LOOKUP


def create_trend_chart(df):
    """Monthly injury trends line chart."""
    monthly = df.groupby(df['EventDate'].dt.to_period('M')).size().reset_index(name='count')
    monthly['EventDate'] = monthly['EventDate'].dt.to_timestamp()

    fig = px.line(
        monthly,
        x='EventDate',
        y='count',
        title='Severe Injuries Over Time',
        labels={'count': 'Number of Injuries', 'EventDate': 'Date'}
    )

    fig.update_layout(
        hovermode='x unified',
        xaxis_title='',
        yaxis_title='Injuries',
        height=400
    )

    return fig


def create_severity_trend_chart(df):
    """Stacked area chart showing hospitalizations and amputations over time."""
    monthly = df.groupby(df['EventDate'].dt.to_period('M')).agg({
        'Hospitalized': 'sum',
        'Amputation': 'sum'
    }).reset_index()
    monthly['EventDate'] = monthly['EventDate'].dt.to_timestamp()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=monthly['EventDate'],
        y=monthly['Hospitalized'],
        name='Hospitalized',
        stackgroup='one',
        mode='lines',
        line=dict(color='#FF6B6B')
    ))

    fig.add_trace(go.Scatter(
        x=monthly['EventDate'],
        y=monthly['Amputation'],
        name='Amputation',
        stackgroup='one',
        mode='lines',
        line=dict(color='#4ECDC4')
    ))

    fig.update_layout(
        title='Injury Severity Over Time',
        hovermode='x unified',
        height=400,
        xaxis_title='',
        yaxis_title='Count'
    )

    return fig


def create_state_choropleth(df):
    """US state choropleth map."""
    by_state = df.groupby('State').size().reset_index(name='count')
    by_state['state_code'] = by_state['State'].map(STATE_ABBREV)

    # Filter out states without valid codes
    by_state = by_state[by_state['state_code'].notna()]

    fig = px.choropleth(
        by_state,
        locations='state_code',
        locationmode='USA-states',
        color='count',
        scope='usa',
        color_continuous_scale='Reds',
        title='Severe Injuries by State',
        labels={'count': 'Injuries', 'state_code': 'State'}
    )

    fig.update_layout(
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        height=500
    )

    return fig


def create_naics_bar_chart(df):
    """Top industries by injury count."""
    by_naics = df.groupby('Primary NAICS').size().reset_index(name='count')
    by_naics = by_naics.nlargest(15, 'count')

    # Map NAICS codes to industry names
    by_naics['industry'] = by_naics['Primary NAICS'].apply(
        lambda x: NAICS_LOOKUP.get(str(x), f'NAICS {x}')
    )

    fig = px.bar(
        by_naics,
        x='count',
        y='industry',
        orientation='h',
        title='Top 15 Industries by Injury Count',
        labels={'count': 'Injuries', 'industry': ''},
        color='count',
        color_continuous_scale='Blues'
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=500,
        showlegend=False
    )

    return fig


def create_body_part_chart(df):
    """Treemap of injuries by body part."""
    by_part = df.groupby('Part of Body Title').size().reset_index(name='count')
    by_part = by_part[by_part['Part of Body Title'].notna()]
    by_part = by_part.nlargest(15, 'count')

    fig = px.treemap(
        by_part,
        path=['Part of Body Title'],
        values='count',
        title='Injuries by Body Part',
        color='count',
        color_continuous_scale='Blues'
    )

    fig.update_layout(height=400)

    return fig


def create_injury_type_pie(df):
    """Donut chart of injury types."""
    by_type = df.groupby('NatureTitle').size().reset_index(name='count')
    by_type = by_type[by_type['NatureTitle'].notna()]
    by_type = by_type.nlargest(8, 'count')

    fig = px.pie(
        by_type,
        values='count',
        names='NatureTitle',
        title='Injury Types Distribution',
        hole=0.4
    )

    fig.update_layout(height=400)

    return fig


def create_event_bar_chart(df):
    """Horizontal bar chart of injury mechanisms/events."""
    by_event = df.groupby('EventTitle').size().reset_index(name='count')
    by_event = by_event[by_event['EventTitle'].notna()]
    by_event = by_event.nlargest(10, 'count')

    fig = px.bar(
        by_event,
        x='count',
        y='EventTitle',
        orientation='h',
        title='Top 10 Injury Mechanisms',
        labels={'count': 'Injuries', 'EventTitle': ''},
        color='count',
        color_continuous_scale='Oranges'
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=400,
        showlegend=False
    )

    return fig
