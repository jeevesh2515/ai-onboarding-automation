# app.py
import streamlit as st
import os
import logging
import time
logging.basicConfig(filename='app.log', level=logging.ERROR)

from dotenv import load_dotenv
import os

load_dotenv()
# 👉 Add your OpenAI API key to the .env file as OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # <-- Your OpenAI API key is loaded here

from src.scraper.company_scraper import CompanyDataScraper
from src.analyzer.business_analyzer import BusinessAnalyzer, BusinessInsights
from src.analyzer.project_estimator import ProjectEstimator
from src.generator.proposal_generator import ProposalGenerator
from src.utils.helpers import clean_text, format_currency, validate_url

# Page configuration
st.set_page_config(
    page_title="AI Client Onboarding Automation",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 2rem;
        border-radius: 10px;
    }
    .step-container {
        border: 2px solid #e0e0e0;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        background: white;
    }
    .step-header {
        color: #667eea;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    .insight-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .success-message {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI-Driven Client Onboarding Automation</h1>
        <p>Transform any company URL into a complete onboarding package in minutes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'company_data' not in st.session_state:
        st.session_state.company_data = None
    if 'business_insights' not in st.session_state:
        st.session_state.business_insights = None
    if 'project_estimate' not in st.session_state:
        st.session_state.project_estimate = None
    if 'proposal' not in st.session_state:
        st.session_state.proposal = None
    
    # Step 1: URL Input
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-header">Step 1: Enter Company Website</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        company_url = st.text_input(
            "Company Website URL",
            placeholder="https://example.com",
            key="company_url"
        )
    
    with col2:
        analyze_button = st.button("🔍 Analyze", type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 2: Company Analysis
    if analyze_button and company_url:
        with st.spinner("🕵️ Analyzing company website..."):
            scraper = CompanyDataScraper()
            st.session_state.company_data = scraper.scrape_company_basics(company_url)
            
        if 'error' not in st.session_state.company_data:
            st.markdown('<div class="success-message">✅ Company analysis completed!</div>', 
                       unsafe_allow_html=True)
    
    # Display company analysis results
    if st.session_state.company_data and 'error' not in st.session_state.company_data:
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        st.markdown('<div class="step-header">Step 2: Company Intelligence</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown("**🏢 Company Name**")
            st.write(st.session_state.company_data.get('company_name', 'Unknown'))
            st.markdown("**🏭 Industry**")
            st.write(st.session_state.company_data.get('industry', 'Unknown'))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown("**⚙️ Tech Stack**")
            tech_stack = st.session_state.company_data.get('tech_stack', [])
            if tech_stack:
                for tech in tech_stack[:5]:
                    st.write(f"• {tech}")
            else:
                st.write("Standard web technologies")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown("**🎯 Services**")
            services = st.session_state.company_data.get('services', [])
            if services:
                for service in services[:5]:
                    st.write(f"• {service}")
            else:
                st.write("Service information not found")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Business Insights Generation
        if st.button("🧠 Generate Business Insights", type="primary"):
            with st.spinner("🤖 AI is analyzing business needs..."):
                analyzer = BusinessAnalyzer(os.getenv('OPENAI_API_KEY'))
                st.session_state.business_insights = analyzer.analyze_business_needs(
                    st.session_state.company_data
                )
                
                estimator = ProjectEstimator()
                st.session_state.project_estimate = estimator.estimate_project_scope(
                    st.session_state.business_insights,
                    st.session_state.company_data
                )
            
            st.markdown('<div class="success-message">✅ Business insights generated!</div>', 
                       unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display business insights
    if st.session_state.business_insights:
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        st.markdown('<div class="step-header">Step 3: Business Intelligence</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown("**🎯 Target Audience**")
            for audience in st.session_state.business_insights.target_audience:
                st.write(f"• {audience}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown("**⚡ Pain Points**")
            for pain in st.session_state.business_insights.pain_points:
                st.write(f"• {pain}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown("**🚀 Opportunities**")
            for opp in st.session_state.business_insights.opportunities:
                st.write(f"• {opp}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="insight-card">', unsafe_allow_html=True)
            st.markdown("**💡 Project Recommendations**")
            for rec in st.session_state.business_insights.project_recommendations:
                st.write(f"• {rec}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display project estimate
    if st.session_state.project_estimate:
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        st.markdown('<div class="step-header">Step 4: Project Estimation</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if (
                "project_estimate" in st.session_state
                and st.session_state.project_estimate
                and "estimated_cost" in st.session_state.project_estimate
            ):
                st.metric(
                    "💰 Total Investment",
                    f"${st.session_state.project_estimate['estimated_cost']:,}"
                )
            else:
                st.warning("Project estimate not available.")
        
        with col2:
            if (
                "project_estimate" in st.session_state
                and st.session_state.project_estimate
                and "timeline_weeks" in st.session_state.project_estimate
            ):
                st.metric(
                    "⏱️ Timeline",
                    f"{st.session_state.project_estimate['timeline_weeks']} weeks"
                )
            else:
                st.warning("Project timeline not available.")
        
        with col3:
            if (
                "project_estimate" in st.session_state
                and st.session_state.project_estimate
                and "total_hours" in st.session_state.project_estimate
            ):
                st.metric(
                    "👥 Total Hours",
                    f"{st.session_state.project_estimate['total_hours']} hrs"
                )
            else:
                st.warning("Project total hours not available.")
        
        # Phase breakdown
        st.markdown("**📋 Phase Breakdown**")
        if (
            "project_estimate" in st.session_state
            and st.session_state.project_estimate
            and "phase_breakdown" in st.session_state.project_estimate
        ):
            phase_data = st.session_state.project_estimate['phase_breakdown']
            for phase, hours in phase_data.items():
                st.write(f"• {phase.replace('_', ' ').title()}: {hours} hours")
        else:
            st.warning("Project phase breakdown not available.")
        
        # Generate Proposal Button
        if st.button("📄 Generate Complete Proposal", type="primary"):
            with st.spinner("📝 Creating your customized proposal..."):
                generator = ProposalGenerator()
                st.session_state.proposal = generator.generate_proposal(
                    st.session_state.company_data,
                    st.session_state.business_insights,
                    st.session_state.project_estimate
                )
            
            st.markdown('<div class="success-message">✅ Proposal generated successfully!</div>', 
                       unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display generated proposal
    if st.session_state.proposal:
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        st.markdown('<div class="step-header">Step 5: Generated Proposal</div>', unsafe_allow_html=True)
        
        # Display HTML proposal
        st.markdown("**📱 Interactive Proposal Preview**")
        if (
            "proposal" in st.session_state
            and st.session_state.proposal
            and "html_content" in st.session_state.proposal
        ):
            html_bytes = st.session_state.proposal["html_content"].encode("utf-8")
            company_key = st.session_state.company_data['company_name'].replace(' ', '_') if "company_data" in st.session_state else "default"
            unique_key = f"download_html_{company_key}_{int(time.time()*1000)}"  # adds a timestamp for uniqueness

            st.download_button(
                label="💾 Download HTML Version",
                data=html_bytes,
                file_name=f"proposal_{company_key}.html",
                mime="text/html",
                key=unique_key
            )
        else:
            st.warning("Proposal HTML content not available.")
        
        # Download links
        col1, col2 = st.columns(2)
        with col1:
            if (
                "proposal" in st.session_state
                and st.session_state.proposal
                and "pdf_path" in st.session_state.proposal
                and os.path.exists(st.session_state.proposal["pdf_path"])
            ):
                with open(st.session_state.proposal["pdf_path"], "rb") as f:
                    st.download_button(
                        label="Download Proposal PDF",
                        data=f,
                        file_name=os.path.basename(st.session_state.proposal["pdf_path"]),
                        mime="application/pdf",
                        key="download_pdf"
                    )
            else:
                st.warning("Proposal PDF not available.")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
