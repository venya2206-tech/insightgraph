import httpx
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.source import Source, Chunk
from app.models.entity import Entity
from app.models.claim import Claim
from app.schemas.source import SourceCreate
from app.services.chunker import semantic_chunk
from app.services.nlp_service import NLPService


class IngestionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.nlp = NLPService()

    async def ingest_source(self, research_id: UUID, source: SourceCreate) -> Source:
        db_source = Source(
            research_id=research_id,
            source_type=source.source_type,
            original_input=source.input,
            url=source.url,
        )

        if source.source_type == 'url':
            raw_text = await self._scrape_url(source.url)
            db_source.raw_text = raw_text
            db_source.title = await self._extract_title(raw_text)
        elif source.source_type == 'text':
            db_source.raw_text = source.input
            db_source.title = source.input[:100]

        db_source.processed = True
        self.db.add(db_source)
        await self.db.commit()
        await self.db.refresh(db_source)

        if db_source.raw_text:
            chunks = semantic_chunk(db_source.raw_text)
            for i, chunk_text in enumerate(chunks):
                chunk = Chunk(
                    source_id=db_source.id,
                    chunk_index=i,
                    text=chunk_text,
                )
                self.db.add(chunk)
                await self.db.commit()
                await self.db.refresh(chunk)

                nlp_results = self.nlp.process_chunk(chunk_text)

                for ent_data in nlp_results['entities']:
                    entity = Entity(
                        chunk_id=chunk.id,
                        name=ent_data['name'],
                        entity_type=ent_data['entity_type'],
                        confidence=ent_data['confidence']
                    )
                    self.db.add(entity)

                for claim_data in nlp_results['claims']:
                    claim = Claim(
                        chunk_id=chunk.id,
                        claim_text=claim_data['claim_text'],
                        claim_type=claim_data['claim_type'],
                        confidence=claim_data['confidence']
                    )
                    self.db.add(claim)

            await self.db.commit()

        return db_source

    async def _scrape_url(self, url: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                    tag.decompose()
                return soup.get_text(separator='\n', strip=True)
        except Exception as e:
            return f'Error scraping URL: {str(e)}'

    async def _extract_title(self, text: str) -> str:
        lines = text.strip().split('\n')
        for line in lines[:5]:
            if len(line.strip()) > 10:
                return line.strip()[:200]
        return 'Untitled'
