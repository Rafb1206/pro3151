drop table if exists public.customers cascade;
CREATE TABLE public.customers (
	customer_id BIGINT NOT NULL,
	name text NULL,
	cpf text NULL,
	phone text NULL,
	email text NULL,
	payment_status varchar(1) NOT NULL,
	is_active bool DEFAULT true NOT NULL,
	insert_date timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
	trial_expires_at timestamptz NULL,
	CONSTRAINT customers_pkey PRIMARY KEY (customer_id)
);
CREATE UNIQUE INDEX ix_customers_cpf_unique ON public.customers USING btree (cpf) WHERE (cpf IS NOT NULL);

drop table if exists public.stores;
CREATE TABLE public.stores (
    store_id BIGINT NOT  null,
	customer_id BIGINT NOT NULL,
    name text NULL,
    cnpj text NULL,
    is_active bool DEFAULT true NOT NULL,
    insert_date timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT stores_pkey PRIMARY KEY (store_id)
);
-- public.data_sources foreign keys
CREATE INDEX idx_stores_customer_id ON public.stores USING btree (customer_id, store_id);
CREATE UNIQUE INDEX ix_stores_cnpj_unique ON public.stores USING btree (cnpj) WHERE (cnpj IS NOT NULL);
ALTER TABLE public.stores ADD CONSTRAINT stores_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);



-- Table 2: Orders Analytics (Converted to PostgreSQL types)
drop table if exists public.orders_analytics 
CREATE TABLE IF NOT EXISTS public.orders_analytics (
    -- IDs are often Strings in analytics tables to handle various source systems
    customer_id BIGINT, 
    store_id BIGINT,
    data_source TEXT,
    
    -- INT64 maps to BIGINT in Postgres
    buyer_id BIGINT,
    buyer_nick TEXT,
    order_id BIGINT,
    pack_id BIGINT,
    
    -- Ideally, convert String dates to TIMESTAMP for better querying
    -- If your raw data is messy, keep it as TEXT. Here I use TIMESTAMP for best practice.
    order_date TIMESTAMP, 
    
    prod_id TEXT,
    prod_sku TEXT,
    prod_desc TEXT,
    item_picture TEXT,
    order_link TEXT,
    item_category_id TEXT,
    tipo_anuncio TEXT,
    order_quantity BIGINT, -- changed from string to bigint for math
    
    -- Monetary/Price values
    -- FLOAT64 maps to DOUBLE PRECISION. 
    -- For strict financial accounting, use NUMERIC, but for analytics DOUBLE PRECISION is faster.
    order_unit_price DOUBLE PRECISION,
    order_total_price DOUBLE PRECISION,
    fixed_fee DOUBLE PRECISION,
    total_fixed_fee DOUBLE PRECISION,
    percetage_fee DOUBLE PRECISION,
    value_percentage_fee DOUBLE PRECISION,
    total_percentage_fee DOUBLE PRECISION,
    order_fee DOUBLE PRECISION,
    order_total_fee DOUBLE PRECISION,
    order_rebait DOUBLE PRECISION,
    order_total_rebait DOUBLE PRECISION,
    order_total_free_fee DOUBLE PRECISION,
    
    tax_regime TEXT,
    total_tax DOUBLE PRECISION,
    user_defined_tax DOUBLE PRECISION,
    user_tax_amount DOUBLE PRECISION,
    gov_tax_amount DOUBLE PRECISION,
    prod_cost DOUBLE PRECISION,
    prod_extra_cost DOUBLE PRECISION,
    net_profit DOUBLE PRECISION,
    profit_margin DOUBLE PRECISION,
    target_margin DOUBLE PRECISION,
    target_price DOUBLE PRECISION,
    
    order_status TEXT
);

-- Optional: Create an index on customer_id to speed up joins between the two tables
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON public.orders_analytics USING btree (customer_id, store_id);