"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, ResearchProject } from "@/lib/api";

export default function AddSourcePage() {
  const router = useRouter();
  const [projects, setProjects] = useState<ResearchProject[]>([]);
  const [selectedProject, setSelectedProject] = useState("");
  const [sourceType, setSourceType] = useState("text");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    api.getProjects().then(setProjects);
  }, []);

  async function handleSubmit() {
    if (!selectedProject || !input) return;
    setLoading(true);
    try {
      await api.addSource(selectedProject, sourceType, input);
      setSuccess(true);
      setInput("");
      setTimeout(() => setSuccess(false), 3000);
    } catch (error) {
      console.error("Error adding source:", error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-2xl mx-auto">
        <button
          onClick={() => router.push("/")}
          className="text-gray-400 hover:text-white mb-6"
        >
          ← Back to Dashboard
        </button>

        <h1 className="text-3xl font-bold mb-6">Add Source</h1>

        <div className="bg-gray-800 p-6 rounded-lg">
          {/* Project Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">Research Project</label>
            <select
              value={selectedProject}
              onChange={(e) => setSelectedProject(e.target.value)}
              className="w-full bg-gray-700 p-3 rounded"
            >
              <option value="">Select a project...</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.topic}
                </option>
              ))}
            </select>
          </div>

          {/* Source Type */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">Source Type</label>
            <div className="flex gap-4">
              {["text", "url", "pdf"].map((type) => (
                <button
                  key={type}
                  onClick={() => setSourceType(type)}
                  className={`px-4 py-2 rounded ${
                    sourceType === type
                      ? "bg-blue-600"
                      : "bg-gray-700 hover:bg-gray-600"
                  }`}
                >
                  {type.toUpperCase()}
                </button>
              ))}
            </div>
          </div>

          {/* Input */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">
              {sourceType === "text"
                ? "Paste your text"
                : sourceType === "url"
                ? "Enter URL"
                : "Upload PDF"}
            </label>
            {sourceType === "text" ? (
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Paste your research text here..."
                className="w-full bg-gray-700 p-3 rounded h-40"
              />
            ) : (
              <input
                type={sourceType === "url" ? "url" : "file"}
                value={sourceType === "url" ? input : undefined}
                onChange={(e) =>
                  sourceType === "url"
                    ? setInput(e.target.value)
                    : setInput(e.target.files?.[0]?.name || "")
                }
                placeholder={sourceType === "url" ? "https://example.com/article" : ""}
                className="w-full bg-gray-700 p-3 rounded"
              />
            )}
          </div>

          {/* Submit */}
          <button
            onClick={handleSubmit}
            disabled={loading || !selectedProject || !input}
            className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-600 py-3 rounded font-semibold"
          >
            {loading ? "Processing..." : "Add Source"}
          </button>

          {success && (
            <div className="mt-4 bg-green-600 p-3 rounded text-center">
              Source added successfully! ✅
            </div>
          )}
        </div>
      </div>
    </div>
  );
}