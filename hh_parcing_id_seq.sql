-- SEQUENCE: public.hh_parcing_id_seq

-- DROP SEQUENCE IF EXISTS public.hh_parcing_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.hh_parcing_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1
    OWNED BY public.hh_table.id;

ALTER SEQUENCE public.hh_parcing_id_seq
    OWNER TO postgres;