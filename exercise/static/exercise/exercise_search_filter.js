/**
 * Created by Ian on 1/4/2016.
 */


function onClick(exercises) {

    var name_box = document.getElementById('name_box');
    var name = name_box.value.toLowerCase();

    var muscle_box = document.getElementById('muscle_select');
    var muscle_pk = muscle_box.options[muscle_box.selectedIndex].value;

    var equipment_box = document.getElementById('equipment_select');
    var equipment_pk = equipment_box.options[equipment_box.selectedIndex].value;

    var filtered_exercises = [];
    var named_exercises = [];

    for (var i = 0; i < exercises.length; i++) {
        var exercise = exercises[i];
        if ((exercise['name'].toLowerCase().indexOf(name) != -1) && (muscle_pk == -1 || exercise['muscles_worked'] == muscle_pk) && (equipment_pk == -1 || exercise['equipment'] == equipment_pk)) {
            if ($.inArray(exercises[i]['pk'], filtered_exercises) === -1) {
                filtered_exercises.push(exercises[i]['pk']);
                named_exercises.push(exercises[i]['name']);
            }
        }
    }
    var list = $('#exercise_list');
    list.find('li').remove();
    list = document.getElementById('exercise_list');
    for (i = 0; i < filtered_exercises.length; i++) {
        var li = document.createElement('li');
        var link = document.createElement('a');
        link.setAttribute('href', "/exercise/exercise/" + filtered_exercises[i]);
        link.appendChild(document.createTextNode(named_exercises[i]));
        li.appendChild(link);
        list.appendChild(li);
    }

}