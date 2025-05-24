from django.shortcuts import render
from django.conf import settings
import pandas as pd
import networkx as nx
from pyvis.network import Network
from itertools import combinations
import plotly.express as px
import plotly.io as pio
from collections import Counter, defaultdict
import os


file_path = os.path.join(settings.MEDIA_ROOT, 'parsed_data.csv')
file_content = "No graph could be generated."


def author_analytics(request):  
        graph_created = False
        df = validate_path(file_path)
        try:
            df['AU'] = df['AU'].apply(parse_authors)
            G = nx.Graph()

            for au in df['AU']:
                for au1, au2 in combinations(au, 2):
                    if G.has_edge(au1, au2):
                        G[au1][au2]['weight'] += 1
                    else:
                         G.add_edge(au1, au2, weight=1)
            
            net = Network(height='600px', width='100%', bgcolor='#ffffff', font_color='black')
            net.from_nx(G)

            # Optional: improve layout
            net.repulsion(node_distance=200, spring_length=200)

            # Save the interactive network as an HTML file
            os.makedirs('static', exist_ok=True)
            net.save_graph('static/author_network.html')
            graph_created = True

        except Exception as e:
            print(f"it was not possivel to analyse this data --- Err = {e}")
            graph_created = False
        return render(request, 'analytics/author_analytics.html', {
        'graph': graph_created 
        })

def cientific_prod(request):
    df = validate_path(file_path)
    graph_created = False
    try:
        df['AU'] = df['AU'].apply(parse_authors)
        all_authors = [author for sublist in df['AU'] for author in sublist]
        print(all_authors)
        # Count each author's occurrences
        author_counts = Counter(all_authors)
        # Print each author and how many times they appear
        for author, count in author_counts.items():
            print(f"{author}: {count} publications")

        author_year_counts = defaultdict(int)
        for _, row in df.iterrows():
            year = row['PY']
            for author in row['AU']:
                author_year_counts[(author, year)] += 1

        data = [{
            'Author': author,
            'Year': year,
            'Publications': count
        } for (author, year), count in author_year_counts.items()]

        count_df = pd.DataFrame(data)
        # limit to top N authors to reduce clutter and file size
        top_authors = count_df['Author'].value_counts().head(10).index
        filtered_df = count_df[count_df['Author'].isin(top_authors)]

        # Plot using Plotly Express
        fig = px.bar(filtered_df, 
             x='Year', 
             y='Publications', 
             color='Author', 
             barmode='group',
             title="Scientific Production per Year by Author")

        
        os.makedirs('static', exist_ok=True)
        # Save figure as a full HTML file
        chart_path = 'static/author_production_chart.html'
        pio.write_html(fig, file=chart_path, include_plotlyjs='cdn', auto_open=False)
        graph_created = True

        return render(request, 'analytics/cientific_prod.html', {
        'graph': graph_created 
        })
        
    except Exception as e:
        print(f'faild in cientific_prod, Err == {e}')

def validate_path(file_path):
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return None
    else:
        print(f"File does not exist at path: {file_path}")
        return None

## parsing AU column content to avoid 'and's
def parse_authors(author_str):
    if pd.isna(author_str):
        return[]
    author_str = author_str.replace(' and ', ',')
    # creating a list with no wite spaces and separeted by ','
    return [a.strip() for a in author_str.split(',') if a.strip()]