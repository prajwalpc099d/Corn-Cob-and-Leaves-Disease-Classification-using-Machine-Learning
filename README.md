# 🌽 Corn Disease Classification Web Application

A Flask-based web application for classifying corn diseases using multiple deep learning models. The application supports both corn cob and corn leaf disease classification.

## Features

- **Multiple Model Support**: Uses 5 different deep learning architectures (ResNet50, MobileNetV2, VGG16, DenseNet201, InceptionV3)
- **Dual Classification**: Separate models for corn cob and corn leaf disease detection
- **Interactive Results**: Visual comparison of model predictions with confidence scores
- **Modern UI**: Beautiful glassmorphic design with responsive layout

## Prerequisites

- **Python 3.8, 3.9, 3.10, or 3.11** (Python 3.12+ may have compatibility issues with TensorFlow 2.15.0)
- All model files (.h5 files) in the project root directory
- Minimum 4GB RAM (8GB+ recommended for loading all models)
- Disk space: ~2GB for dependencies + model files

## Required Model Files

The application requires the following model files to be present in the root directory:

**Corn Cob Models:**
- `resnet50_cob.h5`
- `mobilenetv2_cob.h5`
- `vgg16_cob.h5`
- `densenet201_cob.h5`
- `inceptionv3_cob.h5`

**Corn Leaf Models:**
- `resnet50_leaf.h5`
- `mobilenetv2_leaf.h5`
- `vgg16_leaf.h5`
- `densenet201_leaf.h5`
- `inceptionv3_leaf.h5`

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Upgrade pip (recommended):**
   ```bash
   pip install --upgrade pip
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note:** Installation may take 10-15 minutes as TensorFlow is a large package (~500MB). 
   Ensure you have a stable internet connection.

6. **Ensure all model files (.h5) are in the root directory**

7. **Ensure the background image exists:**
   - Place `img.jpg` in the `static/` directory (optional, for background)

## Running the Application

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your web browser and navigate to:**
   ```
   http://localhost:5001
   ```

3. **Upload an image:**
   - Choose either "Upload Corn Cob Image" or "Upload Corn Leaf Image"
   - Select an image file
   - Click the predict button
   - View the results with model predictions and confidence scores

## Project Structure

```
GUI/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── *.h5                        # Model files (10 total)
├── static/
│   ├── img.jpg                # Background image (optional)
│   └── uploads/               # Uploaded images (auto-created)
└── templates/
    ├── index.html             # Main upload page
    └── result.html            # Results display page
```

## Corn Cob Classes

- Damaged
- Maize
- NotVertical
- Vertical

## Corn Leaf Classes

- Blight
- Common_Rust
- Gray_Leaf_Spot
- Healthy

## Troubleshooting

### Models Not Loading
- Ensure all .h5 model files are in the same directory as `app.py`
- Check the console output for specific error messages
- Verify that TensorFlow is properly installed

### Port Already in Use
- Change the port in `app.py` (line 137) from `5001` to another port (e.g., `5002`)

### Missing Dependencies
- Run `pip install -r requirements.txt` again
- Ensure you're using the correct Python version (3.8-3.11 recommended)
- If TensorFlow installation fails, try: `pip install tensorflow==2.15.0 --no-cache-dir`
- For Apple Silicon (M1/M2 Macs), you may need: `pip install tensorflow-macos==2.15.0` instead

### Version Compatibility Issues
- **TensorFlow 2.15.0** is required for loading the trained .h5 models
- **NumPy 1.24.3** is required (NumPy 2.0+ is incompatible with TensorFlow 2.15.0)
- If you encounter version conflicts, create a fresh virtual environment and install from requirements.txt

### Image Upload Issues
- Ensure the `static/uploads/` directory exists (it will be created automatically)
- Check file permissions

## Notes

- The application will work even if some model files are missing (it will use available models)
- Uploaded images are saved in `static/uploads/` for display
- The application runs in debug mode by default (change `debug=True` to `debug=False` in production)

## License

This project is provided as-is for educational and research purposes.

