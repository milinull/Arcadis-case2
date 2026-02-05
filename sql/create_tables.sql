CREATE SCHEMA case2;

-- Tabela contaminante
CREATE TABLE case2.contaminante(
	id SERIAL PRIMARY KEY,
	cas VARCHAR(50) UNIQUE NOT NULL,
	nome VARCHAR(250) NOT NULL
);

-- Tabela de dados de cada contaminante
CREATE TABLE case2.avaliacao_risco(
	id SERIAL PRIMARY KEY,
	contaminante_id INTEGER NOT NULL,
	efeito VARCHAR(2) NOT NULL CHECK (efeito IN ('C', 'NC')),
	solu_concentracao INTEGER DEFAULT 500,
	vor VARCHAR(150),
	valor_vor NUMERIC(20, 15),
	ambiente VARCHAR(15) CHECK (ambiente IN ('Aberto', 'Fechado')),
	concentracao_max NUMERIC(20, 15),
	
	CONSTRAINT fk_contaminante
	FOREIGN KEY(contaminante_id)
	REFERENCES case2.contaminante (id)
);

CREATE VIEW case2.vw_analise_processada AS
WITH base AS (
    SELECT
        a.id,
        a.contaminante_id,
        c.cas,
        c.nome,
        a.ambiente,
        a.efeito,
        a.vor,
        a.valor_vor,
        a.concentracao_max,
        a.solu_concentracao,

        -- Regra 2.2: menor valor entre C e NC
        MIN(a.concentracao_max) OVER (
            PARTITION BY a.contaminante_id, a.ambiente
        ) AS valor_considerado

    FROM case2.avaliacao_risco a
    JOIN case2.contaminante c
        ON c.id = a.contaminante_id
)

SELECT
    id,
    cas,
    nome,
    efeito,
    ambiente,
    vor,
    valor_vor,
    concentracao_max,
    solu_concentracao,
    valor_considerado,

    -- Regra 2.4: valor exibido
    CASE
        WHEN valor_considerado < valor_vor
            THEN valor_vor
        ELSE valor_considerado
    END AS valor_final,

    -- Regra 2.3: cinza
    (valor_considerado > solu_concentracao) AS aplicar_cinza,

    -- Regra 2.4: laranja
    (valor_considerado < valor_vor) AS aplicar_laranja

FROM base;

SELECT * FROM case2.contaminante;
SELECT * FROM case2.avaliacao_risco;
SELECT * FROM case2.vw_analise_processada;

DROP VIEW IF EXISTS case2.vw_analise_processada;
DROP TABLE IF EXISTS case2.avaliacao_risco;
DROP TABLE IF EXISTS case2.contaminante;