from flask import Flask, render_template, request, url_for
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI rendering
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)

def generate_plots(N, mu, sigma2, S):

    # STEP 1
    # TODO 1: Generate a random dataset X of size N with values between 0 and 1
    # and a random dataset Y with normal additive error (mean mu, variance sigma^2).
    # Hint: Use numpy's random's functions to generate values for X and Y
    X = np.random.uniform(0, 1, N)  # Generate random values for X between 0 and 1
    Y = np.random.normal(loc=mu, scale=np.sqrt(sigma2), size=N)  # Generate Y with specified mean and variance

    # TODO 2: Fit a linear regression model to X and Y
    # Hint: Use Scikit Learn
    model = LinearRegression()  # Initialize the model
    model.fit(X.reshape(-1, 1), Y)  # Fit the model
    slope = model.coef_[0]  # Extract slope from the fitted model
    intercept = model.intercept_  # Extract intercept from the fitted model

    # TODO 3: Generate a scatter plot of (X, Y) with the fitted regression line
    # Hint: Use Matplotlib
    # Label the x-axis as "X" and the y-axis as "Y".
    # Add a title showing the regression line equation using the slope and intercept values.
    # Finally, save the plot to "static/plot1.png" using plt.savefig()
    plot1_path = "static/plot1.png"
    plt.figure()
    plt.scatter(X, Y, color='blue', alpha=0.5, label='Data')
    X_line = np.linspace(0, 1, 100)
    Y_line = slope * X_line + intercept
    plt.plot(X_line, Y_line, color='red', label='Regression Line')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Regression Line: Y = {slope:.2f} * X + {intercept:.2f}")
    plt.legend()
    plt.savefig(plot1_path)
    plt.close()
    
    # Step 2: Run S simulations and create histograms of slopes and intercepts

    # TODO 1: Initialize empty lists for slopes and intercepts
    # Hint: You will store the slope and intercept of each simulation's linear regression here.
    slopes = []  # Initialize empty list for slopes
    intercepts = []  # Initialize empty list for intercepts

    # TODO 2: Run a loop S times to generate datasets and calculate slopes and intercepts
    # Hint: For each iteration, create random X and Y values using the provided parameters
    for _ in range(S):
        # TODO: Generate random X values with size N between 0 and 1
        X_sim = np.random.uniform(0, 1, N)  # Generate X values

        # TODO: Generate Y values with normal additive error (mean mu, variance sigma^2)
        Y_sim = np.random.normal(loc=mu, scale=np.sqrt(sigma2), size=N)  # Generate Y values

        # TODO: Fit a linear regression model to X_sim and Y_sim
        sim_model = LinearRegression()  # Initialize model
        sim_model.fit(X_sim.reshape(-1, 1), Y_sim)  # Fit model

        # TODO: Append the slope and intercept of the model to slopes and intercepts lists
        slopes.append(sim_model.coef_[0])  # Append slope
        intercepts.append(sim_model.intercept_)  # Append intercept

    # Plot histograms of slopes and intercepts
    plt.figure(figsize=(10, 5))
    plt.hist(slopes, bins=20, alpha=0.5, color="blue", label="Slopes")
    plt.hist(intercepts, bins=20, alpha=0.5, color="orange", label="Intercepts")
    plt.axvline(slope, color="blue", linestyle="--", linewidth=1, label=f"Slope: {slope:.2f}")
    plt.axvline(intercept, color="orange", linestyle="--", linewidth=1, label=f"Intercept: {intercept:.2f}")
    plt.title("Histogram of Slopes and Intercepts")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plot2_path = "static/plot2.png"
    plt.savefig(plot2_path)
    plt.close()

    # Below code is already provided
    # Calculate proportions of more extreme slopes and intercepts
    # For slopes, we will count how many are greater than the initial slope; for intercepts, count how many are less.
    slope_more_extreme = sum(s > slope for s in slopes) / S  # Already provided
    intercept_more_extreme = sum(i < intercept for i in intercepts) / S  # Already provided

    return plot1_path, plot2_path, slope_more_extreme, intercept_more_extreme

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input as strings to pass back to the template
        N = request.form["N"]
        mu = request.form["mu"]
        sigma2 = request.form["sigma2"]
        S = request.form["S"]

        # Convert inputs to appropriate data types for calculations
        N_int = int(N)
        mu_float = float(mu)
        sigma2_float = float(sigma2)
        S_int = int(S)

        # Ensure the 'static' directory exists
        if not os.path.exists('static'):
            os.makedirs('static')

        # Generate plots and results
        plot1, plot2, slope_extreme, intercept_extreme = generate_plots(N_int, mu_float, sigma2_float, S_int)

        return render_template(
            "index.html",
            plot1=plot1,
            plot2=plot2,
            slope_extreme=slope_extreme,
            intercept_extreme=intercept_extreme,
            N=N,
            mu=mu,
            sigma2=sigma2,
            S=S
        )

    else:
        # For GET request, set default values
        return render_template("index.html", N='', mu='', sigma2='', S='')


if __name__ == "__main__":
    app.run(debug=True, port=3000)
