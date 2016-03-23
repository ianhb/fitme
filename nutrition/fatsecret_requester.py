import os

from fatsecret import Fatsecret

from nutrition.models import Food, Serving

fs = Fatsecret(os.environ['fs_consumer'], os.environ['fs_secret'])


def search(query):
    foods = fs.foods_search(query)
    db_foods = Food.objects.all()
    return_foods = []
    for food in foods:
        fs_id = food['food_id']
        try:
            return_foods.append(db_foods.get(fs_id=fs_id))
        except Food.DoesNotExist:
            food = get_food(fs_id)
            if food is not None:
                return_foods.append(food)
    return return_foods


def get_food(fs_id):
    details = fs.food_get(fs_id)
    if 'brand' in details:
        name = details['brand'] + details['food_name']
    else:
        name = details['food_name']

    if 'serving_id' in details['servings']['serving']:
        head_serving = details['servings']['serving']
        one_serving = True

    else:
        head_serving = details['servings']['serving'][0]
        one_serving = False

    good_servings = []

    if 'metric_serving_unit' in head_serving and head_serving['metric_serving_unit'] == 'g':
        if one_serving:
            if 'metric_serving_unit' in head_serving and head_serving['metric_serving_unit'] == 'g':
                multiplyer = float(head_serving['metric_serving_amount']) / 100.0
                serv_desc = head_serving['serving_description']
                good_servings.append((serv_desc, multiplyer))
        else:
            for servings in details['servings']['serving']:
                if 'metric_serving_unit' in servings and servings['metric_serving_unit'] == 'g':
                    multiplyer = float(servings['metric_serving_amount']) / 100.0
                    serv_desc = servings['serving_description']
                    good_servings.append((serv_desc, multiplyer))
        multiplyer = 100.0 / float(head_serving['metric_serving_amount'])
        calories = int(round(float(head_serving['calories']) * multiplyer))
        carbs = int(round(float(head_serving['carbohydrate']) * multiplyer))
        fat = int(round(float(head_serving['fat']) * multiplyer))
        protein = int(round(float(head_serving['protein']) * multiplyer))
        if 'calcium' in head_serving:
            calcium = int(round(float(head_serving['calcium']) * multiplyer))
        else:
            calcium = 0
        if 'iron' in head_serving:
            iron = int(round(float(head_serving['iron']) * multiplyer))
        else:
            iron = 0
        if 'vitamin_a' in head_serving:
            vita = int(round(float(head_serving['vitamin_a']) * multiplyer))
        else:
            vita = 0
        if 'vitamin_c' in head_serving:
            vitc = int(round(float(head_serving['vitamin_c']) * multiplyer))
        else:
            vitc = 0

        if len(good_servings) > 0:
            new_food = Food(name=name, fs_id=fs_id, calories_per_100g=calories, carbohydrates_per_100g=carbs,
                            fat_per_100g=fat, protein_per_100g=protein, vitamin_a_per_100g=vita, vitamin_c_per_100g=vitc,
                            iron_per_100g=iron, calcium_per_100g=calcium)
            new_food.save()
            for desc, mult in good_servings:
                Serving(food=new_food, name=desc, scalar=mult).save()

            return new_food
    return None
