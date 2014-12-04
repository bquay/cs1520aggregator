window.onbeforeunload = function clearSearch(e) {
    var leagueDisOption = document.getElementById('disabled');
    leagueDisOption.selected = true;
}