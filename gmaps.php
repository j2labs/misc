<?

$mapsurl = "http://maps.google.com/maps";
$source_address = "595 Market St. San Francisco, CA 94105";
$destination_address = "14 Wall St. New York, NY 10005";

/**
 * These variables are shared among the xml parsers and reset
 * when parseSegments is called
 */
$mapOfSegments = array();
$segsFound = 0;
$characterData = array();
$charsFound = 0;
$map = array();
/* end of special xml variables */

$directions = getDirections($source_address, $destination_address);
print "The directions structure:<pre>"; print_r($directions); print "</pre>";

function getDirections($source_address, $destination_address) {
    global $mapsurl;
    global $map;

    $source_address = preg_replace("| |", "%20", $source_address);
    $destination_address = preg_replace("| |", "%20", $destination_address);

    print "URL: $mapsurl?saddr=$source_address&daddr=$destination_address";
    $data = file("$mapsurl?saddr=$source_address&daddr=$destination_address");

    // Line 3 contains the xml structure with the directions on it
    $segments = $data[2];
    $data = null;
    $segments = preg_replace("|^.*<segments|", "<segments", $segments);
    $segments = preg_replace("|</segments>.*$|", "", $segments);
    $segments = preg_replace("|<b>|", "", $segments);
    $segments = preg_replace("|</b>|", "", $segments);

    parseSegments($segments);

    return $map;
}

function parseSegments($segments) {
    global $segsFound;
    global $mapOfSegments;
    global $characterData;
    global $map;

    // reset elements
    $segsFound = 0;
    $mapOfSegments = array();
    $dataFound = 0;
    $characterData = array();
    $map = array();

    $xml_parser = xml_parser_create();
    xml_set_element_handler($xml_parser, "startElement", "endElement");
    xml_set_character_data_handler($xml_parser, "characterDataFunction");

    if (!xml_parse($xml_parser, $segments)) {
	die(sprintf("XML error: %s at line %d",
		    xml_error_string(xml_get_error_code($xml_parser)),
		    xml_get_current_line_number($xml_parser)));
    }

    xml_parser_free($xml_parser);
    $map = $mapOfSegments[0];
    $map['STEPS'] = array_splice($mapOfSegments, 1, count($mapOfSegments));

    // Map character data into array
    for($i=0; $i<sizeof($map['STEPS']); $i++) {
	$map['STEPS'][$i]['TEXT'] = $characterData[$i]['TEXT'];
    }
}

function startElement($parser, $name, $attrs) {
    global $depth;
    global $segsFound;
    global $mapOfSegments;
    
    $mapOfSegments[$segsFound]['ID'] = $attrs['ID'];
    $mapOfSegments[$segsFound]['POINTINDEX'] = $attrs['POINTINDEX'];
    $mapOfSegments[$segsFound]['METERS'] = $attrs['METERS'];
    $mapOfSegments[$segsFound]['SECONDS'] = $attrs['SECONDS'];
    $mapOfSegments[$segsFound++]['DISTANCE'] = $attrs['DISTANCE'];
}

function endElement($parser, $name) {
    global $charsFound;
    $charsFound++;
}

function characterDataFunction($parser, $string) {
    global $charsFound;
    global $characterData;
    $characterData[$charsFound]['TEXT'] = $string;
}

?>
