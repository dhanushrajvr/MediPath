-- SQLite schema for MediPath

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    phone TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS intake_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    raw_text TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS symptoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intake_session_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    severity TEXT,
    duration TEXT,
    FOREIGN KEY(intake_session_id) REFERENCES intake_sessions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    appointment_date TEXT NOT NULL,  -- YYYY-MM-DD
    appointment_time TEXT NOT NULL, -- HH:MM (24h)
    available INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(department_id) REFERENCES departments(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS triage_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intake_session_id INTEGER NOT NULL,
    tool_name TEXT NOT NULL,
    input_json TEXT,
    output_json TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(intake_session_id) REFERENCES intake_sessions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS triage_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intake_session_id INTEGER NOT NULL,
    urgency TEXT NOT NULL,
    symptoms TEXT NOT NULL, -- JSON array of symptom names
    department TEXT,
    suggested_slot TEXT,
    emergency INTEGER NOT NULL, 
    clarification_required INTEGER NOT NULL,
    explanation TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(intake_session_id) REFERENCES intake_sessions(id) ON DELETE CASCADE
);
