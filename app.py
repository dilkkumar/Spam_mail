from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)

# Load the trained model and vectorizer
try:
    model = joblib.load('spam_detector_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
except Exception as e:
    print(f"Error loading model/vectorizer: {e}")
    model, vectorizer = None, None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None or vectorizer is None:
        return jsonify({"error": "Model or vectorizer not loaded properly."}), 500

    data = request.get_json()
    email_text = data.get("email")

    if not email_text:
        return jsonify({"error": "No email text provided."}), 400

    try:
        # Vectorize the input email text using the loaded vectorizer
        vectorized_text = vectorizer.transform([email_text])
        
        # Predict whether the email is spam (1) or not spam (0)
        prediction = model.predict(vectorized_text)[0]
        
        # Return the result based on the prediction
        result = "Spam" if prediction == 1 else "Not Spam"
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

