import os
import time
import uuid
from flask import Flask, render_template, request, jsonify
from mlgan.generator.run import run as build_generator
from mlgan.core import data_sources
from technic import ganImage
from pathlib import Path
import ast

app = Flask(__name__)
app.secret_key = 'dev key'

config = data_sources.load_yaml(Path("../config/generator/complete_floorplan.yaml"))
config["settings"]["input_shape"] = ast.literal_eval(
    config["settings"]["input_shape"]
)

generator = build_generator(config)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():

    filename = f"{str(uuid.uuid4())}"
    image = request.files['image']
    image_ext = image.filename.rsplit('.', 1)[1].lower()
    new_image_filename = f"{filename}.{image_ext}"
    new_image_path = os.path.join('static/image/user', new_image_filename)

    image.save(new_image_path)
    image_path = f'/static/image/user/{new_image_filename}'  # Chemin de l'image enregistrée


    return jsonify({'imagePath': image_path})


@app.route('/AI', methods=['POST'])
def send_data_to_ia():
    print("Envoie des données vers l'IA")
    test1 = "static\image\IA\Plan.jpg"
    test2 = ""
    if request.method == "POST":
        data = { 'image' : request.json['img_plan'], 'surface_total': request.json['surface_total'], 'liste_piece': request.json['liste_piece']}
        print(data)
        time.sleep(5.5)
        # Envoyer la data et récupérer les images ici !
        urls = ganImage.ganFloorPlan(generator, data)
        test2 = {"plan1": urls[1], "plan2": urls[2], "plan3": urls[3] }
        print({'plans': urls})

    return jsonify({'plans': test2})  # envoyer les chemins des images


@app.route('/like', methods=['POST'])
def like():
    print("Envoie le like vers l'IA")
    if request.method == "POST":
        data = {'like': request.json['Like']}
        print(data)
        # Envoyer le like à l'IA ici !
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
