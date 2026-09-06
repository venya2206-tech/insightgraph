const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ResearchProject {
  id: string;
  topic: string;
  description: string;
  created_at: string;
}

export interface Source {
  id: string;
  research_id: string;
  source_type: string;
  title: string;
  processed: boolean;
}

export interface Entity {
  name: string;
  entity_type: string;
  frequency: number;
}

export interface GraphOverview {
  total_nodes: { label: string[]; count: number }[];
  total_relationships: { type: string; count: number }[];
  top_entities: Entity[];
}

export interface Report {
  report: string;
  data_used: {
    entities: string;
    categories: string;
    overview: GraphOverview;
  };
}

export const api = {
  async getProjects(): Promise<ResearchProject[]> {
    const res = await fetch(`${API_BASE}/research`);
    if (!res.ok) return [];
    return res.json();
  },

  async createProject(topic: string, description: string): Promise<ResearchProject> {
    const res = await fetch(`${API_BASE}/research`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, description }),
    });
    return res.json();
  },

  async addSource(researchId: string, sourceType: string, input: string): Promise<Source> {
    const res = await fetch(`${API_BASE}/ingestion/research/${researchId}/sources`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source_type: sourceType, input }),
    });
    return res.json();
  },

  async getOverview(): Promise<GraphOverview> {
    const res = await fetch(`${API_BASE}/api/v1/analysis/overview`);
    if (!res.ok) return { total_nodes: [], total_relationships: [], top_entities: [] };
    return res.json();
  },

  async getEntityFrequency(limit: number = 20): Promise<Entity[]> {
    const res = await fetch(`${API_BASE}/api/v1/analysis/entities/frequency?limit=${limit}`);
    if (!res.ok) return [];
    return res.json();
  },

  async generateReport(): Promise<Report> {
    const res = await fetch(`${API_BASE}/api/v1/reports/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: "{}",
    });
    return res.json();
  },

  async getEntityRelationships(entityName: string) {
    const res = await fetch(`${API_BASE}/knowledge-graph/entity/${entityName}`);
    if (!res.ok) return null;
    return res.json();
  },
};
