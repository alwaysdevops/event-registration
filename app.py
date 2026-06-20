from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "change-this-in-production"

EVENTS = [
    {"id": 1, "name": "Python Conference 2026"},
    {"id": 2, "name": "Data Science Workshop"},
    {"id": 3, "name": "Cloud DevOps Meetup"},
]
REGISTRATIONS = []

HOME_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Event Registration</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; }
    form, table { max-width: 700px; margin-bottom: 2rem; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; }
    .flash { color: green; margin-bottom: 1rem; }
  </style>
</head>
<body>
  <h1>Event Registration</h1>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <div class="flash">{{ messages[0] }}</div>
    {% endif %}
  {% endwith %}

  <section>
    <h2>Available Events</h2>
    <table>
      <thead>
        <tr><th>ID</th><th>Event</th></tr>
      </thead>
      <tbody>
        {% for event in events %}
          <tr><td>{{ event.id }}</td><td>{{ event.name }}</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </section>

  <section>
    <h2>Register for an Event</h2>
    <form method="post" action="{{ url_for('register') }}">
      <div>
        <label for="name">Name</label><br>
        <input type="text" id="name" name="name" required>
      </div>
      <div>
        <label for="email">Email</label><br>
        <input type="email" id="email" name="email" required>
      </div>
      <div>
        <label for="event_id">Event</label><br>
        <select id="event_id" name="event_id" required>
          <option value="">Select an event</option>
          {% for event in events %}
            <option value="{{ event.id }}">{{ event.name }}</option>
          {% endfor %}
        </select>
      </div>
      <div style="margin-top: 1rem;">
        <button type="submit">Register</button>
      </div>
    </form>
  </section>

  <section>
    <h2>Recent Registrations</h2>
    {% if registrations %}
      <table>
        <thead>
          <tr><th>Name</th><th>Email</th><th>Event</th></tr>
        </thead>
        <tbody>
          {% for registration in registrations %}
            <tr>
              <td>{{ registration.name }}</td>
              <td>{{ registration.email }}</td>
              <td>{{ registration.event_name }}</td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    {% else %}
      <p>No registrations yet.</p>
    {% endif %}
  </section>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HOME_TEMPLATE, events=EVENTS, registrations=REGISTRATIONS)

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    event_id = request.form.get("event_id")

    if not name or not email or not event_id:
        flash("All fields are required.")
        return redirect(url_for("index"))

    selected_event = next((e for e in EVENTS if str(e["id"]) == event_id), None)
    if selected_event is None:
        flash("Selected event is invalid.")
        return redirect(url_for("index"))

    registration = {
        "name": name,
        "email": email,
        "event_id": selected_event["id"],
        "event_name": selected_event["name"],
    }
    REGISTRATIONS.append(registration)
    flash(f"Thanks, {name}! You have registered for {selected_event['name']}.")
    return redirect(url_for("index"))

@app.route("/api/events")
def api_events():
    return {"events": EVENTS}

@app.route("/api/registrations")
def api_registrations():
    return {"registrations": REGISTRATIONS}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
