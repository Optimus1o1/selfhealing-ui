# System Architecture Diagrams & Formal Specifications

**Moon Sanctum Labs** — *Decode. Build. Evolve.*  
**Lead Engineer:** Aniket Nandi (Kolkata, IST)  
**Project:** SelfHeal — Intelligent Self-Healing UI Automation Framework  
**Version:** `1.0.0rc1`  
**Target Platform:** Python 3.11+ / Microsoft Playwright / SQLite WAL Mode  

---

## Table of Diagrams

1. [System Context Diagram (C4 Level 1)](#1-system-context-diagram-c4-level-1)
2. [High-Level System Architecture](#2-high-level-system-architecture)
3. [Component Architecture Diagram](#3-component-architecture-diagram)
4. [Data Flow Diagram — Level 0 (Context Level)](#4-data-flow-diagram--level-0-context-level)
5. [Data Flow Diagram — Level 1 (Subsystem Level)](#5-data-flow-diagram--level-1-subsystem-level)
6. [Data Flow Diagram — Level 2 (Intelligence & Decision Engine)](#6-data-flow-diagram--level-2-intelligence--decision-engine)
7. [Entity Relationship Diagram (ERD)](#7-entity-relationship-diagram-erd)
8. [System Use Case Diagram](#8-system-use-case-diagram)
9. [Successful Healing Sequence Diagram (Happy Path)](#9-successful-healing-sequence-diagram-happy-path)
10. [Rejected Healing Sequence Diagram (Safety Guardrails)](#10-rejected-healing-sequence-diagram-safety-guardrails)
11. [Database & Concurrency Architecture (WAL Mode)](#11-database--concurrency-architecture-wal-mode)
12. [CI/CD Deployment & Packaging Workflow](#12-cicd-deployment--packaging-workflow)

---

## 1. System Context Diagram (C4 Level 1)

The System Context diagram describes the boundary of the SelfHeal framework, its users, and external integrations in an automated test environment.

```mermaid
flowchart TB
    QA["QA Engineer / Test Developer"]
    CI["CI/CD Runner (GitHub Actions)"]
    
    subgraph SystemBoundary ["SelfHeal Framework Boundary"]
        SelfHeal["SelfHeal Engine\n(Playwright Wrapper & Deterministic Heuristics)"]
        Dashboard["Audit Dashboard\n(Streamlit Local Portal)"]
        CLI["CLI Management Utility\n(selfheal CLI)"]
    end
    
    Browser["Web Browser Engine\n(Chromium / Firefox / WebKit via Playwright)"]
    AUT["Application Under Test (AUT)\n(Target Web Application DOM)"]
    AuditDB[("SQLite WAL Database\n(artifacts/selfheal.db)")]

    QA -->|"Writes pytest scripts using healed_locator()"| SelfHeal
    QA -->|"Reviews & Promotes baselines (V1 -> V2)"| Dashboard
    QA -->|"Manages baselines & database via"| CLI
    CI -->|"Executes test runs headlessly"| SelfHeal
    
    SelfHeal -->|"Dispatches DOM actions & evaluations"| Browser
    Browser -->|"Renders & manipulates"| AUT
    SelfHeal -->|"Reads/Writes fingerprints & healing events"| AuditDB
    Dashboard -->|"Queries runs, metrics & updates status"| AuditDB
    CLI -->|"Resets & inspects schema"| AuditDB
```

---

## 2. High-Level System Architecture

A multi-tiered architectural overview illustrating the five operational layers: Test Execution, Failure Detection, Intelligence & Decision, Storage, and Presentation/Audit.

```mermaid
flowchart TD
    subgraph ExecutionLayer ["1. Test Execution Layer"]
        Pytest["Test Script (pytest)"]
        Plugin["Pytest Plugin (pytest_plugin.py)"]
        SHPage["SelfHealingPage (src/selfheal/engine/page.py)"]
        SHLoc["SelfHealingLocator (src/selfheal/engine/locator.py)"]
        ExecMgr["ExecutionManager (src/selfheal/engine/executor.py)"]
    end

    subgraph DetectionLayer ["2. Failure Detection & Extraction Layer"]
        PlaywrightNative["Playwright Locator API"]
        Classifier["FailureClassifier (src/selfheal/detection/failure_detector.py)"]
        DOMScan["DOMScanner (src/selfheal/scanner/dom_scanner.py)"]
        InBrowserJS["In-Browser Extractor (src/selfheal/scanner/dom_extractor.js)"]
    end

    subgraph IntelligenceLayer ["3. Intelligence & Decision Layer"]
        SimScorer["SimilarityScorer (src/selfheal/intelligence/scoring.py)"]
        SimEngine["Similarity Algorithms (src/selfheal/intelligence/similarity.py)"]
        DecisionEngine["HealingDecisionEngine (src/selfheal/intelligence/decision_engine.py)"]
    end

    subgraph StorageLayer ["4. Persistence & Audit Layer"]
        Repo["BaselineRepository (src/selfheal/baseline/repository.py)"]
        DBMgr["DatabaseManager (src/selfheal/database/connection.py)"]
        SQLiteDB[("SQLite WAL Storage (artifacts/selfheal.db)")]
    end

    subgraph PresentationLayer ["5. Reporting & Governance Layer"]
        ReportGen["HTML/JSON ReportGenerator (src/selfheal/reporting/)"]
        Dashboard["Streamlit 9-Section Dashboard (src/selfheal/dashboard/app.py)"]
        CLIApp["Click CLI Utility (src/selfheal/cli.py)"]
    end

    Pytest --> Plugin --> SHPage --> SHLoc --> ExecMgr
    ExecMgr --> PlaywrightNative
    PlaywrightNative -- "Action Succeeded" --> ExecMgr
    PlaywrightNative -- "Timeout / Exception" --> Classifier
    
    Classifier -- "Actionability Failure (Hidden/Disabled)" --> ExecMgr
    Classifier -- "Locator Not Found" --> DOMScan --> InBrowserJS
    
    InBrowserJS -- "Candidate Array" --> DOMScan --> SimScorer
    Repo -- "Active Baseline Fingerprint" --> SimScorer
    
    SimScorer <--> SimEngine
    SimScorer -- "Ranked Scored Candidates" --> DecisionEngine
    DecisionEngine -- "Approved / Rejected Decision" --> ExecMgr
    
    ExecMgr -- "Commit Baseline / Log Event" --> Repo
    Repo <--> DBMgr <--> SQLiteDB
    
    SQLiteDB --> ReportGen
    SQLiteDB --> Dashboard
    SQLiteDB --> CLIApp
```

---

## 3. Component Architecture Diagram

Detailed component interface boundaries showing classes, dependencies, and invocation contracts.

```mermaid
classDiagram
    direction TB
    
    class SelfHealingPage {
        -Page _raw_page
        -BaselineRepository _repo
        -ExecutionManager _executor
        +healed_locator(selector, key) SelfHealingLocator
        +goto(url) Response
        +screenshot(path) bytes
    }

    class SelfHealingLocator {
        -Page _page
        -str _selector
        -str _target_key
        -ExecutionManager _executor
        +click() Any
        +fill(value) Any
        +text_content() str
        +first() SelfHealingLocator
        +last() SelfHealingLocator
        +nth(index) SelfHealingLocator
    }

    class ExecutionManager {
        -SelfHealConfig config
        -BaselineRepository repo
        -FailureClassifier classifier
        -DOMScanner scanner
        -SimilarityScorer scorer
        -HealingDecisionEngine decision_engine
        +execute_action(page, selector, key, action_name, fn) Any
        -_capture_baseline_snapshot(page, selector, key) ElementFingerprint
        -_log_healed_event(...) void
        -_log_rejected_event(...) void
    }

    class FailureClassifier {
        -int grace_period_ms
        +classify_failure(page, selector, exc) FailureClassification
    }

    class DOMScanner {
        -str _script
        +scan(page, max_candidates) List~CandidateElement~
    }

    class SimilarityScorer {
        -Dict weights
        +score_candidate(base, cand) ScoredCandidate
        +rank_candidates(base, candidates) List~ScoredCandidate~
    }

    class HealingDecisionEngine {
        -Thresholds thresholds
        +evaluate(key, selector, ranked) HealingDecision
        +synthesize_locator(candidate) str
    }

    class BaselineRepository {
        -DatabaseManager db
        +get_active_fingerprint(key) ElementFingerprint
        +save_fingerprint(fp) void
        +promote_healed_locator(key, new_loc, score, approver) void
        +log_healing_event(event) int
        +get_latency_percentiles() Dict
    }

    SelfHealingPage --> SelfHealingLocator : creates
    SelfHealingPage --> ExecutionManager : delegates
    SelfHealingLocator --> ExecutionManager : invokes actions
    ExecutionManager --> FailureClassifier : triages errors
    ExecutionManager --> DOMScanner : extracts elements
    ExecutionManager --> SimilarityScorer : scores elements
    ExecutionManager --> HealingDecisionEngine : evaluates gating
    ExecutionManager --> BaselineRepository : persists audit trail
```

---

## 4. Data Flow Diagram — Level 0 (Context Level)

Level 0 DFD illustrates external data flowing into and out of the SelfHeal framework environment.

```mermaid
flowchart LR
    Tester["QA Test Script"]
    Browser["Target Web Application"]
    DashboardUser["QA Reviewer"]
    
    SelfHealSystem(("0.0\nSelfHeal\nSystem"))
    
    DB[("SQLite WAL Database")]
    Reports["HTML / JSON Artifacts"]

    Tester -->|"Target Key, Selector, Test Action"| SelfHealSystem
    Browser -->|"DOM Snapshots, Bounding Boxes, Exceptions"| SelfHealSystem
    SelfHealSystem -->|"Synthesized Replacement Selector & Retried Action"| Browser
    SelfHealSystem -->|"Test Status (Pass/Healed/Fail)"| Tester
    SelfHealSystem -->|"Persisted Fingerprints & Event Logs"| DB
    DB -->|"Historical Audit Data"| SelfHealSystem
    SelfHealSystem -->|"Formatted Reports"| Reports
    DashboardUser -->|"Approval / Rejection Sign-off"| SelfHealSystem
    SelfHealSystem -->|"Interactive Analytics Views"| DashboardUser
```

---

## 5. Data Flow Diagram — Level 1 (Subsystem Level)

Level 1 DFD shows the flow of data through major subsystem processes during test execution.

```mermaid
flowchart TD
    Script["Test Script"]
    P1["1.0 Action Interception & Baseline Snapshot"]
    P2["2.0 Failure Classification & Triage"]
    P3["3.0 DOM Candidate Extraction"]
    P4["4.0 Multi-Dimensional Similarity Scoring"]
    P5["5.0 Confidence & Margin Decision Gating"]
    P6["6.0 Candidate Uniqueness Verification & Retry"]
    P7["7.0 Audit Trail & Baseline Evolution"]
    
    D1[("element_fingerprints")]
    D2[("healing_events")]
    D3[("locator_history")]
    D4[("test_runs")]

    Script -->|"healed_locator.click()"| P1
    P1 -->|"Pre-execution Fingerprint"| D1
    P1 -- "Action Throws Timeout/Exception" --> P2
    
    P2 -- "Loc Count == 0 (Eligible)" --> P3
    P2 -- "Hidden/Disabled/Syntax Error" -->|"UnhealableFailureError"| Script
    
    P3 -->|"Array of Candidate Elements"| P4
    D1 -->|"Active Baseline Fingerprint"| P4
    
    P4 -->|"Ranked Candidates + Score Breakdown"| P5
    P5 -- "Score < 0.80 or Margin < 0.10" -->|"HealingConfidenceError"| P7
    P5 -- "Approved Candidate" --> P6
    
    P6 -- "Count == 1 (Unique) -> Retry OK" --> P7
    P6 -- "Count != 1 (Ambiguous) -> Reject" --> P7
    
    P7 -->|"Log Healing Record"| D2
    P7 -->|"Update Test Summary"| D4
    P7 -->|"Promote New Selector (if Automatic)"| D3
    P7 -->|"Return Execution Result"| Script
```

---

## 6. Data Flow Diagram — Level 2 (Intelligence & Decision Engine)

Level 2 DFD details the internal mathematical score generation and decision tree.

```mermaid
flowchart TD
    BaseFP["Baseline Fingerprint"]
    Cand["Extracted Candidate Element"]
    
    subgraph SimCalculators ["Similarity Sub-Calculators"]
        F1["compute_text_similarity\n(Levenshtein, Jaro-Winkler, Token Sort, Synonyms)"]
        F2["compute_type_and_role_similarity\n(Tag, Input Type, ARIA Role Matrix)"]
        F3["compute_attributes_similarity\n(Jaccard on Keys & Value Pairs)"]
        F4["compute_parent_similarity\n(Tag match, Parent ID JW, Class Jaccard)"]
        F5["compute_children_similarity\n(Count Delta, Child Tag Jaccard)"]
        F6["compute_position_similarity\n(Euclidean Centroid Delta / Viewport Diagonal)"]
    end

    BaseFP & Cand --> F1 & F2 & F3 & F4 & F5 & F6

    W1["w_text = 0.30"] --> M1["Weighted Text Score"]
    W2["w_role = 0.20"] --> M2["Weighted Role Score"]
    W3["w_attr = 0.20"] --> M3["Weighted Attr Score"]
    W4["w_parent = 0.15"] --> M4["Weighted Parent Score"]
    W5["w_child = 0.10"] --> M5["Weighted Child Score"]
    W6["w_pos = 0.05"] --> M6["Weighted Pos Score"]

    F1 --> M1
    F2 --> M2
    F3 --> M3
    F4 --> M4
    F5 --> M5
    F6 --> M6

    M1 & M2 & M3 & M4 & M5 & M6 --> Sum["Total Similarity Score\nS = sum(w_i * s_i)"]
    
    Sum --> Rank["Rank All Candidates by S (Descending)"]
    
    Rank --> Gate1{"Top Score S1 >= 0.80?"}
    Gate1 -- "No" --> R1["REJECTED_LOW_CONFIDENCE"]
    Gate1 -- "Yes" --> Gate2{"Multiple Candidates?"}
    
    Gate2 -- "Yes" --> Gate3{"Margin (S1 - S2) >= 0.10?"}
    Gate2 -- "No" --> Synth["Synthesize Locator (#id, data-testid, text, class)"]
    Gate3 -- "No" --> R2["REJECTED_AMBIGUOUS_MATCH"]
    Gate3 -- "Yes" --> Synth
    
    Synth --> Out["HealingDecision(APPROVED, Healed Locator, S1, Breakdown)"]
```

---

## 7. Entity Relationship Diagram (ERD)

Derived directly from `src/selfheal/database/schema.sql`.

```mermaid
erDiagram
    PROJECTS ||--o{ TEST_RUNS : "initiates"
    TEST_RUNS ||--o{ HEALING_EVENTS : "contains"
    ELEMENT_FINGERPRINTS ||--o{ LOCATOR_HISTORY : "tracks"
    ELEMENT_FINGERPRINTS ||--o{ HEALING_EVENTS : "evaluates"

    PROJECTS {
        INTEGER id PK "AUTOINCREMENT"
        TEXT name UK "NOT NULL"
        TEXT description "Nullable"
        TIMESTAMP created_at "DEFAULT CURRENT_TIMESTAMP"
    }

    TEST_RUNS {
        INTEGER id PK "AUTOINCREMENT"
        TEXT run_uuid UK "NOT NULL"
        TEXT project_name "NOT NULL"
        TEXT policy "NOT NULL DEFAULT 'assisted'"
        TIMESTAMP started_at "DEFAULT CURRENT_TIMESTAMP"
        TIMESTAMP completed_at "Nullable"
        INTEGER total_steps "DEFAULT 0"
        INTEGER passed_count "DEFAULT 0"
        INTEGER failed_count "DEFAULT 0"
        INTEGER healed_count "DEFAULT 0"
        TEXT status "DEFAULT 'RUNNING'"
    }

    ELEMENT_FINGERPRINTS {
        INTEGER id PK "AUTOINCREMENT"
        TEXT target_key "NOT NULL (Indexed)"
        INTEGER version "DEFAULT 1"
        TEXT status "active | pending_review | rejected | archived"
        TEXT tag_name "Element tag (e.g. button, input)"
        TEXT element_id "DOM id attribute"
        TEXT class_list "JSON array of CSS classes"
        TEXT inner_text "Sanitized inner text"
        TEXT aria_role "Implicit or explicit ARIA role"
        TEXT accessible_name "W3C accessible name"
        TEXT input_type "Type attribute (text, submit, etc.)"
        TEXT attributes_json "JSON dict of non-sensitive attributes"
        TEXT parent_tag "Container tag name"
        TEXT parent_id "Container DOM id"
        TEXT parent_classes "JSON array of parent classes"
        INTEGER children_count "Number of immediate child nodes"
        TEXT children_tags "JSON array of child tag names"
        REAL bounding_box_x "Viewport relative X"
        REAL bounding_box_y "Viewport relative Y"
        REAL bounding_box_width "Element width"
        REAL bounding_box_height "Element height"
        TEXT page_url "URL where captured"
        TEXT original_selector "Selector used to capture"
        TEXT screenshot_path "Local file path to evidence"
        TIMESTAMP created_at "DEFAULT CURRENT_TIMESTAMP"
        TIMESTAMP updated_at "DEFAULT CURRENT_TIMESTAMP"
    }

    HEALING_EVENTS {
        INTEGER id PK "AUTOINCREMENT"
        INTEGER run_id FK "REFERENCES test_runs(id) ON DELETE CASCADE"
        TEXT target_key "NOT NULL (Indexed)"
        TEXT original_locator "NOT NULL"
        TEXT healed_locator "Replacement locator"
        REAL similarity_score "Computed match score"
        TEXT score_breakdown_json "JSON dict of dimension scores"
        TEXT decision "APPROVED | REJECTED_*"
        TEXT reason "Decision explanation"
        TEXT status "pending_review | promoted | rejected"
        INTEGER retry_success "1 if retry passed, else 0"
        REAL latency_ms "Total healing duration in ms"
        TIMESTAMP created_at "DEFAULT CURRENT_TIMESTAMP"
    }

    LOCATOR_HISTORY {
        INTEGER id PK "AUTOINCREMENT"
        TEXT target_key "NOT NULL (Indexed)"
        TEXT old_locator "NOT NULL"
        TEXT new_locator "NOT NULL"
        REAL similarity_score "Score achieved at promotion"
        TEXT change_type "HEALED_PROMOTED | MANUAL_OVERRIDE"
        TIMESTAMP promoted_at "DEFAULT CURRENT_TIMESTAMP"
        TEXT approved_by "User or system identifier"
    }
```

---

## 8. System Use Case Diagram

Identifies user roles, system boundaries, and primary interactions.

```mermaid
flowchart LR
    QA(("QA Engineer"))
    CI(("CI Runner"))
    Admin(("System Admin"))

    subgraph SelfHealSystem ["SelfHeal Framework Boundaries"]
        UC1(["Execute Test with Self-Healing"])
        UC2(["Capture Initial Element Baseline"])
        UC3(["Triage Failure & Classify Actionability"])
        UC4(["Evaluate Candidates & Heal Locator"])
        UC5(["Review Healing Events on Dashboard"])
        UC6(["Approve & Promote Baseline to V2"])
        UC7(["Reject Incorrect Repair"])
        UC8(["Inspect Multi-Dimension Scores & Diffs"])
        UC9(["Reset Database / Purge History"])
        UC10(["Generate HTML / JSON Test Report"])
    end

    QA --> UC1
    QA --> UC5
    QA --> UC6
    QA --> UC7
    QA --> UC8
    
    CI --> UC1
    CI --> UC10
    
    Admin --> UC9
    
    UC1 -.->|"triggers if missing"| UC2
    UC1 -.->|"triggers on failure"| UC3
    UC3 -.->|"triggers if count == 0"| UC4
    UC4 -.->|"logs audit trail for"| UC5
    UC6 -.->|"updates baseline table"| UC2
```

---

## 9. Successful Healing Sequence Diagram (Happy Path)

Trace of Scenario B: Original `#btnLogin` mutated to `#btnSignInSubmit`.

```mermaid
sequenceDiagram
    autonumber
    actor Script as Test Script (pytest)
    participant Page as SelfHealingPage
    participant Loc as SelfHealingLocator
    participant Exec as ExecutionManager
    participant PW as Playwright Native
    participant Class as FailureClassifier
    participant Scanner as DOMScanner
    participant JS as in-browser JS (dom_extractor.js)
    participant Scorer as SimilarityScorer
    participant Dec as HealingDecisionEngine
    participant Repo as BaselineRepository
    participant DB as SQLite WAL

    Script->>Loc: click()
    Loc->>Exec: execute_action(action="click", selector="#btnLogin", key="auth.submit")
    Exec->>PW: click("#btnLogin", timeout=2500ms)
    Note over PW: 2,500 ms elapses without element
    PW-->>Exec: TimeoutError ("locator.click: Timeout 2500ms exceeded")
    
    Exec->>Class: classify_failure(page, "#btnLogin", TimeoutError)
    Class->>PW: locator("#btnLogin").count()
    PW-->>Class: 0
    Note over Class: Sleep grace_period_ms (500ms) for SPA hydration
    Class->>PW: locator("#btnLogin").count()
    PW-->>Class: 0
    Class-->>Exec: FailureClassification(LOCATOR_NOT_FOUND, is_healable=True)

    Exec->>Repo: get_active_fingerprint("auth.submit")
    Repo->>DB: SELECT * FROM element_fingerprints WHERE target_key='auth.submit' AND status='active'
    DB-->>Repo: BaselineRecord (tag=button, id=btnLogin, text="Login")
    Repo-->>Exec: ElementFingerprint

    Exec->>Scanner: scan(page, max_candidates=100)
    Scanner->>JS: page.evaluate(DOM_EXTRACTOR_SCRIPT)
    JS-->>Scanner: Array of 14 CandidateElement objects
    Scanner-->>Exec: List[CandidateElement]

    Exec->>Scorer: rank_candidates(baseline, candidates)
    Scorer->>Scorer: RapidFuzz Levenshtein, JW, Synonyms, Jaccard, BoundingBox
    Scorer-->>Exec: List[ScoredCandidate] (Top: #btnSignInSubmit, Score=0.8487)

    Exec->>Dec: evaluate("auth.submit", "#btnLogin", ranked_candidates)
    Note over Dec: S1 (0.8487) >= 0.80 (OK)<br/>Margin (0.8487 - 0.4210 = 0.4277) >= 0.10 (OK)
    Dec->>Dec: synthesize_locator(top) -> "#btnSignInSubmit"
    Dec-->>Exec: HealingDecision(APPROVED, healed_locator="#btnSignInSubmit", score=0.8487)

    Exec->>PW: locator("#btnSignInSubmit").count()
    PW-->>Exec: 1 (Strict Uniqueness Confirmed)
    
    Exec->>PW: locator("#btnSignInSubmit").first.click()
    PW-->>Exec: Action Dispatched Successfully!

    Exec->>Repo: log_healing_event(target_key="auth.submit", decision="APPROVED", score=0.8487, retry=1)
    Repo->>DB: INSERT INTO healing_events (...) VALUES (...)
    DB-->>Repo: event_id = 1
    Repo-->>Exec: Success

    Exec-->>Loc: Action Succeeded
    Loc-->>Script: Continues Execution cleanly
```

---

## 10. Rejected Healing Sequence Diagram (Safety Guardrails)

Trace showing the two mandatory safety guardrails: Actionability Failure and Ambiguous Match Rejection.

```mermaid
sequenceDiagram
    autonumber
    actor Script as Test Script
    participant Exec as ExecutionManager
    participant PW as Playwright Native
    participant Class as FailureClassifier
    participant Scanner as DOMScanner
    participant Scorer as SimilarityScorer
    participant Dec as HealingDecisionEngine
    participant Repo as BaselineRepository

    rect rgb(30, 20, 20)
        Note over Script,Repo: SCENARIO 1: ACTIONABILITY REJECTION (Element Disabled / Hidden)
        Script->>Exec: execute_action("#btnDisabled", "checkout.express")
        Exec->>PW: click("#btnDisabled", timeout=2500ms)
        PW-->>Exec: TimeoutError ("element is disabled - waiting for element to be enabled...")
        Exec->>Class: classify_failure("#btnDisabled")
        Class->>PW: locator("#btnDisabled").count()
        PW-->>Class: 1
        Class->>PW: locator("#btnDisabled").first.is_enabled()
        PW-->>Class: False
        Class-->>Exec: FailureClassification(ELEMENT_DISABLED, is_healable=False)
        Exec->>Repo: log_rejected_event(decision="REJECTED_ACTIONABILITY")
        Exec-->>Script: raise UnhealableFailureError ("ELEMENT_DISABLED")
    end

    rect rgb(20, 25, 30)
        Note over Script,Repo: SCENARIO 2: AMBIGUITY REJECTION (Confidence Margin < 0.10)
        Script->>Exec: execute_action("#payOption", "pay.method")
        Exec->>PW: click("#payOption", timeout=2500ms)
        PW-->>Exec: TimeoutError
        Exec->>Class: classify_failure("#payOption")
        Class-->>Exec: FailureClassification(LOCATOR_NOT_FOUND, is_healable=True)
        Exec->>Scanner: scan(page)
        Scanner-->>Exec: Candidates (#payOption1, #payOption2)
        Exec->>Scorer: rank_candidates(baseline, candidates)
        Scorer-->>Exec: Ranked: S1 = 0.8769 (#payOption1), S2 = 0.8720 (#payOption2)
        Exec->>Dec: evaluate("pay.method", "#payOption", ranked)
        Note over Dec: S1 (0.8769) >= 0.80 (Passes Threshold)<br/>Margin: 0.8769 - 0.8720 = 0.0049 < 0.10 (FAILS MARGIN!)
        Dec-->>Exec: HealingDecision(REJECTED_AMBIGUOUS_MATCH, margin=0.0049)
        Exec->>Repo: log_rejected_event(decision="REJECTED_AMBIGUOUS_MATCH")
        Exec-->>Script: raise HealingConfidenceError ("Ambiguous match: margin 0.0049 < 0.10")
    end
```

---

## 11. Database & Concurrency Architecture (WAL Mode)

Illustrates how SQLite Write-Ahead Logging (WAL) facilitates concurrent non-blocking reads from the Streamlit Dashboard and test runs while ensuring atomic writes.

```mermaid
flowchart TD
    subgraph Writers ["Writers (Exclusive Lock during Write Transaction)"]
        TestRunner["Pytest Test Execution Process\n(INSERT healing_events, test_runs)"]
        PromoteAction["Dashboard QA Admin\n(UPDATE element_fingerprints, locator_history)"]
    end

    subgraph SQLiteEngine ["SQLite Core Engine (PRAGMA journal_mode=WAL)"]
        ConnPool["Connection Manager (Timeout=30s, check_same_thread=False)"]
        WALFile["selfheal.db-wal\n(Write-Ahead Log Sequential Ring)"]
        SHMFile["selfheal.db-shm\n(Shared Memory Index & Readers Lock Table)"]
        MainDB["selfheal.db\n(Main B-Tree Database Pages)"]
        Checkpoint["Passive / Truncate Checkpointer"]
    end

    subgraph Readers ["Readers (Non-blocking Snapshot Isolation)"]
        Dashboard1["Streamlit Tab: Live Execution"]
        Dashboard2["Streamlit Tab: Healing Analytics"]
        Dashboard3["Streamlit Tab: Performance Monitor"]
        CLIReader["CLI Command (selfheal baselines)"]
    end

    TestRunner -->|"Exclusive Write Tx"| ConnPool
    PromoteAction -->|"Exclusive Write Tx"| ConnPool
    
    ConnPool -->|"Appends committed pages"| WALFile
    ConnPool <-->|"Tracks reader offsets"| SHMFile
    
    WALFile -->|"Checkpoint Flush"| Checkpoint -->|"Writes dirty pages"| MainDB

    SHMFile <--> Dashboard1 & Dashboard2 & Dashboard3 & CLIReader
    MainDB -->|"Point-in-time Read Snapshot"| Dashboard1 & Dashboard2 & Dashboard3 & CLIReader
```

---

## 12. CI/CD Deployment & Packaging Workflow

Maps the automated testing, verification, packaging, and artifact publishing defined in `.github/workflows/ci.yml`.

```mermaid
flowchart TD
    Push["Developer git push / pull_request (master)"]

    subgraph GHA ["GitHub Actions Runner (Ubuntu / Windows / macOS Matrix)"]
        Checkout["1. actions/checkout@v4"]
        SetupPy["2. actions/setup-python@v5 (Python 3.11, 3.12)"]
        InstallDeps["3. pip install -r requirements.txt & editable selfheal"]
        InstallBrowsers["4. playwright install --with-deps chromium"]
        
        subgraph TestPhase ["5. Test & Validation Suite"]
            Lint["Code Audit / py_compile"]
            UnitTests["pytest tests/unit/ -v"]
            EdgeTests["pytest tests/healing/ -v"]
            DemoTests["pytest tests/demo/ -v"]
            Bench57["python tests/evaluation/benchmark.py (57 cases)"]
            Bench52["python tests/evaluation/holdout_benchmark.py (52 cases)"]
        end

        subgraph BuildPhase ["6. Release Candidate Packaging"]
            BuildPkg["python -m build"]
            ArtifactWheel["dist/selfheal-1.0.0rc1-py3-none-any.whl"]
            ArtifactSdist["dist/selfheal-1.0.0rc1.tar.gz"]
        end

        subgraph UploadPhase ["7. Evidence & Report Preservation"]
            SaveDB["actions/upload-artifact@v4 (artifacts/selfheal.db)"]
            SaveReports["actions/upload-artifact@v4 (artifacts/reports/)"]
            SaveScreenshots["actions/upload-artifact@v4 (artifacts/screenshots/)"]
        end
    end

    Push --> Checkout --> SetupPy --> InstallDeps --> InstallBrowsers
    InstallBrowsers --> Lint --> UnitTests --> EdgeTests --> DemoTests
    DemoTests --> Bench57 --> Bench52
    Bench52 --> BuildPkg --> ArtifactWheel & ArtifactSdist
    ArtifactWheel & ArtifactSdist --> SaveDB & SaveReports & SaveScreenshots
```

