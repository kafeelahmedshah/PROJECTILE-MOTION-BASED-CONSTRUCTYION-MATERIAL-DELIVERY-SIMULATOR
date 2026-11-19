# Projectile Motion Based Construction Material Delivery Simulator

An interactive Streamlit web application that demonstrates projectile motion through a construction-material delivery scenario.

## Features

- Adjust initial velocity, launch angle, launch height, gravity, and target distance.
- Visualize the projectile trajectory and landing point.
- Calculate time of flight, maximum height, horizontal range, and time to peak.
- Inspect position, velocity components, speed, and displacement at a selected time.
- View a motion data table and download it as CSV.
- Assess whether the projectile lands within the selected target tolerance.
- Review the physics concepts and ideal-model assumptions.

## Project files

- `app.py` — Streamlit application
- `requirements.txt` — Python dependencies
- `README.md` — project documentation

## Run locally

1. Install Python 3.9 or later.
2. Open a terminal in this project folder.
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

5. Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Deploy using GitHub and Streamlit Community Cloud

1. Create a new public GitHub repository.
2. Upload `app.py`, `requirements.txt`, and `README.md` to the repository's root folder.
3. Sign in to Streamlit Community Cloud using your GitHub account.
4. Select **Create app** and choose your repository, branch, and `app.py` as the main file.
5. Click **Deploy**.

## Physics model

The application assumes ideal projectile motion with no air resistance.

Let:
- `u` = initial velocity (m/s)
- `theta` = launch angle
- `h0` = launch height (m)
- `g` = gravitational acceleration (m/s²)
- `t` = time (s)

Velocity components:

- `Vx = u cos(theta)`
- `Vy = u sin(theta) - gt`

Position:

- `x = (u cos(theta))t`
- `y = h0 + (u sin(theta))t - 0.5gt²`

For landing at ground level (`y = 0`), the positive time of flight is:

`T = (u sin(theta) + sqrt((u sin(theta))² + 2gh0)) / g`

Maximum height:

`Hmax = h0 + (u sin(theta))² / (2g)`

Horizontal range:

`R = (u cos(theta))T`

## Important limitation

This is an educational physics simulator, not a real-world construction-site delivery system. It does not model air resistance, wind, material shape, tumbling, collisions, obstacles, or equipment constraints. Do not use its results to plan or operate real material launches.


## Project development team

- BSPHY-2025-017
- BSPHY-2025-044
- BSPHY-2025-006
- BSPHY-2025-002
