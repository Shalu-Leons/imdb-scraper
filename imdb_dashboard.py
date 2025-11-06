import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px

# Load your cleaned IMDb dataset
df = pd.read_csv("imdb_top250_cleaned.csv")

# Convert columns properly
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

# Initialize Dash app
app = Dash(__name__)
app.title = "IMDb Top 250 Dashboard"

# Layout
app.layout = html.Div([
    html.H1("🎬 IMDb Top 250 Movies Dashboard", style={'textAlign': 'center'}),

    # Dropdown for Year filter
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            options=[{'label': str(y), 'value': y} for y in sorted(df["Year"].dropna().unique(), reverse=True)],
            id='year-filter',
            placeholder="Select a year to filter",
            multi=False,
            style={'width': '50%'}
        )
    ], style={'textAlign': 'center', 'margin': '20px'}),

    # Charts
    html.Div([
        dcc.Graph(id='top10-chart', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='decade-chart', style={'width': '50%', 'display': 'inline-block'})
    ]),

    html.Hr(),

    html.H3("📊 Movie List"),
    dash_table.DataTable(
        id='movie-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
    )
])

# Callbacks for interactivity
@app.callback(
    [Output('top10-chart', 'figure'),
     Output('decade-chart', 'figure'),
     Output('movie-table', 'data')],
    [Input('year-filter', 'value')]
)
def update_dashboard(selected_year):
    filtered_df = df.copy()
    if selected_year:
        filtered_df = filtered_df[filtered_df["Year"] == selected_year]

    # Top 10 Movies by Rating
    top10 = filtered_df.nlargest(10, "Rating")
    fig_top10 = px.bar(
        top10,
        x="Title",
        y="Rating",
        color="Rating",
        title="Top 10 Movies by Rating",
        text="Rating"
    )

    # Distribution by Decade
    filtered_df["Decade"] = (filtered_df["Year"] // 10) * 10
    decade_count = filtered_df["Decade"].value_counts().reset_index()
    decade_count.columns = ["Decade", "Count"]
    fig_decade = px.pie(decade_count, names="Decade", values="Count", title="Movies by Decade")

    return fig_top10, fig_decade, filtered_df.to_dict('records')


if __name__ == "__main__":
    app.run(debug=True)
