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
            // {
            //     data: null,
            //     className: "dt-center editor-edit",
            //     defaultContent: '<a href="/proposal/{"data":"id"}" class="btn btn-outline-success btn-sm" type="button"><i class="fa fa-pencil" aria-hidden="true"></i></a>',
            //     orderable: false
            // },
            // {
            //     data: null,
            //     className: "dt-center editor-delete btn",
            //     defaultContent: '<a class="btn btn-outline-primary btn-sm" type="button"><i class="fa fa-check"></i></a>',
            //     orderable: false
            // }
        ]
    } );
} );

//ajax datatables for proposals
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
            { "data": "date_created" }
            // {
            //     data: null,
            //     className: "dt-center editor-edit",
            //     defaultContent: '<a class="btn btn-outline-success btn-sm" type="button"><i class="fa fa-pencil" aria-hidden="true"></i></a>',
            //     orderable: false
            // },
            // {
            //     data: null,
            //     className: "dt-center editor-delete btn",
            //     defaultContent: '<a class="btn btn-outline-primary btn-sm" type="button"><i class="fa fa-check"></i></a>',
            //     orderable: false
            // }
        ]
    } );
});

$(document).ready(function() {
    $( '#alert' ).delay( 3000 ).fadeOut( 400 );
});
