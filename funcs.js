var mlbTeams = [
            {
                location: "Arizona",
                mascot: "Diamondbacks"
            },
            {
                location: "Atlanta",
                mascot: "Braves"
            },
            {
                location: "Baltimore",
                mascot: "Orioles"
            },
            {
                location: "Boston",
                mascot: "Red Sox"
            },
            {
                location: "Chicago",
                mascot: "White Sox"
            },
            {
                location: "Chicago",
                mascot: "Cubs"
            },
            {
                location: "Cincinnati",
                mascot: "Reds"
            },
            {
                location: "Cleveland",
                mascot: "Indians"
            },
            {
                location: "Colorado",
                mascot: "Rockies"
            },
            {
                location: "Detroit",
                mascot: "Tigers"
            },
            {
                location: "Florida",
                mascot: "Marlins"
            },
            {
                location: "Houston",
                mascot: "Astros"
            },
            {
                location: "Kansas City",
                mascot: "Royals"
            },
            {
                location: "Los Angeles",
                mascot: "Angels"
            },
            {
                location: "Los Angeles",
                mascot: "Dodgers"
            },
            {
                location: "Milwaukee",
                mascot: "Brewers"
            },
            {
                location: "Minnesota",
                mascot: "Twins"
            },
            {
                location: "New York",
                mascot: "Mets"
            },
            {
                location: "New York",
                mascot: "Yankees"
            },
            {
                location: "Oakland",
                mascot: "Athletics"
            },
            {
                location: "Philadelphia",
                mascot: "Phillies"
            },
            {
                location: "Pittsburgh",
                mascot: "Pirates"
            },
            {
                location: "San Diego",
                mascot: "Padres"
            },
            {
                location: "San Francisco",
                mascot: "Giants"
            },
            {
                location: "Seattle",
                mascot: "Mariners"
            },
            {
                location: "St. Louis",
                mascot: "Cardinals"
            },
            {
                location: "Tampa Bay",
                mascot: "Rays"
            },
            {
                location: "Texas",
                mascot: "Rangers"
            },
            {
                location: "Toronto",
                mascot: "Blue Jays"
            },
            {
                location: "Washington",
                mascot: "Nationals"
            }
        ];

function populateTeams(league) {
	var x = 0, options, option_str, name;
	options = '<option disabled="disabled" selected="selected"></option>';

	if (league === 'MLB') {
		teams = JSON.parse(mlbTeams);
	} else if (league === 'NBA') {
		teams = JSON.parse(mlbTeams);
	} else if (league === 'NFL') {
		teams = JSON.parse(mlbTeams);
	} else if (league === 'NHL') {
		teams = JSON.parse(mlbTeams);
	}
	// using mlbTeams because setting to teams var failed, as did using external JSON file
	while (mlbTeams[x] != null) {
		name = mlbTeams[x].location + ' ' + mlbTeams[x].mascot;
		option_str = '<option value="' + name +'">' + name + '</option>';
		console.log(option_str);
		options = options + option_str;
		x++;
	}

	return options;
}

function createTeamsDropDown(teams) {
	var league = document.getElementById('leagues').value;
	var teamSelect = document.getElementById('teams');
	// display team dropdown
	teamSelect.style.display = 'block';
	teamSelect.innerHTML = populateTeams(league);
	// display submit button
	var submit = document.getElementById('submit-search');
	submit.style.display = 'block';
}

function showResults() {
	var leagues = document.getElementById('leagues');
	var league = leagues.options[leagues.selectedIndex].text;
	
	var teams = document.getElementById('teams');
	var team = teams.options[teams.selectedIndex].text;
	
	var search = league + ' - ' + team;
	
	var results = document.getElementById('results');
	results.innerHTML = '<p>' + search + '</p>';
}