-- SEQUENCE: public.telegram_table_id_seq

-- DROP SEQUENCE IF EXISTS public.telegram_table_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.telegram_table_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9999999
    CACHE 1
    OWNED BY public.telegram_bot_table.id;

ALTER SEQUENCE public.telegram_table_id_seq
    OWNER TO postgres;