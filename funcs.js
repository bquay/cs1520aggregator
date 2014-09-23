'use strict';

function createTeamDropDown(league) {
  var x = 0, options, option_str, name;

  if (league === 'MLB') {
    teams = JSON.parse(mlbTeams);
	console.out(teams);
  } else if (league === 'NBA') {
    teams = JSON.parse(nbaTeams);
  } else if (league === 'NFL') {
    teams = JSON.parse(nflTeams);
  } else if (league === 'NHL') {
    teams = JSON.parse(nhlTeams);
  }

  while (teams.teams[x] != NULL) {
    name = teams.teams[x].location + ' ' + teams.teams[x].mascot;
    option_str = '<option value="' + name +'">' + name + '</option>';
    options = options + option_str;
	x++;
  }

  return options;
}