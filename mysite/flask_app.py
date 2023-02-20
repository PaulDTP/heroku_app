from flask import Flask, render_template
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    # Generate the plot data
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)

    # Generate the plot
    fig, ax = plt.subplots()
    ax.plot(x, y)

    # Save the plot to a buffer
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the buffer as a base64 string
    plts = base64.b64encode(buffer.getvalue()).decode()

    # Pass the plot to the template
    return render_template("index.html", plot_data=plts)