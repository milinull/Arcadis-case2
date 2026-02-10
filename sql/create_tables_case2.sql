CREATE SCHEMA case2;

CREATE TABLE case2.avaliacao_risco (
    id SERIAL PRIMARY KEY,
    cas VARCHAR(50),
    contaminante VARCHAR(255),
    efeito VARCHAR(2) CHECK (efeito IN ('C', 'NC')),
    ambientes_abertos NUMERIC,
    ambientes_fechados NUMERIC,
    vor_nome VARCHAR(150),
    valor_vor NUMERIC,
    solubilidade INTEGER DEFAULT 500,
    menor_valor_final NUMERIC,
    is_cinza BOOLEAN,
    is_laranja BOOLEAN
);

TRUNCATE TABLE case2.avaliacao_risco;

SELECT * FROM case2.avaliacao_risco;

ALTER ROLE postgres SET search_path = case1,case2,case3,public;