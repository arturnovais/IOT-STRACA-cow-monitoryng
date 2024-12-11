import pandas as pd
import requests
from urllib.parse import urlencode

def generate_map(df):
    # Gerar os marcadores em formato JSON
    markers = df.to_dict(orient='records')

    with open('mapa_interativo.html', 'w') as f:
        f.write(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mapa Interativo</title>
        <style>
            #map {{ height: 100vh; width: 100%; }}
        </style>
        <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyA7wviaJXTsZqIsfcoNX5FquWBEfAbtXQc"></script>
        <script>
            function initMap() {{
                const center = {{ lat: {markers[0]['lat']}, lng: {markers[0]['lng']} }};
                const map = new google.maps.Map(document.getElementById("map"), {{
                    zoom: 18,
                    center: center,
                    mapTypeId: 'satellite'
                }});

                // Lista de marcadores
                const markers = {markers};

                // Adicionar pontos vermelhos no mapa
                markers.forEach(location => {{
                    new google.maps.Circle({{
                        strokeColor: '#ff4d00', // Cor da borda
                        strokeOpacity: 1.0,    // Opacidade da borda
                        strokeWeight: 0,       // Espessura da borda (zero para apenas preenchimento)
                        fillColor: '#ff4d00',  // Cor de preenchimento
                        fillOpacity: 1.0,      // Opacidade do preenchimento
                        map: map,
                        center: location,      // Posição do ponto
                        radius: 1             // Raio em metros (simula um pequeno ponto)
                    }});
                }});
            }}
        </script>
    </head>
    <body onload="initMap()">
        <div id="map"></div>
    </body>
    </html>
    """)
