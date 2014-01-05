CREATE EXTENSION pg_trgm;
CREATE INDEX location_name_trigram_idx ON location USING gist(name gist_trgm_ops);
CREATE INDEX location_short_name_trigram_idx ON location USING gist(short_name gist_trgm_ops);
CREATE INDEX location_description_trigram_idx ON location USING gist(description gist_trgm_ops);
