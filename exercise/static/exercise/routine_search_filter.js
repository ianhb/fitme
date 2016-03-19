/**
 * Created by ian on 3/18/16.
 */
function onClick(routine_json) {

    var text = document.getElementById("name_search");
    var diff = document.getElementById("diff");
    var type = document.getElementById("type");

    var filtered_routines = [];

    diff = diff.options[diff.selectedIndex].value;
    type = type.options[type.selectedIndex].value;
    var search_text = text.value.toLowerCase();

    console.log(routine_json);

    var i;

    for (i = 0; i < routine_json.length; i++) {
        var routine = routine_json[i];
        console.log(routine);
        if (routine['name'].toLowerCase().indexOf(search_text) > -1 && (routine['type'] == type || type == -1) &&
            (routine['difficulty'] == diff || diff == -1)) {
            filtered_routines.push(routine);
        }
    }

    var list = $('#routine_table');
    list.find('tr').remove();
    var table = document.getElementById('routine_table');
    var headRow = table.insertRow(0);
    var nameCell = headRow.insertCell(0);
    nameCell.innerHTML = "Name";
    var countCell = headRow.insertCell(1);
    countCell.innerHTML = "Followers";
    var typeCell = headRow.insertCell(2);
    typeCell.innerHTML = "Type";
    var diffCell = headRow.insertCell(3);
    diffCell.innerHTML = "Difficulty";
    for (i = 0; i < filtered_routines.length; i++) {
        var row = table.insertRow(i + 1);
        nameCell = row.insertCell(0);
        countCell = row.insertCell(1);
        typeCell = row.insertCell(2);
        diffCell = row.insertCell(3);
        var link = document.createElement('a');
        link.setAttribute('href', '/exercise/routine/' + filtered_routines[i]['pk']);
        link.appendChild(document.createTextNode(filtered_routines[i]['name']));
        nameCell.appendChild(link);
        countCell.innerText = filtered_routines[i]['follower_count'];
        switch (filtered_routines[i]['type']) {
            case 0:
                typeCell.innerHTML = "Transformation";
                break;
            case 1:
                typeCell.innerHTML = "Bulking";
                break;
            case 2:
                typeCell.innerHTML = "Cutting";
                break
        }
        switch (filtered_routines[i]['difficulty']) {
            case 0:
                diffCell.innerHTML = "Beginner";
                break;
            case 1:
                diffCell.innerHTML = "Intermediate";
                break;
            case 2:
                diffCell.innerHTML = "Advanced";
                break;
        }
    }
}

