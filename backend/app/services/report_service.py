from typing import Dict, List
from app.services.llm_service import LLMService
from app.services.analysis_service import AnalysisService
from app.core.neo4j_driver import get_neo4j_driver


class ReportService:
    def __init__(self):
        self.llm = LLMService()
        self.analysis = AnalysisService()

    async def generate_report(self, research_id: str = None) -> Dict:
        overview = await self.analysis.get_research_overview()
        top_entities = overview.get("top_entities", [])

        entity_list = ", ".join([e["name"] for e in top_entities[:10]])
        entity_types = {}
        for e in top_entities:
            etype = e["entity_type"]
            entity_types[etype] = entity_types.get(etype, 0) + 1

        type_summary = ", ".join([f"{k}: {v}" for k, v in entity_types.items()])

        prompt = f"""Write a professional research report based on the following data:

Entities Found: {entity_list}
Entity Categories: {type_summary}
Total Sources Analyzed: {[n for n in overview.get("total_nodes", []) if "Source" in str(n.get("label", []))][0].get("count", 0) if overview.get("total_nodes") else 0}

Please write:
1. Executive Summary (2-3 sentences)
2. Key Findings (bullet points)
3. Entity Analysis (describe the main entities found)
4. Recommendations (2-3 recommendations based on the data)

Format it as a clean markdown report."""

        report_content = await self.llm.generate(prompt)

        return {
            "report": report_content,
            "data_used": {
                "entities": entity_list,
                "categories": type_summary,
                "overview": overview
            }
        }

    async def get_entity_report(self, entity_name: str) -> Dict:
        entity_data = await self.analysis.find_source_connections(entity_name)

        prompt = f"""Write a detailed analysis about the entity "{entity_name}" based on this data:

Connected Sources: {entity_data}

Write:
1. Entity Profile
2. Sources Mentioning This Entity
3. Key Relationships
4. Significance

Format as markdown."""

        report_content = await self.llm.generate(prompt)

        return {
            "entity": entity_name,
            "report": report_content,
            "connections": entity_data
        }