import { useEffect, useState } from "react";
import "./Orders.css";

const API_URL = "http://localhost:8000";

function Orders() {
  const token = localStorage.getItem("access_token");

  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    customer_id: "",
    product_id: "",
    quantity: "",
    unit_price: "",
    payment_type: "CASH",
    source: "WEB",
  });

  const fetchOrders = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(`${API_URL}/orders/?skip=0&limit=100`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch orders");
      }

      const data = await response.json();
      setOrders(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const createOrder = async (e) => {
    e.preventDefault();

    setMessage("");
    setError("");

    try {
      const response = await fetch(`${API_URL}/orders/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          customer_id: Number(form.customer_id),
          product_id: Number(form.product_id),
          quantity: Number(form.quantity),
          unit_price: Number(form.unit_price),
          payment_status: "Pending",
          payment_type: form.payment_type,
          source: form.source,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to create order");
      }

      setMessage(
        `Order created successfully. Order ID: ${data.order_id}`
      );

      setForm({
        customer_id: "",
        product_id: "",
        quantity: "",
        unit_price: "",
        payment_type: "CASH",
        source: "WEB",
      });

      fetchOrders();
    } catch (err) {
      setError(err.message);
    }
  };

  const cancelOrder = async (orderId) => {
    const confirmCancel = window.confirm(
      `Are you sure you want to cancel Order #${orderId}?`
    );

    if (!confirmCancel) return;

    setMessage("");
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/orders/${orderId}/cancel`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to cancel order");
      }

      setMessage(`Order #${orderId} cancelled successfully.`);
      fetchOrders();
    } catch (err) {
      setError(err.message);
    }
  };

  const retryOrder = async (orderId) => {
    const confirmRetry = window.confirm(
      `Are you sure you want to retry Order #${orderId}?`
    );

    if (!confirmRetry) return;

    setMessage("");
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/orders/${orderId}/retry`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to retry order");
      }

      setMessage(`Order #${orderId} retry successful.`);
      fetchOrders();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="orders-page">
      <div className="orders-header">
        <div>
          <h1>Orders</h1>
          <p>Create and manage customer orders</p>
        </div>

        <button className="refresh-btn" onClick={fetchOrders}>
          Refresh
        </button>
      </div>

      {/* CREATE ORDER */}
      <div className="create-order-card">
        <h2>Create New Order</h2>

        <form onSubmit={createOrder} className="order-form">
          <div className="form-group">
            <label>Customer ID</label>
            <input
              type="number"
              name="customer_id"
              value={form.customer_id}
              onChange={handleChange}
              placeholder="Enter customer ID"
              required
            />
          </div>

          <div className="form-group">
            <label>Product ID</label>
            <input
              type="number"
              name="product_id"
              value={form.product_id}
              onChange={handleChange}
              placeholder="Enter product ID"
              required
            />
          </div>

          <div className="form-group">
            <label>Quantity</label>
            <input
              type="number"
              name="quantity"
              value={form.quantity}
              onChange={handleChange}
              placeholder="Enter quantity"
              min="1"
              required
            />
          </div>

          <div className="form-group">
            <label>Unit Price</label>
            <input
              type="number"
              name="unit_price"
              value={form.unit_price}
              onChange={handleChange}
              placeholder="Enter unit price"
              min="0.01"
              step="0.01"
              required
            />
          </div>

          <div className="form-group">
            <label>Payment Type</label>
            <select
              name="payment_type"
              value={form.payment_type}
              onChange={handleChange}
            >
              <option value="CASH">CASH</option>
              <option value="CARD">CARD</option>
              <option value="UPI">UPI</option>
              <option value="BANK_TRANSFER">BANK TRANSFER</option>
            </select>
          </div>

          <div className="form-group">
            <label>Source</label>
            <select
              name="source"
              value={form.source}
              onChange={handleChange}
            >
              <option value="WEB">WEB</option>
              <option value="MOBILE">MOBILE</option>
              <option value="PARTNER">PARTNER</option>
            </select>
          </div>

          <div className="form-submit">
            <button type="submit">Create Order</button>
          </div>
        </form>
      </div>

      {/* MESSAGES */}
      {message && <div className="success-message">{message}</div>}

      {error && <div className="error-message">{error}</div>}

      {/* ORDER LIST */}
      <div className="orders-list-card">
        <div className="list-header">
          <h2>Order List</h2>
          <span>{orders.length} Orders</span>
        </div>

        {loading ? (
          <p className="loading">Loading orders...</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Order ID</th>
                  <th>Customer</th>
                  <th>Product</th>
                  <th>Quantity</th>
                  <th>Unit Price</th>
                  <th>Payment</th>
                  <th>Source</th>
                  <th>Final Amount</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>
                {orders.length === 0 ? (
                  <tr>
                    <td colSpan="10" className="no-data">
                      No orders found
                    </td>
                  </tr>
                ) : (
                  orders.map((order) => (
                    <tr key={order.order_id}>
                      <td>#{order.order_id}</td>

                      <td>{order.customer_id}</td>

                      <td>{order.product_id}</td>

                      <td>{order.quantity}</td>

                      <td>₹{Number(order.unit_price).toFixed(2)}</td>

                      <td>{order.payment_type}</td>

                      <td>{order.source}</td>

                      <td>
                        ₹{Number(order.final_amount || 0).toFixed(2)}
                      </td>

                      <td>
                        <span
                          className={`status-badge status-${String(
                            order.payment_status
                          ).toLowerCase()}`}
                        >
                          {order.payment_status}
                        </span>
                      </td>

                      <td className="action-buttons">
                        {order.payment_status === "Pending" && (
                          <button
                            className="cancel-btn"
                            onClick={() => cancelOrder(order.order_id)}
                          >
                            Cancel
                          </button>
                        )}

                        {order.payment_status === "Failed" && (
                          <button
                            className="retry-btn"
                            onClick={() => retryOrder(order.order_id)}
                          >
                            Retry
                          </button>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default Orders;