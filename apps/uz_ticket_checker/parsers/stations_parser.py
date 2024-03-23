import requests


def handle_one_phrase_stations(phrase):
    response_express = requests.post(
        'https://de-prod-lb.cashalot.in.ua/rest/stations/express',
        json={
            'language': 'uk',
            'supplier': 'uz_train',
            'transactionId': '3835b4beef23',
            'sourceType': 'FRONTEND',
            'query': phrase,
        }
    )
    query_stations = response_express.json()['stations']
    stations = []
    for query_station in query_stations:
        station_data = {
            'express_3_id': query_station['id'],
            'name': query_station['name'],
            'country': query_station['country'],
            'weight': query_station['weight']
        }
        stations.append(station_data)
    return stations



