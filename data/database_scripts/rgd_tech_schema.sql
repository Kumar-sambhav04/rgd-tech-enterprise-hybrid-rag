-- RGD Tech Enterprise Hybrid RAG
-- PostgreSQL schema
-- Final ALC model:
--   support: customer/order/support operational data
--   admin: all data
-- PDF ALC is represented by documents/document_chunks.access_level.
-- Support-accessible PDFs use 'support'; admin-only PDFs use 'admin'.

CREATE SCHEMA IF NOT EXISTS rgd;
SET search_path TO rgd;

CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    customer_segment VARCHAR(30) NOT NULL CHECK (customer_segment IN ('consumer','business')),
    status VARCHAR(20) NOT NULL CHECK (status IN ('active','inactive')),
    registration_date DATE NOT NULL
);

CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    sku VARCHAR(40) UNIQUE NOT NULL,
    product_name VARCHAR(120) NOT NULL,
    category VARCHAR(30) NOT NULL,
    price NUMERIC(12,2) NOT NULL CHECK (price >= 0),
    warranty_months INT NOT NULL CHECK (warranty_months >= 0),
    status VARCHAR(20) NOT NULL CHECK (status IN ('active','discontinued'))
);

CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    order_status VARCHAR(30) NOT NULL,
    total_amount NUMERIC(12,2) NOT NULL CHECK (total_amount >= 0),
    payment_status VARCHAR(30) NOT NULL,
    shipping_status VARCHAR(30) NOT NULL
);

CREATE TABLE order_items (
    order_item_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL REFERENCES orders(order_id),
    product_id VARCHAR(20) NOT NULL REFERENCES products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    discount NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (discount >= 0)
);

CREATE TABLE payments (
    payment_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL REFERENCES orders(order_id),
    payment_method VARCHAR(30) NOT NULL,
    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    payment_status VARCHAR(30) NOT NULL,
    payment_date DATE NOT NULL
);

CREATE TABLE shipments (
    shipment_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL REFERENCES orders(order_id),
    carrier VARCHAR(50) NOT NULL,
    tracking_number VARCHAR(60) UNIQUE,
    shipped_date DATE,
    estimated_delivery DATE,
    actual_delivery DATE,
    shipment_status VARCHAR(30) NOT NULL
);

CREATE TABLE returns (
    return_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL REFERENCES orders(order_id),
    order_item_id VARCHAR(20) NOT NULL REFERENCES order_items(order_item_id),
    return_reason VARCHAR(120) NOT NULL,
    return_date DATE NOT NULL,
    return_status VARCHAR(30) NOT NULL,
    inspection_result VARCHAR(80)
);

CREATE TABLE refunds (
    refund_id VARCHAR(20) PRIMARY KEY,
    return_id VARCHAR(20) NOT NULL REFERENCES returns(return_id),
    payment_id VARCHAR(20) NOT NULL REFERENCES payments(payment_id),
    refund_amount NUMERIC(12,2) NOT NULL CHECK (refund_amount >= 0),
    refund_status VARCHAR(30) NOT NULL,
    processed_date DATE
);

CREATE TABLE warehouses (
    warehouse_id VARCHAR(20) PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    city VARCHAR(80) NOT NULL
);

CREATE TABLE inventory (
    product_id VARCHAR(20) NOT NULL REFERENCES products(product_id),
    warehouse_id VARCHAR(20) NOT NULL REFERENCES warehouses(warehouse_id),
    quantity_available INT NOT NULL CHECK (quantity_available >= 0),
    quantity_reserved INT NOT NULL CHECK (quantity_reserved >= 0),
    reorder_level INT NOT NULL CHECK (reorder_level >= 0),
    PRIMARY KEY (product_id, warehouse_id)
);

CREATE TABLE employees (
    employee_id VARCHAR(20) PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    department VARCHAR(40) NOT NULL,
    role VARCHAR(60) NOT NULL,
    access_level VARCHAR(30) NOT NULL CHECK (access_level IN ('support','admin')),
    status VARCHAR(20) NOT NULL CHECK (status IN ('active','inactive'))
);

CREATE TABLE documents (
    document_id VARCHAR(30) PRIMARY KEY,
    filename VARCHAR(150) UNIQUE NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    department VARCHAR(40) NOT NULL,
    version VARCHAR(20) NOT NULL,
    effective_date DATE NOT NULL,
    access_level VARCHAR(30) NOT NULL CHECK (access_level IN ('support','admin')),
    status VARCHAR(20) NOT NULL CHECK (status IN ('active','expired'))
);

CREATE TABLE document_chunks (
    chunk_id VARCHAR(40) PRIMARY KEY,
    document_id VARCHAR(30) NOT NULL REFERENCES documents(document_id),
    page_number INT NOT NULL CHECK (page_number > 0),
    section VARCHAR(150) NOT NULL,
    access_level VARCHAR(30) NOT NULL CHECK (access_level IN ('support','admin'))
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_payments_order ON payments(order_id);
CREATE INDEX idx_shipments_order ON shipments(order_id);
CREATE INDEX idx_returns_order ON returns(order_id);
CREATE INDEX idx_refunds_return ON refunds(return_id);
CREATE INDEX idx_documents_access ON documents(access_level);
CREATE INDEX idx_chunks_document ON document_chunks(document_id);
CREATE INDEX idx_chunks_access ON document_chunks(access_level);
