import streamlit as st
import time
import random
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Agentica Stream - Live AI Agent Network",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .logo {
        font-size: 4rem;
        font-weight: 900;
        font-family: 'JetBrains Mono', monospace;
        background: linear-gradient(135deg, #00ff88, #6366f1, #ff0080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        animation: logoGlow 3s ease-in-out infinite alternate;
    }
    
    .tagline {
        font-size: 1.2rem;
        color: #888;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 2rem;
    }
    
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(0, 255, 136, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid #00ff88;
        margin-bottom: 2rem;
    }
    
    .live-dot {
        width: 10px;
        height: 10px;
        background: #ff4444;
        border-radius: 50%;
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.3; transform: scale(1.2); }
    }
    
    @keyframes logoGlow {
        0% { filter: brightness(1) drop-shadow(0 0 20px rgba(0, 255, 136, 0.3)); }
        100% { filter: brightness(1.2) drop-shadow(0 0 30px rgba(99, 102, 241, 0.4)); }
    }
    
    .agent-card {
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .agent-card:hover {
        border-color: #00ff88;
        background: rgba(0, 255, 136, 0.1);
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0, 255, 136, 0.2);
    }
    
    .agent-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .agent-icon { font-size: 2rem; }
    .agent-name { font-size: 1.2rem; font-weight: bold; color: white; }
    .status-active { color: #00ff88; }
    .status-working { color: #ffaa00; }
    .status-idle { color: #888; }
    
    .terminal {
        background: #0a0a0a;
        border: 2px solid #00ff88;
        border-radius: 10px;
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        color: #00ff88;
        max-height: 300px;
        overflow-y: auto;
        margin: 1rem 0;
        box-shadow: inset 0 0 20px rgba(0, 255, 136, 0.1);
    }
    
    .metric-card {
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border-top: 4px solid #00ff88;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(0, 255, 136, 0.1);
        transform: translateY(-2px);
    }
    
    .metric-number {
        font-size: 2rem;
        font-weight: bold;
        color: #00ff88;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-label {
        color: #888;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00ff88, #6366f1);
        color: #0a0a0a;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        transition: all 0.3s ease;
        padding: 0.75rem 2rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 255, 136, 0.3);
    }
    
    .network-stats {
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .footer {
        text-align: center;
        color: #888;
        font-family: 'JetBrains Mono', monospace;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(0, 255, 136, 0.2);
    }
    
    .stMetric > div > div {
        color: #00ff88 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .stMetric > div > div[data-testid="metric-container"] > div {
        color: #888 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agents' not in st.session_state:
    st.session_state.agents = [
        {
            'name': 'Security Guardian',
            'icon': '🛡️',
            'status': 'active',
            'activity': 'Scanning emails and monitoring threats in real-time...',
            'metrics': {'scanned': 247, 'blocked': 12, 'rate': '99.8%'}
        },
        {
            'name': 'Schedule Master',
            'icon': '📅',
            'status': 'working',
            'activity': 'Organizing your calendar and optimizing time blocks...',
            'metrics': {'events': 18, 'free_time': '3.5h', 'efficiency': '95%'}
        },
        {
            'name': 'Health Monitor',
            'icon': '🏥',
            'status': 'active',
            'activity': 'Tracking wellness metrics and health reminders...',
            'metrics': {'steps': 8247, 'sleep': '7.5h', 'score': '85%'}
        },
        {
            'name': 'Data Analyst',
            'icon': '📊',
            'status': 'working',
            'activity': 'Processing quarterly reports and generating insights...',
            'metrics': {'reports': 15, 'insights': 47, 'accuracy': '97.2%'}
        },
        {
            'name': 'Communication Hub',
            'icon': '📱',
            'status': 'active',
            'activity': 'Managing messages and prioritizing communications...',
            'metrics': {'messages': 89, 'priority': 7, 'response': '2.3min'}
        }
    ]

if 'log_messages' not in st.session_state:
    st.session_state.log_messages = [
        '[14:23:45] 🛡️ [SECURITY] Blocked phishing attempt from suspicious domain',
        '[14:23:52] 📅 [SCHEDULE] Optimized tomorrow\'s meeting blocks for better focus time',
        '[14:24:01] 🏥 [HEALTH] Reminder: Take a 5-minute break - you\'ve been working for 2 hours',
        '[14:24:15] 🛡️ [SECURITY] Email scan complete - 127 emails processed, all clean',
        '[14:24:28] 📅 [SCHEDULE] Calendar sync complete - 3 new events added'
    ]

if 'network_stats' not in st.session_state:
    st.session_state.network_stats = {
        'uptime': '99.97%',
        'active_agents': 5,
        'tasks_completed': 2847,
        'cpu_usage': 23.5,
        'memory_usage': 67.8
    }

# Log message templates
log_templates = [
    '🛡️ [SECURITY] Quarantined suspicious email attachment',
    '📅 [SCHEDULE] Rescheduled conflicting meetings for optimal flow',
    '🏥 [HEALTH] Water reminder - you should drink some water now',
    '🛡️ [SECURITY] Updated firewall rules - {} new threats blocked',
    '📅 [SCHEDULE] Found {}-minute gap for focused work',
    '🏥 [HEALTH] Posture check - consider adjusting your workspace',
    '🛡️ [SECURITY] System scan complete - no vulnerabilities found',
    '📅 [SCHEDULE] Meeting prep reminder for upcoming call',
    '🏥 [HEALTH] Great job! You\'ve hit your step goal for today',
    '📊 [DATA] Generated monthly performance report with {} key insights',
    '📱 [COMM] Prioritized urgent message from team lead',
    '📊 [DATA] Anomaly detected in sales data - investigating...',
    '📱 [COMM] Auto-replied to {} low-priority emails'
]

def generate_log_entry():
    """Generate a new log entry"""
    template = random.choice(log_templates)
    if '{}' in template:
        if 'threats' in template:
            value = random.randint(1, 5)
        elif 'insights' in template:
            value = random.randint(5, 15)
        elif 'emails' in template:
            value = random.randint(3, 12)
        else:
            value = random.randint(15, 60)
        template = template.format(value)
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    return f"[{timestamp}] {template}"

def create_health_chart():
    """Create health metrics visualization"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    steps = [7500, 8200, 6800, 9100, 8247, 7900, 8500]
    sleep = [7.2, 6.8, 8.1, 7.5, 7.5, 8.2, 7.0]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=days,
        y=steps,
        mode='lines+markers',
        name='Daily Steps',
        line=dict(color='#00ff88', width=3),
        marker=dict(size=8),
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=days,
        y=[s * 1000 for s in sleep],  # Scale for dual axis
        mode='lines+markers',
        name='Sleep Hours',
        line=dict(color='#6366f1', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title=dict(text="Health Metrics - Last 7 Days", font=dict(color='white', size=18)),
        xaxis=dict(title='Day', color='white', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(
            title='Steps',
            color='#00ff88',
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis2=dict(
            title='Sleep Hours',
            overlaying='y',
            side='right',
            color='#6366f1',
            tickvals=[6000, 7000, 8000, 9000],
            ticktext=['6h', '7h', '8h', '9h']
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(
            x=0,
            y=1,
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='rgba(0, 255, 136, 0.2)',
            borderwidth=1
        )
    )
    
    return fig

def create_network_activity_chart():
    """Create network activity visualization"""
    hours = list(range(24))
    activity = [random.randint(20, 100) for _ in hours]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=activity,
        mode='lines',
        name='Network Activity',
        line=dict(color='#00ff88', width=2),
        fill='tonexty',
        fillcolor='rgba(0, 255, 136, 0.1)'
    ))
    
    fig.update_layout(
        title=dict(text="24-Hour Network Activity", font=dict(color='white', size=18)),
        xaxis=dict(title='Hour', color='white', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Activity Level', color='white', gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False
    )
    
    return fig

def update_agent_status():
    """Randomly update agent statuses"""
    for agent in st.session_state.agents:
        if random.random() < 0.3:  # 30% chance to change status
            statuses = ['active', 'working', 'idle']
            agent['status'] = random.choice(statuses)
            
            # Update metrics slightly
            if 'scanned' in agent['metrics']:
                agent['metrics']['scanned'] += random.randint(1, 5)
            if 'events' in agent['metrics']:
                agent['metrics']['events'] += random.randint(0, 2)
            if 'steps' in agent['metrics']:
                agent['metrics']['steps'] += random.randint(50, 200)

# Main application
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="logo">AGENTICA</div>
        <div class="tagline">Real-time AI Agent Network Monitoring</div>
        <div class="live-indicator">
            <div class="live-dot"></div>
            <span>LIVE - All Systems Operational</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh every 5 seconds
    placeholder = st.empty()
    
    # Add new log entry occasionally
    if random.random() < 0.7:  # 70% chance
        new_entry = generate_log_entry()
        st.session_state.log_messages.append(new_entry)
        if len(st.session_state.log_messages) > 15:
            st.session_state.log_messages = st.session_state.log_messages[-15:]
    
    # Update agent statuses
    update_agent_status()
    
    # Network Statistics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">99.97%</div>
            <div class="metric-label">Network Uptime</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        active_count = sum(1 for agent in st.session_state.agents if agent['status'] == 'active')
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{active_count}/5</div>
            <div class="metric-label">Active Agents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.session_state.network_stats['tasks_completed'] += random.randint(0, 3)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{st.session_state.network_stats['tasks_completed']:,}</div>
            <div class="metric-label">Tasks Completed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        cpu_usage = st.session_state.network_stats['cpu_usage'] + random.uniform(-2, 2)
        cpu_usage = max(10, min(80, cpu_usage))
        st.session_state.network_stats['cpu_usage'] = cpu_usage
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{cpu_usage:.1f}%</div>
            <div class="metric-label">CPU Usage</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        memory_usage = st.session_state.network_stats['memory_usage'] + random.uniform(-1, 1)
        memory_usage = max(50, min(85, memory_usage))
        st.session_state.network_stats['memory_usage'] = memory_usage
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{memory_usage:.1f}%</div>
            <div class="metric-label">Memory Usage</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Agent Status Cards
    st.markdown("## 🤖 Agent Status")
    
    for i, agent in enumerate(st.session_state.agents):
        status_class = f"status-{agent['status']}"
        status_text = agent['status'].upper()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            <div class="agent-card">
                <div class="agent-header">
                    <span class="agent-icon">{agent['icon']}</span>
                    <span class="agent-name">{agent['name']}</span>
                    <span class="{status_class}">● {status_text}</span>
                </div>
                <p style="color: #ccc; margin: 0;">{agent['activity']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Display agent-specific metrics
            for key, value in agent['metrics'].items():
                st.metric(key.title().replace('_', ' '), value)
    
    # Live Activity Log
    st.markdown("## 📊 Live Activity Log")
    
    log_content = '\n'.join(reversed(st.session_state.log_messages[-10:]))
    st.markdown(f"""
    <div class="terminal">
        <div style="color: #00ff88; margin-bottom: 10px;">[AGENTICA NETWORK LOG] - Real-time Agent Activity</div>
        <div style="font-size: 0.8rem; line-height: 1.4;">
            {log_content.replace(chr(10), '<br>')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏥 Health Metrics")
        health_chart = create_health_chart()
        st.plotly_chart(health_chart, use_container_width=True)
    
    with col2:
        st.markdown("### 🌐 Network Activity")
        network_chart = create_network_activity_chart()
        st.plotly_chart(network_chart, use_container_width=True)
    
    # Control Panel
    st.markdown("## ⚙️ Control Panel")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Refresh All Agents"):
            st.success("All agents refreshed successfully!")
            time.sleep(1)
            st.rerun()
    
    with col2:
        if st.button("📊 Generate Report"):
            st.info("Generating comprehensive system report...")
            time.sleep(1)
            st.success("Report generated and saved!")
    
    with col3:
        if st.button("🛡️ Security Scan"):
            st.warning("Initiating full security scan...")
            time.sleep(2)
            st.success("Security scan complete - No threats detected!")
    
    with col4:
        if st.button("🔧 Optimize Network"):
            st.info("Optimizing network performance...")
            time.sleep(1)
            st.success("Network optimization complete!")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Agentica Stream v2.1.0 | Powered by Advanced AI Networks</p>
        <p>Status: All systems operational | Last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
    
    # Auto-refresh
    time.sleep(3)
    st.rerun()

if __name__ == "__main__":
    main()
