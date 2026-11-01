-- Self-Healing UI Automation Database Schema (SQLite)

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_uuid TEXT NOT NULL UNIQUE,
    project_name TEXT NOT NULL,
    policy TEXT NOT NULL DEFAULT 'assisted',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    total_steps INTEGER DEFAULT 0,
    passed_count INTEGER DEFAULT 0,
    failed_count INTEGER DEFAULT 0,
    healed_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'RUNNING'
);

CREATE TABLE IF NOT EXISTS element_fingerprints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_key TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    status TEXT DEFAULT 'active', -- active, pending_review, rejected, archived
    tag_name TEXT,
    element_id TEXT,
    class_list TEXT, -- JSON array
    inner_text TEXT,
    aria_role TEXT,
    accessible_name TEXT,
    input_type TEXT,
    attributes_json TEXT, -- JSON dictionary of non-sensitive attributes
    parent_tag TEXT,
    parent_id TEXT,
    parent_classes TEXT, -- JSON array
    children_count INTEGER DEFAULT 0,
    children_tags TEXT, -- JSON array
    bounding_box_x REAL,
    bounding_box_y REAL,
    bounding_box_width REAL,
    bounding_box_height REAL,
    page_url TEXT,
    original_selector TEXT,
    screenshot_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_fingerprint_key_status ON element_fingerprints(target_key, status);

CREATE TABLE IF NOT EXISTS healing_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER,
    target_key TEXT NOT NULL,
    original_locator TEXT NOT NULL,
    healed_locator TEXT,
    similarity_score REAL,
    score_breakdown_json TEXT,
    decision TEXT NOT NULL, -- APPROVED, REJECTED_LOW_CONFIDENCE, REJECTED_AMBIGUOUS, REJECTED_ACTIONABILITY
    reason TEXT,
    status TEXT DEFAULT 'pending_review', -- pending_review, promoted, rejected
    retry_success INTEGER DEFAULT 0,
    latency_ms REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(run_id) REFERENCES test_runs(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_healing_run_id ON healing_events(run_id);
CREATE INDEX IF NOT EXISTS idx_healing_target_key ON healing_events(target_key);

CREATE TABLE IF NOT EXISTS locator_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_key TEXT NOT NULL,
    old_locator TEXT NOT NULL,
    new_locator TEXT NOT NULL,
    similarity_score REAL,
    change_type TEXT DEFAULT 'HEALED_PROMOTED', -- HEALED_PROMOTED, MANUAL_OVERRIDE
    promoted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_by TEXT DEFAULT 'system'
);

CREATE INDEX IF NOT EXISTS idx_history_key ON locator_history(target_key);
