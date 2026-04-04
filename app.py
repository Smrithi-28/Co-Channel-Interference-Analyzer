from flask import Flask, render_template, request
from utils.cci_calc import calculate_si
from utils.grid_generator import generate_grid
from utils.chatbot import get_response
from utils.graph_generator import generate_sir_graph

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    si = si_db = None
    sir_graph = None
    chat_reply = None

    if request.method == 'POST':
        # Check which form was submitted
        if "N" in request.form:  # CCI Analyzer
            try:
                N = int(request.form['N'])
                n = float(request.form['n'])
                i0 = int(request.form['i0'])

                valid_N = [1, 3, 4, 7, 9]  # valid cluster sizes
                if N not in valid_N:
                    raise ValueError("Invalid cluster size N")

                # Calculate S/I
                si, si_db = calculate_si(N, n, i0)

                # Generate grid and S/I graph
                generate_grid(N, i0)
                generate_sir_graph(n, i0)
                sir_graph = "static/sir_plot.png"

            except ValueError as e:
                si = si_db = f"Error: {str(e)}"
                sir_graph = None

        elif "chat_message" in request.form:  # Chatbot
            msg = request.form['chat_message']
            try:
                chat_reply = get_response(msg)
            except Exception as e:
                chat_reply = f"Error: {str(e)}"

    return render_template('index.html', si=si, si_db=si_db, sir_graph=sir_graph, chat_reply=chat_reply)

if __name__ == "__main__":
    app.run(debug=True)