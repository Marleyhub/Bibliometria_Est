from django.shortcuts import render
from django.conf import settings
import pandas as pd
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt
import os, base64, io


file_path = os.path.join(settings.MEDIA_ROOT, 'parsed_data.csv')
file_content = "No graph could be generated."


def author_analytics(request):  
         
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
            
            pos = nx.spring_layout(G, k=0.5, iterations=50)
            weights = [G[u][v]['weight'] for u, v in G.edges()]
            edges = G.edges(data=True)
            weights = [data['weight'] for _, _, data in edges]

            plt.figure(figsize=(10, 8))
            nx.draw(
                G, pos,
                with_labels=True,
                node_color='skyblue',
                node_size=300,
                font_size=10,
                edge_color='gray',
                width=weights
            )

            plt.title("Author Co-occurrence Network (Spring Layout)")
            plt.axis('off')
            plt.title("Author Co-occurrence Network")
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            # Encode plot to base64 string
            image_png = buffer.getvalue()
            graph_base64 = base64.b64encode(image_png).decode('utf-8')
            buffer.close()
             
        except Exception as e:
            print(f"it was not possivel to analyse this data --- Err = {e}")
            graph_base64 = None
            
        return render(request, 'analytics/author_analytics.html', {
        'graph' : graph_base64
})

def validate_path(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print(df)
    else:
        file_content = f"File does not exist at path: {file_path}"
    return df

## parsing AU column content to avoid 'and's
def parse_authors(author_str):
    if pd.isna(author_str):
        return[]
    author_str = author_str.replace(' and ', ',')
    # creating a list with no wite spaces and separeted by ','
    return [a.strip() for a in author_str.split(',') if a.strip()]