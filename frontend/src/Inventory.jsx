import { useEffect, useState } from "react";
import "./Inventory.css";

function Inventory() {
  const [products, setProducts] = useState([]);
  const [error, setError] = useState("");

  const fetchInventory = async () => {
    const token = localStorage.getItem("access_token");

    setError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/products/report",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to load inventory");
        return;
      }

      setProducts(data);
    } catch {
      setError("Backend server is not running");
    }
  };

  useEffect(() => {
    fetchInventory();
  }, []);

  return (
    <div className="inventory-page">

      <div className="inventory-header">
        <div>
          <h1>Inventory</h1>
          <p>Monitor product stock and reservations</p>
        </div>

        <button
          className="inventory-refresh-button"
          onClick={fetchInventory}
        >
          Refresh Inventory
        </button>
      </div>

      {error && (
        <div className="inventory-error">
          {error}
        </div>
      )}

      <div className="inventory-table-container">

        <table className="inventory-table">

          <thead>
            <tr>
              <th>Product ID</th>
              <th>Product Name</th>
              <th>Available Stock</th>
              <th>Reserved Stock</th>
              <th>Total Stock</th>
            </tr>
          </thead>

          <tbody>
            {products.map((product) => (
              <tr key={product.product_id}>

                <td className="product-id">
                  {product.product_id}
                </td>

                <td className="product-name">
                  {product.product_name}
                </td>

                <td>
                  {product.available_stock}
                </td>

                <td>
                  {product.reserved_stock}
                </td>

                <td className="total-stock">
                  {product.total_stock}
                </td>

              </tr>
            ))}
          </tbody>

        </table>

      </div>

    </div>
  );
}

export default Inventory;