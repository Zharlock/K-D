-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public."Pet"
(

    CONSTRAINT "Pet_pkey" PRIMARY KEY (pet_id)
);

CREATE TABLE IF NOT EXISTS public.customer
(
    id_type integer,
    nif numeric,
    CONSTRAINT customer_pkey PRIMARY KEY (customer_id),
    CONSTRAINT customer_email_key UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS public.enclosure
(

    CONSTRAINT enclosure_pkey PRIMARY KEY (enclosure_id)
);

CREATE TABLE IF NOT EXISTS public."Checkin"
(
    id_checkin serial NOT NULL,
    id_agenda integer NOT NULL,
    date_created timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    enclosure_id integer NOT NULL,
    PRIMARY KEY (id_checkin)
);

CREATE TABLE IF NOT EXISTS public."Checkout"
(
    id_checkout serial NOT NULL,
    id_checkin integer NOT NULL,
    date_created timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    obs text,
    id_pay integer NOT NULL,
    id_funcionario integer NOT NULL,
    PRIMARY KEY (id_checkout)
);

CREATE TABLE IF NOT EXISTS public."Funcionario"
(
    id_funcionario serial NOT NULL,
    nome text NOT NULL,
    cargo text NOT NULL,
    PRIMARY KEY (id_funcionario)
);

CREATE TABLE IF NOT EXISTS public."Pagamento"
(
    id_pay serial NOT NULL,
    payment text NOT NULL,
    PRIMARY KEY (id_pay)
);

CREATE TABLE IF NOT EXISTS public."Customer_type"
(
    id_type serial NOT NULL,
    type text NOT NULL,
    PRIMARY KEY (id_type)
);

CREATE TABLE IF NOT EXISTS public."Agenda"
(
    id_agenda serial NOT NULL,
    pet_id integer NOT NULL,
    customer_id integer NOT NULL,
    date_begin timestamp without time zone,
    date_end timestamp without time zone,
    id_oferta integer NOT NULL,
    date_mark timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_agenda)
);

CREATE TABLE IF NOT EXISTS public."Ofertas"
(
    id_oferta serial NOT NULL,
    tipo text,
    valor_dia integer,
    PRIMARY KEY (id_oferta)
);

ALTER TABLE IF EXISTS public."Pet"
    ADD CONSTRAINT "costumerID" FOREIGN KEY (customer_id)
    REFERENCES public.customer (customer_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Pet"
    ADD CONSTRAINT enclosure FOREIGN KEY (enclosure_id)
    REFERENCES public.enclosure (enclosure_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.customer
    ADD FOREIGN KEY (id_type)
    REFERENCES public."Customer_type" (id_type) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Checkin"
    ADD FOREIGN KEY (enclosure_id)
    REFERENCES public.enclosure (enclosure_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Checkin"
    ADD FOREIGN KEY (id_agenda)
    REFERENCES public."Agenda" (id_agenda) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Checkout"
    ADD FOREIGN KEY (id_pay)
    REFERENCES public."Pagamento" (id_pay) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Checkout"
    ADD FOREIGN KEY (id_funcionario)
    REFERENCES public."Funcionario" (id_funcionario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Checkout"
    ADD FOREIGN KEY (id_checkin)
    REFERENCES public."Checkin" (id_checkin) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Agenda"
    ADD CONSTRAINT pet_id FOREIGN KEY (pet_id)
    REFERENCES public."Pet" (pet_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Agenda"
    ADD CONSTRAINT id_oferta FOREIGN KEY (id_oferta)
    REFERENCES public."Ofertas" (id_oferta) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Agenda"
    ADD FOREIGN KEY (customer_id)
    REFERENCES public.customer (customer_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;