var userTeams = [];
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
                mascot: "Hornets"
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
                mascot: "Bucks"
            },
            {
                location: "Minnesota",
                mascot: "Timberwolves"
            },
			{
                location: "New Jersey",
                mascot: "Nets"
            },
			{
                location: "New Orleans",
                mascot: "Pelicans"
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
	var league = document.getElementById('leagues').value;
	var teamSelect = document.getElementById('teams');
	teamSelect.innerHTML = populateTeams(league);
	teamSelect.style.display = "block";
}

function addTeam() {
	var displayTeams = document.getElementById('selectedTeams');
	var leagues = document.getElementById('leagues');
    var leagueInput = leagues.options[leagues.selectedIndex].text;
	
	var teams = document.getElementById('teams');
	var teamInput = teams.options[teams.selectedIndex].text;

	var newTeam = leagueInput + " " + teamInput;
	
	if(userTeams.indexOf(newTeam) <= -1){
		userTeams.push(newTeam);
	}
	var stringTeam = "";
	for(oldTeam in userTeams){
		stringTeam = stringTeam + userTeams[oldTeam] + "<br>";
	}
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

function chooseTeams() {
    var formElement = document.getElementById('addTeamForm');
    
    var leagues = document.getElementById('leagues');
    var leagueInput = document.getElementById('league');
	leagueInput.value = leagues.options[leagues.selectedIndex].text;
	
	var teams = document.getElementById('teams');
	var teamInput = document.getElementById('team');
	teamInput.value = teams.options[teams.selectedIndex].text;
	
	formElement.submit();
}