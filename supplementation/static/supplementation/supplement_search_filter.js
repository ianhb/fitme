/**
 * Created by Ian on 1/7/2016.
 */

function onClick(supplement_json) {

    var cat_box = document.getElementById("cat_select");
    var cat_pk = cat_box.options[cat_box.selectedIndex].value;

    var brand_box = document.getElementById("brand_select");
    var brand_pk = brand_box.options[brand_box.selectedIndex].value;

    var text_box = document.getElementById("name_search");
    var search_text = text_box.value.toLowerCase();

    var i;

    var filter_supplements = [];

    for (i = 0; i < supplement_json.length; i++) {
        var supplement = supplement_json[i];
        if ((cat_pk == -1 || supplement['category'] == cat_pk) && (brand_pk == -1 || supplement['brand'] == brand_pk) &&
            (supplement['name'].toLowerCase().indexOf(search_text) > -1)) {
            filter_supplements.push(supplement);
        }
    }

    var list = $('#supplement_list');
    list.find('li').remove();
    list = document.getElementById('supplement_list');
    for (i = 0; i < filter_supplements.length; i++) {
        var li = document.createElement('li');
        var link = document.createElement('a');
        link.setAttribute('href', '/supplementation/' + filter_supplements[i]['pk']);
        link.appendChild(document.createTextNode(filter_supplements[i]['name']));
        li.appendChild(link);
        list.appendChild(li);
    }
}