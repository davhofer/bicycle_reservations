var ojp_request = "<?xml version=\"1.0\" encoding=\"utf-8\"?> <OJP xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns=\"http://www.siri.org.uk/siri\" version=\"1.0\" xmlns:ojp=\"http://www.vdv.de/ojp\" xsi:schemaLocation=\"http://www.siri.org.uk/siri ../ojp-xsd-v1.0/OJP.xsd\">    <OJPRequest>        <ServiceRequest>            <RequestTimestamp>2022-03-24T10:45:23.372Z</RequestTimestamp>            <RequestorRef>API-Explorer</RequestorRef>            <ojp:OJPTripRequest>                <RequestTimestamp>2022-03-24T10:45:23.372Z</RequestTimestamp>                <ojp:Origin>                    <ojp:PlaceRef>                        <ojp:StopPlaceRef>8507000</ojp:StopPlaceRef>                        <ojp:LocationName>                            <ojp:Text>START_LOC</ojp:Text>                        </ojp:LocationName>                    </ojp:PlaceRef>                    <ojp:DepArrTime>START_TIME</ojp:DepArrTime>                </ojp:Origin>                <ojp:Destination>                    <ojp:PlaceRef>                        <ojp:StopPlaceRef>8503000</ojp:StopPlaceRef>                        <ojp:LocationName>                            <ojp:Text>END_LOC</ojp:Text>                        </ojp:LocationName>                    </ojp:PlaceRef>                </ojp:Destination>                <ojp:Params>                    <ojp:IncludeTrackSections>true</ojp:IncludeTrackSections>                    <ojp:IncludeTurnDescription></ojp:IncludeTurnDescription>                    <ojp:IncludeIntermediateStops></ojp:IncludeIntermediateStops>                </ojp:Params>            </ojp:OJPTripRequest>        </ServiceRequest>    </OJPRequest></OJP>";

const time_format = "2022-03-24T11:45:02";

// START_LOC
// END_LOC
// START_TIME

var start = "Bern";
var end = "Zürich";
var start_time = "2022-03-24T11:45:02";

ojp_request = ojp_request.replace('START_LOC', start);

ojp_request = ojp_request.replace('END_LOC', end);
ojp_request = ojp_request.replace('START_TIME', start_time);


var xhr = new XMLHttpRequest();
xhr.open("POST", "https://api.opentransportdata.swiss/ojp2020", true);
xhr.setRequestHeader('Content-Type', 'application/xml');
xhr.setRequestHeader('Authorization', 'Bearer 57c5dbbbf1fe4d0001000018dc333f3fe02340138e090d6325923a19');

xhr.send(ojp_request);

var ans;

xhr.onreadystatechange = function() {
    if (xhr.readyState == 4 && xhr.status == 200) {
        ans = xhr.responseXML.children[0].innerHTML;
        console.log(ans);
    } else {
        console.log("Not successfull??");
    }
};