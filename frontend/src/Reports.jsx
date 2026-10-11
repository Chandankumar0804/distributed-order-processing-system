import { useEffect, useState } from "react";
import "./Reports.css";

function Reports() {
  const [orderReport, setOrderReport] = useState(null);
  const [error, setError] = useState("");

  const API_URL = "http://127.0.0.1:8000";

  const fetchOrderReport = async () => {
    const token = localStorage.getItem("access_token");

    setError("");

    try {
      const response = await fetch(
        `${API_URL}/orders/report`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to load report");
        return;
      }

      setOrderReport(data);
    } catch {
      setError("Backend server is not running");
    }
  };

  useEffect(() => {
    fetchOrderReport();
  }, []);

  if (error) {
    return (
      <div className="reports-page">
        <div className="reports-error">
          {error}
        </div>
      </div>
    );
  }

  if (!orderReport) {
    return (
      <div className="reports-page">
        <div className="reports-loading">
          Loading reports...
        </div>
      </div>
    );
  }

  return (
    <div className="reports-page">

      <div className="reports-header">
        <div>
          <h1>Reports</h1>
          <p>Order processing and revenue summary</p>
        </div>

        <button
          className="reports-refresh-button"
          onClick={fetchOrderReport}
        >
          Refresh Report
        </button>
      </div>

      <div className="reports-summary-card">

        <h2>Processing Summary</h2>

        <div className="reports-table-container">

          <table className="reports-table">

            <thead>
              <tr>
                <th>Status</th>
                <th>Total Orders</th>
              </tr>
            </thead>

            <tbody>
              <tr>
                <td>Total Orders</td>
                <td>{orderReport.total_orders}</td>
              </tr>

              <tr>
                <td>Pending</td>
                <td>{orderReport.pending_orders}</td>
              </tr>

              <tr>
                <td>Processing</td>
                <td>{orderReport.processing_orders}</td>
              </tr>

              <tr>
                <td>Failed</td>
                <td>{orderReport.failed_orders}</td>
              </tr>

              <tr>
                <td>Cancelled</td>
                <td>{orderReport.cancelled_orders}</td>
              </tr>
            </tbody>

          </table>

        </div>

      </div>

      <div className="revenue-card">

        <h2>Total Revenue</h2>

        <p>
          ₹{orderReport.total_revenue}
        </p>

      </div>

    </div>
  );
}

export default Reports;