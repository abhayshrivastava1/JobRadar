import React, { useEffect, useState } from "react";
import axios from "axios";
import ExpandableText from "./ExpandableText";



export default function Dashboard() {
  const [filtered, setFiltered] = useState([]);
  const [manual, setManual] = useState([]);
  const [activeTab, setActiveTab] = useState("filtered"); // tab state
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const [filteredRes, manualRes] = await Promise.all([
          axios.get("http://localhost:5000/api/filtered"),
          axios.get("http://localhost:5000/api/manual"),
        ]);
        setFiltered(filteredRes.data);
        setManual(manualRes.data);
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    }
    fetchData();
  }, []);

  const renderTable = (data, columns) => (
    <div className="overflow-x-auto shadow-lg rounded-lg">
      <table className="min-w-full divide-y divide-gray-300">
        <thead className="bg-gray-800 text-white sticky top-0">
          <tr>
            {columns.map((col) => (
              <th
                key={col}
                className="px-4 py-3 text-left text-sm font-semibold tracking-wide"
              >
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((row, i) => (
            <tr
              key={i}
              className="hover:bg-gray-100 transition-colors duration-200"
            >
              {columns.map((col) => (
                <td key={col} className="px-4 py-2 text-sm text-gray-700">
                  {col === "Link" ? (
                    <a
                      href={row[col]}
                      target="_blank"
                      rel="noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {row[col]}
                    </a>
                  ) : col === "Message" ? (
                    <ExpandableText text={row[col]} />
                  ) : (
                    row[col]
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-gray-500 text-lg animate-pulse">
          Loading jobs
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">
         Jobs Dashboard
      </h1>

      {/* Tabs */}
      <div className="flex space-x-4 mb-6">
        <button
          className={`px-5 py-2 rounded-lg font-semibold transition-colors duration-200 ${
            activeTab === "filtered"
              ? "bg-blue-600 text-white shadow-md"
              : "bg-gray-200 text-gray-800 hover:bg-gray-300"
          }`}
          onClick={() => setActiveTab("filtered")}
        >
          Filtered Jobs
        </button>
        <button
          className={`px-5 py-2 rounded-lg font-semibold transition-colors duration-200 ${
            activeTab === "manual"
              ? "bg-blue-600 text-white shadow-md"
              : "bg-gray-200 text-gray-800 hover:bg-gray-300"
          }`}
          onClick={() => setActiveTab("manual")}
        >
          Manual Review
        </button>
      </div>

      {/* Content */}
      {activeTab === "filtered" ? (
        <section className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            Filtered Jobs
          </h2>
          {renderTable(filtered, [
            "Company",
            "Message",
            "Link",
            "Matched Keywords",
          ])}
        </section>
      ) : (
        <section className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            Manual Review Jobs
          </h2>
          {renderTable(manual, ["Company","Message", "Link"])}
        </section>
      )}
    </div>
  );
}
