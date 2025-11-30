import os
import sys
from flask import Flask, render_template, request, url_for
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# -----------------------------
# Create upload folder
# -----------------------------
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -----------------------------
# Load Models
# -----------------------------
def load_all_models():
    """Load all models with proper error handling and relative paths."""
    cob_model_files = [
        ("ResNet50", "resnet50_cob.h5", (250, 250)),
        ("MobileNetV2", "mobilenetv2_cob.h5", (224, 224)),
        ("VGG16", "vgg16_cob.h5", (224, 224)),
        ("DenseNet201", "densenet201_cob.h5", (224, 224)),
        ("InceptionV3", "inceptionv3_cob.h5", (299, 299))
    ]
    leaf_model_files = [
        ("ResNet50", "resnet50_leaf.h5", (250, 250)),
        ("MobileNetV2", "mobilenetv2_leaf.h5", (224, 224)),
        ("VGG16", "vgg16_leaf.h5", (224, 224)),
        ("DenseNet201", "densenet201_leaf.h5", (224, 224)),
        ("InceptionV3", "inceptionv3_leaf.h5", (299, 299))
    ]
    
    cob_models = []
    leaf_models = []
    
    # Load cob models
    for name, filename, size in cob_model_files:
        model_path = os.path.join(BASE_DIR, filename)
        if os.path.exists(model_path):
            try:
                model = load_model(model_path)
                cob_models.append((name, model, size))
                print(f"✓ Loaded {name} (Cob)")
            except Exception as e:
                print(f"✗ Error loading {name} (Cob): {e}")
        else:
            print(f"✗ Model file not found: {model_path}")
    
    # Load leaf models
    for name, filename, size in leaf_model_files:
        model_path = os.path.join(BASE_DIR, filename)
        if os.path.exists(model_path):
            try:
                model = load_model(model_path)
                leaf_models.append((name, model, size))
                print(f"✓ Loaded {name} (Leaf)")
            except Exception as e:
                print(f"✗ Error loading {name} (Leaf): {e}")
        else:
            print(f"✗ Model file not found: {model_path}")
    
    if not cob_models:
        print("WARNING: No cob models loaded!")
    if not leaf_models:
        print("WARNING: No leaf models loaded!")
    
    return cob_models, leaf_models

print("Loading models...")
cob_models, leaf_models = load_all_models()
print(f"Loaded {len(cob_models)} cob models and {len(leaf_models)} leaf models")

cob_classes = ['Damaged', 'Maize', 'NotVertical', 'Vertical']
leaf_classes = ['Blight', 'Common_Rust', 'Gray_Leaf_Spot', 'Healthy']

# -----------------------------
# Preprocessing
# -----------------------------
def preprocess(img, size):
    img = img.resize(size)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    return np.expand_dims(img_array, axis=0)

# -----------------------------
# Prediction Helper
# -----------------------------
def run_prediction(models, classes, img, filename, mode):
    results = []

    for model_name, model, size in models:
        processed_img = preprocess(img, size)
        prediction = model.predict(processed_img, verbose=0)
        predicted_class = classes[np.argmax(prediction)]
        confidence = float(np.max(prediction)) * 100
        results.append({
            "Model": model_name,
            "Prediction": predicted_class,
            "Confidence (%)": confidence
        })

    df = pd.DataFrame(results)

    # Get best prediction
    best_result = df.loc[df["Confidence (%)"].idxmax()].to_dict()

    # Save uploaded image to static/uploads
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    img.save(save_path)
    img_url = url_for("static", filename=f"uploads/{filename}")

    # Plotly chart as HTML
    fig = px.bar(df, x="Model", y="Confidence (%)", color="Prediction", text="Prediction",
                 title=f"Corn {mode} Model Confidence Comparison")
    fig.update_traces(textposition="outside")
    graph_html = pio.to_html(fig, full_html=False)

    return df.to_dict(orient="records"), best_result, graph_html, img_url

# -----------------------------
# Flask Routes
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict_cob", methods=["POST"])
def predict_cob():
    if not cob_models:
        return "No cob models available. Please ensure model files are present.", 500
    if "file" not in request.files:
        return "No file uploaded", 400
    file = request.files["file"]
    if file.filename == "":
        return "No file selected", 400
    
    try:
        img = Image.open(file).convert("RGB")
        results, best_result, graph_html, img_url = run_prediction(
            cob_models, cob_classes, img, file.filename, "Cob"
        )
        return render_template("result.html",
                               results=results,
                               best_result=best_result,
                               graph_html=graph_html,
                               img_url=img_url,
                               mode="Cob")
    except Exception as e:
        return f"Error processing image: {str(e)}", 500

@app.route("/predict_leaf", methods=["POST"])
def predict_leaf():
    if not leaf_models:
        return "No leaf models available. Please ensure model files are present.", 500
    if "file" not in request.files:
        return "No file uploaded", 400
    file = request.files["file"]
    if file.filename == "":
        return "No file selected", 400
    
    try:
        img = Image.open(file).convert("RGB")
        results, best_result, graph_html, img_url = run_prediction(
            leaf_models, leaf_classes, img, file.filename, "Leaf"
        )
        return render_template("result.html",
                               results=results,
                               best_result=best_result,
                               graph_html=graph_html,
                               img_url=img_url,
                               mode="Leaf")
    except Exception as e:
        return f"Error processing image: {str(e)}", 500

if __name__ == "__main__":
    # Check if models are loaded
    if not cob_models and not leaf_models:
        print("\n" + "="*50)
        print("ERROR: No models loaded!")
        print("Please ensure all model .h5 files are in the same directory as app.py")
        print("="*50 + "\n")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("Starting Flask application...")
    print("Access the application at: http://localhost:5001")
    print("="*50 + "\n")
    app.run(host="0.0.0.0", port=5001, debug=True)
