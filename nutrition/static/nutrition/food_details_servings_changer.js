/**
 * Created by ian on 3/19/16.
 */

function onClick() {

    var defServingOption = document.getElementById("serving_select");
    var servingCountBox = document.getElementById("servings");

    var scalar = defServingOption.options[defServingOption.selectedIndex].value * servingCountBox.value;

    var calories = Math.round(document.getElementById("defcalories").value * scalar);
    var carbs = Math.round(document.getElementById("defcarb").value * scalar);
    var fat = Math.round(document.getElementById("deffat").value * scalar);
    var pro = Math.round(document.getElementById("defpro").value * scalar);
    var vita = Math.round(document.getElementById("defvita").value * scalar);
    var vitc = Math.round(document.getElementById("defvitc").value * scalar);
    var iron = Math.round(document.getElementById("defiron").value * scalar);
    var calc = Math.round(document.getElementById("defcalc").value * scalar);

    document.getElementById("calories").innerHTML = "Calories: " + calories + " kcal";
    document.getElementById("carbs").innerHTML = "Carbohydrates: " + carbs + " g";
    document.getElementById("fat").innerHTML = "Fat: " + fat + " g";
    document.getElementById("protein").innerHTML = "Protein: " + pro + " g";
    document.getElementById("vita").innerHTML = "Vitamin A: " + vita + "% DV";
    document.getElementById("vitc").innerHTML = "Vitamin C: " + vitc + "% DV";
    document.getElementById("iron").innerHTML = "Iron: " + iron + "% DV";
    document.getElementById("calc").innerHTML = "Calcium: " + calc + "% DV";

}