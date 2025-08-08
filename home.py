import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from io import BytesIO
import json

# Page configuration
st.set_page_config(
    page_title="ASEAN-DIWA Dashboard",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with women-focused color scheme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #e91e63 0%, #ad1457 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(233, 30, 99, 0.3);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(233, 30, 99, 0.1);
        text-align: center;
        border-top: 3px solid #e91e63;
    }
    .country-card {
        background: #fce4ec;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #e91e63;
        margin-bottom: 1rem;
    }
    .indicator-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(233, 30, 99, 0.05);
        border-left: 4px solid #f8bbd9;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #fce4ec;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #e91e63, #ad1457);
        color: white;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ad1457, #880e4f);
        box-shadow: 0 4px 8px rgba(233, 30, 99, 0.3);
        transform: translateY(-2px);
    }
    
    /* Selectbox and other input styling */
    .stSelectbox > div > div {
        border-color: #e91e63;
    }
    
    /* Metric value styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #fce4ec, #f8bbd9);
        border: 1px solid #e91e63;
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data
@st.cache_data
def generate_sample_data():
    countries = ['Brunei', 'Cambodia', 'Indonesia', 'Laos', 'Malaysia', 'Myanmar', 
                'Philippines', 'Singapore', 'Thailand', 'Vietnam', 'Papua New Guinea', 'Timor-Leste']
    
    years = [2018, 2019, 2020, 2021, 2022, 2023]
    
    indicators = {
        'Internet Usage (%)': {'male': (60, 95), 'female': (55, 92), 'all': (57, 93)},
        'Mobile Phone Ownership (%)': {'male': (70, 98), 'female': (65, 96), 'all': (67, 97)},
        'Digital Literacy (%)': {'male': (45, 85), 'female': (40, 82), 'all': (42, 83)},
        'ICT Employment (%)': {'male': (15, 35), 'female': (10, 30), 'all': (12, 32)},
        'Online Shopping (%)': {'male': (30, 70), 'female': (35, 75), 'all': (32, 72)},
        'Digital Banking (%)': {'male': (25, 80), 'female': (20, 78), 'all': (22, 79)}
    }
    
    data = []
    for country in countries:
        for year in years:
            for indicator, ranges in indicators.items():
                for gender in ['male', 'female', 'all']:
                    min_val, max_val = ranges[gender]
                    # Add some country-specific variations
                    if country == 'Singapore':
                        value = np.random.uniform(max_val - 10, max_val)
                    elif country in ['Cambodia', 'Laos', 'Myanmar']:
                        value = np.random.uniform(min_val, min_val + 20)
                    else:
                        value = np.random.uniform(min_val, max_val)
                    
                    data.append({
                        'Country': country,
                        'Year': year,
                        'Indicator': indicator,
                        'Gender': gender,
                        'Value': round(value, 1)
                    })
    
    return pd.DataFrame(data)

# Country coordinates for map
@st.cache_data
def get_country_coordinates():
    return {
        'Brunei': {'lat': 4.5353, 'lon': 114.7277},
        'Cambodia': {'lat': 12.5657, 'lon': 104.9910},
        'Indonesia': {'lat': -0.7893, 'lon': 113.9213},
        'Laos': {'lat': 19.8563, 'lon': 102.4955},
        'Malaysia': {'lat': 4.2105, 'lon': 101.9758},
        'Myanmar': {'lat': 21.9162, 'lon': 95.9560},
        'Philippines': {'lat': 12.8797, 'lon': 121.7740},
        'Singapore': {'lat': 1.3521, 'lon': 103.8198},
        'Thailand': {'lat': 15.8700, 'lon': 100.9925},
        'Vietnam': {'lat': 14.0583, 'lon': 108.2772},
        'Papua New Guinea': {'lat': -6.3150, 'lon': 143.9555},
        'Timor-Leste': {'lat': -8.8742, 'lon': 125.7275}
    }

# Initialize data
df = generate_sample_data()
country_coords = get_country_coordinates()

# Sidebar navigation
st.sidebar.title("🌏 ASEAN-DIWA")
st.sidebar.markdown("Digital Inclusion for Women in ASEAN")

st.sidebar.markdown("---")

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

# Navigation buttons
st.sidebar.subheader("📋 Navigation")

if st.sidebar.button("🏠 Dashboard", use_container_width=True):
    st.session_state.current_page = "Dashboard"
    
if st.sidebar.button("🗺️ ASEAN Map", use_container_width=True):
    st.session_state.current_page = "ASEAN Map"
    
if st.sidebar.button("📊 Country Profiles", use_container_width=True):
    st.session_state.current_page = "Country Profiles"
    
if st.sidebar.button("📈 Comparison", use_container_width=True):
    st.session_state.current_page = "Comparison"
    
if st.sidebar.button("ℹ️ About", use_container_width=True):
    st.session_state.current_page = "About"

page = st.session_state.current_page

# Dashboard Page
if page == "Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>ASEAN Digital Inclusion for Women Alliance (DIWA)</h1>
        <p>Bridging the Digital Gender Gap in Southeast Asia</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Project Brief
    with st.expander("📋 Project Brief", expanded=True):
        st.markdown("""
        **ASEAN-DIWA** is a comprehensive initiative aimed at promoting digital inclusion and reducing 
        the digital gender gap across ASEAN member states and partner countries. Our mission is to:
        
        - 📊 **Monitor** digital gender disparities through data-driven insights
        - 🎯 **Identify** key areas requiring targeted interventions
        - 🤝 **Collaborate** with stakeholders to implement inclusive digital policies
        - 📈 **Track** progress towards achieving digital equality
        
        This dashboard provides interactive visualizations and country-specific analysis to support 
        evidence-based decision making for digital inclusion initiatives.
        """)
    
    # Key Metrics Overview
    st.subheader("📊 Key Indicators Overview")
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_year = st.selectbox("Select Year:", sorted(df['Year'].unique(), reverse=True))
    with col2:
        selected_gender = st.selectbox("View by Gender:", ['all', 'female', 'male'])
    with col3:
        selected_countries = st.multiselect("Select Countries:", 
                                          options=df['Country'].unique(),
                                          default=df['Country'].unique()[:6])
    
    # Filter data
    filtered_data = df[
        (df['Year'] == selected_year) & 
        (df['Gender'] == selected_gender) & 
        (df['Country'].isin(selected_countries))
    ]
    
    # Create metrics cards
    indicators = df['Indicator'].unique()
    
    # Display metrics in a grid
    cols = st.columns(3)
    for i, indicator in enumerate(indicators):
        with cols[i % 3]:
            indicator_data = filtered_data[filtered_data['Indicator'] == indicator]
            avg_value = indicator_data['Value'].mean()
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>{indicator}</h3>
                <h2 style="color: #e91e63;">{avg_value:.1f}%</h2>
                <p>Average across selected countries</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Interactive Charts
    st.subheader("📈 Interactive Visualizations")
    
    tab1, tab2, tab3 = st.tabs(["📊 By Indicator", "🌍 By Country", "📅 Trends"])
    
    with tab1:
        selected_indicator = st.selectbox("Choose Indicator:", indicators)
        
        chart_data = filtered_data[filtered_data['Indicator'] == selected_indicator]
        
        if not chart_data.empty:
            fig = px.bar(chart_data, x='Country', y='Value', 
                        title=f'{selected_indicator} - {selected_gender.title()} ({selected_year})',
                        color='Value', color_continuous_scale='Reds')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Download button
            if st.button("📥 Download Chart Data"):
                csv = chart_data.to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name=f'{selected_indicator}_{selected_year}_{selected_gender}.csv',
                    mime='text/csv'
                )
    
    with tab2:
        country_summary = filtered_data.groupby('Country')['Value'].mean().reset_index()
        country_summary = country_summary.sort_values('Value', ascending=False)
        
        fig = px.bar(country_summary, x='Country', y='Value',
                    title=f'Average Digital Inclusion Score by Country ({selected_year})',
                    color='Value', color_continuous_scale='Pinkyl')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        trend_data = df[
            (df['Gender'] == selected_gender) & 
            (df['Country'].isin(selected_countries))
        ].groupby(['Year', 'Indicator'])['Value'].mean().reset_index()
        
        fig = px.line(trend_data, x='Year', y='Value', color='Indicator',
                     title=f'Trends Over Time - {selected_gender.title()}',
                     color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Navigation Guide
    st.subheader("🧭 Explore More")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="indicator-section">
            <h4>🗺️ Interactive Map</h4>
            <p>Explore geographical patterns of digital inclusion across ASEAN countries with our interactive choropleth maps.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Visit ASEAN Map", key="map_btn"):
            st.session_state.current_page = "ASEAN Map"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="indicator-section">
            <h4>📊 Country Profiles</h4>
            <p>Dive deep into individual country analysis with detailed breakdowns and downloadable reports.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Country Profiles", key="profile_btn"):
            st.session_state.current_page = "Country Profiles"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="indicator-section">
            <h4>📈 Compare Countries</h4>
            <p>Create side-by-side comparisons between countries with customizable charts and rankings.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Compare Countries", key="compare_btn"):
            st.session_state.current_page = "Comparison"
            st.rerun()

# ASEAN Map Page
elif page == "ASEAN Map":
    st.title("🗺️ ASEAN Interactive Map")
    st.markdown("Explore digital inclusion indicators across ASEAN countries")
    
    # Map controls
    col1, col2, col3 = st.columns(3)
    with col1:
        map_indicator = st.selectbox("Select Indicator for Map:", df['Indicator'].unique())
    with col2:
        map_year = st.selectbox("Select Year:", sorted(df['Year'].unique(), reverse=True))
    with col3:
        map_gender = st.selectbox("View by Gender:", ['all', 'female', 'male'], key='map_gender')
    
    # Prepare map data
    map_data = df[
        (df['Indicator'] == map_indicator) & 
        (df['Year'] == map_year) & 
        (df['Gender'] == map_gender)
    ].copy()
    
    # Add coordinates
    map_data['lat'] = map_data['Country'].map(lambda x: country_coords[x]['lat'])
    map_data['lon'] = map_data['Country'].map(lambda x: country_coords[x]['lon'])
    
    # Create choropleth-style scatter map
    fig = px.scatter_geo(
        map_data, 
        lat='lat', 
        lon='lon',
        color='Value',
        size='Value',
        hover_name='Country',
        hover_data={'Value': ':.1f', 'Indicator': True, 'lat': False, 'lon': False},
        color_continuous_scale='Reds',
        title=f'{map_indicator} - {map_gender.title()} ({map_year})',
        size_max=50
    )
    
    fig.update_layout(
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='lightgray',
            showcountries=True,
            countrycolor='white',
            showocean=True,
            oceancolor='lightblue',
            center=dict(lat=10, lon=115),  # Center on ASEAN region
            projection_scale=3
        ),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Country comparison section
    st.subheader("🔄 Quick Country Comparison")
    
    col1, col2 = st.columns(2)
    with col1:
        country1 = st.selectbox("Select First Country:", map_data['Country'].unique())
    with col2:
        country2 = st.selectbox("Select Second Country:", 
                               [c for c in map_data['Country'].unique() if c != country1])
    
    if country1 and country2:
        comp_data = map_data[map_data['Country'].isin([country1, country2])]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            val1 = comp_data[comp_data['Country'] == country1]['Value'].iloc[0]
            st.metric(country1, f"{val1:.1f}%")
        
        with col2:
            val2 = comp_data[comp_data['Country'] == country2]['Value'].iloc[0]
            diff = val2 - val1
            st.metric(country2, f"{val2:.1f}%", f"{diff:+.1f}%")
        
        with col3:
            st.markdown(f"**Gap:** {abs(diff):.1f} percentage points")

# Country Profiles Page
elif page == "Country Profiles":
    st.title("📊 Country Profiles")
    st.markdown("Detailed analysis for each ASEAN country")
    
    # Country selection
    countries = sorted(df['Country'].unique())
    
    # Create country grid
    cols = st.columns(4)
    selected_country = None
    
    for i, country in enumerate(countries):
        with cols[i % 4]:
            if st.button(f"🏴 {country}", key=f"country_{i}", use_container_width=True):
                selected_country = country
    
    # Use session state to persist selection
    if 'selected_country' not in st.session_state:
        st.session_state.selected_country = countries[0]
    
    if selected_country:
        st.session_state.selected_country = selected_country
    
    country = st.session_state.selected_country
    
    st.markdown(f"## 📍 {country} Profile")
    
    # Country overview
    country_data = df[df['Country'] == country]
    
    # Latest year data
    latest_year = country_data['Year'].max()
    latest_data = country_data[country_data['Year'] == latest_year]
    
    # Overview metrics
    st.subheader("📊 Key Indicators Overview")
    
    gender_tabs = st.tabs(["👥 All", "👩 Female", "👨 Male"])
    
    for i, gender in enumerate(['all', 'female', 'male']):
        with gender_tabs[i]:
            gender_data = latest_data[latest_data['Gender'] == gender]
            
            cols = st.columns(3)
            for j, (_, row) in enumerate(gender_data.iterrows()):
                with cols[j % 3]:
                    st.metric(row['Indicator'], f"{row['Value']:.1f}%")
    
    # Trends analysis
    st.subheader("📈 Trends Over Time")
    
    trend_indicator = st.selectbox("Select Indicator for Trends:", 
                                  country_data['Indicator'].unique(),
                                  key="trend_indicator")
    
    trend_data = country_data[country_data['Indicator'] == trend_indicator]
    
    fig = px.line(trend_data, x='Year', y='Value', color='Gender',
                 title=f'{trend_indicator} Trends in {country}',
                 markers=True,
                 color_discrete_map={'male': '#1f77b4', 'female': '#e91e63', 'all': '#ff7f0e'})
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Country summary
    st.subheader("📝 Country Summary")
    
    # Generate summary based on data
    avg_all = latest_data[latest_data['Gender'] == 'all']['Value'].mean()
    gender_gap = (latest_data[latest_data['Gender'] == 'male']['Value'].mean() - 
                  latest_data[latest_data['Gender'] == 'female']['Value'].mean())
    
    summary_text = f"""
    **{country}** shows an average digital inclusion score of **{avg_all:.1f}%** across all indicators in {latest_year}.
    
    **Key Insights:**
    - Gender Gap: {abs(gender_gap):.1f} percentage points {'(male advantage)' if gender_gap > 0 else '(female advantage)'}
    - Strongest Indicator: {latest_data[latest_data['Gender'] == 'all'].nlargest(1, 'Value')['Indicator'].iloc[0]}
    - Area for Improvement: {latest_data[latest_data['Gender'] == 'all'].nsmallest(1, 'Value')['Indicator'].iloc[0]}
    
    **Recommendations:**
    - Focus on closing gender gaps in digital access and skills
    - Strengthen digital infrastructure and affordability
    - Promote inclusive digital policies and programs
    """
    
    st.markdown(summary_text)
    
    # Download section
    st.subheader("📥 Download Report")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Download PDF Report"):
            st.info("PDF download functionality would be implemented with additional libraries")
    
    with col2:
        if st.button("🖼️ Download PNG Chart"):
            st.info("PNG download functionality would be implemented with additional libraries")
    
    # Raw data download
    country_csv = country_data.to_csv(index=False)
    st.download_button(
        label="📊 Download Raw Data (CSV)",
        data=country_csv,
        file_name=f'{country}_digital_inclusion_data.csv',
        mime='text/csv'
    )

# Comparison Page
elif page == "Comparison":
    st.title("📈 Country Comparison")
    st.markdown("Compare digital inclusion indicators across countries")
    
    # Comparison controls
    col1, col2 = st.columns(2)
    
    with col1:
        comp_indicator = st.selectbox("Select Indicator:", df['Indicator'].unique())
        comp_year = st.selectbox("Select Year:", sorted(df['Year'].unique(), reverse=True))
    
    with col2:
        comp_countries = st.multiselect("Select Countries to Compare:", 
                                       df['Country'].unique(),
                                       default=df['Country'].unique()[:5])
        chart_type = st.selectbox("Chart Type:", ["Bar Chart", "Line Chart", "Radar Chart"])
    
    if comp_countries:
        # Filter data
        comp_data = df[
            (df['Indicator'] == comp_indicator) & 
            (df['Year'] == comp_year) & 
            (df['Country'].isin(comp_countries))
        ]
        
        # Create visualizations
        if chart_type == "Bar Chart":
            fig = px.bar(comp_data, x='Country', y='Value', color='Gender',
                        title=f'{comp_indicator} Comparison ({comp_year})',
                        barmode='group',
                        color_discrete_map={'male': '#1f77b4', 'female': '#e91e63', 'all': '#ff7f0e'})
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Line Chart":
            # Show trends for selected countries
            trend_data = df[
                (df['Indicator'] == comp_indicator) & 
                (df['Country'].isin(comp_countries)) &
                (df['Gender'] == 'all')  # Show all gender for clarity
            ]
            
            fig = px.line(trend_data, x='Year', y='Value', color='Country',
                         title=f'{comp_indicator} Trends Comparison',
                         markers=True,
                         color_discrete_sequence=px.colors.qualitative.Set1)
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Radar Chart":
            # Create radar chart for all indicators
            radar_data = df[
                (df['Year'] == comp_year) & 
                (df['Country'].isin(comp_countries)) &
                (df['Gender'] == 'all')
            ].pivot(index='Country', columns='Indicator', values='Value').reset_index()
            
            fig = go.Figure()
            
            indicators = [col for col in radar_data.columns if col != 'Country']
            
            for _, row in radar_data.iterrows():
                fig.add_trace(go.Scatterpolar(
                    r=[row[ind] for ind in indicators],
                    theta=indicators,
                    fill='toself',
                    name=row['Country']
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title=f"All Indicators Comparison ({comp_year})",
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Rankings
        st.subheader("🏆 Rankings")
        
        ranking_data = comp_data[comp_data['Gender'] == 'all'].sort_values('Value', ascending=False)
        ranking_data['Rank'] = range(1, len(ranking_data) + 1)
        
        st.dataframe(
            ranking_data[['Rank', 'Country', 'Value']].rename(columns={'Value': f'{comp_indicator} (%)'}),
            use_container_width=True
        )
        
        # Download options
        st.subheader("📥 Download Options")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Download Comparison Data"):
                csv = comp_data.to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name=f'comparison_{comp_indicator}_{comp_year}.csv',
                    mime='text/csv'
                )
        
        with col2:
            if st.button("📈 Download Chart"):
                st.info("Chart download functionality would be implemented with additional libraries")

# About Page
elif page == "About":
    st.title("ℹ️ About ASEAN-DIWA")
    
    st.markdown("""
    ## 🌟 Mission
    
    The ASEAN Digital Inclusion for Women Alliance (DIWA) is dedicated to bridging the digital gender gap 
    across Southeast Asia through data-driven insights, collaborative partnerships, and targeted interventions.
    
    ## 🎯 Objectives
    
    - **Data Collection & Analysis**: Comprehensive monitoring of digital inclusion indicators
    - **Policy Support**: Evidence-based recommendations for inclusive digital policies  
    - **Capacity Building**: Training and resources for stakeholders
    - **Regional Collaboration**: Facilitating knowledge sharing across ASEAN countries
    
    ## 📊 Key Indicators
    
    Our dashboard tracks six critical indicators of digital inclusion:
    
    1. **Internet Usage**: Percentage of population using the internet
    2. **Mobile Phone Ownership**: Access to mobile communication technology
    3. **Digital Literacy**: Skills and knowledge for effective digital participation
    4. **ICT Employment**: Participation in information and communication technology sectors
    5. **Online Shopping**: Engagement in digital commerce activities
    6. **Digital Banking**: Access and usage of digital financial services
    
    ## 🌍 Geographic Coverage
    
    - **ASEAN Member States**: Brunei, Cambodia, Indonesia, Laos, Malaysia, Myanmar, Philippines, Singapore, Thailand, Vietnam
    - **Partner Countries**: Papua New Guinea, Timor-Leste
    
    ## 📈 Data Sources
    
    *Note: This dashboard currently displays generated sample data for demonstration purposes. 
    In production, data would be sourced from:*
    
    - National statistical offices
    - ITU World Telecommunication/ICT Indicators Database
    - World Bank Development Indicators
    - GSMA Mobile Connectivity Index
    - Regional surveys and studies
    
    ## 🤝 Partners
    
    ASEAN-DIWA collaborates with various organizations including:
    
    - ASEAN Secretariat
    - UN Women
    - International Telecommunication Union (ITU)
    - World Bank
    - National governments and statistical offices
    - Civil society organizations
    
    ## 📞 Contact
    
    For more information about ASEAN-DIWA:
    
    - Email: info@asean-diwa.org
    - Website: www.asean-diwa.org
    - Follow us on social media for updates
    
    ---
    
    *This dashboard was developed to support evidence-based decision making for digital inclusion initiatives across the ASEAN region.*
    """)
    
    # Technical information
    with st.expander("🔧 Technical Information"):
        st.markdown("""
        **Dashboard Features:**
        - Interactive visualizations with Plotly
        - Multi-page navigation with persistent state
        - Data filtering and export capabilities
        - Responsive design for various screen sizes
        - Download functionality for reports and data
        
        **Built with:**
        - Streamlit for the web framework
        - Pandas for data manipulation
        - Plotly for interactive charts
        - NumPy for data generation
        
        **Browser Compatibility:**
        - Chrome, Firefox, Safari, Edge (latest versions)
        - Mobile-responsive design
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "© 2024 ASEAN-DIWA | Digital Inclusion for Women in ASEAN | "
    "Dashboard v1.0"
    "</div>", 
    unsafe_allow_html=True
)