import Login from "./Login";
import Register from "./Register";
import Dashboard from "./Dashboard";
import Orders from "./Orders";
import Inventory from "./Inventory";
import CustomerReport from "./CustomerReport";
import Reports from "./Reports";
import "./App.css";

function Navigation() {
  const logout = () => {
    localStorage.removeItem("access_token");
    window.location.href = "/";
  };

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <img src="/Logo.png" alt="Order Processing System"></img>
        <span>Order Processing System</span>
      </div>

      <div className="nav-links">
        <a href="/dashboard">Dashboard</a>
        <a href="/orders">Orders</a>
        <a href="/inventory">Inventory</a>
        <a href="/customer-report">Customer Report</a>
        <a href="/reports">Reports</a>

        <button onClick={logout}>
          Logout
        </button>
      </div>
    </nav>
  );
}

function App() {
  const path = window.location.pathname.toLowerCase();

  const token = localStorage.getItem("access_token");

  // Login page
  if (path === "/") {
    return <Login />;
  }

  // Register page
  if (path === "/register") {
    return <Register />;
  }

  // Protected pages
  if (!token) {
    window.location.href = "/";
    return null;
  }

  return (
    <>
      <Navigation />

      {path === "/dashboard" && <Dashboard />}

      {path === "/orders" && <Orders />}

      {path === "/inventory" && <Inventory />}

      {path === "/customer-report" && <CustomerReport />}

      {path === "/reports" && <Reports />}
    </>
  );
}

export default App;