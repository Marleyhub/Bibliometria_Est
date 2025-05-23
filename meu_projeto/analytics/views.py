from django.shortcuts import render
from django.conf import settings
import pandas as pd
import networkx as nx
from pyvis.network import Network
from itertools import combinations
import matplotlib.pyplot as plt
import os, base64, io


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