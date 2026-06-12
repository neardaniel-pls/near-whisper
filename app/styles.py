CSS = """
/* ── Global ── */
.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: var(--neutral-800);
}
::-webkit-scrollbar-thumb {
    background: var(--neutral-600);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--primary-500);
}

/* ── Header ── */
.app-header {
    text-align: center;
    padding: 1.5rem 1rem 0.5rem;
    margin-bottom: 0.5rem;
}
.app-header h1 {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #00d4ff, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -0.5px;
}
.app-header p {
    color: var(--neutral-400);
    font-size: 0.9rem;
    margin: 0.25rem 0 0;
}

/* ── Sidebar ── */
.sidebar-section {
    padding: 0.75rem;
}
.sidebar-section .gr-group {
    border: 1px solid var(--border-color-primary) !important;
    border-radius: var(--radius-lg) !important;
}

/* ── Model Info Card ── */
.model-info-card {
    background: var(--neutral-800);
    border: 1px solid var(--neutral-700);
    border-radius: var(--radius-lg);
    padding: 1rem;
    margin-top: 0.5rem;
}
.model-info-card .info-row {
    display: flex;
    justify-content: space-between;
    padding: 0.25rem 0;
    font-size: 0.85rem;
}
.model-info-card .info-label {
    color: var(--neutral-400);
}
.model-info-card .info-value {
    color: var(--neutral-200);
    font-weight: 500;
}
.model-info-card .speed-bar {
    height: 4px;
    background: var(--neutral-700);
    border-radius: 2px;
    margin-top: 0.5rem;
    overflow: hidden;
}
.model-info-card .speed-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #00d4ff, #7c3aed);
    border-radius: 2px;
    transition: width 0.4s ease;
}
.model-info-card .best-for {
    margin-top: 0.5rem;
    padding: 0.4rem 0.6rem;
    background: rgba(0, 212, 255, 0.08);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: var(--radius-sm);
    color: var(--primary-400);
    font-size: 0.8rem;
    text-align: center;
}

/* ── Status Badge ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 500;
    transition: all 0.3s ease;
}
.status-ready {
    background: rgba(34, 197, 94, 0.12);
    color: #4ade80;
    border: 1px solid rgba(34, 197, 94, 0.25);
}
.status-loading {
    background: rgba(250, 204, 21, 0.12);
    color: #facc15;
    border: 1px solid rgba(250, 204, 21, 0.25);
}
.status-error {
    background: rgba(239, 68, 68, 0.12);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.25);
}
.status-success {
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
    border: 1px solid rgba(34, 197, 94, 0.3);
}
.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
}
.status-ready .status-dot {
    background: #4ade80;
    box-shadow: 0 0 6px rgba(74, 222, 128, 0.5);
}
.status-loading .status-dot {
    background: #facc15;
    animation: pulse 1.2s infinite;
}
.status-error .status-dot {
    background: #f87171;
}
.status-success .status-dot {
    background: #4ade80;
    box-shadow: 0 0 6px rgba(74, 222, 128, 0.6);
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Transcribe Button Glow ── */
.transcribe-btn button {
    background: linear-gradient(135deg, #00d4ff, #0891b2) !important;
    border: none !important;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.15) !important;
    transition: all 0.3s ease !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px;
}
.transcribe-btn button:hover {
    box-shadow: 0 0 30px rgba(0, 212, 255, 0.3) !important;
    transform: translateY(-1px);
}

/* ── Secondary Buttons ── */
.action-btn button {
    transition: all 0.2s ease !important;
}
.action-btn button:hover {
    transform: translateY(-1px);
}

/* ── Output Area ── */
.output-area textarea {
    font-family: 'JetBrains Mono', ui-monospace, monospace !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
}

/* ── Audio Input Cards ── */
.audio-input-card {
    border: 1px solid var(--border-color-primary) !important;
    border-radius: var(--radius-lg) !important;
    transition: border-color 0.3s ease;
}
.audio-input-card:hover {
    border-color: var(--primary-600) !important;
}

/* ── Footer ── */
.app-footer {
    text-align: center;
    padding: 1.5rem 0 0.5rem;
    color: var(--neutral-500);
    font-size: 0.75rem;
    border-top: 1px solid var(--neutral-800);
    margin-top: 1rem;
}
.app-footer a {
    color: var(--primary-400);
    text-decoration: none;
}
.app-footer a:hover {
    text-decoration: underline;
}

/* ── Copy Button ── */
.copy-btn button {
    font-size: 0.85rem !important;
}

/* ── Section Dividers ── */
.section-divider {
    border: none;
    border-top: 1px solid var(--neutral-700);
    margin: 0.5rem 0;
}

/* ── Tab Styling ── */
.tabs {
    border: 1px solid var(--neutral-700) !important;
    border-radius: var(--radius-lg) !important;
    overflow: hidden;
}

/* ── Dropdown scroll fix ── */
.sidebar-section,
.sidebar-section > div,
.sidebar-section .gr-group,
.sidebar-section .gr-panel {
    overflow: visible !important;
}
"""
