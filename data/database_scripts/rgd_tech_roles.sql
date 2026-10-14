-- ============================================================
-- READ-ONLY ROLES FOR HYBRID RAG
-- ============================================================


-- Development setup.
-- These roles are recreated when this script is run.

DROP ROLE IF EXISTS rag_support;
DROP ROLE IF EXISTS rag_admin;


-- Create login roles.
-- Replace these placeholders with strong passwords BEFORE running.
CREATE ROLE rag_support
LOGIN
PASSWORD 'support123';

CREATE ROLE rag_admin
LOGIN
PASSWORD 'admin123';


-- ============================================================
-- SCHEMA ACCESS
-- ============================================================

GRANT USAGE ON SCHEMA rgd
TO rag_support, rag_admin;


-- Remove any accidentally granted privileges.
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA rgd
FROM rag_support, rag_admin;


-- ============================================================
-- SUPPORT
-- READ-ONLY: LIMITED TABLE ACCESS
-- ============================================================

GRANT SELECT ON
    rgd.customers,
    rgd.products,
    rgd.orders,
    rgd.order_items,
    rgd.payments,
    rgd.shipments,
    rgd.returns,
    rgd.refunds
TO rag_support;


-- ============================================================
-- ADMIN
-- READ-ONLY: ALL TABLE ACCESS
-- ============================================================

GRANT SELECT ON ALL TABLES IN SCHEMA rgd
TO rag_admin;


-- Admin automatically gets SELECT on future tables created
-- by the same object owner.
ALTER DEFAULT PRIVILEGES IN SCHEMA rgd
GRANT SELECT ON TABLES TO rag_admin;