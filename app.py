from flask import Flask, render_template, request
from src.pipeline.prediction_pipeline import PredictionPipeline, CustomeClass

app = Flask(__name__)

# Define the route for the homepage
@app.route("/", methods=["GET", "POST"])
def prediction_data():
    if request.method == "GET":
        return render_template("home.html")
    
    else:
        # Collecting form data from the user
        data = CustomeClass(
            annual_inc = float(request.form.get("annual_inc")),
            loan_amnt = float(request.form.get("loan_amnt")),
            grade = request.form.get("grade"),
            term = request.form.get("term"),
            dti = float(request.form.get("dti")),
            home_ownership = request.form.get("home_ownership"),
            emp_length = request.form.get("emp_length"),
        )

        # Getting data in the correct format
        final_data = data.get_data_DataFrame()

        # Prediction Pipeline
        pipeline_prediction = PredictionPipeline()
        pred = pipeline_prediction.predict(final_data)

        # Interpret the result
        if pred == 0:
            return render_template("results.html", final_result="Your loan is charged off: {}".format(pred))
        elif pred == 1:
            return render_template("results.html", final_result="Your loan is fully paid: {}".format(pred))
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)