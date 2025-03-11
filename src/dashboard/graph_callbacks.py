# src/dashboard/graph_callbacks.py
import dash
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from .app import app
from dash.dependencies import Input, Output, State, MATCH

@app.callback(
    Output({'type': 'tab-graph', 'index': MATCH}, 'figure'),
    [Input({'type': 'update-data-to-display-button', 'index': MATCH}, 'n_clicks')],
    [State('imported-data-store', 'data'),
     State({'type': 'display-vector-dropdown', 'index': MATCH}, 'value'),
     State({'type': 'selected-display-data-table', 'index': MATCH}, 'selectedRows')]
)
def update_graph(n_clicks, imported_data, selected_vector, selected_rows):
    # from dash.exceptions import PreventUpdate
    if not n_clicks or imported_data is None or not selected_vector or not selected_rows:
        raise PreventUpdate

    traces = []
    # Pour chaque ligne sélectionnée (chaque dictionnaire représentant une ligne dans la grille)
    for sel in selected_rows:
        file_name = sel.get("file")
        measure = sel.get("data")
        if not file_name or not measure:
            continue

        # Rechercher dans les données importées l'objet dont le fileName correspond
        data_item = next((item for item in imported_data if item.get('fileName') == file_name), None)
        if data_item is None:
            continue

        # Déterminer l'axe x en fonction du vecteur d'affichage sélectionné.
        # On prend ici la première "cellule" du fichier importé.
        data_table = data_item.get("dataTable", [])
        if not data_table:
            continue
        cell = data_table[0]
        # Vérifier si le vecteur principal correspond à la sélection
        mdv = cell.get("main_display_vector", {})
        if isinstance(mdv, dict) and mdv.get("name", "").strip() == selected_vector:
            x_values = mdv.get("values", [])
        else:
            # Sinon, rechercher dans les paramètres
            params = cell.get("parameters", [])
            x_values = []
            for p in params:
                if isinstance(p, dict) and p.get("name", "").strip() == selected_vector:
                    x_values.append(p.get("value"))
            # Vous pouvez adapter ici la logique de regroupement si nécessaire

        # Pour l'axe y, on récupère la série associée à la grandeur (measure)
        y_values = []
        for cell in data_item.get("dataTable", []):
            if isinstance(cell, dict):
                values = cell.get("values", {})
                if isinstance(values, dict):
                    series = values.get(measure, [])
                    # On concatène les séries issues de chaque cellule
                    y_values.extend(series)
        # Ajuster la longueur de x si besoin (par exemple, si x_values est une valeur unique)
        if len(x_values) == 1 and len(y_values) > 1:
            x_values = [x_values[0]] * len(y_values)

        trace = go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines+markers",
            name=f"{file_name} - {measure}"
        )
        traces.append(trace)

    fig = go.Figure(data=traces)
    fig.update_layout(
        xaxis_title=selected_vector,
        yaxis_title="Valeurs",
        title="Graphique des mesures"
    )
    return fig

