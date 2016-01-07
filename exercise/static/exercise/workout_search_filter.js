/**
 * Created by Ian on 1/7/2016.
 */

function onClick(workout_json) {

    var muscle_boxes = document.getElementsByClassName("muscle_box");
    var text_box = document.getElementById("name_search");

    var search_text = text_box.value.toLowerCase();

    var i;
    var muscles = [];

    for (i = 0; i < muscle_boxes.length; i++) {
        if (muscle_boxes[i].checked) {
            muscles.push(muscle_boxes[i].value);
        }
    }

    console.log(muscles);
    console.log(search_text);

    var filtered_workouts = [];

    for (i = 0; i < workout_json.length; i++) {
        var workout = workout_json[i];
        if (muscle_overlap(workout['muscles_worked'], muscles) && (workout['name'].toLowerCase().indexOf(search_text) > -1)) {
            filtered_workouts.push(workout);
        }
    }

    console.log(filtered_workouts);

    var list = $('#workout_list');
    list.find('li').remove();
    list = document.getElementById('workout_list');
    for (i = 0; i < filtered_workouts.length; i++) {
        var li = document.createElement('li');
        var link = document.createElement('a');
        link.setAttribute('href', '/exercise/workout/' + filtered_workouts[i]['pk']);
        link.appendChild(document.createTextNode(filtered_workouts[i]['name']));
        li.appendChild(link);
        list.appendChild(li);
    }
}


function muscle_overlap(workout_muscles, checked_muscles) {
    for (var i = 0; i < workout_muscles.length; i++) {
        for (var j = 0; j < checked_muscles.length; j++) {
            if (checked_muscles[j] == workout_muscles[i]) {
                return true;
            }
        }
    }
    return false;
}

