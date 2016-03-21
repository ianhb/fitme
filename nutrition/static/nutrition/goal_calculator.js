/**
 * Created by ian on 3/21/16.
 */

function msj(age, gender, weight, height) {
    var msj = ((10 * weight) + (6.25 * height) - (5 * age));
    if (gender == 'M') {
        msj += 5;
    } else {
        msj -= 161;
    }
    return Math.round(msj);
}

function kma(weight, body_fat) {
    var lbm = Number(weight) - (Number(weight) * Number(body_fat) / 100.0);
    var kma = 370 + (21.6 * lbm);
    return Math.round(kma);
}

function onSuggestChange() {

    var ft = document.getElementById('ht_ft').value;
    var inch = document.getElementById('ht_in').value;
    var height = (Number(ft * 12) + Number(inch)) * (2.54);
    var gender = document.getElementById('gender').value.substr(0, 1);
    var age = document.getElementById('age').value;
    var weight = document.getElementById('weight').value / 2.2;
    var bf = document.getElementById('bf').value;

    var bmrval;
    var rmrval;

    if (weight != '') {
        bmrval = msj(age, gender, weight, height);
        document.getElementById('bmr').value = bmrval;
        if (bf != '') {
            rmrval = kma(weight, bf);
            document.getElementById('rmr').value = rmrval;
        }
    }

    var activity_box = document.getElementById('activity');
    var activity_val = activity_box.options[activity_box.selectedIndex].value;

    var goal_box = document.getElementById('goal');
    var goal_val = goal_box.options[goal_box.selectedIndex].value;

    var suggested_cals = 0;

    if (rmrval != null) {
        suggested_cals = Math.round(rmrval * Number(activity_val));
    } else
    if (bmrval != null) {
        suggested_cals = Math.round(bmrval * Number(activity_val));
    }

    switch (Number(goal_val)) {
        case 1:
            suggested_cals += Math.max(500, Math.round(suggested_cals * 0.2));
            break;
        case -1:
            suggested_cals -= Math.max(500, Math.round(suggested_cals * 0.2));
            break;
    }

    document.getElementById('suggested_cal').value = suggested_cals;
    document.getElementById('calorie_goal').value = suggested_cals;
    document.getElementById('diet_type').value = goal_val;
    onCalorieChange()

}

function onCalorieChange() {
    var calories = document.getElementById('calorie_goal');
    var carb_box = document.getElementById('carb_grams');
    var fat_box = document.getElementById('fat_grams');
    var protein_box = document.getElementById('protein_grams');

    carb_box.value = Math.round(Number(document.getElementById('carb_percent').value)/100.0 * Number(calories.value) / 4);
    fat_box.value = Math.round(Number(document.getElementById('fat_percent').value)/100.0 * Number(calories.value) / 9);
    protein_box.value = Math.round(Number(document.getElementById('protein_percent').value)/100.0 * Number(calories.value) / 4);

}

function onMacroChange(caller) {
    // TODO: implement changing percentages/grams changes other values
    var calories = document.getElementById('calorie_goal');
    var carb_box = document.getElementById('carb_grams');
    var fat_box = document.getElementById('fat_grams');
    var protein_box = document.getElementById('protein_percent');
    var carb_perc_box = document.getElementById('carb_percent');
    var fat_perc_box = document.getElementById('fat_percent');
    var protein_perc_box = document.getElementById('protein_percent');

    switch (caller) {
        case carb_box:
        case fat_box:
        case protein_box:
            break;
        case carb_perc_box:
        case fat_perc_box:
        case protein_perc_box:
            break;
    }

}
