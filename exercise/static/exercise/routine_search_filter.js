/**
 * Created by ian on 3/18/16.
 */
function onClick(routine_json) {

    var text_box = document.getElementById("name_search");

    var search_text = text_box.value.toLowerCase();

    var i;

    var filtered_routines = [];

    for (i = 0; i < routine_json.length; i++) {
        var routine = routine_json[i];
        if (routine['name'].toLowerCase().indexOf(search_text) > -1) {
            filtered_routines.push(routine);
        }
    }

    console.log(filtered_routines);

    var list = $('#routine_table');
    list.find('tr').remove();
    var table = document.getElementById('routine_table');
    var headRow = table.insertRow(0);
    var nameCell = headRow.insertCell(0);
    nameCell.innerHTML = "Name";
    var countCell = headRow.insertCell(1);
    countCell.innerHTML = "Followers";
    for (i = 0; i < filtered_routines.length; i++) {
        var row = table.insertRow(i + 1);
        nameCell = row.insertCell(0);
        countCell = row.insertCell(1);
        var link = document.createElement('a');
        link.setAttribute('href', '/exercise/routine/' + filtered_routines[i]['pk']);
        link.appendChild(document.createTextNode(filtered_routines[i]['name']));
        nameCell.appendChild(link);
        countCell.innerText = filtered_routines[i]['follower_count'];
    }
}

