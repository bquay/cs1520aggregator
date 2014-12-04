var userTeams = [];

window.onload = function getUserTeams() {
    var existingTeams = document.getElementById("userTeams");
    var i;
    if (existingTeams != null) {
        for (i = 0; i < existingTeams.options.length; i++) {
            var team = existingTeams.options[i].value;
            userTeams.push(team);
        }
    }
}

window.onbeforeunload = function cacheUserTeams(e) {
    var teamsStr = "";
    
	//var team;
	for(team in userTeams){
		teamsStr = teamsStr + userTeams[team] + ",";
	}
    
    var xmlHttp = createXmlHttp();
    
    postParameters(xmlHttp, '/updateCache', 'userTeams='+teamsStr);
}

function toggleButton(button, disabled) {
    if (disabled == true) {
        button.disabled = true;
        button.style['background-color'] = '#dddddd';
        button.style['color'] = '#000000';
    } else {
        button.disabled = false;
        button.style['background-color'] = '#333333';
        button.style['color'] = '#FFFFFF';
    }
    
}

function createXmlHttp() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    if (!(xmlhttp)) {
        alert("Your browser doesn't support AJAX. You should try a new browser.");
    }
    return xmlhttp;
}

function postParameters(xmlHttp, target, parameters) {
    if (xmlHttp) {
        xmlHttp.open("POST", target, true);
        xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlHttp.send(parameters);
    }
}

function contains(arr, option) {
    var found = new Boolean(false);    
    var i;
    
    for(i = 0; i < arr.options.length; i++) {        
        if (arr.options[i].text == option) {
            found = true;
            break;
        }            
    }
    
    return found;
}

function addTeamToUserList() {	
	var teams = document.getElementById('teams');
	var teamInput = teams.options[teams.selectedIndex].value;
	
	if(userTeams.indexOf(teamInput) <= -1){
		userTeams.push(teamInput);
	}
}

function removeTeamFromUserList(tbFrom) {
    // find index of team to be removed
    var removeTeam = tbFrom.options[tbFrom.selectedIndex].value;
    var removeIndex;    
    var i;
    
    for (i = 0; i < userTeams.length; i++) {
        // check if team at index is team to remove
        if (userTeams[i] == removeTeam) {
            removeIndex = i;
            break;
        }
    }
    
    // splice list accordingly
	if(userTeams.length > 0){
		userTeams.splice(removeIndex,1);
	}
}

function addTeamToView(tbFrom, tbTo) {    
    var arrFrom = new Array(); var arrTo = new Array(); 
    var arrLU = new Array();
    var i;
    
    for (i = 0; i < tbTo.options.length; i++) {
        arrLU[tbTo.options[i].text] = tbTo.options[i].value;
        arrTo[i] = tbTo.options[i].text;
    }
    
    var fLength = 0;
    var tLength = arrTo.length;
    
    for(i = 0; i < tbFrom.options.length; i++) {
        arrLU[tbFrom.options[i].text] = tbFrom.options[i].value;
        
        if (tbFrom.options[i].selected && tbFrom.options[i].value != "") {
            if (contains(tbTo, tbFrom.options[i].text) == false) {
                //var saveButton = document.getElementById('saveButton');
                //toggleButton(saveButton, false);
                
                addTeamToUserList();
                
                arrTo[tLength] = tbFrom.options[i].text;
                tLength++;
            }
        } 
            
        arrFrom[fLength] = tbFrom.options[i].text;
        fLength++;        
    }

    tbFrom.length = 0;
    tbTo.length = 0;
    var ii;
    
    for(ii = 0; ii < arrFrom.length; ii++) {
        var no = new Option();
        no.value = arrLU[arrFrom[ii]];
        no.text = arrFrom[ii];
        tbFrom[ii] = no;
    }

    for(ii = 0; ii < arrTo.length; ii++) {
        var no = new Option();
        no.value = arrLU[arrTo[ii]];
        no.text = arrTo[ii];
        tbTo[ii] = no;
    }
}

function removeTeamFromView(tbFrom) {    
    var arrFrom = new Array();
    var arrLU = new Array();
    var i;
    
    var fLength = 0;
    
    for(i = 0; i < tbFrom.options.length; i++) {
        arrLU[tbFrom.options[i].text] = tbFrom.options[i].value;
        
        if (!tbFrom.options[i].selected && tbFrom.options[i].value != "") {
            arrFrom[fLength] = tbFrom.options[i].text;
            fLength++;
        } else {
            //var saveButton = document.getElementById('saveButton');
            //toggleButton(saveButton, false);
            removeTeamFromUserList(tbFrom);
        }
    }

    tbFrom.length = 0;
    var ii;
    
    for(ii = 0; ii < arrFrom.length; ii++) {
        var no = new Option();
        no.value = arrLU[arrFrom[ii]];
        no.text = arrFrom[ii];
        tbFrom[ii] = no;
    }
}

function saveTeams(form) {
    //var saveButton = document.getElementById('saveButton');
    //toggleButton(saveButton, true);
      
    var teamsStr = "";
    
	var team;
	for(team in userTeams){
		teamsStr = teamsStr + userTeams[team] + ",";
	}
    
    var xmlHttp = createXmlHttp();
    
    postParameters(xmlHttp, '/saveTeams', 'userTeams='+teamsStr);
    
    alert("Your teams were successfully saved!");
}

function createTeamOptions() {
    var league = document.getElementById("leagues");
    var leagueInput = leagues.options[leagues.selectedIndex].text;
    
    var xmlHttp = createXmlHttp();

    // onreadystatechange will be called every time the state of the XML HTTP object changes
    xmlHttp.onreadystatechange = function() {
        // we really only care about 4 (response complete) here.
        if (xmlHttp.readyState == 4) {
            var i = 0;
            // we parse the content of the response
            var json = JSON.parse(xmlHttp.responseText);
            var teams = json.teams;
            var teamsSelect = document.getElementById("teams");
            var teamsSelectHTML = '';
            var option_str = '';
            
            while (teams[i] != null) {                        
                name = teams[i].location + ' ' + teams[i].mascot;
                var value_str = leagueInput.toUpperCase() + '-' + name;
                option_str = '<option value="' + value_str +'">' + name + '</option>';
                teamsSelectHTML = teamsSelectHTML + option_str;
                i++;
            }
            
            teamsSelect.innerHTML = teamsSelectHTML;
            teamsSelect.setAttribute("size", teams.length);
            teamsSelect.style.display = 'block';
        }
    }
    postParameters(xmlHttp, '/teamsAjax', 'league='+leagueInput);
}