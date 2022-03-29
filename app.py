from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('model.sav', 'rb'))


@app.route('/', methods=('GET', 'POST'))
def create():
    if request.method == "POST":
        req = request.form
        result = process(req)
        return render_template('result.html', text=result)
    return render_template('create.html')


def process(data):
    year = data['year']
    mileage = data['mileage']
    condition = 1
    brand_dict = encoding(data['brand'],
                          ['bmw', 'buick', 'cadillac', 'chevrolet', 'chrysler', 'dodge', 'ford', 'gmc', 'heartland',
                           'honda',
                           'hyundai', 'infiniti', 'jeep', 'kia', 'mercedes-benz', 'nissan', 'other_brand'])

    state_dict = encoding(data['state'], ['alabama', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut',
                                          'florida', 'georgia', 'illinois', 'indiana', 'kentucky', 'louisiana',
                                          'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'nevada',
                                          'new jersey', 'new york', 'north carolina', 'ohio', 'oklahoma', 'oregon',
                                          'other_state', 'pennsylvania', 'south carolina', 'tennessee', 'texas', 'utah',
                                          'virginia', 'washington', 'west virginia', 'wisconsin'])
    status_dict = encoding(data['title_status'], ['clean vehicle', 'salvage insurance'])

    color_dict = encoding(data['color'], ['beige', 'black', 'blue', 'brown', 'charcoal', 'gold', 'gray', 'green',
                                          'magnetic metallic', 'no_color', 'orange', 'other_color', 'red',
                                          'shadow black', 'silver', 'white', 'yellow'])
    overall_dict = {'year': year, 'mileage': mileage, 'condition': condition}
    overall_dict.update(brand_dict)
    overall_dict.update(state_dict)
    overall_dict.update(status_dict)
    overall_dict.update(color_dict)

    observation = pd.DataFrame(overall_dict, index=[0])
    pred = model.predict(observation)
    return pred[0]

def encoding(cur_value, l_vaues):
    val_dict = {}
    for br in l_vaues:
        if cur_value == br:
            val_dict[br] = 1
        else:
            val_dict[br] = 0
    return val_dict


if __name__ == "__main__":
    app.debug = True
    app.run()
