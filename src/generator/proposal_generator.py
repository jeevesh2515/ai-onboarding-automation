# src/generator/proposal_generator.py
from jinja2 import Environment, FileSystemLoader
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
import os
from typing import Dict
from src.analyzer.business_analyzer import BusinessInsights
import logging

class ProposalGeneratorError(Exception):
    pass

class ProposalGenerator:
    def __init__(self, templates_dir: str = "templates"):
        self.styles = getSampleStyleSheet()
        
    def generate_proposal(self, company_data: Dict, business_insights: BusinessInsights, project_estimate: Dict) -> Dict:
        """Generate a comprehensive project proposal"""
        try:
            if not company_data or not business_insights or not project_estimate:
                raise ProposalGeneratorError("Missing required data for proposal generation.")
            
            proposal_data = {
                'company_name': company_data.get('company_name', 'Valued Client'),
                'date': datetime.now().strftime('%B %d, %Y'),
                'industry': company_data.get('industry', 'Technology'),
                'insights': business_insights,
                'estimate': project_estimate,
            }
            
            # Generate HTML version
            html_proposal = self._generate_html_proposal(proposal_data)
            
            # Generate PDF version
            pdf_path = self._generate_pdf_proposal(proposal_data)
            
            return {
                'html_content': html_proposal,
                'pdf_path': pdf_path,
                'proposal_data': proposal_data
            }
        except ProposalGeneratorError as e:
            logging.error(f"ProposalGenerator error: {e}")
            return {"error": str(e)}
        except Exception as e:
            logging.error(f"Unexpected error in ProposalGenerator: {e}")
            return {"error": "Failed to generate proposal."}
    
    def _generate_html_proposal(self, data: Dict) -> str:
        company_name = data.get("company_name", "N/A")
        industry = data.get("industry", "N/A")
        estimate = data.get("estimate", {})
        estimated_cost = estimate.get("estimated_cost", "N/A")
        timeline_weeks = estimate.get("timeline_weeks", "N/A")
        total_hours = estimate.get("total_hours", "N/A")
        phase_breakdown = estimate.get("phase_breakdown", {})

        html_content = f"""
        <html>
        <head>
            <title>Proposal for {company_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2E86C1; }}
                .section {{ margin-bottom: 32px; }}
                .phases-table {{ border-collapse: collapse; width: 60%; }}
                .phases-table th, .phases-table td {{ border: 1px solid #ddd; padding: 8px; }}
                .phases-table th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Proposal for {company_name}</h1>
            <div class="section">
                <strong>Industry:</strong> {industry}<br>
                <strong>Estimated Cost:</strong> ${estimated_cost}<br>
                <strong>Timeline:</strong> {timeline_weeks} weeks<br>
                <strong>Total Hours:</strong> {total_hours} hrs
            </div>
            <div class="section">
                <h2>Project Phases</h2>
                <table class="phases-table">
                    <tr>
                        <th>Phase</th>
                        <th>Hours</th>
                    </tr>
                    {''.join(f'<tr><td>{phase}</td><td>{hours}</td></tr>' for phase, hours in phase_breakdown.items())}
                </table>
            </div>
        </body>
        </html>
        """
        return html_content
    
    def _generate_pdf_proposal(self, data: Dict) -> str:
        """Create PDF version of the proposal"""
        filename = f"proposal_{data['company_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        filepath = os.path.join('generated_proposals', filename)
        os.makedirs('generated_proposals', exist_ok=True)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#2C3E50')
        )
        story.append(Paragraph(f"Project Proposal for {data['company_name']}", title_style))
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['Heading2']))
        summary_text = f"""
        Based on our analysis of {data['company_name']}, we've identified key opportunities 
        to enhance your digital presence and drive business growth. This proposal outlines 
        a strategic approach to address your specific needs in the {data['industry']} industry.
        """
        story.append(Paragraph(summary_text, self.styles['Normal']))
        story.append(Spacer(1, 15))
        
        # Project Overview Table
        estimate = data.get('estimate', {})
        project_data = [
            ['Timeline', f"{estimate.get('timeline_weeks', 'N/A')} weeks"],
            ['Total Investment', f"${estimate.get('estimated_cost', 'N/A')}"],
            ['Total Hours', f"{estimate.get('total_hours', 'N/A')} hours"]
        ]
        table = Table(project_data, colWidths=[200, 300])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Build PDF
        doc.build(story)
        return filepath
