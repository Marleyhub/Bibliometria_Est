from django.shortcuts import render
from django.conf import settings
import pandas as pd
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt
import os

def author_analytics(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'parsed_data.csv')
    file_content = "No graph could be generated."

    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            print(df)

            if not df.empty and 'AU' in df.columns and 'PY' in df.columns:
                G = nx.from_pandas_edgelist(df, source='AU', target='PY', edge_attr=True)
                
                # Convert the graph to a human-readable format
                file_content = f"Graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges"
            else:
                file_content = "DataFrame missing required 'source' and 'target' columns."
        else:
            file_content = f"File does not exist at path: {file_path}"

    except Exception as e:
        file_content = f"Error analyzing DataFrame: {e}"

    return render(request, 'analytics/author_analytics.html', {
        'file_content': file_content,
    })