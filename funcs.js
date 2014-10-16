var numTeams = 1;
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

var nbaTeams = [
            {
                location: "Atlanta",
                mascot: "Hawks"
            },
			{
                location: "Boston",
                mascot: "Celtics"
            },
			{
                location: "Charlotte",
                mascot: "Bobcats"
            },
			{
                location: "Chicago",
                mascot: "Bulls"
            },
			{
                location: "Cleveland",
                mascot: "Cavaliers"
            },
			{
                location: "Dallas",
                mascot: "Mavericks"
            },
			{
                location: "Denver",
                mascot: "Nuggets"
            },
			{
                location: "Detroit",
                mascot: "Pistons"
            },
			{
                location: "Golden State",
                mascot: "Warriors"
            },
			{
                location: "Houston",
                mascot: "Rockets"
            },
			{
                location: "Indiana",
                mascot: "Pacers"
            },
			{
                location: "LA",
                mascot: "Clippers"
            },
			{
                location: "LA",
                mascot: "Lakers"
            },
			{
                location: "Memphis",
                mascot: "Grizzlies"
            },
			{
                location: "Miami",
                mascot: "Heat"
            },
			{
                location: "Milwaukee",
                mascot: "Timberwolves"
            },
			{
                location: "New Jersey",
                mascot: "Nets"
            },
			{
                location: "New Orleans",
                mascot: "Hornets"
            },
			{
                location: "New York",
                mascot: "Knicks"
            },
			{
                location: "Oklahoma City",
                mascot: "Thunder"
            },
			{
                location: "Orlando",
                mascot: "Magic"
            },
			{
                location: "Philadelphia",
                mascot: "Sixers"
            },
			{
                location: "Phoenix",
                mascot: "Suns"
            },
			{
                location: "Portland",
                mascot: "Trail Blazers"
            },
			{
                location: "Sacramento",
                mascot: "Kings"
            },
			{
                location: "San Antonio",
                mascot: "Spurs"
            },
			{
                location: "Toronto",
                mascot: "Raptors"
            },
			{
                location: "Utah",
                mascot: "Jazz"
            },
			{
                location: "Washington",
                mascot: "Wizards"
            }
		];

var nflTeams = [
			{
                location: "Arizona",
                mascot: "Cardinals"
            },
			{
                location: "Atlanta",
                mascot: "Falcons"
            },
			{
                location: "Baltimore",
                mascot: "Ravens"
            },
			{
                location: "Buffalo",
                mascot: "Bills"
            },
			{
                location: "Carolina",
                mascot: "Panthers"
            },
			{
                location: "Chicago",
                mascot: "Bears"
            },
			{
                location: "Cincinnati",
                mascot: "Bengals"
            },
			{
                location: "Cleveland",
                mascot: "Browns"
            },
			{
                location: "Dallas",
                mascot: "Cowboys"
            },
			{
                location: "Denver",
                mascot: "Broncos"
            },
			{
                location: "Detroit",
                mascot: "Lions"
            },
			{
                location: "Green Bay",
                mascot: "Packers"
            },
			{
                location: "Houston",
                mascot: "Texans"
            },
			{
                location: "Indianapolis",
                mascot: "Colts"
            },
			{
                location: "Jacksonville",
                mascot: "Jaguars"
            },
			{
                location: "Kansas City",
                mascot: "Chiefs"
            },
			{
                location: "Miami",
                mascot: "Dolphins"
            },
			{
                location: "Minnesota",
                mascot: "Vikings"
            },
			{
                location: "New England",
                mascot: "Patriots"
            },
			{
                location: "New Orleans",
                mascot: "Saints"
            },
			{
                location: "New York",
                mascot: "Giants"
            },
			{
                location: "New York",
                mascot: "Jets"
            },
			{
                location: "Oakland",
                mascot: "Raiders"
            },
			{
                location: "Philadelphia",
                mascot: "Eagles"
            },
			{
                location: "Pittsburgh",
                mascot: "Steelers"
            },
			{
                location: "Saint Louis",
                mascot: "Rams"
            },
			{
                location: "San Diego",
                mascot: "Chargers"
            },
			{
                location: "San Francisco",
                mascot: "49ers"
            },
			{
                location: "Seattle",
                mascot: "Seahawks"
            },
			{
                location: "Tampa Bay",
                mascot: "Buccaneers"
            },
			{
                location: "Tennessee",
                mascot: "Titans"
            },
			{
                location: "Washington",
                mascot: "Redskins"
            }
		];
		
