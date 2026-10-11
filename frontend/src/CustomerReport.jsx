import { useEffect, useState } from "react";

function CustomerReport() {
  const [customers, setCustomers] = useState([]);
  const [error, setError] = useState("");

  const fetchCustomerReport = async () => {
    const token = localStorage.getItem("access_token");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/customers/report",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to load customer report");
        return;
      }

      setCustomers(data);
    } catch {
      setError("Backend server is not running");
    }
  };

  useEffect(() => {
    fetchCustomerReport();
  }, []);

  return (
    <div className="page-container">

      <h1 className="page-title">
        Customer-wise Report
      </h1>

      <button onClick={fetchCustomerReport}>
        Refresh Report
      </button>

      {error && (
        <p style={{ color: "red" }}>
          {error}
        </p>
      )}

      <div className="table-container">

        <table>

          <thead>
            <tr>
              <th>Customer ID</th>
              <th>Customer Name</th>
              <th>Email</th>
              <th>Total Orders</th>
              <th>Pending</th>
              <th>Processing</th>
              <th>Failed</th>
              <th>Cancelled</th>
              <th>Total Spent</th>
            </tr>
          </thead>

          <tbody>
            {customers.map((customer) => (
              <tr key={customer.customer_id}>
                <td>{customer.customer_id}</td>
                <td>{customer.customer_name}</td>
                <td>{customer.email}</td>
                <td>{customer.total_orders}</td>
                <td>{customer.pending_orders}</td>
                <td>{customer.processing_orders}</td>
                <td>{customer.failed_orders}</td>
                <td>{customer.cancelled_orders}</td>
                <td>₹{customer.total_spent}</td>
              </tr>
            ))}
          </tbody>

        </table>

      </div>

    </div>
  );
}

export default CustomerReport;