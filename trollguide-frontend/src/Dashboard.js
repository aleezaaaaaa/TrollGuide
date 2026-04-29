import React, { useEffect, useState } from "react";
import {
  PieChart, Pie, Cell,
  BarChart, Bar, XAxis, YAxis, Tooltip,
  ResponsiveContainer
} from "recharts";

const COLORS = ["#00C49F", "#FF4C4C"];

function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/dashboard");
        const json = await res.json();

        // 🔥 fallback safety
        setData({
          total: json.total || 0,
          safe: json.safe || 0,
          toxic: json.toxic || 0,
          crime_distribution: json.crime_distribution || {}
        });

      } catch (err) {
        console.error(err);
        setError("Failed to load dashboard");
      }
    };

    fetchData();

    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  if (error) return <h2 style={{ color: "red" }}>{error}</h2>;
  if (!data) return <h2 style={{ color: "white" }}>Loading...</h2>;

  const pieData = [
    { name: "Safe", value: data.safe },
    { name: "Toxic", value: data.toxic }
  ];

  const crimeData = Object.keys(data.crime_distribution).map(key => ({
    name: key,
    value: data.crime_distribution[key]
  }));

  return (
    <div style={{
      background: "#000",
      color: "#fff",
      minHeight: "100vh",
      padding: "30px",
      fontFamily: "Arial"
    }}>

      <h1 style={{ color: "#FFD700", textAlign: "center" }}>
        📊 TrollGuide Dashboard
      </h1>

      <h3 style={{ textAlign: "center" }}>
        Total Analyses: {data.total}
      </h3>

      {/* CHART GRID */}
      <div style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: "40px",
        marginTop: "30px"
      }}>

        {/* PIE */}
        <div style={{ width: "300px", height: "300px" }}>
          <h3 style={{ textAlign: "center" }}>Safe vs Toxic</h3>

          <ResponsiveContainer>
            <PieChart>
              <Pie data={pieData} dataKey="value" outerRadius={100}>
                {pieData.map((entry, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* BAR */}
        <div style={{ width: "400px", height: "300px" }}>
          <h3 style={{ textAlign: "center" }}>Crime Distribution</h3>

          <ResponsiveContainer>
            <BarChart data={crimeData}>
              <XAxis dataKey="name" stroke="#fff" />
              <YAxis stroke="#fff" />
              <Tooltip />
              <Bar dataKey="value" fill="#FFD700" />
            </BarChart>
          </ResponsiveContainer>
        </div>

      </div>

      {/* EMPTY STATE */}
      {data.total === 0 && (
        <p style={{ textAlign: "center", marginTop: "20px" }}>
          No data yet. Run some analyses first 🚀
        </p>
      )}

    </div>
  );
}

export default Dashboard;