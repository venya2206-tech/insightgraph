"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

interface EntityRelationship {
  entity: string;
  sources: { source_title: string; source_type: string }[];
  related_entities: { related_entity: string; entity_type: string }[];
}

export default function KnowledgeGraphPage() {
  const router = useRouter();
  const [entityName, setEntityName] = useState("");
  const [result, setResult] = useState<EntityRelationship | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function searchEntity() {
    if (!entityName) return;
    setLoading(true);
    setError("");
    try {
      const data = await api.getEntityRelationships(entityName);
      if (data) {
        setResult(data);
      } else {
        setError("Entity not found");
      }
    } catch (err) {
      setError("Error fetching entity");
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

        <h1 className="text-3xl font-bold mb-6">🔍 Knowledge Graph Explorer</h1>

        {/* Search */}
        <div className="bg-gray-800 p-6 rounded-lg mb-8">
          <h2 className="text-xl font-bold mb-4">Find Entity Relationships</h2>
          <div className="flex gap-4">
            <input
              type="text"
              placeholder="Enter entity name (e.g., Google, Microsoft)"
              value={entityName}
              onChange={(e) => setEntityName(e.target.value)}
              className="flex-1 bg-gray-700 p-3 rounded"
              onKeyPress={(e) => e.key === "Enter" && searchEntity()}
            />
            <button
              onClick={searchEntity}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-6 py-3 rounded"
            >
              {loading ? "Searching..." : "Search"}
            </button>
          </div>
          {error && (
            <div className="mt-4 bg-red-600 p-3 rounded">{error}</div>
          )}
        </div>

        {/* Results */}
        {result && (
          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-2xl font-bold mb-6 text-blue-400">
              {result.entity}
            </h2>

            {/* Sources mentioning this entity */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-3 text-green-400">
                📄 Sources Mentioning This Entity
              </h3>
              {result.sources.length === 0 ? (
                <p className="text-gray-400">No sources found</p>
              ) : (
                <div className="space-y-2">
                  {result.sources.map((source, idx) => (
                    <div key={idx} className="bg-gray-700 p-3 rounded">
                      <div className="font-medium">{source.source_title}</div>
                      <div className="text-sm text-gray-400">
                        Type: {source.source_type}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Related entities */}
            <div>
              <h3 className="text-lg font-semibold mb-3 text-yellow-400">
                🔗 Related Entities
              </h3>
              {result.related_entities.length === 0 ? (
                <p className="text-gray-400">No related entities found</p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {result.related_entities.map((entity, idx) => (
                    <button
                      key={idx}
                      onClick={() => {
                        setEntityName(entity.related_entity);
                        searchEntity();
                      }}
                      className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-full cursor-pointer"
                    >
                      {entity.related_entity} ({entity.entity_type})
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Instructions */}
        {!result && !loading && (
          <div className="bg-gray-800 p-6 rounded-lg text-center">
            <p className="text-gray-400">
              Enter an entity name above to explore its relationships in the knowledge graph.
            </p>
            <p className="text-gray-500 mt-2 text-sm">
              Try: Google, Microsoft, McKinsey, Amazon
            </p>
          </div>
        )}
      </div>
    </div>
  );
}