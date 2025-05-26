
Project using Python 3.10.9

************************************How to run
                                    
1 - git clone https://github.com/Marleyhub/Bibliometria_Est
2 - run "pip install -r requirements.txt" at root of the project ./Bibliometria_Est/
    . for development create venv inside meu_projeto "python -m venv .venv"
3 - Go to ./Bibliometria_Est/my_project
4 - run "python manage.py runserver"
5 - App running on "http://localhost:8000" (route for index)

 
🌐 URL Routing Overview — Django Project

This project is structured into multiple Django apps, each with its own URL configuration. The main URL dispatcher connects to each app, which handles specific functionalities such as home display, file uploads, and analytics.

🔁 General Flow
User visits a URL in the browser

Django's root index/ loads http://localhost:8000 includes routes for each app:

index/
upload/
analytic/

Each app has its own urls.py, which maps specific paths to views (functions).
Views handle the request and returns a HTML templates.

🏠 index/urls.py
/ → Main index or landing page
/begin_upload → Redirects to upload process

📁 upload/urls.py
/upload/ → Displays file upload form
/upload/upload_this → Receives and processes uploaded data

📊 analytic/urls.py
/analytic/author_analytics → Co-authorship graph
/analytic/cientific_prod → Scientific output analytics
/analytic/trend_evolution → Time-based evolution of research trends





