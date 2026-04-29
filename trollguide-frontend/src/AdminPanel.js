import React, { useEffect, useState } from "react";

function AdminPanel() {
  const [records, setRecords] = useState([]);
  const [search, setSearch] = useState("");

  const fetchRecords = () => {
    fetch("http://127.0.0.1:8000/admin/records", {
      headers: {
        Authorization: "Basic " + btoa("admin:1234")
      }
    })
      .then(res => res.json())
      .then(data => setRecords(data));
  };

  useEffect(() => {
    fetchRecords();
  }, []);

  const deleteRecord = (id) => {
    fetch(`http://127.0.0.1:8000/admin/delete/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: "Basic " + btoa("admin:1234")
      }
    }).then(() => fetchRecords());
  };

  const searchRecords = () => {
    fetch(`http://127.0.0.1:8000/admin/search?query=${search}`, {
      headers: {
        Authorization: "Basic " + btoa("admin:1234")
      }
    })
      .then(res => res.json())
      .then(data => setRecords(data));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>🛠 Admin Panel</h1>

      <input
        placeholder="Search text..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <button onClick={searchRecords}>Search</button>
      <button onClick={fetchRecords}>Reset</button>

      <table border="1" cellPadding="10" style={{ marginTop: "20px" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Text</th>
            <th>Label</th>
            <th>Confidence</th>
            <th>Keywords</th>
            <th>Crime</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {records.map(r => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>{r.text}</td>
              <td>{r.label}</td>
              <td>{r.confidence}</td>
              <td>{r.keywords}</td>
              <td>{r.crime}</td>
              <td>
                <button onClick={() => deleteRecord(r.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminPanel;