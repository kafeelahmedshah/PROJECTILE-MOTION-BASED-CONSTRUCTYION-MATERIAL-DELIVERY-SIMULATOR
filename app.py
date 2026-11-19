
# ---------------- AUTOMATIC PROJECTILE ANIMATION ----------------
st.markdown("## 🚀 Automatic Projectile Motion")

st.write(
    "Set your physics values in the sidebar and press Start. "
    "The object will automatically travel along its projectile path."
)

# Animation speed
animation_speed = st.sidebar.slider(
    "Animation speed",
    min_value=0.02,
    max_value=0.20,
    value=0.06,
    step=0.01
)

# Animation controls
if "auto_play" not in st.session_state:
    st.session_state.auto_play = False

if "animation_frame" not in st.session_state:
    st.session_state.animation_frame = 0

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ START", use_container_width=True):
        st.session_state.auto_play = True
        st.session_state.animation_frame = 0

with col2:
    if st.button("⏸ PAUSE", use_container_width=True):
        st.session_state.auto_play = False

with col3:
    if st.button("↺ RESET", use_container_width=True):
        st.session_state.auto_play = False
        st.session_state.animation_frame = 0

# Prepare trajectory
animation_frames = 100
frame_times = np.linspace(0, flight_time, animation_frames)

frame_x = x0 + ux * frame_times
frame_y = (
    y0 + uy * frame_times
    - 0.5 * gravity * frame_times**2
)

# Prevent negative display below landing level
frame_y = np.maximum(frame_y, target_y)

# Create graph
animation_placeholder = st.empty()
status_placeholder = st.empty()

def draw_projectile(frame):
    fig = go.Figure()

    # Complete trajectory
    fig.add_trace(go.Scatter(
        x=frame_x,
        y=frame_y,
        mode="lines",
        name="Projectile Path",
        line=dict(color="#00E5FF", width=4)
    ))

    # Already travelled path
    fig.add_trace(go.Scatter(
        x=frame_x[:frame + 1],
        y=frame_y[:frame + 1],
        mode="lines",
        name="Travelled Path",
        line=dict(color="#FFD166", width=5)
    ))

    # Moving object
    fig.add_trace(go.Scatter(
        x=[frame_x[frame]],
        y=[frame_y[frame]],
        mode="markers",
        name="Construction Material",
        marker=dict(
            size=22,
            color="orange",
            line=dict(color="white", width=2)
        )
    ))

    # Launch point
    fig.add_trace(go.Scatter(
        x=[x0],
        y=[y0],
        mode="markers",
        name="Launch Point",
        marker=dict(size=12, color="green")
    ))

    # Target point
    fig.add_trace(go.Scatter(
        x=[target_x],
        y=[target_y],
        mode="markers",
        name="Target",
        marker=dict(size=15, color="red", symbol="x")
    ))

    fig.update_layout(
        template="plotly_dark",
        height=520,
        title="Automatic Projectile Motion Simulation",
        xaxis_title="Horizontal Distance (m)",
        yaxis_title="Vertical Height (m)",
        paper_bgcolor="#102d46",
        plot_bgcolor="#071426",
        xaxis=dict(range=[
            min(x0, target_x) - 5,
            max(x0 + range_x, target_x) + 10
        ]),
        yaxis=dict(range=[
            min(0, target_y) - 2,
            max(max_height, y0, target_y) + 10
        ])
    )

    return fig

# Automatic animation loop
if st.session_state.auto_play:

    for frame in range(
        st.session_state.animation_frame,
        animation_frames
    ):

        if not st.session_state.auto_play:
            break

        fig = draw_projectile(frame)

        animation_placeholder.plotly_chart(
            fig,
            use_container_width=True,
            key=f"projectile_frame_{frame}"
        )

        current_t = frame_times[frame]
        current_vy = uy - gravity * current_t
        current_speed = math.sqrt(ux**2 + current_vy**2)

        status_placeholder.markdown(
            f"""
            **Time:** {current_t:.2f} s

            **Horizontal position:** {frame_x[frame]:.2f} m

            **Vertical position:** {frame_y[frame]:.2f} m

            **Current speed:** {current_speed:.2f} m/s
            """
        )

        st.session_state.animation_frame = frame + 1
        time.sleep(animation_speed)

    if st.session_state.animation_frame >= animation_frames:
        st.session_state.auto_play = False
        status_placeholder.success(
            "Projectile has completed its motion and reached the landing level."
        )
        st.rerun()

else:
    frame = min(
        st.session_state.animation_frame,
        animation_frames - 1
    )

    animation_placeholder.plotly_chart(
        draw_projectile(frame),
        use_container_width=True
    )

    status_placeholder.info(
        "Press START to watch the projectile move automatically."
    )
