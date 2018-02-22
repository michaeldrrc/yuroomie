window.onload = function() {
    this.document.getElementById('filter_submit').onclick = submitForm;
}

function submitForm() {
    var string = "";
    var first = true; 
    if(document.getElementById('minPrice').value!='') {
        if(!first) string += "~";
        else first = false;
        string+="prl=" + document.getElementById('minPrice').value;
    }

    if(document.getElementById('maxPrice').value!='') {
        if(!first) string += "~";
        else first = false;
        string+="prh=" + document.getElementById('maxPrice').value;
    }

    if(document.getElementById('male').checked || 
            document.getElementById('female').checked || 
            document.getElementById('other').checked) {
        if(!first) string += "~";
        else first = false;
        string+="gen=";
        if(document.getElementById('male').checked) string+="m";
        if(document.getElementById('female').checked) string+="f";
        if(document.getElementById('other').checked) string+="o";
    }

    if(document.getElementById('house').checked || 
            document.getElementById('town').checked || 
            document.getElementById('condo').checked || 
            document.getElementById('apart').checked) {
        if(!first) string += "~";
        else first = false;
        string+="type=";
        if(document.getElementById('house').checked) string+="h";
        if(document.getElementById('town').checked) string+="t";
        if(document.getElementById('condo').checked) string+="c";
        if(document.getElementById('apart').checked) string+="a";
    }

    if(document.getElementById('room1').checked || 
            document.getElementById('room2').checked || 
            document.getElementById('room3').checked || 
            document.getElementById('room4').checked) {
        if(!first) string += "~";
        else first = false;
        string+="rms=";
        if(document.getElementById('room1').checked) string+=1;
        if(document.getElementById('room2').checked) string+=2;
        if(document.getElementById('room3').checked) string+=3;
        if(document.getElementById('room4').checked) string+=4;
    }     

    if(document.getElementById('park1').checked || 
            document.getElementById('park2').checked || 
            document.getElementById('park3').checked || 
            document.getElementById('park4').checked) {
        if(!first) string += "~";
        else first = false;
        string+="par=";
        if(document.getElementById('park1').checked) string+=1;
        if(document.getElementById('park2').checked) string+=2;
        if(document.getElementById('park3').checked) string+=3;
        if(document.getElementById('park4').checked) string+=4;
    }       

    document.getElementById('filter_for_form').value = string;
    document.getElementById('filterForm').submit();
}