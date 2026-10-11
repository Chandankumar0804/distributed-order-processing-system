import { useEffect, useState } from "react";
import "./Dashboard.css";

function Dashboard() {
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");

  const fetchReport = async () => {
    const token = localStorage.getItem("access_token");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/orders/report",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to load dashboard");
        return;
      }

      setReport(data);
    } catch {
      setError("Backend server is not running");
    }
  };

  useEffect(() => {
    fetchReport();
  }, []);

  if (error) {
    return (
      <div className="dashboard-page">
        <div className="dashboard-error">
          {error}
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="dashboard-page">
        <div className="dashboard-loading">
          Loading dashboard...
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">

      <div className="dashboard-header">
        <div>
          <h1>Dashboard</h1>
          <p>Order Processing Overview</p>
        </div>

        <button onClick={fetchReport}>
          Refresh Dashboard
        </button>
      </div>

      <div className="dashboard-cards">

        <div className="dashboard-card">
          <h3>Total Orders</h3>
          <p>{report.total_orders}</p>
        </div>

        <div className="dashboard-card">
          <h3>Pending Orders</h3>
          <p>{report.pending_orders}</p>
        </div>

        <div className="dashboard-card">
          <h3>Processing Orders</h3>
          <p>{report.processing_orders}</p>
        </div>

        <div className="dashboard-card">
          <h3>Failed Orders</h3>
          <p>{report.failed_orders}</p>
        </div>

        <div className="dashboard-card">
          <h3>Cancelled Orders</h3>
          <p>{report.cancelled_orders}</p>
        </div>

        <div className="dashboard-card revenue-card">
          <h3>Total Revenue</h3>
          <p>₹{report.total_revenue}</p>
        </div>

      </div>

    </div>
  );
}

export default Dashboard;