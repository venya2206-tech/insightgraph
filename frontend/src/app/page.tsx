"use client";

import { useEffect, useState } from "react";
import { api, ResearchProject, GraphOverview } from "@/lib/api";

export default function Dashboard() {
  const [projects, setProjects] = useState<ResearchProject[]>([]);
  const [overview, setOverview] = useState<GraphOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [showNewProject, setShowNewProject] = useState(false);
  const [topic, setTopic] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const [projectsData, overviewData] = await Promise.all([
        api.getProjects(),
        api.getOverview(),
      ]);
      // Safety check: ensure projectsData is always an array
      setProjects(Array.isArray(projectsData) ? projectsData : []);
      setOverview(overviewData);
    } catch (error) {
      console.error("Error loading data:", error);
      setProjects([]);
    } finally {
      setLoading(false);
    }
  }

  async function createProject() {
    if (!topic) return;
    try {
      await api.createProject(topic, description);
      setTopic("");
      setDescription("");
      setShowNewProject(false);
      loadData();
    } catch (error) {
      console.error("Error creating project:", error);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold">🔍 InsightGraph</h1>
            <p className="text-gray-400 mt-2">AI-Powered Research Platform</p>
          </div>
          <button
            onClick={() => setShowNewProject(true)}
            className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold"
          >
            + New Research
          </button>
        </div>

        {/* Stats */}
        {overview && (
          <div className="grid grid-cols-4 gap-4 mb-8">
            <div className="bg-gray-800 p-6 rounded-lg">
              <div className="text-3xl font-bold text-blue-400">
                {overview.total_nodes.find((n) => n.label[0] === "Source")?.count || 0}
              </div>
              <div className="text-gray-400">Sources</div>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg">
              <div className="text-3xl font-bold text-green-400">
                {overview.total_nodes.find((n) => n.label[0] === "Entity")?.count || 0}
              </div>
              <div className="text-gray-400">Entities</div>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg">
              <div className="text-3xl font-bold text-yellow-400">
                {overview.total_nodes.find((n) => n.label[0] === "Claim")?.count || 0}
              </div>
              <div className="text-gray-400">Claims</div>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg">
              <div className="text-3xl font-bold text-purple-400">
                {overview.total_relationships.find((r) => r.type === "MENTIONS")?.count || 0}
              </div>
              <div className="text-gray-400">Relationships</div>
            </div>
          </div>
        )}

        {/* New Project Form */}
        {showNewProject && (
          <div className="bg-gray-800 p-6 rounded-lg mb-8">
            <h2 className="text-xl font-bold mb-4">Create New Research Project</h2>
            <input
              type="text"
              placeholder="Topic (e.g., AI Impact on Economy)"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="w-full bg-gray-700 p-3 rounded mb-4"
            />
            <textarea
              placeholder="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-gray-700 p-3 rounded mb-4 h-24"
            />
            <div className="flex gap-4">
              <button
                onClick={createProject}
                className="bg-green-600 hover:bg-green-700 px-6 py-2 rounded"
              >
                Create
              </button>
              <button
                onClick={() => setShowNewProject(false)}
                className="bg-gray-600 hover:bg-gray-700 px-6 py-2 rounded"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* Projects List */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold mb-4">Research Projects</h2>
          {projects.length === 0 ? (
            <p className="text-gray-400">No projects yet. Create one to get started!</p>
          ) : (
            <div className="space-y-4">
              {projects.map((project) => (
                <div
                  key={project.id}
                  className="bg-gray-700 p-4 rounded-lg hover:bg-gray-600 cursor-pointer"
                >
                  <h3 className="font-semibold">{project.topic}</h3>
                  <p className="text-gray-400 text-sm">{project.description}</p>
                  <p className="text-gray-500 text-xs mt-2">
                    Created: {new Date(project.created_at).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Top Entities */}
        {overview && overview.top_entities.length > 0 && (
          <div className="bg-gray-800 rounded-lg p-6 mt-8">
            <h2 className="text-xl font-bold mb-4">Top Entities</h2>
            <div className="flex flex-wrap gap-2">
              {overview.top_entities.map((entity, idx) => (
                <span
                  key={idx}
                  className="bg-gray-700 px-3 py-1 rounded-full text-sm"
                >
                  {entity.name} ({entity.entity_type})
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
