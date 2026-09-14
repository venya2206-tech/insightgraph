"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

export default function ReportsPage() {
  const router = useRouter();
  const [report, setReport] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [reportData, setReportData] = useState<any>(null);

  async function generateReport() {
    setLoading(true);
    try {
      const result = await api.generateReport();
      setReport(result.report);
      setReportData(result.data_used);
    } catch (error) {
      console.error("Error generating report:", error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <button
          onClick={() => router.push("/")}
          className="text-gray-400 hover:text-white mb-6"
        >
          ← Back to Dashboard
        </button>

        <h1 className="text-3xl font-bold mb-6">📝 Research Reports</h1>

        {/* Generate Button */}
        <div className="bg-gray-800 p-6 rounded-lg mb-8">
          <h2 className="text-xl font-bold mb-4">Generate AI Report</h2>
          <p className="text-gray-400 mb-4">
            Click below to generate a research report based on all your ingested data.
          </p>
          <button
            onClick={generateReport}
            disabled={loading}
            className="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 px-6 py-3 rounded font-semibold"
          >
            {loading ? "Generating..." : "🚀 Generate Report"}
          </button>
        </div>

        {/* Report Display */}
        {report && (
          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-bold mb-4">Generated Report</h2>
            
            {/* Data Used */}
            {reportData && (
              <div className="bg-gray-700 p-4 rounded mb-6">
                <h3 className="font-semibold mb-2">Data Used:</h3>
                <div className="text-sm text-gray-300">
                  <p><strong>Entities:</strong> {reportData.entities}</p>
                  <p><strong>Categories:</strong> {reportData.categories}</p>
                </div>
              </div>
            )}

            {/* Report Content */}
            <div className="prose prose-invert max-w-none">
              <div className="whitespace-pre-wrap bg-gray-700 p-4 rounded">
                {report}
              </div>
            </div>
          </div>
        )}

        {/* Instructions */}
        {!report && !loading && (
          <div className="bg-gray-800 p-6 rounded-lg text-center">
            <p className="text-gray-400">
              Click the button above to generate a research report from your data.
            </p>
            <p className="text-gray-500 mt-2 text-sm">
              The report will be created based on all entities and sources in your knowledge graph.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}