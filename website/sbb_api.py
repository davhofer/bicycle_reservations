import requests
from xml.dom import minidom
import datetime


opuic_lookup = {'Moutier': 8500105,
 'Olten': 8500218,
 'Nyon': 8501030,
 'Chur': 8509000,
 'Winterthur': 8506000,
 'St. Gallen': 8506302,
 'Zug': 8502204,
 'Aarau': 8502113,
 'Brig': 8501609,
 'Laufen': 8500113,
 'Amriswil': 8506109,
 'Arth-Goldau': 8505004,
 'Basel SBB': 8500010,
 'Wil SG': 8506206,
 'Lugano': 8505300,
 'Bern': 8507000,
 'Oensingen': 8500212,
 'Biasca': 8505209,
 'Sargans': 8509411,
 'Zürich Oerlikon': 8503006,
 'Frauenfeld': 8506100,
 'Neuchâtel': 8504221,
 'Romanshorn': 8506121,
 'Morges': 8501037,
 'Luzern': 8505000,
 'Zürich HB': 8503000,
 'Locarno': 8505400,
 'Thun': 8507100,
 'Biel/Bienne': 8504300,
 'Biel':8504300,
 'Bienne':8504300,
 'Mendrisio': 8505305,
 'Flüelen': 8505112,
 'Chiasso': 8505307,
 'Lenzburg': 8502119,
 'Delémont': 8500109,
 'Gossau SG': 8506210,
 'Zürich Flughafen': 8503016,
 'Weinfelden': 8506105,
 'Solothurn': 8500207,
 'Grenchen Süd': 8500202,
 'Genève': 8501008,
 'Genf': 8501008,
 'Visp': 8501605,
 'Sissach': 8500026,
 'Flawil': 8506209,
 'Uzwil': 8506208,
 'Münsingen': 8507006,
 'Bellinzona': 8505213,
 'Fribourg/Freiburg': 8504100,
 'Fribourg': 8504100,
 'Freiburg': 8504100,
 'Yverdon-les-Bains': 8504200,
 'Lausanne': 8501120,
 'Landquart': 8509002,
 'Genève-Aéroport': 8501026,
 'Liestal': 8500023}


def send_request(start, end, start_time):
    AUTH_TOKEN = 'Bearer 57c5dbbbf1fe4d0001000018dc333f3fe02340138e090d6325923a19'

    xml = """<?xml version=\"1.0\" encoding=\"utf-8\"?> <OJP xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns=\"http://www.siri.org.uk/siri\" version=\"1.0\" xmlns:ojp=\"http://www.vdv.de/ojp\" xsi:schemaLocation=\"http://www.siri.org.uk/siri ../ojp-xsd-v1.0/OJP.xsd\">    <OJPRequest>        <ServiceRequest>            <RequestTimestamp>TIMESTAMP_ONE</RequestTimestamp>            <RequestorRef>API-Explorer</RequestorRef>            <ojp:OJPTripRequest>                <RequestTimestamp>TIMESTAMP_TWO</RequestTimestamp>                <ojp:Origin>                    <ojp:PlaceRef>                        <ojp:StopPlaceRef>START_OPUIC</ojp:StopPlaceRef>                        <ojp:LocationName>                            <ojp:Text>START_LOC</ojp:Text>                        </ojp:LocationName>                    </ojp:PlaceRef>                    <ojp:DepArrTime>START_TIME</ojp:DepArrTime>                </ojp:Origin>                <ojp:Destination>                    <ojp:PlaceRef>                        <ojp:StopPlaceRef>END_OPUIC</ojp:StopPlaceRef>                        <ojp:LocationName>                            <ojp:Text>END_LOC</ojp:Text>                        </ojp:LocationName>                    </ojp:PlaceRef>                </ojp:Destination>                <ojp:Params>                    <ojp:IncludeTrackSections>true</ojp:IncludeTrackSections>                    <ojp:IncludeTurnDescription></ojp:IncludeTurnDescription>                    <ojp:IncludeIntermediateStops>true</ojp:IncludeIntermediateStops>                </ojp:Params>            </ojp:OJPTripRequest>        </ServiceRequest>    </OJPRequest></OJP>"""
    xml = xml.replace('START_LOC', start)
    xml = xml.replace('END_LOC', end)

    # TIMESTAMP_ONE, TIMESTAMP_TWO, START_OPUIC, END_OPUIC

    xml = xml.replace('START_OPUIC', str(opuic_lookup[start]))
    xml = xml.replace('END_OPUIC', str(opuic_lookup[end]))

    ts = datetime.datetime.now().replace(microsecond=0).isoformat()

    xml = xml.replace('TIMESTAMP_ONE', ts)
    xml = xml.replace('TIMESTAMP_TWO', ts)


    xml = xml.replace('START_TIME', start_time)


    api_link = "https://api.opentransportdata.swiss/ojp2020"

    headers = {
        'Content-Type': 'application/xml',
        'Authorization': AUTH_TOKEN
    } 

    r = requests.post(api_link, data=xml, headers=headers)
    if r.status_code == 200:
        doc = minidom.parseString(r.text)
        best_trips = []
        trips = doc.getElementsByTagName('ojp:Trip')
        print("trips", len(trips))
        for trip in trips:
            trip_sections = []

            trip_legs = trip.getElementsByTagName('ojp:TripLeg')
            print("trip_legs", len(trip_legs))

            l = len(trip_legs)
            for i in range(l):
                leg = trip_legs[i]

                try:
                    stops = leg.getElementsByTagName('ojp:TimedLeg')[0].getElementsByTagName('ojp:LegIntermediates')

                    board = leg.getElementsByTagName('ojp:TimedLeg')[0].getElementsByTagName('ojp:LegBoard')[0]
                    alight = leg.getElementsByTagName('ojp:TimedLeg')[0].getElementsByTagName('ojp:LegAlight')[0]


                    if len(stops) > 0:
                        stops.append(alight)
                    else:
                        stops = [alight]

                    service = leg.getElementsByTagName('ojp:TimedLeg')[0].getElementsByTagName('ojp:Service')[0]
                    ic = service.getElementsByTagName('ojp:Mode')[0].getElementsByTagName('ojp:ShortName')[0].getElementsByTagName('ojp:Text')[0].firstChild.nodeValue


                    current = board
                    if ic == 'IC':
                        line = service.getElementsByTagName('ojp:PublishedLineName')[0].getElementsByTagName('ojp:Text')[0].firstChild.nodeValue

                        for next_stop in stops:
                            try:
                                start_loc = current.getElementsByTagName('ojp:StopPointName')[0].getElementsByTagName('ojp:Text')[0].firstChild.nodeValue
                                start_time = current.getElementsByTagName('ojp:ServiceDeparture')[0].getElementsByTagName('ojp:TimetabledTime')[0].firstChild.nodeValue
                                end_loc = next_stop.getElementsByTagName('ojp:StopPointName')[0].getElementsByTagName('ojp:Text')[0].firstChild.nodeValue
                                end_time = next_stop.getElementsByTagName('ojp:ServiceArrival')[0].getElementsByTagName('ojp:TimetabledTime')[0].firstChild.nodeValue
                                
                                trip_sections.append((start_loc, start_time, end_loc, end_time, line))
                                current = next_stop
                            except:
                                current = next_stop
                                
                                

                except Exception as e:
                    print(e)
                    continue
                    
            if len(trip_sections) > len(best_trips):
                best_trips = trip_sections
        return best_trips

    else:
        print('Request failed!')
        
    



if __name__ == '__main__':

    test_time = "2022-03-25T10:00:00"
    print(send_request('Luzern', 'Chur', test_time))
