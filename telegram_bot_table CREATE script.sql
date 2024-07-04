-- Table: public.telegram_bot_table

-- DROP TABLE IF EXISTS public.telegram_bot_table;

CREATE TABLE IF NOT EXISTS public.telegram_bot_table
(
    id bigint NOT NULL DEFAULT nextval('telegram_table_id_seq'::regclass),
    data_ins timestamp without time zone NOT NULL DEFAULT LOCALTIMESTAMP,
    status bigint NOT NULL DEFAULT 0,
    telegram_id bigint NOT NULL DEFAULT 0,
    text character varying(254) COLLATE pg_catalog."default" DEFAULT ''::character varying,
    salary bigint DEFAULT 0,
    employment character varying COLLATE pg_catalog."default" DEFAULT ''::character varying,
    CONSTRAINT telegram_bot_table_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.telegram_bot_table
    OWNER to postgres;
-- Index: idx_telegram_id

-- DROP INDEX IF EXISTS public.idx_telegram_id;

CREATE INDEX IF NOT EXISTS idx_telegram_id
    ON public.telegram_bot_table USING btree
    (telegram_id ASC NULLS LAST)
    INCLUDE(telegram_id)
    WITH (deduplicate_items=False)
    TABLESPACE pg_default;