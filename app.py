import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Projectile Motion | Construction Material Delivery",
    page_icon="🏗️",
    layout="wide",
)

st.markdown("""
<style>
.main-header {font-size:2.1rem;font-weight:800;line-height:1.2;}
.sub-header {color:#64748b;font-size:1rem;}
.metric-card {padding:14px;border:1px solid rgba(128,128,128,.25);border-radius:12px;}
.small-note {font-size:.88rem;color:#64748b;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏗️ Projectile Motion Based Construction Material Delivery Simulator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">An interactive physics working model for understanding projectile motion and material delivery.</div>', unsafe_allow_html=True)

with st.expander("👥 Project Development Team", expanded=True):
    st.markdown("**Developed by the following team members:**")
    team_cols = st.columns(4)
    team_ids = ["BSPHY-2025-017", "BSPHY-2025-044", "BSPHY-2025-006", "BSPHY-2025-002"]
    for col, student_id in zip(team_cols, team_ids):
        col.markdown(f"**{student_id}**")

st.divider()

st.sidebar.header("⚙️ Simulation Controls")
st.sidebar.caption("Change the values to see how the projectile path changes.")

material = st.sidebar.selectbox(
    "Construction material",
    ["Brick", "Cement bag", "Sand bag", "Concrete block", "Other material"]
)
velocity = st.sidebar.slider("Initial velocity (m/s)", 1.0, 40.0, 20.0, 0.5)
angle_deg = st.sidebar.slider("Launch angle (degrees)", 1, 89, 45, 1)
launch_height = st.sidebar.slider("Launch height (m)", 0.0, 20.0, 2.0, 0.5)
gravity = st.sidebar.selectbox("Gravitational acceleration (m/s²)", [9.81, 9.80, 10.0], index=0)
target_distance = st.sidebar.slider("Construction target distance (m)", 1.0, 150.0, 30.0, 1.0)
tolerance = st.sidebar.slider("Target tolerance (m)", 0.5, 10.0, 2.0, 0.5)

theta = math.radians(angle_deg)
vx0 = velocity * math.cos(theta)
vy0 = velocity * math.sin(theta)

# Solve y(t) = h0 + vy0*t - 0.5*g*t^2 = 0 for the positive landing time.
discriminant = vy0**2 + 2 * gravity * launch_height
flight_time = (vy0 + math.sqrt(discriminant)) / gravity
range_x = vx0 * flight_time
max_height = launch_height + (vy0**2) / (2 * gravity)
time_to_peak = vy0 / gravity

# A safe time sample for plotting the complete trajectory.
times = np.linspace(0, flight_time, 300)
xs = vx0 * times
ys = launch_height + vy0 * times - 0.5 * gravity * times**2
ys = np.maximum(ys, 0)

# Distance travelled along the curved path, approximated numerically.
path_distance = float(np.sum(np.sqrt(np.diff(xs)**2 + np.diff(ys)**2)))

st.subheader("📊 Main Simulation Results")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Time of flight", f"{flight_time:.2f} s")
m2.metric("Maximum height", f"{max_height:.2f} m")
m3.metric("Horizontal range", f"{range_x:.2f} m")
m4.metric("Time to maximum height", f"{time_to_peak:.2f} s")

st.divider()
left, right = st.columns([1.65, 1])

with left:
    st.subheader("📈 Projectile Trajectory")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="lines", name="Projectile path",
        line=dict(width=4), hovertemplate="Distance: %{x:.2f} m<br>Height: %{y:.2f} m<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=[0, range_x], y=[launch_height, 0], mode="markers",
        name="Launch / landing", marker=dict(size=10),
        hovertemplate="x: %{x:.2f} m<br>y: %{y:.2f} m<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=[target_distance], y=[0], mode="markers+text",
        name="Construction target", marker=dict(size=15, symbol="x"),
        text=["Target"], textposition="top center"
    ))
    fig.add_hline(y=0, line_width=2, line_color="gray")
    fig.update_layout(
        xaxis_title="Horizontal distance (m)",
        yaxis_title="Vertical height (m)",
        height=470, template="plotly_white",
        legend=dict(orientation="h", y=1.12),
        margin=dict(l=10, r=10, t=35, b=10),
    )
    fig.update_xaxes(rangemode="tozero")
    fig.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("🎯 Delivery Assessment")
    error = abs(range_x - target_distance)
    if error <= tolerance:
        st.success(f"Target reached within tolerance!\n\nLanding error: {error:.2f} m")
    else:
        st.warning(f"Target missed.\n\nLanding error: {error:.2f} m")
    st.write(f"**Predicted landing position:** {range_x:.2f} m")
    st.write(f"**Target position:** {target_distance:.2f} m")
    st.write(f"**Difference:** {error:.2f} m")
    st.caption("Try adjusting the launch angle or initial velocity to bring the landing point closer to the target.")

st.divider()
st.subheader("⏱️ Inspect the Projectile at Any Time")
selected_time = st.slider(
    "Simulation time (seconds)", 0.0, float(flight_time),
    min(float(flight_time), float(flight_time / 2)),
    step=max(float(flight_time / 200), 0.001),
)
x_now = vx0 * selected_time
y_now = max(0.0, launch_height + vy0 * selected_time - 0.5 * gravity * selected_time**2)
vx_now = vx0
vy_now = vy0 - gravity * selected_time
speed_now = math.sqrt(vx_now**2 + vy_now**2)
displacement = math.sqrt(x_now**2 + (y_now - launch_height)**2)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Current horizontal position", f"{x_now:.2f} m")
c2.metric("Current vertical height", f"{y_now:.2f} m")
c3.metric("Current speed", f"{speed_now:.2f} m/s")
c4.metric("Displacement from launch", f"{displacement:.2f} m")

st.subheader("🧭 Vector Analysis")
v1, v2, v3 = st.columns(3)
v1.metric("Horizontal velocity (Vx)", f"{vx_now:.2f} m/s")
v2.metric("Vertical velocity (Vy)", f"{vy_now:.2f} m/s")
v3.metric("Acceleration due to gravity", f"{gravity:.2f} m/s² downward")

st.markdown("#### Velocity components")
st.latex(r"V_x = u\cos\theta")
st.latex(r"V_y = u\sin\theta - gt")
st.markdown("#### Position equations")
st.latex(r"x = (u\cos\theta)t")
st.latex(r"y = h_0 + (u\sin\theta)t - \frac{1}{2}gt^2")
st.markdown("#### Important projectile formulas")
f1, f2 = st.columns(2)
with f1:
    st.latex(r"T = \frac{u\sin\theta + \sqrt{(u\sin\theta)^2+2gh_0}}{g}")
    st.latex(r"H_{max}=h_0+\frac{(u\sin\theta)^2}{2g}")
with f2:
    st.latex(r"R = (u\cos\theta)T")
    st.latex(r" a_x=0,\quad a_y=-g")

st.divider()
st.subheader("📋 Motion Data Table")
sample_times = np.linspace(0, flight_time, 11)
table_x = vx0 * sample_times
table_y = np.maximum(0, launch_height + vy0 * sample_times - 0.5 * gravity * sample_times**2)
table_vy = vy0 - gravity * sample_times
table_speed = np.sqrt(vx0**2 + table_vy**2)
motion_df = pd.DataFrame({
    "Time (s)": np.round(sample_times, 2),
    "Horizontal position (m)": np.round(table_x, 2),
    "Vertical position (m)": np.round(table_y, 2),
    "Horizontal velocity (m/s)": np.round(np.full_like(sample_times, vx0), 2),
    "Vertical velocity (m/s)": np.round(table_vy, 2),
    "Speed (m/s)": np.round(table_speed, 2),
})
st.dataframe(motion_df, use_container_width=True, hide_index=True)
csv = motion_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download motion data (CSV)", data=csv, file_name="projectile_motion_data.csv", mime="text/csv")

st.divider()
st.subheader("📚 Physics Concepts Demonstrated")
concepts = [
    ("Projectile motion", "The curved path followed by an object launched into the air."),
    ("Horizontal component", "Horizontal velocity remains constant when air resistance is ignored."),
    ("Vertical component", "Vertical velocity changes because of gravitational acceleration."),
    ("Initial velocity and angle", "The launch speed is resolved into horizontal and vertical components."),
    ("Time of flight", "The total time from launch until the projectile reaches ground level."),
    ("Maximum height", "The greatest vertical height reached by the projectile."),
    ("Horizontal range", "The horizontal distance from launch point to landing point."),
    ("Trajectory", "The parabolic path followed in the ideal projectile model."),
    ("Distance and displacement", "Distance is the path length; displacement is the straight-line change in position."),
    ("Velocity and acceleration", "Velocity describes the rate of position change; acceleration describes the rate of velocity change."),
]
for title, description in concepts:
    with st.expander(title):
        st.write(description)

with st.expander("⚠️ Model assumptions and limitations"):
    st.write("""
    - This is an ideal projectile-motion model.
    - Air resistance, wind, rotation, collisions, and changes in launch speed are ignored.
    - The material is treated as a point object.
    - The material's mass does not change the trajectory in this ideal model.
    - The landing surface is assumed to be level with the ground reference (y = 0).
    - This is an educational simulator, not a real construction-site equipment safety or engineering tool.
    """)

st.caption("University Physics Project | Projectile Motion Based Construction Material Delivery Simulator")
