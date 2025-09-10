import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  ExternalLink,
  Filter,
  Eye,
  Users,
  Briefcase,
} from "lucide-react";
import ExpandableText from "./ExpandableText";

export default function JobsDashboardDynamic() {
  const [filteredJobs, setFilteredJobs] = useState([]);
  const [manualReviewJobs, setManualReviewJobs] = useState([]);
  const [activeTab, setActiveTab] = useState("filtered");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const [filteredRes, manualRes] = await Promise.all([
          axios.get("http://localhost:5000/api/filtered"),
          axios.get("http://localhost:5000/api/manual"),
        ]);
        setFilteredJobs(filteredRes.data || []);
        setManualReviewJobs(manualRes.data || []);
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    }
    fetchData();
  }, []);

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  const renderTable = (jobs, showKeywords = false) => {
    if (jobs.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center py-16 text-center fade-in">
          <Briefcase className="w-16 h-16 text-gray-300 mb-4" />
          <td className="px-6 py-4">
            <ExpandableText text={message} />
          </td>
          <h3 className="text-lg font-medium text-gray-500 mb-2">
            No jobs found
          </h3>
          <p className="text-gray-400">
            There are no jobs to display at the moment.
          </p>
        </div>
      );
    }

    return (
      <div className="overflow-x-auto fade-in">
        <table className="w-full border-collapse">
          <thead>
            <tr className="table-header">
              <th className="px-6 py-4 text-left">
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4" />
                  Company
                </div>
              </th>
              <th className="px-6 py-4 text-left">Message</th>
              <th className="px-6 py-4 text-left">
                <div className="flex items-center gap-2">
                  <ExternalLink className="w-4 h-4" />
                  Link
                </div>
              </th>
              {showKeywords && (
                <th className="px-6 py-4 text-left">
                  <div className="flex items-center gap-2">
                    <Filter className="w-4 h-4" />
                    Matched Keywords
                  </div>
                </th>
              )}
            </tr>
          </thead>
          <tbody>
            {jobs.map((job, index) => {
              // normalize fields
              const company = job.Company || job.company;
              const message = job.Message || job.message;
              const link = job.Link || job.link;
              let keywords = [];

              if (showKeywords) {
                if (Array.isArray(job["Matched Keywords"])) {
                  keywords = job["Matched Keywords"];
                } else if (typeof job["Matched Keywords"] === "string") {
                  try {
                    keywords = JSON.parse(
                      job["Matched Keywords"].replace(/'/g, '"')
                    );
                  } catch {
                    keywords = job["Matched Keywords"]
                      .replace(/[\[\]']+/g, "")
                      .split(",")
                      .map((s) => s.trim())
                      .filter(Boolean);
                  }
                } else if (Array.isArray(job.keywords)) {
                  keywords = job.keywords;
                }
              }

              return (
                <tr key={job.id || index} className="table-row table-row-hover">
                  <td className="px-6 py-4">
                    <div className="font-medium text-gray-900">{company}</div>
                  </td>
                  <td className="px-6 py-4">
                    {/* 👇 ab yahan expandable text use ho raha hai */}
                    <ExpandableText text={message} />
                  </td>
                  <td className="px-6 py-4">
                    <a
                      href={link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="table-link inline-flex items-center gap-1"
                    >
                      <span>View Job</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </td>
                  {showKeywords && (
                    <td className="px-6 py-4">
                      <div className="flex flex-wrap gap-1">
                        {keywords.map((kw, idx) => (
                          <span key={idx} className="keyword-badge">
                            {kw}
                          </span>
                        ))}
                      </div>
                    </td>
                  )}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-gray-500 text-lg animate-pulse">
          Loading jobs...
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 slide-in">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Jobs Dashboard
          </h1>
        </div>

        {/* Stats Cards */}
        <div className="dashboard-card p-6 rounded-xl mb-8 slide-in">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Filtered Jobs */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide">
                  Filtered Jobs
                </h3>
                <p className="text-3xl font-bold text-blue-600 mt-2">
                  {filteredJobs.length}
                </p>
              </div>
              <div className="p-3 bg-primary-light rounded-lg">
                <Filter className="w-6 h-6 text-primary-dark" />
              </div>
            </div>

            {/* Manual Review */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide">
                  Manual Review
                </h3>
                <p className="text-3xl font-bold text-blue-600 mt-2">
                  {manualReviewJobs.length}
                </p>
              </div>
              <div className="p-3 bg-primary-light rounded-lg">
                <Eye className="w-6 h-6 text-primary-dark" />
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="dashboard-card">
          <div className="border-b border-border">
            <nav className="flex space-x-2 p-2">
              <button
                onClick={() => handleTabChange("filtered")}
                className={`px-4 py-2 rounded-lg transition-all duration-200 font-medium 
      flex items-center gap-2
      ${
        activeTab === "filtered"
          ? "bg-blue-500 text-white shadow-md"
          : "text-gray-600 hover:bg-blue-100"
      }`}
              >
                <Filter className="w-4 h-4" />
                Filtered Jobs ({filteredJobs.length})
              </button>

              <button
                onClick={() => handleTabChange("manual")}
                className={`px-4 py-2 rounded-lg transition-all duration-200 font-medium 
      flex items-center gap-2
      ${
        activeTab === "manual"
          ? "bg-blue-500 text-white shadow-md"
          : "text-gray-600 hover:bg-blue-100"
      }`}
              >
                <Eye className="w-4 h-4" />
                Manual Review ({manualReviewJobs.length})
              </button>
            </nav>
          </div>

          {/* Table Content */}
          <div className="min-h-[400px]">
            {activeTab === "filtered" && (
              <div key="filtered">{renderTable(filteredJobs, true)}</div>
            )}
            {activeTab === "manual" && (
              <div key="manual">{renderTable(manualReviewJobs, false)}</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
