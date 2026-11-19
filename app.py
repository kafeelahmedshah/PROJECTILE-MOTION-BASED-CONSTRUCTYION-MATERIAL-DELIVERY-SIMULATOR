
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Projectile Motion Simulator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #071426, #102d46);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.hero {
    background: linear-gradient(120deg, #123b5a, #087e8b);
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 20px;
}
.hero h1 {
    font-size: 34px;
    color: white;
}
.hero p {
    font-size: 17px;
}
.metric-card {
    background: #173653;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #26758a;
}
.team-card {
    background: #102c43;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #26758a;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- PROJECT HEADER ----------------
st.markdown("""
<div class="hero">
<h1>🏗️ PROJECTILE MOTION</h1>
<h2>Construction Material Delivery Simulator</h2>
<p>University Physics Project | Interactive Simulation</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 👨‍🎓 Project Development Team")

team = [
    "BSPHY-2025-017",
    "BSPHY-2025-044",
    "BSPHY-2025-006",
    "BSPHY-2025-002"
]

cols = st.columns(4)
for col, roll in zip(cols, team):
    with col:
        st.markdown(
            f'<div class="team-card"><b>{roll}</b></div>',
            unsafe_allow_html=True
        )

st.divider()

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.title("⚙️ Simulation Controls")

st.sidebar.subheader("Launch Position")
x0 = st.sidebar.number_input("Initial X position (m)", 0.0, 1000.0, 0.0)
y0 = st.sidebar.number_input("Launch height (m)", 0.0, 500.0, 10.0)

st.sidebar.subheader("Projectile Parameters")
velocity = st.sidebar.slider("Initial velocity (m/s)", 1.0, 100.0, 30.0)
angle = st.sidebar.slider("Launch angle (degrees)", 1, 89, 45)
gravity = st.sidebar.slider("Gravity (m/s²)", 1.0, 20.0, 9.81)

st.sidebar.subheader("Target")
target_x = st.sidebar.number_input("Target horizontal position (m)", 0.0, 2000.0, 70.0)
target_y = st.sidebar.number_input("Landing height (m)", 0.0, 500.0, 0.0)

st.sidebar.subheader("Presentation")
projector_mode = st.sidebar.checkbox("Large text presentation mode", False)

# ---------------- PHYSICS CALCULATIONS ----------------
theta = math.radians(angle)

ux = velocity * math.cos(theta)
uy = velocity * math.sin(theta)

discriminant = uy**2 + 2 * gravity * (y0 - target_y)

if discriminant < 0:
    st.error("The projectile cannot reach the selected landing height. Adjust the inputs.")
    st.stop()

flight_time = (uy + math.sqrt(discriminant)) / gravity

max_height = y0 + (uy**2 / (2 * gravity))
range_x = ux * flight_time
landing_x = x0 + range_x

horizontal_range = range_x

# ---------------- RESULTS ----------------
st.markdown("## 📊 Live Physics Results")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Time of Flight", f"{flight_time:.2f} s")
c2.metric("Maximum Height", f"{max_height:.2f} m")
c3.metric("Horizontal Range", f"{horizontal_range:.2f} m")
c4.metric("Horizontal Velocity", f"{ux:.2f} m/s")

st.metric("Predicted Landing Position", f"{landing_x:.2f} m")

if abs(landing_x - target_x) <= 2:
    st.success("🎯 Target reached within 2 metres!")
else:
    st.warning(
        f"Target difference: {abs(landing_x-target_x):.2f} metres. "
        "Adjust the launch settings to improve accuracy."
    )

# ---------------- TRAJECTORY DATA ----------------
t = np.linspace(0, flight_time, 150)

x = x0 + ux * t
y = y0 + uy * t - 0.5 * gravity * t**2

y = np.maximum(y, target_y)

# ---------------- ANIMATED GRAPH ----------------
st.markdown("## 🚀 Live Projectile Motion Simulator")

st.write(
    "The graph displays the trajectory of a construction material "
    "in an ideal projectile-motion model."
)

if "animation_running" not in st.session_state:
    st.session_state.animation_running = False

play_col, pause_col, reset_col = st.columns(3)

with play_col:
    if st.button("▶ Play Animation", use_container_width=True):
        st.session_state.animation_running = True

with pause_col:
    if st.button("⏸ Pause", use_container_width=True):
        st.session_state.animation_running = False

with reset_col:
    if st.button("↺ Reset", use_container_width=True):
        st.session_state.animation_running = False

if st.session_state.animation_running:
    position = st.slider(
        "Animation position",
        min_value=0,
        max_value=149,
        value=0,
        key="animation_position"
    )
else:
    position = st.slider(
        "Move projectile manually",
        min_value=0,
        max_value=149,
        value=0,
        key="manual_position"
    )

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode="lines",
    name="Projectile trajectory",
    line=dict(color="#00E5FF", width=4)
))

fig.add_trace(go.Scatter(
    x=[x0],
    y=[y0],
    mode="markers",
    name="Launch point",
    marker=dict(size=13, color="green")
))

fig.add_trace(go.Scatter(
    x=[target_x],
    y=[target_y],
    mode="markers",
    name="Target",
    marker=dict(size=15, color="red", symbol="x")
))

fig.add_trace(go.Scatter(
    x=[x[position]],
    y=[y[position]],
    mode="markers",
    name="Moving material",
    marker=dict(size=18, color="orange")
))

fig.update_layout(
    template="plotly_dark",
    height=520,
    title="Projectile Trajectory",
    xaxis_title="Horizontal Distance (metres)",
    yaxis_title="Vertical Height (metres)",
    legend=dict(orientation="h"),
    paper_bgcolor="#102d46",
    plot_bgcolor="#071426"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- CURRENT POSITION ----------------
current_time = t[position]
current_x = x[position]
current_y = y[position]
current_vy = uy - gravity * current_time

current_speed = math.sqrt(ux**2 + current_vy**2)

st.markdown("### 📍 Current Projectile Position")

p1, p2, p3, p4 = st.columns(4)
p1.metric("Time", f"{current_time:.2f} s")
p2.metric("X Position", f"{current_x:.2f} m")
p3.metric("Y Position", f"{current_y:.2f} m")
p4.metric("Speed", f"{current_speed:.2f} m/s")

# ---------------- THEORY ----------------
st.divider()
st.markdown("## 📚 Physics Theory")

st.markdown("""
### 1. Projectile Motion

Projectile motion is the motion of an object thrown into the air
under the influence of gravity.

Examples:
- A ball thrown into the air.
- Material delivered from an elevated platform.
- Water flowing from a fountain.

### 2. Horizontal Component

Horizontal velocity remains constant when air resistance is ignored.

\[
u_x = u\\cos\\theta
\]

### 3. Vertical Component

Initial vertical velocity is:

\[
u_y = u\\sin\\theta
\]

Vertical acceleration:

\[
a_y = -g
\]

### 4. Time of Flight

For a landing height equal to the ground level:

\[
T = \\frac{u\\sin\\theta +
\\sqrt{(u\\sin\\theta)^2+2g(y_0-y_g)}}{g}
\]

### 5. Maximum Height

\[
H = y_0 + \\frac{u^2\\sin^2\\theta}{2g}
\]

### 6. Horizontal Range

\[
R = u\\cos\\theta \\times T
\]

### 7. Trajectory Equation

\[
y = y_0 + (x-x_0)\\tan\\theta
- \\frac{g(x-x_0)^2}{2u^2\\cos^2\\theta}
\]

### 8. Acceleration Due to Gravity

Near Earth's surface:

\[
g = 9.81\\ m/s^2
\]
""")

# ---------------- DERIVATIONS ----------------
st.markdown("## 🧮 Mathematical Derivations")

with st.expander("Derivation of Horizontal Motion"):
    st.write("Horizontal acceleration is zero.")
    st.latex(r"a_x=0")
    st.latex(r"v_x=u_x=u\cos\theta")
    st.latex(r"x=x_0+u\cos\theta \ t")

with st.expander("Derivation of Vertical Motion"):
    st.write("Vertical acceleration is constant and downward.")
    st.latex(r"a_y=-g")
    st.latex(r"v_y=u\sin\theta-gt")
    st.latex(r"y=y_0+u\sin\theta \ t-\frac{1}{2}gt^2")

with st.expander("Derivation of Maximum Height"):
    st.write("At maximum height, vertical velocity becomes zero.")
    st.latex(r"v_y=0")
    st.latex(r"0=u_y^2-2g(H-y_0)")
    st.latex(r"H=y_0+\frac{u^2\sin^2\theta}{2g}")

with st.expander("Derivation of Time of Flight"):
    st.write("Put the landing height into the vertical position equation.")
    st.latex(r"y_g=y_0+u_yT-\frac{1}{2}gT^2")
    st.latex(r"\frac{1}{2}gT^2-u_yT-(y_0-y_g)=0")
    st.latex(
        r"T=\frac{u_y+\sqrt{u_y^2+2g(y_0-y_g)}}{g}"
    )

# ---------------- VECTOR ANALYSIS ----------------
st.markdown("## 🧭 Vector Analysis")

v1, v2 = st.columns(2)

with v1:
    st.markdown("### Horizontal Component")
    st.latex(r"V_x=u\cos\theta")
    st.metric("Horizontal velocity", f"{ux:.2f} m/s")
    st.metric("Horizontal acceleration", "0 m/s²")

with v2:
    st.markdown("### Vertical Component")
    st.latex(r"V_y=u\sin\theta-gt")
    st.metric("Initial vertical velocity", f"{uy:.2f} m/s")
    st.metric("Vertical acceleration", f"{-gravity:.2f} m/s²")

# ---------------- DISTANCE AND DISPLACEMENT ----------------
st.markdown("## 📏 Distance and Displacement")

st.write(
    f"Horizontal displacement: {range_x:.2f} m"
)

vertical_displacement = target_y - y0
displacement = math.sqrt(range_x**2 + vertical_displacement**2)

st.write(f"Vertical displacement: {vertical_displacement:.2f} m")
st.write(f"Resultant displacement: {displacement:.2f} m")
st.write(
    "Distance travelled is the length of the curved trajectory, "
    "not the straight-line displacement."
)

# ---------------- DATA TABLE ----------------
st.markdown("## 📋 Simulation Data")

data = pd.DataFrame({
    "Time (s)": t,
    "Horizontal Position (m)": x,
    "Vertical Position (m)": y,
    "Horizontal Velocity (m/s)": np.full(len(t), ux),
    "Vertical Velocity (m/s)": uy - gravity * t
})

st.dataframe(data, use_container_width=True)

csv = data.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Simulation CSV",
    data=csv,
    file_name="projectile_motion_results.csv",
    mime="text/csv"
)

# ---------------- PRESENTATION MODE ----------------
st.divider()
st.markdown("## 🎤 Presentation Mode")

default_intro = (
    "Our project demonstrates projectile motion through a construction "
    "material delivery simulator. It explains how velocity, launch angle "
    "and gravity determine the motion of an object."
)

default_script = (
    "First, we select the initial velocity and launch angle. "
    "The simulator calculates horizontal and vertical velocity. "
    "Next, it displays the trajectory, time of flight, maximum height "
    "and horizontal range. This model demonstrates the principles "
    "of two-dimensional projectile motion."
)

intro = st.text_area("Edit Project Introduction", default_intro)
script = st.text_area("Edit Presentation Speech", default_script)

st.markdown("### Project Introduction")
st.write(intro)

st.markdown("### Presentation Speech")
st.write(script)

# ---------------- ASSUMPTIONS ----------------
st.divider()
st.markdown("## ⚠️ Model Assumptions")

st.write("""
- Air resistance is ignored.
- Gravity is constant.
- Earth is treated as a flat reference plane.
- The projectile is treated as a point object.
- Material mass does not change the ideal trajectory.
- This is an educational simulation, not a real construction-site
  delivery or material-launching system.
""")

st.success("Projectile Motion Simulator loaded successfully.")
st.caption("University Physics Project | Educational Simulation")
