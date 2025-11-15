# 📄 CV Analyzer

The CV Analyzer is a Streamlit-based web application that leverages an AI agent to provide comprehensive feedback and analysis on uploaded PDF resumes. It extracts text from CVs, parses structured data, and then uses a specialized AI agent to generate a detailed report, including strengths, areas for improvement, an ATS compatibility score, and actionable recommendations.

## ✨ Features

*   **PDF CV Upload**: Easily upload your CV in PDF format through a user-friendly interface.
*   **AI-Powered Analysis**: Utilizes the "Pathen CV Analysis Expert" AI agent to evaluate CV content.
*   **Constructive Feedback**: Provides practical and constructive feedback on your CV, even if the extracted data is partial or incomplete.
*   **Structured Analysis Report**: The AI agent generates a detailed report in a structured JSON format, which includes:
    *   **Summary**: A concise overview of the CV's strengths and weaknesses.
    *   **Strengths**: Highlights the positive aspects of the CV.
    *   **Improvements**: Suggests specific areas and actions for enhancing the CV.
    *   **ATS Score**: An estimated Applicant Tracking System (ATS) compatibility score out of 100.
    *   **Recommendations**: Prioritized next steps to help users improve their resume for job applications.
*   **Text Extraction**: Extracts raw text content from PDF documents.
*   **Resume Data Parsing**: Automatically parses key structured information from the CV, such as:
    *   Name
    *   Email
    *   Phone
    *   Education
    *   Experience
    *   Skills
*   **Interactive Streamlit UI**: A clean and intuitive web interface built with Streamlit for seamless user interaction and report visualization.
*   **Gemini API Integration**: Leverages the Gemini API (via `openai-agents`) for advanced AI capabilities.

## 🚀 Getting Started

### Prerequisites

*   Python 3.8+
*   A Google Gemini API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/cv_analyzer_backend.git
    cd cv_analyzer_backend
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate   # On Windows
    source venv/bin/activate # On macOS/Linux
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your Gemini API Key:**
    Create a `.env` file in the root directory of the project and add your Gemini API key:
    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```

### Running the Application

1.  **Start the Streamlit application:**
    ```bash
    streamlit run main.py
    ```

2.  Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## 🛠️ Technologies Used

*   **Python**: The core programming language.
*   **Streamlit**: For building the interactive web application.
*   **`openai-agents`**: For integrating and managing the AI agent.
*   **PyPDF2**: For PDF text extraction.
*   **Google Gemini API**: Powers the AI analysis capabilities.

## 📂 Project Structure

```
.
├── .env                      # Environment variables (e.g., GEMINI_API_KEY)
├── .gitignore                # Specifies intentionally untracked files to ignore
├── connection.py             # Handles API key loading and AI model configuration
├── main.py                   # Main Streamlit application logic and UI
├── requirements.txt          # Python dependencies
├── tools.py                  # Custom tools for PDF extraction and resume parsing
└── README.md                 # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue.

## 📄 License

This project is licensed under the MIT License.