var nhlTeams = [
			{
                location: "Anaheim",
                mascot: "Ducks"
            },
			{
                location: "Atlanta",
                mascot: "Thrashers"
            },
			{
                location: "Boston",
                mascot: "Bruins"
            },
			{
                location: "Buffalo",
                mascot: "Sabres"
            },
			{
                location: "Calgary",
                mascot: "Flames"
            },
			{
                location: "Carolina",
                mascot: "Hurricanes"
            },
			{
                location: "Chicago",
                mascot: "Blackhawks"
            },
			{
                location: "Colorado",
                mascot: "Avalanche"
            },
			{
                location: "Columbus",
                mascot: "Blue Jackets"
            },
			{
                location: "Dallas",
                mascot: "Stars"
            },
			{
                location: "Detroit",
                mascot: "Red Wings"
            },
			{
                location: "Edmonton",
                mascot: "Oilers"
            },
			{
                location: "Florida",
                mascot: "Panthers"
            },
			{
                location: "Los Angeles",
                mascot: "Kings"
            },
			{
                location: "Minnesota",
                mascot: "Wild"
            },
			{
                location: "Montreal",
                mascot: "Canadiens"
            },
			{
                location: "Nashville",
                mascot: "Predators"
            },
			{
                location: "New Jersey",
                mascot: "Devils"
            },
			{
                location: "New York",
                mascot: "Islanders"
            },
			{
                location: "New York",
                mascot: "Rangers"
            },
			{
                location: "Ottawa",
                mascot: "Senators"
            },
			{
                location: "Philadelphia",
                mascot: "Flyers"
            },
			{
                location: "Phoenix",
                mascot: "Coyotes"
            },
			{
                location: "Pittsburgh",
                mascot: "Penguins"
            },
			{
                location: "Saint Louis",
                mascot: "Blues"
            },
			{
                location: "San Jose",
                mascot: "Sharks"
            },
			{
                location: "Tampa Bay",
                mascot: "Lightning"
            },
			{
                location: "Toronto",
                mascot: "Maple Leafs"
            },
			{
                location: "Vancouver",
                mascot: "Canucks"
            },
			{
                location: "Washington",
                mascot: "Capitals"
            }
		];
		
function populateTeams(league) {
	var x = 0, options, option_str, name, teams;
	options = '<option disabled="disabled" selected="selected"></option>';

	if (league === 'mlb') {
		teams = mlbTeams;
		//teams = JSON.parse(mlbTeams);
	} else if (league === 'nba') {
		teams = nbaTeams;
		//teams = JSON.parse(nbaTeams);
	} else if (league === 'nfl') {
		teams = nflTeams;
		//teams = JSON.parse(nflTeams);
	} else if (league === 'nhl') {
		teams = nhlTeams;
		//teams = JSON.parse(nhlTeams);
	} else{}
	
	while (teams[x] != null) {
		name = teams[x].location + ' ' + teams[x].mascot;
		option_str = '<option value="' + name +'">' + name + '</option>';
		console.log(option_str);
		options = options + option_str;
		x++;
	}
	return options;
}

function createTeamsDropDown() {
	var league = document.getElementById('leagues'+ numTeams).value;
	var teamSelect = document.getElementById('teams'+ numTeams);
	teamSelect.innerHTML = populateTeams(league);
	teamSelect.style.display = "block";
}

function showResults() {
	var leagues = document.getElementById('leagues' + numTeams);
	var league = leagues.options[leagues.selectedIndex].text;
	
	var teams = document.getElementById('teams' + numTeams);
	var team = teams.options[teams.selectedIndex].text;
	
	var search = league + ' - ' + team;
	
	var results = document.getElementById('results');
	results.innerHTML = '<p>' + search + '</p>';
}

function showResultsAll() {
	for (i = numTeams; i > 0; i--) {
		var leagues = document.getElementById('leagues' + i);
		var league = leagues.options[leagues.selectedIndex].text;
	
		var teams = document.getElementById('teams' + i);
		var team = teams.options[teams.selectedIndex].text;
	
		var search = league + ' - ' + team;
	
		var results = document.getElementById('results');
		results.innerHTML = results.innerHTML + '<br><p>' + search + '</p>';
	}
}

function addTeam(){
	numTeams++;
	var searchForm = document.getElementById('search');
	var newLine = document.createElement('div');
	newLine.setAttribute('id',"break" + numTeams);
	newLine.innerHTML = "<br><br>";
	searchForm.appendChild(newLine);
	var leagueSelect = document.createElement('select');
	leagueSelect.setAttribute('id','leagues' + numTeams);
	leagueSelect.setAttribute('onchange',"createTeamsDropDown();");
	var leagueString = "<option disabled=\"disabled\" selected=\"selected\"></option>";
	leagueString = leagueString + "<optgroup label=\"Professional\">";
	leagueString = leagueString + "<option value=\"mlb\">MLB</option>";
	leagueString = leagueString + "<option value=\"nba\">NBA</option>";
	leagueString = leagueString + "<option value=\"nfl\">NFL</option>";
	leagueString = leagueString + "<option value=\"nhl\">NHL</option>";
	leagueString = leagueString + "</optgroup>";
	leagueString = leagueString + "<optgroup label=\"NCAA\">";
	leagueString = leagueString + "<option value=\"baseball\">Baseball</option>";
	leagueString = leagueString + "<option value=\"softball\">Softball</option>";
	leagueString = leagueString + "<option value=\"football\">Football</option>";
	leagueString = leagueString + "<option value=\"hockey\">Hockey</option>";
	leagueString = leagueString + "<option value=\"womens-basketball\">Women's Basketball</option>";
	leagueString = leagueString + "<option value=\"mens-basketball\">Men's Basketball</option>";
	leagueString = leagueString + "</optgroup>";
	leagueSelect.innerHTML = leagueString;
	searchForm.appendChild(leagueSelect);
	var teamSelect = document.createElement('select');
	teamSelect.setAttribute('id','teams'+numTeams);
	teamSelect.innerHTML = "<option disabled=\"disabled\" selected=\"selected\"></option>";
	teamSelect.style.display ='none';
	searchForm.appendChild(teamSelect);
}

function removeTeam(){
	var searchForm = document.getElementById('search');
	var leagueSelect = document.getElementById('leagues' +numTeams);
	var teamSelect = document.getElementById('teams' +numTeams);
	var breaks = document.getElementById('break' + numTeams);
	searchForm.removeChild(leagueSelect);
	searchForm.removeChild(teamSelect);
	searchForm.removeChild(breaks);
	numTeams--;
}