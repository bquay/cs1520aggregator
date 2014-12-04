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


function setLeagueAndTeamAndSubmitForm(form) {
    var leagues = document.getElementById('leagues');
    var leagueInput = document.getElementById('league');
	leagueInput.value = leagues.options[leagues.selectedIndex].text;
	
	var teams = document.getElementById('teams');
	var teamInput = document.getElementById('team');
    if (teams.options[teams.selectedIndex] == null || teams.options[teams.selectedIndex].text == '') {
        alert('Please select a league and a team.');
    } else {
        teamInput.value = teams.options[teams.selectedIndex].text;
        form.submit();
    }
	
	form.submit();
}

function changeFeed(form) {
	var teams = document.getElementById('teams');
	var teamInput = document.getElementById('team');
	teamInput.value = teams.options[teams.selectedIndex].text;
	
	form.submit();
}

function moreArticles(offset, team)
{
    var league = document.getElementById("content");
    
    var xmlHttp = createXmlHttp();
    // onreadystatechange will be called every time the state of the XML HTTP object changes
    xmlHttp.onreadystatechange = function() {
        // we really only care about 4 (response complete) here.
        if (xmlHttp.readyState == 4) {
            var i = 0;
            // we parse the content of the response
            //console.log(xmlHttp.responseText);
            try
            {
                var json = xmlHttp.responseText.substr(0, xmlHttp.responseText.lastIndexOf(',')) + "]}";
            
                var json_parsed = JSON.parse(json);
                var articles = json_parsed.articles;

                var contentDiv = document.getElementById("content");
                var newArticles = '<table style="width:100%" align="center" cellpadding="10px" cellspacing="5px"><tr>';
                while (articles[i] != null) {                        
					if ((i != 0) && (i%3==0) ){
						newArticles += "</tr><tr>";
					}
					newArticles += '<td class="articleTable">';
					if( articles[i].image != null){
						newArticles += '<div class="displayArticle"><img class="articleImg" src="'+ articles[i].image +'"/></div>';
					}
                    newArticles += '<div class="articleTitle"><a href="'+articles[i].link+'" target="_blank"><h2>'+articles[i].headline+'</h2></a></div>';
					newArticles += "</td>";
                    i++;
                }
				newArticles += "</tr></table>";
                contentDiv.innerHTML = contentDiv.innerHTML + newArticles;
            } catch (err)
            {
                console.log("None left");
                var contentDiv = document.getElementById("content");
                contentDiv.innerHTML += "There are no more articles related to the" +  team + "<br>";
            }
        }
    }
    postParameters(xmlHttp, '/getMoreArticles', 'offset='+ offset + '&team=' + team);
}