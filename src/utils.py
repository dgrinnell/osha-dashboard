"""Utility functions and lookup tables."""

# State name to abbreviation mapping
STATE_ABBREV = {
    'ALABAMA': 'AL', 'ALASKA': 'AK', 'ARIZONA': 'AZ', 'ARKANSAS': 'AR',
    'CALIFORNIA': 'CA', 'COLORADO': 'CO', 'CONNECTICUT': 'CT',
    'DELAWARE': 'DE', 'FLORIDA': 'FL', 'GEORGIA': 'GA', 'HAWAII': 'HI',
    'IDAHO': 'ID', 'ILLINOIS': 'IL', 'INDIANA': 'IN', 'IOWA': 'IA',
    'KANSAS': 'KS', 'KENTUCKY': 'KY', 'LOUISIANA': 'LA', 'MAINE': 'ME',
    'MARYLAND': 'MD', 'MASSACHUSETTS': 'MA', 'MICHIGAN': 'MI',
    'MINNESOTA': 'MN', 'MISSISSIPPI': 'MS', 'MISSOURI': 'MO',
    'MONTANA': 'MT', 'NEBRASKA': 'NE', 'NEVADA': 'NV',
    'NEW HAMPSHIRE': 'NH', 'NEW JERSEY': 'NJ', 'NEW MEXICO': 'NM',
    'NEW YORK': 'NY', 'NORTH CAROLINA': 'NC', 'NORTH DAKOTA': 'ND',
    'OHIO': 'OH', 'OKLAHOMA': 'OK', 'OREGON': 'OR', 'PENNSYLVANIA': 'PA',
    'RHODE ISLAND': 'RI', 'SOUTH CAROLINA': 'SC', 'SOUTH DAKOTA': 'SD',
    'TENNESSEE': 'TN', 'TEXAS': 'TX', 'UTAH': 'UT', 'VERMONT': 'VT',
    'VIRGINIA': 'VA', 'WASHINGTON': 'WA', 'WEST VIRGINIA': 'WV',
    'WISCONSIN': 'WI', 'WYOMING': 'WY', 'DISTRICT OF COLUMBIA': 'DC',
    'PUERTO RICO': 'PR', 'VIRGIN ISLANDS': 'VI', 'GUAM': 'GU'
}

# Common NAICS codes to industry names
NAICS_LOOKUP = {
    '622110': 'Hospitals',
    '491110': 'Postal Service',
    '445110': 'Grocery Stores',
    '236220': 'Commercial Construction',
    '493110': 'Warehousing',
    '213112': 'Oil/Gas Support',
    '238210': 'Electrical Contractors',
    '238160': 'Roofing Contractors',
    '237310': 'Highway Construction',
    '238220': 'Plumbing/HVAC',
    '561730': 'Landscaping',
    '484121': 'Trucking (Long-Distance)',
    '484110': 'Trucking (General)',
    '492110': 'Couriers/Messengers',
    '311615': 'Poultry Processing',
    '326199': 'Plastics Manufacturing',
    '332710': 'Machine Shops',
    '321999': 'Wood Products',
    '238910': 'Site Preparation',
    '236115': 'Single-Family Construction',
    '236116': 'Multi-Family Construction',
    '238350': 'Finish Carpentry',
    '238310': 'Drywall/Insulation',
    '238320': 'Painting Contractors',
    '722511': 'Full-Service Restaurants',
    '722513': 'Limited-Service Restaurants',
    '311611': 'Meat Processing',
    '311612': 'Meat Rendering',
    '423110': 'Auto Wholesalers',
    '441110': 'New Car Dealers',
    '441120': 'Used Car Dealers',
    '444110': 'Home Centers',
    '444120': 'Paint/Wallpaper Stores',
    '452210': 'Department Stores',
    '452311': 'Warehouse Clubs',
    '454110': 'Mail-Order Houses',
    '531110': 'Lessors - Residential',
    '531120': 'Lessors - Commercial',
    '541330': 'Engineering Services',
    '561320': 'Temporary Help Services',
    '561720': 'Janitorial Services',
    '562111': 'Solid Waste Collection',
    '562119': 'Other Waste Collection',
    '621111': 'Physician Offices',
    '623110': 'Nursing Care Facilities',
    '623210': 'Residential Mental Health',
    '624120': 'Services for Elderly/Disabled',
    '713940': 'Fitness Centers',
    '721110': 'Hotels/Motels',
    '811111': 'Auto Repair (General)',
    '811121': 'Auto Body Repair',
}


def get_industry_name(naics_code):
    """Get industry name from NAICS code."""
    return NAICS_LOOKUP.get(str(naics_code), f'NAICS {naics_code}')


def get_state_abbrev(state_name):
    """Get state abbreviation from full name."""
    if state_name:
        return STATE_ABBREV.get(state_name.upper(), state_name)
    return None
