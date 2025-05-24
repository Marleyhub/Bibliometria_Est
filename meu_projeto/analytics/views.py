from django.shortcuts import render
from django.conf import settings
import pandas as pd
import networkx as nx
from pyvis.network import Network
from itertools import combinations
import plotly.express as px
import plotly.io as pio
from collections import defaultdict, Counter
import os, re


file_path = os.path.join(settings.MEDIA_ROOT, 'parsed_data.csv')
file_content = "No graph could be generated."


def author_analytics(request):  
        graph_created = False
        df = validate_path(file_path)
        try:
            df['AU'] = df['AU'].apply(parse_authors)
            G = nx.Graph()

            # Adding relationship
            for au in df['AU']:
                for au1, au2 in combinations(au, 2):
                    if G.has_edge(au1, au2):
                        G[au1][au2]['weight'] += 1
                    else:
                         G.add_edge(au1, au2, weight=1)
            
            # Creating chart
            net = Network(height='600px', width='100%', bgcolor='#ffffff', font_color='black')
            net.from_nx(G)
            net.repulsion(node_distance=200, spring_length=200)
            # Saving chart
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
        # parsing white valued keys and " and " 
        df['AU'] = df['AU'].apply(parse_authors)
        author_year_counts = defaultdict(int)

        # couting each publication per year
        for _, row in df.iterrows():
            year = row['PY']
            for author in row['AU']:
                author_year_counts[(author, year)] += 1
        data = [{
            'Author': author,
            'Year': year,
            'Publications': count
        } for (author, year), count in author_year_counts.items()]

        # setting couting to dataframe
        count_df = pd.DataFrame(data)
        top_authors = count_df['Author'].value_counts().head(10).index
        filtered_df = count_df[count_df['Author'].isin(top_authors)]

        # Plot using Plotly Express
        fig = px.bar(filtered_df, 
             x='Year', 
             y='Publications', 
             color='Author', 
             barmode='group',
             title="Scientific Production per Year by Author")
        
        # saving fig
        os.makedirs('static', exist_ok=True)
        chart_path = 'static/author_production_chart.html'
        pio.write_html(fig, file=chart_path, include_plotlyjs='cdn', auto_open=False)
        graph_created = True

        return render(request, 'analytics/cientific_prod.html', {
        'graph': graph_created 
        })
        
    except Exception as e:
        print(f'faild in cientific_prod, Err == {e}')

def trend_evolution(request):
    df = validate_path(file_path)
    graph_created = False

    try:
        if 'TI' in df.columns and 'PY' in df.columns:
            df = df[['TI', 'PY']]

            year_keywords = defaultdict(list) 

            for _, row in df.iterrows():
                year = row['PY']
                tokens = clean_and_tokenize(row['TI'])
                year_keywords[year].extend(tokens)

            yearly_counts = {year: Counter(words) for year, words in year_keywords.items()}

            all_counts = Counter()
            for counts in yearly_counts.values():
                all_counts.update(counts)

            top_keywords = [kw for kw, _ in all_counts.most_common(10)]

            heatmap_data = []
            for kw in top_keywords:
                for year in sorted(yearly_counts):
                    heatmap_data.append({
                    "Keyword": kw,
                    "Year": year,
                    "Frequency": yearly_counts[year][kw]
            })

            heatmap_df = pd.DataFrame(heatmap_data)

            fig = px.density_heatmap(
                heatmap_df,
                x="Year",
                y="Keyword",
                z="Frequency",
                color_continuous_scale="YlGnBu",
                title="Keyword Trends by Year (No scikit-learn)"
            )

            os.makedirs('static', exist_ok=True)
            chart_path = 'static/trend_evolution.html'
            fig.write_html(chart_path, include_plotlyjs='cdn')
            graph_created = True
        else:
            print("Columns for trend evolution not found")

    except Exception as e: 
        print("Thera was an error into evolution logic -- Err: {e}")
        return graph_created 
    
    return render(request, 'analytics/trend_evolution.html', {
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