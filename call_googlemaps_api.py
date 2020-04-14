# Dependencies
import boto3
import googlemaps
from datetime import datetime
import os

# Origin/Destination
squamish = os.environ.get('SQUAMISH_ADDRESS')
east_van = os.environ.get('EAST_VAN_ADDRESS')
downtown_van = os.environ.get('VAN_ADDRESS')

# API Key
api_key = os.environ.get('API_KEY')


def lambda_handler(event, context):
    # UTC time now
    now = datetime.utcnow()

    # define DynamoDB client and traffi-times table
    client = boto3.resource('dynamodb')
    table = client.Table(os.environ.get('TABLE'))

    # GoogleMaps API Call
    gmaps = googlemaps.Client(key=api_key)

    # commute time for squamish ->> east van and squamish ->> vancouver
    morning_commute = gmaps.distance_matrix([squamish], [east_van, downtown_van],
                                            mode="driving", departure_time="now")

    # commute time for east van ->> squamish and vancouver ->> squamish
    afternoon_commute = gmaps.distance_matrix([east_van, downtown_van], [squamish],
                                              mode="driving", departure_time="now")

    # filter drive time from JSON return
    squamish_east_van_travel_time = morning_commute['rows'][0]['elements'][0]['duration_in_traffic']['value']
    squamish_downtown_travel_time = morning_commute['rows'][0]['elements'][1]['duration_in_traffic']['value']
    east_van_squamish_travel_time = afternoon_commute['rows'][0]['elements'][0]['duration_in_traffic']['value']
    downtown_squamish_travel_time = afternoon_commute['rows'][1]['elements'][0]['duration_in_traffic']['value']

    # put drive times and time of departure into DynamoDB table
    table.put_item(Item={'datetime': str(now), 'downtown-squamish': downtown_squamish_travel_time,
                         'east_van-squamish': east_van_squamish_travel_time,
                         'squamish-downtown': squamish_downtown_travel_time,
                         'squamish-east-van': squamish_east_van_travel_time})

    return {'message': 'SUCCESS'}
