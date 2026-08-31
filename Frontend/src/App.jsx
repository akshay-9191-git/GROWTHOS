import { useEffect, useState } from "react";
import "./App.css";

const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";

function App() {
  // =========================================================
  // STATE
  // =========================================================

  const [dashboard, setDashboard] = useState(null);
  const [opportunities, setOpportunities] = useState([]);
  const [actions, setActions] = useState([]);
  const [apiConnected, setApiConnected] = useState(false);

  const [strategyPerformance, setStrategyPerformance] = useState([]);
  const [strategyLoading, setStrategyLoading] = useState(true);
  const [strategyError, setStrategyError] = useState("");

  const [loading, setLoading] = useState(true);
  const [opportunitiesLoading, setOpportunitiesLoading] = useState(true);
  const [actionsLoading, setActionsLoading] = useState(true);

  const [creatingAction, setCreatingAction] = useState(null);
  const [executingAction, setExecutingAction] = useState(null);

  const [actionMessage, setActionMessage] = useState("");
  const [actionResult, setActionResult] = useState(null);

  const [error, setError] = useState("");
  const [opportunitiesError, setOpportunitiesError] = useState("");
  const [actionsError, setActionsError] = useState("");

  const [outcomeStats, setOutcomeStats] = useState(null);
  const [typePerformance, setTypePerformance] = useState([]);
  const [outcomeLoading, setOutcomeLoading] = useState(true);
  const [outcomeError, setOutcomeError] = useState("");

  const [recordingOutcome, setRecordingOutcome] = useState(null);
  const [outcomeRevenue, setOutcomeRevenue] = useState({});
  const [outcomeMessage, setOutcomeMessage] = useState("");
  const [recordedOutcomes, setRecordedOutcomes] = useState({});

  // =========================================================
  // HELPER - FORMAT CURRENCY
  // IMPORTANT:
  // This is placed BEFORE any function that uses it.
  // =========================================================

  const formatCurrency = (value) => {
    const amount = Number(value || 0);

    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(amount);
  };

  // =========================================================
  // LOAD STRATEGY PERFORMANCE
  // =========================================================

  const loadStrategyPerformance = async () => {
    try {
      setStrategyLoading(true);
      setStrategyError("");

      const response = await fetch(
        `${API_BASE}/actions/analytics/strategies`
      );

      if (!response.ok) {
        throw new Error(
          `Strategy analytics request failed: ${response.status}`
        );
      }

      const data = await response.json();

      console.log("Strategy performance:", data);

      if (!data.success) {
        throw new Error("Strategy analytics API failed.");
      }

      setStrategyPerformance(
        Array.isArray(data.strategies)
          ? data.strategies
          : []
      );
    } catch (err) {
      console.error("Strategy performance error:", err);

      setStrategyPerformance([]);
      setStrategyError(
        "Unable to load strategy performance."
      );
    } finally {
      setStrategyLoading(false);
    }
  };

  // =========================================================
  // LOAD DASHBOARD
  // =========================================================

  const loadDashboard = async () => {
    try {
      setError("");

      const response = await fetch(
        `${API_BASE}/dashboard/`
      );

      if (!response.ok) {
        throw new Error(
          `Dashboard request failed: ${response.status}`
        );
      }
      

      const data = await response.json();

      if (!data.success) {
        throw new Error(
          "Dashboard API returned an unsuccessful response."
        );
      }
      setApiConnected(true);
      setDashboard(data.dashboard);
    } catch (err) {
      console.error("Dashboard error:", err);
      setApiConnected(false);
      setError("Unable to load dashboard.");
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // LOAD OPPORTUNITIES
  // =========================================================

  const loadOpportunities = async () => {
    try {
      setOpportunitiesLoading(true);
      setOpportunitiesError("");

      const response = await fetch(
        `${API_BASE}/opportunities/`
      );

      if (!response.ok) {
        throw new Error(
          `Opportunities request failed: ${response.status}`
        );
      }

      const data = await response.json();



      let opportunityList = [];

      if (Array.isArray(data)) {
        opportunityList = data;
      } else if (Array.isArray(data.top_opportunities)) {
        opportunityList = data.top_opportunities;
      } else if (Array.isArray(data.opportunities)) {
        opportunityList = data.opportunities;
      } else if (Array.isArray(data.high_priority)) {
        opportunityList = [
          ...data.high_priority,
          ...(Array.isArray(data.medium_priority)
            ? data.medium_priority
            : []),
        ];
      }

      setOpportunities(opportunityList);
    } catch (err) {
      console.error("Opportunities error:", err);

      setOpportunities([]);
      setOpportunitiesError(
        "Unable to load opportunities."
      );
    } finally {
      setOpportunitiesLoading(false);
    }
  };

  // =========================================================
  // LOAD OUTCOME ANALYTICS
  // =========================================================

  const loadOutcomeAnalytics = async () => {
    try {
      setOutcomeLoading(true);
      setOutcomeError("");

      const [statsResponse, typeResponse] =
        await Promise.all([
          fetch(`${API_BASE}/actions/outcomes/stats`),
          fetch(`${API_BASE}/actions/outcomes/by-type`),
        ]);

      if (!statsResponse.ok) {
        throw new Error(
          `Outcome stats request failed: ${statsResponse.status}`
        );
      }

      if (!typeResponse.ok) {
        throw new Error(
          `Type performance request failed: ${typeResponse.status}`
        );
      }

      const statsData = await statsResponse.json();
      const typeData = await typeResponse.json();

      console.log("Outcome stats:", statsData);
      console.log("Type performance:", typeData);

      if (!statsData.success) {
        throw new Error("Outcome stats API failed.");
      }

      if (!typeData.success) {
        throw new Error("Type performance API failed.");
      }

      setOutcomeStats(
        statsData.stats ||
          statsData.statistics ||
          null
      );

      setTypePerformance(
        Array.isArray(typeData.performance)
          ? typeData.performance
          : []
      );
    } catch (err) {
      console.error(
        "Outcome analytics error:",
        err
      );

      setOutcomeError(
        "Unable to load outcome analytics."
      );
    } finally {
      setOutcomeLoading(false);
    }
  };

  // =========================================================
  // LOAD GROWTH ACTIONS
  // =========================================================

  const loadActions = async () => {
    try {
      setActionsLoading(true);
      setActionsError("");

      const response = await fetch(
        `${API_BASE}/actions/`
      );

      if (!response.ok) {
        throw new Error(
          `Actions request failed: ${response.status}`
        );
      }

      const data = await response.json();

   

      if (!data.success) {
        throw new Error(
          "Actions API returned an unsuccessful response."
        );
      }

      setActions(
        Array.isArray(data.actions)
          ? data.actions
          : []
      );
    } catch (err) {
      console.error("Actions error:", err);

      setActions([]);
      setActionsError(
        "Unable to load growth actions."
      );
    } finally {
      setActionsLoading(false);
    }
  };

  // =========================================================
  // RECORD ACTION OUTCOME
  // =========================================================

  const recordOutcome = async (
    actionId,
    converted
  ) => {
    try {
      setRecordingOutcome(actionId);
      setOutcomeMessage("");

      const revenue =
        Number(outcomeRevenue[actionId] || 0);

      const response = await fetch(
        `${API_BASE}/actions/outcome/${actionId}?converted=${converted}&revenue_generated=${revenue}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.detail ||
            "Failed to record action outcome."
        );
      }

      console.log(
        "Outcome recorded:",
        data
      );

      setOutcomeMessage(
        converted
          ? `Conversion recorded for ${actionId}.`
          : `No conversion recorded for ${actionId}.`
      );

      // Clear entered revenue
      setOutcomeRevenue((previous) => {
        const updated = { ...previous };
        delete updated[actionId];
        return updated;
      });

      // Refresh affected data
      await Promise.all([
        loadDashboard(),
        loadActions(),
        loadOutcomeAnalytics(),
        loadStrategyPerformance(),
      ]);
    } catch (err) {
      console.error(
        "Record outcome error:",
        err
      );

      setOutcomeMessage(
        err.message ||
          "Unable to record outcome."
      );
    } finally {
      setRecordingOutcome(null);
    }
  };

  // =========================================================
  // CREATE GROWTH ACTION
  // =========================================================

  const handleTakeAction = async (item) => {
    const key = `${item.user_id}-${item.product_id}`;

    try {
      setCreatingAction(key);
      setActionMessage("");
      setActionResult(null);

      const response = await fetch(
        `${API_BASE}/actions/execute/${item.user_id}/${item.product_id}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.detail ||
            "Failed to create growth action."
        );
      }

      console.log(
        "Growth action created:",
        data.action
      );

      setActionMessage(
        `Action ${data.action.action_id} created successfully.`
      );

      await Promise.all([
        loadDashboard(),
        loadActions(),
      ]);
    } catch (err) {
      console.error(
        "Create action error:",
        err
      );

      setActionMessage(
        err.message ||
          "Unable to create growth action."
      );
    } finally {
      setCreatingAction(null);
    }
  };

  // =========================================================
  // RUN / EXECUTE GROWTH ACTION
  // =========================================================

  const runGrowthAction = async (actionId) => {
    try {
      setExecutingAction(actionId);
      setActionResult(null);

      const response = await fetch(
        `${API_BASE}/actions/run/${actionId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.detail ||
            "Action execution failed."
        );
      }

      setActionResult({
        type: "success",
        message: `Action ${actionId} executed successfully.`,
      });

      await Promise.all([
        loadActions(),
        loadDashboard(),
      ]);
    } catch (err) {
      console.error(
        "Action execution error:",
        err
      );

      setActionResult({
        type: "error",
        message:
          err.message ||
          "Unable to execute growth action.",
      });
    } finally {
      setExecutingAction(null);
    }
  };

  // =========================================================
  // INITIAL LOAD
  // =========================================================

  useEffect(() => {
    loadDashboard();
    loadOpportunities();
    loadActions();
    loadOutcomeAnalytics();
    loadStrategyPerformance();
  }, []);

  // =========================================================
  // REFRESH EVERYTHING
  // =========================================================

  const handleRefresh = async () => {
    setLoading(true);

    await Promise.all([
      loadDashboard(),
      loadOpportunities(),
      loadActions(),
      loadOutcomeAnalytics(),
      loadStrategyPerformance(),
    ]);
  };

  // =========================================================
  // HELPERS
  // =========================================================

  const getIntentClass = (intent) => {
    switch (
      String(intent || "").toUpperCase()
    ) {
      case "HIGH":
        return "high";

      case "MEDIUM":
        return "medium";

      case "LOW":
        return "low";

      default:
        return "low";
    }
  };

  const getIntentIcon = (intent) => {
    switch (
      String(intent || "").toUpperCase()
    ) {
      case "HIGH":
        return "🔥";

      case "MEDIUM":
        return "⚡";

      case "LOW":
        return "•";

      default:
        return "•";
    }
  };

  const getStatusClass = (status) => {
    switch (
      String(status || "").toUpperCase()
    ) {
      case "READY":
        return "ready";

      case "EXECUTING":
        return "executing";

      case "COMPLETED":
        return "completed";

      case "FAILED":
        return "failed";

      default:
        return "ready";
    }
  };

  // =========================================================
  // LOADING SCREEN
  // =========================================================

  if (loading && !dashboard) {
    return (
      <div className="app">
        <header className="topbar">
          <div>
            <h1>GrowthOS</h1>

            <p>
              Autonomous AI Growth & Agentic Commerce Platform
            </p>
          </div>

          <div className={`api-status ${apiConnected ? "connected" : "offline"}`}>
  <span className="status-dot"></span>
  {apiConnected ? "API Connected" : "API Offline"}
</div>
        </header>

        <main>
          <div className="loading">
            Loading GrowthOS...
          </div>
        </main>
      </div>
    );
  }

  // =========================================================
  // MAIN UI
  // =========================================================

  return (
    <div className="app">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="topbar">

        <div>
          <h1>GrowthOS</h1>

          <p>
            Autonomous AI Growth & Agentic Commerce Platform
          </p>
        </div>

        <div className="api-status">
          <span className="status-dot"></span>
          API Connected
        </div>

      </header>

      {/* =====================================================
          MAIN
      ===================================================== */}

      <main>

        {/* ===================================================
            OUTCOME ANALYTICS
        =================================================== */}

        <div className="section-card">

          <div className="section-card-heading">

            <div>
              <h2>
                Outcome Analytics
              </h2>

              <p>
                Measure the real business impact of GrowthOS actions
              </p>
            </div>

            <span className="section-icon">
              📊
            </span>

          </div>

          {outcomeMessage && (
            <div className="action-message">
              {outcomeMessage}
            </div>
          )}

          {outcomeLoading && (
            <div className="loading">
              Loading outcome analytics...
            </div>
          )}

          {!outcomeLoading && outcomeError && (
            <div className="error">
              {outcomeError}
            </div>
          )}

          {!outcomeLoading &&
            !outcomeError &&
            outcomeStats && (
              <>

                <div className="performance-grid">

                  <div className="performance-card">

                    <div className="performance-icon">
                      📋
                    </div>

                    <small>
                      Total Outcomes
                    </small>

                    <strong>
                      {outcomeStats.total_outcomes ?? 0}
                    </strong>

                  </div>

                  <div className="performance-card">

                    <div className="performance-icon">
                      ✓
                    </div>

                    <small>
                      Conversions
                    </small>

                    <strong>
                      {outcomeStats.conversions ??
                        outcomeStats.total_conversions ??
                        0}
                    </strong>

                  </div>

                  <div className="performance-card">

                    <div className="performance-icon">
                      ↗
                    </div>

                    <small>
                      Conversion Rate
                    </small>

                    <strong>
                      {outcomeStats.conversion_rate ?? 0}%
                    </strong>

                  </div>

                  <div className="performance-card">

                    <div className="performance-icon">
                      ₹
                    </div>

                    <small>
                      Revenue
                    </small>

                    <strong>
                      {formatCurrency(
                        outcomeStats.total_revenue ?? 0
                      )}
                    </strong>

                  </div>

                </div>

                {/* PERFORMANCE BY TYPE */}

                <div className="type-performance">

                  <h3>
                    Performance by Action Type
                  </h3>

                  {typePerformance.length === 0 ? (

                    <div className="empty">
                      No outcome performance data available yet.
                    </div>

                  ) : (

                    <div className="type-performance-list">

                      {typePerformance.map(
                        (item, index) => (

                          <div
                            className="type-performance-row"
                            key={
                              item.action_type ||
                              index
                            }
                          >

                            <div className="type-name">

                              <strong>
                                {item.action_type ||
                                  "Growth Action"}
                              </strong>

                              <small>
                                {item.actions ?? 0} actions
                              </small>

                            </div>

                            <div className="type-stat">

                              <small>
                                Conversions
                              </small>

                              <strong>
                                {item.conversions ?? 0}
                              </strong>

                            </div>

                            <div className="type-stat">

                              <small>
                                Rate
                              </small>

                              <strong>
                                {item.conversion_rate ?? 0}%
                              </strong>

                            </div>

                            <div className="type-stat">

                              <small>
                                Revenue
                              </small>

                              <strong>
                                {formatCurrency(
                                  item.revenue ?? 0
                                )}
                              </strong>

                            </div>

                          </div>
                        )
                      )}

                    </div>
                  )}

                </div>

              </>
            )}

        </div>

        {/* ===================================================
            STRATEGY LEARNING
        =================================================== */}

        <div className="section-card">

          <div className="section-card-heading">

            <div>
              <h2>
                Strategy Learning
              </h2>

              <p>
                GrowthOS learns which strategies perform best
              </p>
            </div>

            <span className="section-icon">
              🧠
            </span>

          </div>

          {strategyLoading && (
            <div className="loading">
              Loading strategy performance...
            </div>
          )}

          {!strategyLoading && strategyError && (
            <div className="error">
              {strategyError}
            </div>
          )}

          {!strategyLoading &&
            !strategyError &&
            strategyPerformance.length === 0 && (
              <div className="empty">
                No strategy learning data available yet.
              </div>
            )}

          {!strategyLoading &&
            !strategyError &&
            strategyPerformance.length > 0 && (

              <div className="strategy-list">

                {strategyPerformance.map(
                  (strategy, index) => {

                    const name =
                      strategy.strategy ||
                      strategy.name ||
                      strategy.action_type ||
                      `Strategy ${index + 1}`;

                    const conversions =
                      strategy.conversions ??
                      strategy.total_conversions ??
                      0;

                    const actions =
                      strategy.actions ??
                      strategy.total_actions ??
                      0;

                    const conversionRate =
                      strategy.conversion_rate ?? 0;

                    const revenue =
                      strategy.revenue ??
                      strategy.total_revenue ??
                      0;

                    return (

                      <div
                        className="strategy-card"
                        key={`${name}-${index}`}
                      >

                        <div className="strategy-header">

                          <div>

                            <span className="strategy-label">
                              Strategy
                            </span>

                            <h3>
                              {name}
                            </h3>

                          </div>

                          <div className="strategy-rate">

                            <strong>
                              {conversionRate}%
                            </strong>

                            <small>
                              conversion
                            </small>

                          </div>

                        </div>

                        <div className="strategy-bar">

                          <span
                            style={{
                              width: `${Math.min(
                                Number(conversionRate) || 0,
                                100
                              )}%`,
                            }}
                          />

                        </div>

                        <div className="strategy-stats">

                          <div>

                            <small>
                              Actions
                            </small>

                            <strong>
                              {actions}
                            </strong>

                          </div>

                          <div>

                            <small>
                              Conversions
                            </small>

                            <strong>
                              {conversions}
                            </strong>

                          </div>

                          <div>

                            <small>
                              Revenue
                            </small>

                            <strong>
                              {formatCurrency(revenue)}
                            </strong>

                          </div>

                        </div>

                      </div>
                    );
                  }
                )}

              </div>
            )}

        </div>

        {/* =====================================================
            GROWTH OVERVIEW
        ===================================================== */}

        <section className="overview-section">

          <div className="section-heading">

            <div>
              <h2>
                Growth Overview
              </h2>

              <p>
                Real-time performance from your GrowthOS engine
              </p>
            </div>

            <button
              className="refresh-btn"
              onClick={handleRefresh}
            >
              ↻ Refresh
            </button>

          </div>

          {/* Dashboard Error */}

          {error && (
            <div className="error">
              {error}
            </div>
          )}

          {dashboard && (
            <>

              {/* =================================================
                  TOP STAT CARDS
              ================================================= */}

              <div className="stats-grid">

                {/* Opportunities */}

                <div className="stat-card">

                  <div className="stat-icon">
                    🎯
                  </div>

                  <div>

                    <small>
                      Opportunities
                    </small>

                    <strong>
                      {dashboard.opportunities?.total ?? 0}
                    </strong>

                    <span>
                      {dashboard.opportunities?.high ?? 0}{" "}
                      high priority
                    </span>

                  </div>

                </div>

                {/* Actions */}

                <div className="stat-card">

                  <div className="stat-icon">
                    ⚡
                  </div>

                  <div>

                    <small>
                      Growth Actions
                    </small>

                    <strong>
                      {dashboard.actions?.total ?? 0}
                    </strong>

                    <span>
                      {dashboard.actions?.ready ?? 0} ready
                    </span>

                  </div>

                </div>

                {/* Conversions */}

                <div className="stat-card">

                  <div className="stat-icon">
                    ✓
                  </div>

                  <div>

                    <small>
                      Conversions
                    </small>

                    <strong>
                      {dashboard.performance?.total_conversions ?? 0}
                    </strong>

                    <span>
                      {dashboard.performance?.conversion_rate ?? 0}%
                      {" "}conversion rate
                    </span>

                  </div>

                </div>

                {/* Revenue */}

                <div className="stat-card">

                  <div className="stat-icon">
                    ₹
                  </div>

                  <div>

                    <small>
                      Revenue Generated
                    </small>

                    <strong>
                      {formatCurrency(
                        dashboard.performance?.total_revenue
                      )}
                    </strong>

                    <span>
                      Total generated revenue
                    </span>

                  </div>

                </div>

              </div>

              {/* =================================================
                  OPPORTUNITY DISTRIBUTION
              ================================================= */}

              <div className="section-card">

                <div className="section-card-heading">

                  <div>

                    <h2>
                      Growth Opportunities
                    </h2>

                    <p>
                      Customer purchase intent distribution
                    </p>

                  </div>

                  <span className="section-icon">
                    ↗
                  </span>

                </div>

                <div className="intent-grid">

                  {/* HIGH */}

                  <div className="intent-card high">

                    <div className="intent-top">

                      <span>
                        High Intent
                      </span>

                      <strong>
                        {dashboard.opportunities?.high ?? 0}
                      </strong>

                    </div>

                    <div className="intent-bar">

                      <span
                        style={{
                          width: `${
                            dashboard.opportunities?.total
                              ? (
                                  (dashboard.opportunities.high /
                                    dashboard.opportunities.total) *
                                  100
                                )
                              : 0
                          }%`,
                        }}
                      />

                    </div>

                    <small>
                      {dashboard.opportunities?.total
                        ? Math.round(
                            (dashboard.opportunities.high /
                              dashboard.opportunities.total) *
                              100
                          )
                        : 0}
                      % of opportunities
                    </small>

                  </div>

                  {/* MEDIUM */}

                  <div className="intent-card medium">

                    <div className="intent-top">

                      <span>
                        Medium Intent
                      </span>

                      <strong>
                        {dashboard.opportunities?.medium ?? 0}
                      </strong>

                    </div>

                    <div className="intent-bar">

                      <span
                        style={{
                          width: `${
                            dashboard.opportunities?.total
                              ? (
                                  (dashboard.opportunities.medium /
                                    dashboard.opportunities.total) *
                                  100
                                )
                              : 0
                          }%`,
                        }}
                      />

                    </div>

                    <small>
                      {dashboard.opportunities?.total
                        ? Math.round(
                            (dashboard.opportunities.medium /
                              dashboard.opportunities.total) *
                              100
                          )
                        : 0}
                      % of opportunities
                    </small>

                  </div>

                  {/* LOW */}

                  <div className="intent-card low">

                    <div className="intent-top">

                      <span>
                        Low Intent
                      </span>

                      <strong>
                        {dashboard.opportunities?.low ?? 0}
                      </strong>

                    </div>

                    <div className="intent-bar">

                      <span
                        style={{
                          width: `${
                            dashboard.opportunities?.total
                              ? (
                                  (dashboard.opportunities.low /
                                    dashboard.opportunities.total) *
                                  100
                                )
                              : 0
                          }%`,
                        }}
                      />

                    </div>

                    <small>
                      {dashboard.opportunities?.total
                        ? Math.round(
                            (dashboard.opportunities.low /
                              dashboard.opportunities.total) *
                              100
                          )
                        : 0}
                      % of opportunities
                    </small>

                  </div>

                </div>

              </div>

              {/* =================================================
                  GROWTH ACTION SUMMARY
              ================================================= */}

              <div className="section-card">

                <div className="section-card-heading">

                  <div>

                    <h2>
                      Growth Actions
                    </h2>

                    <p>
                      Current action execution pipeline
                    </p>

                  </div>

                  <span className="section-icon">
                    ⚡
                  </span>

                </div>

                <div className="action-grid">

                  <div className="action-card">

                    <div className="action-icon">
                      ◷
                    </div>

                    <small>
                      Ready
                    </small>

                    <strong>
                      {dashboard.actions?.ready ?? 0}
                    </strong>

                  </div>

                  <div className="action-card">

                    <div className="action-icon">
                      〽
                    </div>

                    <small>
                      Executing
                    </small>

                    <strong>
                      {dashboard.actions?.executing ?? 0}
                    </strong>

                  </div>

                  <div className="action-card">

                    <div className="action-icon">
                      ✓
                    </div>

                    <small>
                      Completed
                    </small>

                    <strong>
                      {dashboard.actions?.completed ?? 0}
                    </strong>

                  </div>

                  <div className="action-card">

                    <div className="action-icon">
                      ×
                    </div>

                    <small>
                      Failed
                    </small>

                    <strong>
                      {dashboard.actions?.failed ?? 0}
                    </strong>

                  </div>

                </div>

              </div>

              {/* =================================================
                  PERFORMANCE
              ================================================= */}

              <div className="section-card">

                <div className="section-card-heading">

                  <div>

                    <h2>
                      Performance
                    </h2>

                    <p>
                      Results generated by GrowthOS actions
                    </p>

                  </div>

                  <span className="section-icon">
                    ↗
                  </span>

                </div>

                <div className="performance-grid">

                  <div className="performance-card">

                    <div className="performance-icon">
                      👥
                    </div>

                    <small>
                      Total Outcomes
                    </small>

                    <strong>
                      {dashboard.performance?.total_outcomes ?? 0}
                    </strong>

                  </div>

                  <div className="performance-card">

                    <div className="performance-icon">
                      ✓
                    </div>

                    <small>
                      Conversions
                    </small>

                    <strong>
                      {dashboard.performance?.total_conversions ?? 0}
                    </strong>

                  </div>

                  <div className="performance-card">

                    <div className="performance-icon">
                      ↗
                    </div>

                    <small>
                      Conversion Rate
                    </small>

                    <strong>
                      {dashboard.performance?.conversion_rate ?? 0}%
                    </strong>

                  </div>

                  <div className="performance-card">

                    <div className="performance-icon">
                      ₹
                    </div>

                    <small>
                      Total Revenue
                    </small>

                    <strong>
                      {formatCurrency(
                        dashboard.performance?.total_revenue
                      )}
                    </strong>

                  </div>

                </div>

              </div>

            </>
          )}

        </section>

        {/* =====================================================
            CUSTOMER OPPORTUNITIES
        ===================================================== */}

        <section className="opportunities-section">

          <div className="section-heading">

            <div>

              <h2>
                Customer Opportunities
              </h2>

              <p>
                AI-detected purchase opportunities
              </p>

            </div>

            {!opportunitiesLoading &&
              !opportunitiesError &&
              opportunities.length > 0 && (
                <span>
                  {opportunities.length} shown
                </span>
              )}

          </div>

          {/* Action creation message */}

          {actionMessage && (
            <div className="action-message">
              {actionMessage}
            </div>
          )}

          {/* Loading */}

          {opportunitiesLoading && (
            <div className="loading">
              Loading opportunities...
            </div>
          )}

          {/* Error */}

          {!opportunitiesLoading &&
            opportunitiesError && (
              <div className="error">
                {opportunitiesError}
              </div>
            )}

          {/* Empty */}

          {!opportunitiesLoading &&
            !opportunitiesError &&
            opportunities.length === 0 && (
              <div className="empty">
                No growth opportunities found.
              </div>
            )}

          {/* Opportunity List */}

          {!opportunitiesLoading &&
            !opportunitiesError &&
            opportunities.length > 0 && (

              <div className="opportunity-list">

                {opportunities
                  .slice(0, 20)
                  .map((item, index) => {

                    const intent = String(
                      item.intent || "LOW"
                    ).toUpperCase();

                    const intentClass =
                      getIntentClass(intent);

                    const actionKey =
                      `${item.user_id}-${item.product_id}`;

                    return (

                      <div
                        className="opportunity-card"
                        key={`${item.user_id}-${item.product_id}-${index}`}
                      >

                        {/* CUSTOMER */}

                        <div className="opportunity-main">

                          <div className="customer-avatar">

                            {String(
                              item.user_name || "C"
                            )
                              .charAt(0)
                              .toUpperCase()}

                          </div>

                          <div>

                            <h3>
                              {item.user_name ||
                                `Customer ${item.user_id}`}
                            </h3>

                            <p>
                              {item.product_name ||
                                `Product ${item.product_id}`}
                            </p>

                          </div>

                        </div>

                        {/* INTENT */}

                        <div
                          className={`intent-badge ${intentClass}`}
                        >

                          <span>
                            {getIntentIcon(intent)}
                          </span>

                          {intent}

                        </div>

                        {/* SCORE */}

                        <div className="opportunity-score">

                          <small>
                            Intent score
                          </small>

                          <strong>
                            {item.intent_score ?? 0}
                          </strong>

                        </div>

                        {/* PRODUCT VALUE */}

                        <div className="product-value">

                          <small>
                            Product value
                          </small>

                          <strong>
                            {formatCurrency(
                              item.product_price
                            )}
                          </strong>

                        </div>

                        {/* DETAILS */}

                        <div className="opportunity-details">

                          {Array.isArray(item.reasons) &&
                            item.reasons.map(
                              (
                                reason,
                                reasonIndex
                              ) => (

                                <span
                                  key={reasonIndex}
                                  className="reason"
                                >
                                  {reason}
                                </span>

                              )
                            )}

                        </div>

                        {/* RECOMMENDED ACTION */}

                        <div className="opportunity-action">

                          <small>
                            Recommended action
                          </small>

                          <p>
                            {item.recommended_action ||
                              "Review customer opportunity"}
                          </p>

                          <button
                            onClick={() =>
                              handleTakeAction(item)
                            }
                            disabled={
                              creatingAction ===
                              actionKey
                            }
                          >

                            {creatingAction ===
                            actionKey
                              ? "Creating..."
                              : "Take Action →"}

                          </button>

                        </div>

                      </div>
                    );
                  })}

              </div>
            )}

        </section>

        {/* =====================================================
            GROWTH ACTIONS
        ===================================================== */}

        <section className="actions-section">

          <div className="section-heading">

            <div>

              <h2>
                Growth Actions
              </h2>

              <p>
                AI-generated actions ready for execution
              </p>

            </div>

            {!actionsLoading &&
              !actionsError && (
                <span>
                  {actions.length} actions
                </span>
              )}

          </div>

          {/* Execution result */}

          {actionResult && (
            <div
              className={`action-result ${actionResult.type}`}
            >
              {actionResult.message}
            </div>
          )}

          {/* Loading */}

          {actionsLoading && (
            <div className="loading">
              Loading growth actions...
            </div>
          )}

          {/* Error */}

          {!actionsLoading &&
            actionsError && (
              <div className="error">
                {actionsError}
              </div>
            )}

          {/* Empty */}

          {!actionsLoading &&
            !actionsError &&
            actions.length === 0 && (
              <div className="empty">

                No growth actions have been created yet.

                <br />

                Create an action from a customer opportunity above.

              </div>
            )}

          {/* ACTION LIST */}

          {!actionsLoading &&
            !actionsError &&
            actions.length > 0 && (

              <div className="actions-list">

                {actions.map((action) => {

                  const status =
                    String(
                      action.status || "READY"
                    ).toUpperCase();

                  const statusClass =
                    getStatusClass(status);

                  return (

                    <div
                      className="growth-action-card"
                      key={action.action_id}
                    >

                      {/* ACTION HEADER */}

                      <div className="growth-action-header">

                        <div>

                          <span className="action-id">
                            {action.action_id}
                          </span>

                          <h3>
                            {action.action ||
                              "Growth Action"}
                          </h3>

                        </div>

                        <span
                          className={`action-status ${statusClass}`}
                        >
                          {status}
                        </span>

                      </div>

                      {/* CUSTOMER / PRODUCT */}

                      <div className="growth-action-info">

                        <div>

                          <small>
                            Customer
                          </small>

                          <strong>
                            Customer {action.user_id}
                          </strong>

                        </div>

                        <div>

                          <small>
                            Product
                          </small>

                          <strong>
                            Product {action.product_id}
                          </strong>

                        </div>

                        <div>

                          <small>
                            Priority
                          </small>

                          <strong>
                            {action.priority ||
                              "—"}
                          </strong>

                        </div>

                        <div>

                          <small>
                            Strategy
                          </small>

                          <strong>
                            {action.strategy ||
                              "—"}
                          </strong>

                        </div>

                      </div>

                      {/* MESSAGE */}

                      {action.message && (
                        <div className="growth-action-message">

                          <small>
                            Customer message
                          </small>

                          <p>
                            {action.message}
                          </p>

                        </div>
                      )}

                      {/* INCENTIVE / IMPACT */}

                      <div className="growth-action-details">

                        {action.incentive && (
                          <div>

                            <small>
                              Incentive
                            </small>

                            <span>
                              {action.incentive}
                            </span>

                          </div>
                        )}

                        {action.expected_impact && (
                          <div>

                            <small>
                              Expected impact
                            </small>

                            <span>
                              {action.expected_impact}
                            </span>

                          </div>
                        )}

                      </div>

                      {/* EXECUTE BUTTON */}

                      <div className="growth-action-footer">

                        <small>
                          Created{" "}
                          {action.created_at
                            ? new Date(
                                action.created_at
                              ).toLocaleString("en-IN")
                            : "—"}
                        </small>

                        {/* READY */}

                        {status === "READY" && (

                          <button
                            className="execute-btn"
                            onClick={() =>
                              runGrowthAction(
                                action.action_id
                              )
                            }
                            disabled={
                              executingAction ===
                              action.action_id
                            }
                          >

                            {executingAction ===
                            action.action_id
                              ? "Executing..."
                              : "Execute Action →"}

                          </button>

                        )}

                        {/* EXECUTING */}

                        {status === "EXECUTING" && (

                          <button
                            className="execute-btn"
                            disabled
                          >
                            Executing...
                          </button>

                        )}

                        {/* COMPLETED */}

                        {status === "COMPLETED" && (

                          <div className="outcome-controls">

                            <div className="outcome-revenue">

                              <label>
                                Revenue Generated
                              </label>

                              <input
                                type="number"
                                min="0"
                                placeholder="₹ 0"
                                value={
                                  outcomeRevenue[
                                    action.action_id
                                  ] || ""
                                }
                                onChange={(e) =>
                                  setOutcomeRevenue(
                                    (previous) => ({
                                      ...previous,
                                      [action.action_id]:
                                        e.target.value,
                                    })
                                  )
                                }
                              />

                            </div>

                            <div className="outcome-buttons">

                              <button
                                className="conversion-btn"
                                onClick={() =>
                                  recordOutcome(
                                    action.action_id,
                                    true
                                  )
                                }
                                disabled={
                                  recordingOutcome ===
                                  action.action_id
                                }
                              >

                                {recordingOutcome ===
                                action.action_id
                                  ? "Saving..."
                                  : "✓ Converted"}

                              </button>

                              <button
                                className="no-conversion-btn"
                                onClick={() =>
                                  recordOutcome(
                                    action.action_id,
                                    false
                                  )
                                }
                                disabled={
                                  recordingOutcome ===
                                  action.action_id
                                }
                              >

                                {recordingOutcome ===
                                action.action_id
                                  ? "Saving..."
                                  : "No Conversion"}

                              </button>

                            </div>

                          </div>
                        )}

                        {/* FAILED */}

                        {status === "FAILED" && (

                          <span className="failed-label">
                            × Execution failed
                          </span>

                        )}

                      </div>

                    </div>
                  );
                })}

              </div>
            )}

        </section>

      </main>

      {/* =====================================================
          FOOTER
      ===================================================== */}

      <footer>
        GrowthOS • Autonomous Growth Engine
      </footer>

    </div>
  );
}

export default App;