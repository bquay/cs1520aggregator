function team(league, name) {
    this.league = league;
    this.name = name;
}

var userTeams = [];

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

function createTeamsDropDown() {
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
            var teamsSelectHTML = '<option disabled="disabled" selected="selected"></option>';
            var option_str = '';
            
            while (teams[i] != null) {                        
                name = teams[i].location + ' ' + teams[i].mascot;
                option_str = '<option value="' + name +'">' + name + '</option>';
                console.log(option_str);
                teamsSelectHTML = teamsSelectHTML + option_str;
                i++;
            }
            
            teamsSelect.innerHTML = teamsSelectHTML;
            teamsSelect.style.display = 'block';
        }
    }
    postParameters(xmlHttp, '/teamsAjax', 'league='+leagueInput);
}

function addTeam() {
	var displayTeams = document.getElementById('selectedTeams');
	var leagues = document.getElementById('leagues');
    var leagueInput = leagues.options[leagues.selectedIndex].text;
	
	var teams = document.getElementById('teams');
	var teamInput = teams.options[teams.selectedIndex].text;

	var newTeam = leagueInput + "-" + teamInput;
	
	if(userTeams.indexOf(newTeam) <= -1){
		userTeams.push(newTeam);
	}
	var stringTeam = "";
	for(oldTeam in userTeams){
		stringTeam = stringTeam + userTeams[oldTeam] + "<br>";
	}
    
    teams.style.display = "none";
    teams.innerHTML = "";
	displayTeams.innerHTML = stringTeam;
}

function removeTeam(){
	if(userTeams.length > 0){
		userTeams.splice((userTeams.length-1),1);
	}
	
	var displayTeams = document.getElementById('selectedTeams');
	var stringTeam = "";
	var oldTeam;
	for(oldTeam in userTeams){
		stringTeam = stringTeam + userTeams[oldTeam] + "<br>";
	}
	displayTeams.innerHTML = stringTeam;
}

function saveTeams(form) {
    var teamsToAdd = document.getElementById('teamsToAdd');
    
    var teamsStr = "";
    
	var team;
	for(team in userTeams){
		teamsStr = teamsStr + userTeams[team] + "-";
	}
    
    teamsToAdd.value = teamsStr;
    
    form.submit();
}

function setLeagueAndTeamAndSubmitForm(form) {
    var leagues = document.getElementById('leagues');
    var leagueInput = document.getElementById('league');
	leagueInput.value = leagues.options[leagues.selectedIndex].text;
	
	var teams = document.getElementById('teams');
	var teamInput = document.getElementById('team');
	teamInput.value = teams.options[teams.selectedIndex].text;
	
	form.submit();
}

function changeFeed(form) {
	var teams = document.getElementById('teams');
	var teamInput = document.getElementById('team');
	teamInput.value = teams.options[teams.selectedIndex].text;
	
	form.submit();
}