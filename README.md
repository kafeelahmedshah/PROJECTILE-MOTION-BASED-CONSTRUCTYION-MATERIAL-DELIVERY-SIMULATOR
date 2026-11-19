# Projectile Motion Based Construction Material Delivery Simulator

Interactive, projector-friendly Streamlit application for demonstrating projectile motion through a construction-material delivery example.

## Project Development Team
- BSPHY-2025-017
- BSPHY-2025-044
- BSPHY-2025-006
- BSPHY-2025-002

## Features
- Editable project title, introduction paragraph and presentation explanation in the sidebar.
- Large-text mode for projector presentations.
- Adjustable initial velocity, launch angle, launch height, gravity, target distance and target tolerance.
- Live projectile trajectory graph with launch, target and landing markers.
- Time of flight, maximum height, horizontal range and time-to-peak calculations.
- Time slider to inspect position, speed and displacement.
- Explanations and equations for all requested physics concepts.
- Vector diagram and analysis of distance, displacement, velocity and acceleration.
- Presentation mode and CSV summary download.

## Files
- `app.py` — Streamlit application
- `requirements.txt` — Python dependencies
- `README.md` — documentation

## Run locally
1. Install Python 3.9 or later.
2. Open a terminal in this folder.
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `streamlit run app.py`
5. Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Deploy using GitHub and Streamlit Community Cloud
1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, and `README.md` to its root.
3. Sign in at https://share.streamlit.io/ using GitHub.
4. Select **Create app**, choose your repository and branch, and set `app.py` as the main file.
5. Click **Deploy**.

## Physics equations
Let `u` be initial speed, `theta` launch angle, `h0` launch height, `g` gravitational acceleration and `t` time.

- `ux = u cos(theta)`
- `uy = u sin(theta)`
- `x(t) = ux * t`
- `y(t) = h0 + uy*t - 0.5*g*t^2`
- `T = (uy + sqrt(uy^2 + 2*g*h0)) / g`
- `Hmax = h0 + uy^2/(2*g)`
- `R = ux*T`
- `ax = 0`, `ay = -g`

For equal launch and landing heights, `R = u^2 sin(2*theta)/g`.

## Assumptions and limitations
This is an ideal educational model. It ignores air resistance, wind, object rotation, tumbling, collisions and obstacles. The object is treated as a point mass and the landing surface is level with the ground reference. Do not use it to plan or operate real construction-material launches.
