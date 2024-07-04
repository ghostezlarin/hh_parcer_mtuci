-- Table: public.hh_table

-- DROP TABLE IF EXISTS public.hh_table;

CREATE TABLE IF NOT EXISTS public.hh_table
(
    id bigint NOT NULL DEFAULT nextval('hh_parcing_id_seq'::regclass),
    date_ins timestamp without time zone NOT NULL DEFAULT LOCALTIMESTAMP,
    status bigint NOT NULL DEFAULT 0,
    hh_id bigint NOT NULL DEFAULT 0,
    hh_name character varying(254) COLLATE pg_catalog."default" NOT NULL DEFAULT ''::character varying,
    hh_salary_null bigint NOT NULL DEFAULT 0,
    hh_salary_from bigint NOT NULL DEFAULT 0,
    hh_salary_to bigint NOT NULL DEFAULT 0,
    hh_employment character varying COLLATE pg_catalog."default" NOT NULL DEFAULT ''::character varying,
    hh_schedule character varying COLLATE pg_catalog."default" NOT NULL DEFAULT ''::character varying,
    request_id bigint NOT NULL DEFAULT 1,
    CONSTRAINT hh_table_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.hh_table
    OWNER to postgres;