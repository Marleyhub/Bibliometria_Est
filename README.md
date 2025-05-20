Running it:

1 - run "pip -r requirements.txt" to manage packges and dependencies
2 - App running on "http://localhost:8000/upload" (route for user upload files .ris and .bibTex)
3 - open the virtual enviroment "venv\Scripts\activate"
3 - Go to ./my_project
4 - run "python manage.py runserver"


**************
Next steps:

1 - Criar uma lista e inserir todos os dicts parseados dos arquivos ris e bib
2 - Usar pandas para transformas os dicts em dataframes
3 - inserir try: expect: logica para lidar com erros 
4 - Testes de estresse nas funções bib_parser e ris_parser
6 - Criar rotas para Analises Bibliométricas