import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Projectile Motion Simulator", page_icon="🏗️", layout="wide")

st.markdown("""
<style>
.block-container{padding-top:1.2rem}
.hero{padding:1.2rem;border-radius:14px;background:linear-gradient(110deg,#10243a,#1e5670);color:white}
.hero h1{font-size:2.2rem;margin:0}.hero p{font-size:1.05rem;margin:.4rem 0 0}
.team{padding:12px;border:1px solid #8886;border-radius:10px;text-align:center;font-weight:700}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🎛️ Presentation Controls")
project_title = st.sidebar.text_input("Project title", "Projectile Motion Based Construction Material Delivery Simulator")
intro = st.sidebar.text_area("Introduction paragraph (editable)", "This project demonstrates how an object carrying construction material moves through the air after being launched. By changing launch speed, launch angle and launch height, we can study its trajectory and predict where it lands.", height=120)
talk_track = st.sidebar.text_area("Presentation explanation (editable)", "First, we select the launch speed, angle and height. Then the simulator calculates the horizontal and vertical components, flight time, maximum height and range. Finally, we compare the landing point with the target.", height=120)
large = st.sidebar.toggle("Projector-friendly large text", True)

st.sidebar.divider()
st.sidebar.subheader("Launch settings")
material = st.sidebar.selectbox("Construction material example", ["Brick", "Cement bag", "Sand bag", "Concrete block", "Other material"])
u = st.sidebar.slider("Initial velocity (m/s)", 1.0, 50.0, 20.0, 0.5)
angle = st.sidebar.slider("Launch angle (degrees)", 1, 89, 45, 1)
h0 = st.sidebar.slider("Launch height (m)", 0.0, 30.0, 2.0, 0.5)
g = st.sidebar.selectbox("Gravity (m/s²)", [9.81, 9.80, 10.0], index=0)
target = st.sidebar.slider("Target distance (m)", 1.0, 200.0, 30.0, 1.0)
tolerance = st.sidebar.slider("Target tolerance (m)", 0.5, 15.0, 2.0, 0.5)

theta = math.radians(angle)
ux, uy = u * math.cos(theta), u * math.sin(theta)
flight = (uy + math.sqrt(uy**2 + 2*g*h0)) / g
t_peak = uy / g
height_max = h0 + uy**2/(2*g)
reach = ux * flight
ts = np.linspace(0, flight, 400)
xs = ux * ts
ys = np.maximum(0, h0 + uy*ts - 0.5*g*ts**2)
distance_path = float(np.sum(np.hypot(np.diff(xs), np.diff(ys))))
err = abs(reach-target)
font = 18 if large else 13

st.markdown(f'<div class="hero"><h1>🏗️ {project_title}</h1><p>Interactive Physics Working Model | Construction Material Delivery</p></div>', unsafe_allow_html=True)
st.markdown(f"<div style='font-size:{font}px;line-height:1.6;margin-top:16px'>{intro}</div>", unsafe_allow_html=True)
st.markdown("### 👥 Project Development Team")
cols = st.columns(4)
for c, roll in zip(cols, ["BSPHY-2025-017","BSPHY-2025-044","BSPHY-2025-006","BSPHY-2025-002"]):
    c.markdown(f'<div class="team">{roll}</div>', unsafe_allow_html=True)

sim, concepts, vectors, present = st.tabs(["🚀 Live Simulator","📚 Physics Concepts","🧭 Vector & Motion Analysis","🎤 Presentation Mode"])

with sim:
    st.subheader("Live Projectile Trajectory")
    st.caption(f"Selected example: {material}. Change controls in the sidebar and observe the graph.")
    m = st.columns(4)
    m[0].metric("Time of flight", f"{flight:.2f} s")
    m[1].metric("Maximum height", f"{height_max:.2f} m")
    m[2].metric("Horizontal range", f"{reach:.2f} m")
    m[3].metric("Time to peak", f"{t_peak:.2f} s")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs,y=ys,mode="lines",name="Projectile trajectory",line=dict(width=4),hovertemplate="x: %{x:.2f} m<br>y: %{y:.2f} m<extra></extra>"))
    fig.add_trace(go.Scatter(x=[0,reach],y=[h0,0],mode="markers",name="Launch and landing",marker=dict(size=11)))
    fig.add_trace(go.Scatter(x=[target],y=[0],mode="markers+text",name="Target",marker=dict(size=15,symbol="x"),text=["Target"],textposition="top center"))
    fig.update_layout(template="plotly_white",height=520,xaxis_title="Horizontal distance (m)",yaxis_title="Vertical height (m)",legend=dict(orientation="h",y=1.12),font=dict(size=font))
    fig.update_xaxes(rangemode="tozero"); fig.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig,use_container_width=True)
    if err <= tolerance:
        st.success(f"Target reached within tolerance. Landing error: {err:.2f} m")
    else:
        st.warning(f"Target missed. Landing error: {err:.2f} m. Adjust launch speed or angle.")
    a,b,c=st.columns(3)
    a.metric("Target distance",f"{target:.2f} m"); b.metric("Landing distance",f"{reach:.2f} m"); c.metric("Landing error",f"{err:.2f} m")
    st.subheader("Inspect motion at any time")
    t_now=st.slider("Simulation time (s)",0.0,float(flight),float(flight/2),step=max(float(flight/250),0.001))
    x_now=ux*t_now; y_now=max(0.0,h0+uy*t_now-.5*g*t_now**2); vy_now=uy-g*t_now
    speed=math.hypot(ux,vy_now); disp=math.hypot(x_now,y_now-h0)
    q=st.columns(4)
    q[0].metric("Current x",f"{x_now:.2f} m"); q[1].metric("Current y",f"{y_now:.2f} m")
    q[2].metric("Current speed",f"{speed:.2f} m/s"); q[3].metric("Displacement",f"{disp:.2f} m")

with concepts:
    st.subheader("Physics Principles Explained")
    explain = [
    ("Projectile Motion","The motion of an object launched into the air and then moving under gravity. In the ideal model, its path is a parabola."),
    ("Horizontal and Vertical Components","Initial velocity is split into perpendicular components: uₓ = u cos θ and uᵧ = u sin θ. Horizontal velocity remains constant if air resistance is ignored; vertical velocity changes due to gravity."),
    ("Initial Velocity and Launch Angle","Initial velocity (u) is the launch speed. Launch angle (θ) is measured above the horizontal. Both affect flight time, height and range."),
    ("Acceleration Due to Gravity","Near Earth's surface, g is approximately 9.81 m/s² downward. Taking upward as positive gives aₓ = 0 and aᵧ = −g."),
    ("Time of Flight","Total time from launch until the object reaches ground level: T = [u sin θ + √((u sin θ)² + 2gh₀)] / g."),
    ("Maximum Height","The highest vertical position. At the peak, vertical velocity is zero: H = h₀ + (u sin θ)²/(2g)."),
    ("Horizontal Range","Horizontal distance from launch to landing: R = (u cos θ)T. If launch and landing heights are equal, R = u² sin(2θ)/g."),
    ("Trajectory of Projectile","The curved path of the object. Its equation is y = h₀ + x tan θ − gx²/(2u²cos²θ)."),
    ]
    for title, body in explain:
        with st.expander(title,expanded=True):
            st.markdown(f"<div style='font-size:{font}px;line-height:1.6'>{body}</div>",unsafe_allow_html=True)
    st.markdown("### Formula Summary")
    st.latex(r"u_x=u\cos\theta \qquad u_y=u\sin\theta")
    st.latex(r"x(t)=u\cos\theta\ t")
    st.latex(r"y(t)=h_0+u\sin\theta\ t-\frac{1}{2}gt^2")
    st.latex(r"T=\frac{u\sin\theta+\sqrt{(u\sin\theta)^2+2gh_0}}{g}")
    st.latex(r"H_{\max}=h_0+\frac{(u\sin\theta)^2}{2g}\qquad R=(u\cos\theta)T")

with vectors:
    st.subheader("Vector Analysis")
    st.write("Velocity is a vector because it has magnitude and direction.")
    a,b,c=st.columns(3)
    a.metric("Initial horizontal velocity",f"{ux:.2f} m/s"); b.metric("Initial vertical velocity",f"{uy:.2f} m/s"); c.metric("Initial resultant velocity",f"{u:.2f} m/s")
    vf=go.Figure()
    vf.add_trace(go.Scatter(x=[0,ux],y=[0,uy],mode="lines+markers",name="Initial velocity vector",line=dict(width=5)))
    vf.add_trace(go.Scatter(x=[0,ux],y=[0,0],mode="lines+markers",name="Horizontal component",line=dict(width=3,dash="dash")))
    vf.add_trace(go.Scatter(x=[ux,ux],y=[0,uy],mode="lines+markers",name="Vertical component",line=dict(width=3,dash="dash")))
    vf.update_layout(template="plotly_white",height=380,xaxis_title="Horizontal velocity (m/s)",yaxis_title="Vertical velocity (m/s)",font=dict(size=font))
    st.plotly_chart(vf,use_container_width=True)
    st.subheader("Distance and Displacement")
    st.write(f"**Distance travelled along curved path:** approximately {distance_path:.2f} m.")
    st.write(f"**Displacement at landing:** {math.hypot(reach,-h0):.2f} m (straight-line change from launch to landing).")
    st.info("Distance is the total length of the path. Displacement is the straight-line change from starting point to ending point.")
    st.subheader("Velocity and Acceleration")
    st.write(f"At t = {t_now:.2f} s, Vₓ = {ux:.2f} m/s, Vᵧ = {vy_now:.2f} m/s and resultant speed = {speed:.2f} m/s.")
    st.write(f"Acceleration: aₓ = 0 m/s² and aᵧ = −{g:.2f} m/s² (downward).")

with present:
    st.subheader("Projector Presentation Mode")
    st.markdown(f"<div style='font-size:{font+2}px;line-height:1.7'>{talk_track}</div>",unsafe_allow_html=True)
    st.markdown("### What this model demonstrates")
    for item in [
        "Set the initial speed, launch angle and launch height.",
        "Resolve initial velocity into horizontal and vertical components.",
        "Observe gravity changing vertical velocity while horizontal velocity stays constant in the ideal model.",
        "See the parabolic trajectory and landing point on the graph.",
        "Calculate time of flight, maximum height and horizontal range.",
        "Compare the landing point with a construction delivery target.",
        "Inspect position, velocity, distance and displacement at a selected time."
    ]: st.markdown(f"- {item}")
    summary=pd.DataFrame({"Parameter":["Material","Initial velocity","Launch angle","Launch height","Gravity","Time of flight","Maximum height","Horizontal range","Target distance"],"Value":[material,f"{u:.2f} m/s",f"{angle}°",f"{h0:.2f} m",f"{g:.2f} m/s²",f"{flight:.2f} s",f"{height_max:.2f} m",f"{reach:.2f} m",f"{target:.2f} m"]})
    st.dataframe(summary,use_container_width=True,hide_index=True)
    st.download_button("Download simulation summary CSV",summary.to_csv(index=False).encode(), "simulation_summary.csv","text/csv")

st.divider()
st.subheader("Model Assumptions and Safety Note")
st.markdown("""
- This is an educational physics simulator, not a real construction-site delivery or equipment-control system.
- Air resistance, wind, object rotation, tumbling, collisions and obstacles are not modelled.
- The material is treated as a point object. In this ideal model, mass does not change the trajectory.
- The landing surface is assumed to be level with the ground reference (y = 0).
- Do not use these calculations to launch or handle real construction materials.
""")
st.caption("University Physics Project | Projectile Motion Based Construction Material Delivery Simulator")
