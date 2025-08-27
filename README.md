# AI Client Onboarding Automation 🚀

This project automates client onboarding, business analysis, project estimation, and proposal generation using AI and Streamlit.

## Features

- Scrapes company data from a provided website URL
- Analyzes business needs using OpenAI models
- Estimates project scope and cost
- Generates downloadable PDF proposals

## Project Structure

```
ai-onboarding-automation/
├── app.py
├── .env
├── requirements.txt
├── src/
│   ├── scraper/
│   │   └── company_scraper.py
│   ├── analyzer/
│   │   ├── business_analyzer.py
│   │   └── project_estimator.py
│   ├── generator/
│   │   └── proposal_generator.py
│   └── utils/
│       └── helpers.py
├── generated_proposals/
```

## Setup Instructions

1. **Clone the repository**
    ```sh
    git clone https://github.com/your-username/ai-onboarding-automation.git
    cd ai-onboarding-automation
    ```

2. **Create and activate a virtual environment**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up your `.env` file**
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

5. **Run the Streamlit app**
    ```sh
    streamlit run app.py
    ```

## Usage

1. Enter a company website URL.
2. Click "Scrape Company Data" to fetch basic info.
3. Click "Analyze Business Needs" to get AI-powered insights.
4. Click "Estimate Project Scope" for cost and timeline.
5. Click "Generate Complete Proposal" to create and download the PDF proposal.

## Notes

- Make sure your OpenAI API key has access to the required models.
- All generated proposals are saved in the `generated_proposals/` folder.
- For any issues, check the `app.log` file for error details.