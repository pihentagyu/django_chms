function handleClick(cb) {
    //display("Click, new value = " + cb.checked);
    if( cb.checked) {
    $('#showOnClick').show();
    $('#hideOnClick').hide();
    } else {
        $('#showOnClick').hide();
        $('#hideOnClick').show();
    
    }
}
/**
*For testing
*function display(msg) {
*    var p = document.createElement('p');
*        p.innerHTML = msg;
*        document.body.appendChild(p);
*}
*/
