
Project using Python 3.10.9

************************************How to run
                                    
1 - git clone https://github.com/Marleyhub/Bibliometria_Est
2 - run "pip install -r requirements.txt" at root of the project ./Bibliometria_Est/
    . for development create venv inside meu_projeto "python -m venv .venv"
3 - Go to ./Bibliometria_Est/my_project
4 - run "python manage.py runserver"
5 - App running on "http://localhost:8000" (route for index)


************************************analitics.view() 
                                     
📊 author_analytics View — Co-authorship Network Analysis

🔍 Overview
This Django view analyzes a dataset to create a co-authorship graph based on the AU (Author) column of the input data. It generates an interactive HTML graph showing author collaborations.

    ⚙️ What It Does
    Loads the dataset using validate_path(file_path)
    Parses authors using parse_authors()
    Builds a graph with networkx where authors are nodes and co-authorships are edges
    Visualizes the graph with pyvis
    Saves the result to static/author_network.html
    Renders a template indicating if the graph was successfully created

    🛠 Requirements
    Install required packages:
    pip install networkx pyvis pandas

    📁 Expected Input
    A dataset with an AU column (authors list)
    A valid file path from validate_path()

    🧪 Error Handling
    If processing fails, an error is printed and the template receives 'graph': False.

    📄 Template
    Renders: analytics/author_analytics.html
    Context: { 'graph': True or False }

    ✅ Example Route
    path('author-analytics/', author_analytics, name='author_analytics'),
