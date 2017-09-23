function selectEvent() {
    var eventVal=document.getElementById("id_event_type").value;  

    if (eventVal == "S"){
    $('#Simple').show();
    $('#Multiple').hide();
    $('#Recurring').hide();
    } else if (eventVal == "M"){
        $('#Simple').hide();
        $('#Multiple').show();
        $('#Recurring').hide();
    } else
        {
        $('#Simple').hide();
        $('#Multiple').hide();
        $('#Recurring').show();
    
    }
}
