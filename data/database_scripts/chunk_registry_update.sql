SET search_path TO rgd;

-- Add explicit traceability fields
ALTER TABLE document_chunks
ADD COLUMN IF NOT EXISTS version VARCHAR(20),
ADD COLUMN IF NOT EXISTS chunk_number INT;

-- Remove temporary seed/demo chunks.
DELETE FROM document_chunks
WHERE chunk_id LIKE 'CH-DEMO-%';

ALTER TABLE document_chunks
ALTER COLUMN version SET NOT NULL;

ALTER TABLE document_chunks
ALTER COLUMN chunk_number SET NOT NULL;

ALTER TABLE document_chunks
ADD CONSTRAINT uq_document_version_chunk
UNIQUE (document_id, version, chunk_number);

CREATE INDEX idx_chunks_document_version
ON document_chunks(document_id, version);