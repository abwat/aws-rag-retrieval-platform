# Ingestion

Ingestion normalizes source documents, applies chunking, writes index artifacts, and records the chunking strategy used. Each index build should be reproducible from a source revision and configuration file.

A production ingestion job should run separately from the API so query serving remains stable during document refreshes. Failed ingestion should keep the last known-good index active.

