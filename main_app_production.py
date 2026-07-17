#!/usr/bin/env python3
"""
PermitAI - Production Main Application
Optimized and ready for deployment
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

import streamlit as st

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import configuration and modules
try:
    from config.settings import get_settings
    from config.logging_config import setup_logging
    setup_logging()
    settings = get_settings()
    logger.info(f"PermitAI {settings.APP_VERSION} started in {settings.ENVIRONMENT} mode")
except Exception as e:
    logger.error(f"Configuration error: {e}")
    st.error("Failed to load configuration")
    st.stop()

# ============================================================================
# STREAMLIT CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="PermitAI",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/unfading17/fuzzy-goggles",
        "Report a bug": "https://github.com/unfading17/fuzzy-goggles/issues",
        "About": f"PermitAI v{settings.APP_VERSION} - AI Permit Review System"
    }
)

# Professional Styling
st.markdown("""
    <style>
    :root {
        --primary: #2563eb;
        --secondary: #38bdf8;
        --bg: #020617;
        --card-bg: rgba(15, 23, 42, 0.92);
        --text: #f8fafc;
        --muted: #cbd5e1;
    }
    
    * { box-sizing: border-box; }
    
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    .stApp {
        background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #111827 100%);
        color: var(--text);
    }
    
    .title-banner {
        background: linear-gradient(90deg, #0f172a 0%, #1d4ed8 45%, #38bdf8 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(14, 116, 144, 0.2);
    }
    
    .title-banner h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #2563eb 0%, #38bdf8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        filter: brightness(1.1) !important;
        transform: translateY(-2px) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# STATE INITIALIZATION
# ============================================================================

def initialize_state():
    """Initialize session state."""
    state_defaults = {
        "projects": [],
        "current_project": None,
        "user_type": "General Contractor",
        "review_history": [],
        "app_version": settings.APP_VERSION,
    }
    
    for key, value in state_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    return st.session_state

state = initialize_state()

# ============================================================================
# MAIN INTERFACE
# ============================================================================

def main():
    """Main application interface."""
    
    # Header
    st.markdown("""
        <div class='title-banner'>
            <h1>📋 PermitAI</h1>
            <p>AI-assisted permit readiness review for construction projects</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Projects", len(state.projects))
    with col2:
        st.metric("Reviews Completed", len(state.review_history))
    with col3:
        st.metric("App Version", settings.APP_VERSION)
    
    # Main Content
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📝 New Project", "📊 Dashboard", "⚙️ Settings", "ℹ️ Help"]
    )
    
    with tab1:
        st.header("Create New Project")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            project_name = st.text_input("Project Name *", key="proj_name")
            address = st.text_input("Address", key="address")
            city = st.text_input("City", key="city")
        
        with col2:
            county = st.text_input("County", key="county")
            state_input = st.text_input("State", value="FL", key="state")
            construction_type = st.selectbox(
                "Construction Type",
                ["Residential", "Commercial", "Industrial", "Mixed", "Other"]
            )
        
        with col3:
            area = st.number_input("Area (sqft)", min_value=0, key="area")
            floors = st.number_input("Number of Floors", min_value=1, max_value=200, value=1, key="floors")
            st.session_state.user_type = st.selectbox(
                "User Type",
                ["General Contractor", "Architect", "Engineer", "Developer", "Other"]
            )
        
        if st.button("✅ Create Project", use_container_width=True):
            if not project_name:
                st.error("Please enter a project name")
            else:
                project = {
                    "id": len(state.projects) + 1,
                    "nombre": project_name,
                    "direccion": address,
                    "ciudad": city,
                    "condado": county,
                    "estado": state_input,
                    "tipo_construccion": construction_type,
                    "metros": area,
                    "numero_pisos": floors,
                    "created_at": datetime.now().isoformat(),
                    "documentos": [],
                    "findings": [],
                }
                state.projects.append(project)
                st.session_state.projects = state.projects
                st.success(f"✅ Project '{project_name}' created successfully!")
                logger.info(f"Project created: {project_name}")
                st.rerun()
    
    with tab2:
        st.header("Dashboard")
        if state.projects:
            for i, project in enumerate(state.projects):
                with st.expander(f"📂 {project['nombre']} - {project['ciudad']}, {project['estado']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Type:** {project['tipo_construccion']}")
                        st.write(f"**Area:** {project['metros']} sqft")
                        st.write(f"**Floors:** {project['numero_pisos']}")
                    with col2:
                        st.write(f"**Created:** {project['created_at'][:10]}")
                        st.write(f"**Documents:** {len(project['documentos'])}")
                        st.write(f"**Findings:** {len(project['findings'])}")
        else:
            st.info("No projects yet. Create one in the 'New Project' tab.")
    
    with tab3:
        st.header("Settings")
        st.write(f"**Application Version:** {settings.APP_VERSION}")
        st.write(f"**Environment:** {settings.ENVIRONMENT}")
        st.write(f"**Max Upload Size:** {settings.MAX_UPLOAD_MB} MB")
        st.write(f"**Supported Formats:** {', '.join(settings.SUPPORTED_FORMATS)}")
    
    with tab4:
        st.header("Help & Documentation")
        st.markdown("""
        ### Getting Started
        1. Create a new project with your basic information
        2. Upload construction documents (PDF, images)
        3. Run analysis to get AI-powered findings
        4. Review findings and export reports
        
        ### Features
        - 📄 Document analysis and OCR
        - 🤖 AI-powered code compliance checking
        - 📊 Risk assessment and probability calculation
        - 📋 Professional report generation
        - 💾 Local storage of all data
        
        ### Support
        - 📧 Email: support@permitai.com
        - 🐛 Report bugs: https://github.com/unfading17/fuzzy-goggles/issues
        - 📖 Documentation: https://github.com/unfading17/fuzzy-goggles
        """)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"PermitAI v{settings.APP_VERSION}")
    with col2:
        st.caption("Made with ❤️ for construction professionals")
    with col3:
        st.caption(f"Environment: {settings.ENVIRONMENT}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"Application error: {str(e)[:200]}")
