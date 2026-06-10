from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    user_name = "Ghezai"
    tasks_done = 4
    tasks_total = 7
    progress_percent = round((tasks_done / tasks_total) * 100)

    return render_template(
        "index.html",
        user_name=user_name,
        tasks_done=tasks_done,
        tasks_total=tasks_total,
        progress_percent=progress_percent,
    )


if __name__ == "__main__":
    app.run(debug=True)
