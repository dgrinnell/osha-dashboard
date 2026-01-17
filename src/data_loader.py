"""Data loading module with caching for OSHA injury data."""

import streamlit as st
import pandas as pd
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


@st.cache_data(ttl=300)
def load_severe_injuries():
    """
    Load severe injury CSV with optimized dtypes.
    TTL of 300 seconds (5 min) ensures fresh data on auto-refresh.
    """
    dtype_map = {
        'ID': 'int32',
        'Employer': 'category',
        'City': 'category',
        'State': 'category',
        'Latitude': 'float32',
        'Longitude': 'float32',
        'Primary NAICS': 'category',
        'Hospitalized': 'float32',
        'Amputation': 'float32',
        'NatureTitle': 'category',
        'Part of Body Title': 'category',
        'EventTitle': 'category',
        'SourceTitle': 'category',
    }

    usecols = [
        'ID', 'EventDate', 'City', 'State', 'Latitude', 'Longitude',
        'Primary NAICS', 'Hospitalized', 'Amputation',
        'NatureTitle', 'Part of Body Title', 'EventTitle', 'SourceTitle',
        'Final Narrative'
    ]

    df = pd.read_csv(
        DATA_DIR / "severe_injuries.csv",
        dtype=dtype_map,
        usecols=usecols,
        low_memory=False
    )

    # Parse dates separately for better control
    df['EventDate'] = pd.to_datetime(df['EventDate'], format='%m/%d/%Y', errors='coerce')

    return df


@st.cache_data(ttl=300)
def load_fatalities():
    """Load fatality Excel data."""
    df = pd.read_excel(
        DATA_DIR / "fatalities.xlsx"
    )

    # Parse date columns
    if 'Event Date' in df.columns:
        df['Event Date'] = pd.to_datetime(df['Event Date'], errors='coerce')

    return df


def clean_data(df):
    """Clean and preprocess the injury data."""
    df = df.copy()

    # Strip whitespace from categorical columns
    for col in ['NatureTitle', 'Part of Body Title', 'State', 'City', 'EventTitle', 'SourceTitle']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace('nan', pd.NA)

    # Standardize state names to uppercase
    if 'State' in df.columns:
        df['State'] = df['State'].str.upper()

    # Fill NaN in numeric columns with 0
    for col in ['Hospitalized', 'Amputation']:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    return df
