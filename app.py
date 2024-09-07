from flask import Flask, render_template, request
import requests
import networkx as nx
import folium
from haversine import haversine, Unit

app = Flask(__name__)

# Overpass API URL
OVERPASS_URL = 'https://overpass-api.de/api/interpreter'
OVERPASS_QUERY = '''
[out:json];
way({s},{w},{n},{e})[highway];
(._;>;);
out body;
'''

# Road quietness factors (lower is quieter)
ROAD_QUIETNESS = {
    'motorway': 5,
    'trunk': 4,
    'primary': 3,
    'secondary': 2,
    'residential': 1,
    'service': 1,
    'footway': 0.5,
    'cycleway': 0.5
}

# Function to fetch OSM data
def fetch_osm_data(south, west, north, east):
    overpass_query = OVERPASS_QUERY.format(n=north, s=south, e=east, w=west)
    response = requests.get(OVERPASS_URL, params={'data': overpass_query})
    return response.json()

# Parse OSM data and create a graph
def parse_osm_data(osm_data, path_type='distance'):
    G = nx.Graph()
    nodes = {}
    
    # Extract nodes
    for element in osm_data['elements']:
        if element['type'] == 'node':
            nodes[element['id']] = (element['lat'], element['lon'])

    # Extract ways and create graph edges
    for element in osm_data['elements']:
        if element['type'] == 'way' and 'highway' in element['tags']:
            highway_type = element['tags']['highway']
            node_ids = element['nodes']
            
            for i in range(len(node_ids) - 1):
                node_0, node_1 = node_ids[i], node_ids[i + 1]
                if node_0 in nodes and node_1 in nodes:
                    coords_0 = (nodes[node_0][0], nodes[node_0][1])
                    coords_1 = (nodes[node_1][0], nodes[node_1][1])
                    distance = haversine(coords_0, coords_1, unit=Unit.METERS)
                    
                    if path_type == 'quietness':
                        # Calculate weight based on quietness
                        quietness = ROAD_QUIETNESS.get(highway_type, 3)  # Default to medium quietness if unknown
                        weight = distance * quietness
                    else:
                        # Distance-based weight
                        weight = distance

                    G.add_edge(node_0, node_1, weight=weight)
    
    return G, nodes

# Heuristic function for A* (Haversine distance between two nodes)
def haversine_heuristic(node1, node2, nodes):
    coords_1 = nodes[node1]
    coords_2 = nodes[node2]
    return haversine(coords_1, coords_2, unit=Unit.METERS)

# Calculate shortest path using Dijkstra's algorithm or A* algorithm
def get_shortest_path(graph, nodes, start_coords, end_coords):
    start_node = min(nodes, key=lambda k: haversine(start_coords, nodes[k]))
    end_node = min(nodes, key=lambda k: haversine(end_coords, nodes[k]))
    
    # Find the shortest path using Dijkstra's algorithm
    path = nx.shortest_path(graph, source=start_node, target=end_node, weight='weight')

    # Find the shortest path using A* algorithm
    # path = nx.astar_path(graph, source=start_node, target=end_node, heuristic=lambda n1, n2: haversine_heuristic(n1, n2, nodes), weight='weight')

    return path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show_route', methods=['GET'])
def show_route():
    # Get coordinates and user options from the form
    start_lat = float(request.args.get('start_lat'))
    start_lon = float(request.args.get('start_lon'))
    end_lat = float(request.args.get('end_lat'))
    end_lon = float(request.args.get('end_lon'))
    path_type = request.args.get('path_type')  # distance or quietness

    # Define bounding box with a margin to avoid missing connections
    margin = 0.02
    south, west, north, east = start_lat - margin, start_lon - margin, end_lat + margin, end_lon + margin

    # Fetch map data from OSM
    osm_data = fetch_osm_data(south, west, north, east)

    # Parse OSM data and build graph with the selected path type (distance or quietness)
    graph, nodes = parse_osm_data(osm_data, path_type=path_type)

    # Get the shortest path between start and end coordinates
    path = get_shortest_path(graph, nodes, (start_lat, start_lon), (end_lat, end_lon))

    # Convert the path into coordinates for the folium map
    trail_coords = [(nodes[node][0], nodes[node][1]) for node in path]

    # Create a folium map centered at the start point
    folium_map = folium.Map(location=[start_lat, start_lon], zoom_start=14)
    folium.PolyLine(trail_coords, color="blue", weight=2.5, opacity=1).add_to(folium_map)
    folium.Marker([start_lat, start_lon], popup="Start").add_to(folium_map)
    folium.Marker([end_lat, end_lon], popup="End").add_to(folium_map)

    # Render the map on a new page
    return render_template('route.html', map=folium_map._repr_html_())

if __name__ == '__main__':
    app.run(debug=True)
