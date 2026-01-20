#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
CREATE ROLE church_account LOGIN PASSWORD 'password';
CREATE ROLE migration LOGIN PASSWORD 'password';

GRANT CONNECT ON DATABASE church_accounting TO church_account;
GRANT CONNECT ON DATABASE church_accounting TO migration;

GRANT USAGE ON SCHEMA public TO church_account;
GRANT USAGE, CREATE ON SCHEMA public TO migration;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO church_account;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO church_account;

ALTER DEFAULT PRIVILEGES FOR ROLE migration IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO church_account;

ALTER DEFAULT PRIVILEGES FOR ROLE migration IN SCHEMA public
    GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO church_account;
EOSQL