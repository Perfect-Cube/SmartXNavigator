# SmartXNavigator

SmartXNavigator is a Python-based route planning application that leverages OpenStreetMap (OSM) data to find the optimal route between two points based on various criteria. This tool allows users to select routes based on distance or specific preferences, such as minimizing noise by choosing quieter streets or prioritizing well-lit paths.

## Features
1. **Optimal Route Finding:** Calculates the shortest or quietest path between two points.
2. **Customizable Path Criteria:** Choose between distance-based routes or quieter paths.
2. **Interactive Map:** Visualizes the route on an interactive map using Folium and OpenStreetMap.
3. **Data Retrieval:** Uses Overpass API to fetch detailed map data from OSM.
4. **Dynamic Weight Calculation:** Considers different road types and surrounding areas to estimate path quality.

## How It Works
1. **User Interface:** Users select start and end points on an interactive map and choose the desired path priority (quietest or shortest).
2. **Data Retrieval:** Fetches map data for the selected area using Overpass API, including details about highways and road types.
3. **Data Parsing:** Processes the data to extract node and way information, which is then used to build a graph representation of the map.
4. **Path Calculation:** Computes the optimal route using Dijkstra's algorithm or A* algorithm, with weights based on distance or estimated quietness.
5. **Visualization:** Displays the route on a map using Folium, with markers for start and end points and a polyline for the path.

## Pathfinding Algorithms
1. **Dijkstra's Algorithm :**
Dijkstra's Algorithm is a fundamental pathfinding algorithm used to find the shortest path between nodes in a graph. For SmartXNavigator, Dijkstra's Algorithm provides the following benefits:

- Optimal Pathfinding: Ensures the shortest distance between the start and end points is calculated by exploring all possible paths systematically.
- Flexibility: Can be adapted to consider different types of weights, such as distance or estimated quietness, making it suitable for various routing preferences.
- Comprehensive Solution: Effective for finding the shortest path in graphs with non-negative weights, which fits our needs for accurate route calculation based on distance.

2. **A-Star Algorithm :**
A* Algorithm enhances the pathfinding process by combining the benefits of Dijkstra's Algorithm with heuristics to guide the search more efficiently. Its advantages for SmartXNavigator include:

- Heuristic Optimization: Uses heuristics to estimate the cost from the current node to the goal, speeding up the search process compared to Dijkstra's Algorithm alone.
- Efficient Pathfinding: Reduces the number of nodes explored, leading to faster calculations, which is crucial for real-time route planning on larger maps.
- Customizable: Allows for incorporation of various heuristics, such as estimated travel time or other criteria, aligning with our goal of optimizing routes based on user preferences.

By integrating both Dijkstra's and A* algorithms, SmartXNavigator offers a robust and efficient route planning solution that balances accuracy and performance to deliver optimal paths tailored to your needs.

![Smart X Navigator](https://github.com/user-attachments/assets/9a7bf0e9-31ae-4fd9-bba4-2ac9a79ca450)

![Route-Result](https://github.com/user-attachments/assets/250a6327-297b-422a-b39e-836846bcf254)


## Installation
1. Clone the repository:

        git clone https://github.com/Perfect-Cube/SmartXNavigator.git
   
2. Navigate to the project directory:

        cd SmartXNavigator

3. Install required packages:

        pip install -r requirements.txt
## Usage
1. Run the application:

        python app.py
   
2. Open the application in your web browser. Scroll to the desired area on the map, click to select the start and end points, and choose the path priority.

3. Click "Find Path" to calculate and display the route.

## Code Overview
- **app.py:** Main application script for running the server and handling user inputs.
- **map_data.py:** Contains functions for fetching and parsing map data from Overpass API.
- **path_calculation.py:** Implements the pathfinding algorithm and weight calculations.
- **visualization.py:** Handles the map visualization using Folium.

## Possible Enhancements
- **Weighted Quietness Radius:** Improve the accuracy of quietness estimation by weighting the importance of nearby objects.
- **Additional Path Criteria:** Include options for safety, accessibility, or other user-defined preferences.
- **User Interface Improvements:** Enhance the UI for better usability and visual appeal.
