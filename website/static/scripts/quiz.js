function goHome(){
	window.location.href = "/"
}

//ajax datatables for proposals
$(document).ready(function() {
    $('#proposals_datatable').DataTable( {
        "ajax": "/ajax/proposals",
        "columns": [
            { "data": "id" },
            { "data": "name" },
            { "data": "description" },
            { "data": "proposal_status" },
            { "data": "starting_date" },
            { "data": "ending_date" },
            { "data": "date_created" },
        ]
    } );
} );

//ajax datatables for events
$(document).ready(function() {
    $('#events_datatable').DataTable( {
        "ajax": "/ajax/events",
        "columns": [
			{ "data": "id" },
			{ "data": "name" },
            { "data": "teacher" },
            { "data": "assistant" },
            { "data": "destination" },
            { "data": "atending_class" },
            { "data": "starting_date" },
            { "data": "ending_date" },
            { "data": "starting_location" },
            { "data": "ending_location" },
            { "data": "date_created" }
        ]
    } );
});

$(document).ready(function() {
    $( '#alert' ).delay( 3000 ).fadeOut( 400 );
});
