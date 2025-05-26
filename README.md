
Project using Python 3.10.9

***************************************************************************************************
## ⚙️ Install it

    1 - git clone https://github.com/Marleyhub/Bibliometria_Est
    2 - run "pip install -r requirements.txt" at root of the project ./Bibliometria_Est/
        . for development create venv inside meu_projeto "python -m venv .venv"
    3 - Go to ./Bibliometria_Est/my_project
    4 - run "python manage.py runserver"
    5 - App running on "http://localhost:8000" (route for index)

***************************************************************************************************

## 🌐 URL Routing Overview — Django Project

    This project is structured into multiple Django apps, each with its own URL configuration.
    The main URL dispatcher connects to each app, which handles specific functionalities such 
    as home display, file uploads, and analytics.

## 🔁 General Flow
    User visits a URL in the browser
    Django's root index/ loads http://localhost:8000 includes routes for each app:

    upload/
    analyticS/

    Each app has its own urls.py, which maps specific paths to views (functions).
    Views handle the request and returns a HTML templates.

## 📂 Project Structure (Django apps)
    - index/: Home and navigation
    - upload/: File uploads
    - analytics/: Data visualization

## 🏠 index/urls.py
    - /: Landing page
    - /begin_upload:  Redirects to upload process

## 📁 upload/urls.py
    - /upload/ → Displays file upload form
    - /upload/upload_this → Receives and processes uploaded data

## 📊 analytic/urls.py
    - /analytic/author_analytics: Co-authorship graph
    - /analytic/cientific_prod: Scientific output analytics
    - /analytic/trend_evolution: Time-based evolution of research trends

**********************************************************************************************

## 📁 upload App — Function Reference (view.py)

## upload(request)
    Input: request (HttpRequest)
    Returns: Rendered HTML page (upload/upload.html)

## upload_this(request)
    Input: request (HttpRequest, expects POST with file)
    Returns: Rendered HTML page (upload/upload_this.html) with:
    - form (UploadFileForm)
    - file_content (str or None)
    - filename (str or None)

## save_file(request, filename, uploaded_file)
    Inputs:
    - request (HttpRequest)
    - filename (str)
    - uploaded_file (InMemoryUploadedFile or TemporaryUploadedFile)
    Returns: Full file path as str if successful, else None

## parse_bibtex(file_path)
    - Input: file_path (str)
    Returns: pandas.DataFrame with BibTeX entries
    (Returns empty DataFrame on error)

## parse_ris(file_path)
    - Input: file_path (str)
    Returns: pandas.DataFrame with RIS entries
    (Returns empty DataFrame on error)

## normalize_columns(df)
    Input: df (pandas.DataFrame)
    Returns: pandas.DataFrame with normalized column names based on mapping


## 📁 analytics App — Function Reference (views.py)

## author_analytics(request)
    - Input: request (HttpRequest)
    Returns: Rendered HTML page (analytics/author_analytics.html) with:
    graph (bool) — True if graph was generated and saved successfully

## cientific_prod(request)
    - Input: request (HttpRequest)
    Returns: Rendered HTML page (analytics/cientific_prod.html) with:
    graph (bool) — True if bar chart was created and saved successfully

## trend_evolution(request)
    - Input: request (HttpRequest)
    Returns: Rendered HTML page (analytics/trend_evolution.html) with:
    graph (bool) — True if keyword heatmap was created and saved successfully

## validate_path(file_path)
    - Input: file_path (str)
    Returns: pandas.DataFrame loaded from the CSV if file exists and is valid, else None

## parse_authors(author_str)
    - Input: author_str (str or float if NaN)
    Returns: list[str] — List of author names, parsed and cleaned

## clean_and_tokenize(text)
    - Input: text (str)
    Returns: list[str] — Lowercased and tokenized words with punctuation removed




