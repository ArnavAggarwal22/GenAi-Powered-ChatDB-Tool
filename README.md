# GenAi-Powered-ChatDB-Tool

A conversational AI application that allows users to ask questions in natural language to get insights from a PostgreSQL sales database.



## Features

-   **Natural Language Queries**: Ask complex questions about sales data in plain English.
-   **Text-to-SQL Conversion**: Uses Google's Gemini Pro model via LangChain to automatically convert questions into precise PostgreSQL queries.
-   **Few-Shot Learning**: Employs a set of high-quality examples to guide the AI, ensuring accuracy for complex queries.
-   **Interactive Web Interface**: Built with Streamlit for a simple and user-friendly experience.

## Tech Stack

-   **Backend**: Python
-   **AI Framework**: LangChain
-   **Language Model**: Google Gemini Pro (`gemini-1.5-flash`)
-   **Database**: PostgreSQL
-   **Web Framework**: Streamlit
-   **Database Driver**: `psycopg2-binary`

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd <your-repository-name>
