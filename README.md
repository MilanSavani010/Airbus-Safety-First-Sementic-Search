# SRM_Demo Dashboard

## Overview
The **SRM_Demo Dashboard** is a Streamlit-based frontend application for interacting with the backend search functionality. It provides a user-friendly interface to input queries, retrieve results, and access document content directly.

## Features
- **Search Functionality**: Enter a query to search indexed documents.
- **Customizable Result Count**: Adjust the number of results displayed using a slider.
- **Document Previews**: Displays snippets from matched documents alongside page numbers.
- **PDF Access**: Provides direct links to view PDF files, jumping to the relevant page.

---

## Technologies Used
- **Streamlit**: Framework for building web applications.
- **Requests**: For interacting with the backend RESTful APIs.
- **Python**: Used for all application logic.

---

## How It Works
1. **Query Input**: Enter a search query through the text box.
2. **Result Limit**: Use the slider to choose the maximum number of results displayed.
3. **Search Execution**: Press the **Search** button to send the query to the backend API.
4. **Render Results**: Results include:
   - File name and corresponding page.
   - Snippet of text from the document.
   - Link to open the PDF (jumps directly to the relevant page).

---
## Bird Eye View
```mermaid
    sequenceDiagram
       participant User
       participant Streamlit_Frontend as Streamlit Frontend (app.py)
       participant Flask_Server as Flask Server (server.py)
       participant Search_Engine as Search Engine (search_engine.py)
       participant PDF_Storage as PDF Storage
       
   
       User->>+Streamlit_Frontend: Enters query and clicks Search
       Streamlit_Frontend->>+Flask_Server: HTTP GET /api/search
       Flask_Server->>+Search_Engine: search_query_across_batches(query, top_k)
       Search_Engine-->>-Flask_Server: List of search results
       Flask_Server-->>-Streamlit_Frontend: JSON results
       Streamlit_Frontend-->>User: Displays results & links to PDFs
       
       User->>+Streamlit_Frontend: Clicks Open PDF
       Streamlit_Frontend->>+Flask_Server: HTTP GET /api/open-pdf
       Flask_Server->>+PDF_Storage: Retrieve requested PDF
       PDF_Storage-->>-Flask_Server: PDF File
       Flask_Server-->>-Streamlit_Frontend: Serve PDF file for inline viewing
       Streamlit_Frontend-->>User: Opens PDF for viewing
   

```
```mermaid
graph TD
    %% Frontend Section
    subgraph Frontend
        A[app.py <br> Streamlit Interface: <br> Handles user input, displays results]
    end

    %% API Layer
    subgraph API_Layer
        B[server.py <br> Flask API Server: <br> Serves REST APIs for search and PDF retrieval]
    end

    %% Batch Processor Details
    subgraph Batch_Processor["batch_processor.py <br> Batch PDF Processing"]
        P1[Load PDF Chunks: <br> load_pdf_chunks_from_files pymupdf4llm pretrained model]

        P2[Prepare Chunks: <br> prepare_chunks: Word level chunking,cleaning]
        P3[Embed Chunks: <br> embed_chunks SentenceTransformer]
        P4[Save Embeddings: <br> save_index FAISS Dence Vector Indenxing, Metadata mapping]
        P5[Save Metadata: <br> save_metadata]
        P6[Logging: <br> Use logger.py]
    end

    %% Document Processing (Other Components)
    subgraph Document_Processing
        D[search_engine.py <br> Loads indexes, performs search]
        E[path_manager.py <br> Utilities for managing file paths]
    end

    %% Utilities Section
    subgraph Utilities
        F[logger.py <br> Centralized logging for all tasks]
    end

    %% Storage Layer
    subgraph Storage
        G[PDF Storage <br> Stores raw PDF files]
        H[Index Data <br> FAISS Vector Indexes , Metadata JSONs]
    end

    %% Connecting the frontend
    A --> B
    B --> D
    %% Retrieve specific PDFs
    B --> G 
    %% Access the index and metadata for search
    D --> H 

    %% Batch Processor Workflow
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P3 --> P5
    P4 --> H 
    P5 --> H 
    P6 --> F

    %% Batch Processor Setup
    E --> P1 
    P1 --> G 
```
## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/MilanSavani010/SRM_Demo
   cd SRM_Demo
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the **backend server**:
   - Navigate to the directory that contains `server.py` and run:
     ```bash
     python server.py
     ```

5. Launch the **Streamlit app**:
   - Run the Streamlit dashboard:
     ```bash
     streamlit run app.py
     ```

---

## User Guide

1. Open the dashboard in your browser (usually default at: `http://localhost:8501`).
2. Use the text input box to write your query.
3. Adjust the slider to select the number of results to display (default: 5).
4. Click the "Search" button to get results.
5. View the list of search results with:
   - File name
   - Page number
   - Text snippet
   - Link to view the PDF (direct navigation to the relevant page).

---

## Example Flow

1. Query:  
   Enter a query, such as `"safety procedures"`.

2. Result Customization:  
   Slide the adjustable bar to select how many top results to display (e.g., 3).

3. Search Results:  
   Results will show:
   ```
   document.pdf - Page 2
   "Text snippet matching the query"
   [Open PDF File]
   ```

4. Open PDF:  
   Click the `Open PDF File` link to view the document directly, opening the relevant page.

---

## Future Enhancements
- Add authentication for dashboard access.
- Implement result sorting and filtering.
- Include a file upload feature for users to index their documents dynamically.
- Optimize query performance for larger datasets.

---

## Contributing
Contributions are always welcome. Please feel free to open issues or submit a pull request.

---
