TRUNCATE TABLE case2.avaliacao_risco CASCADE;

INSERT INTO case2.contaminante (cas, nome) VALUES
('630-20-6', 'Tetrachloroethane, 1,1,1,2-'),
('71-55-6',  'Trichloroethane, 1,1,1-'),
('79-34-5',  'Tetrachloroethane, 1,1,2,2-'),
('79-00-5',  'Trichloroethane, 1,1,2-'),
('75-34-3',  'Dichloroethane, 1,1-'),
('107-06-2', 'Dichloroethane, 1,2-'),
('74-87-3',  'Chloromethane'),
('75-09-2',  'Methylene Chloride'),
('56-23-5',  'Carbon Tetrachloride'),
('106-93-4', 'Dibromoethane, 1,2-'),
('76-01-7',  'Pentachloroethane');

INSERT INTO case2.avaliacao_risco (contaminante_id, efeito, ambiente, concentracao_max, vor, valor_vor, solu_concentracao)
SELECT id, 'C', 'Aberto', 79.2743508421658, 'Ficticio 01', 15, 500.0 FROM case2.contaminante WHERE cas = '630-20-6' UNION ALL
SELECT id, 'C', 'Fechado', 9.4762105236626, 'Ficticio 01', 15, 500.0 FROM case2.contaminante WHERE cas = '630-20-6';

INSERT INTO case2.avaliacao_risco (contaminante_id, efeito, ambiente, concentracao_max, vor, valor_vor, solu_concentracao)
SELECT id, 'NC', 'Aberto', 22987.8564772035, 'Ficticio 02', 1000, 500.0 FROM case2.contaminante WHERE cas = '71-55-6' UNION ALL
SELECT id, 'NC', 'Fechado', 2078.70016625216, 'Ficticio 02', 1000, 500.0 FROM case2.contaminante WHERE cas = '71-55-6';

INSERT INTO case2.avaliacao_risco (contaminante_id, efeito, ambiente, concentracao_max, vor, valor_vor, solu_concentracao)
SELECT id, 'C', 'Aberto', 30.2836927093189, 'Ficticio 02', 50, 500.0 FROM case2.contaminante WHERE cas = '79-34-5' UNION ALL
SELECT id, 'C', 'Fechado', 5.5633121395447, 'Ficticio 02', 50, 500.0 FROM case2.contaminante WHERE cas = '79-34-5';

INSERT INTO case2.avaliacao_risco (contaminante_id, efeito, ambiente, concentracao_max, vor, valor_vor, solu_concentracao)
SELECT id, 'C',  'Aberto', 52.3284517427652, 'Ficticio 01', 220, 500.0 FROM case2.contaminante WHERE cas = '79-00-5' UNION ALL
SELECT id, 'C',  'Fechado', 7.6966185108817, 'Ficticio 01', 220, 500.0 FROM case2.contaminante WHERE cas = '79-00-5' UNION ALL
SELECT id, 'NC', 'Aberto', 5.3396379329352, 'Ficticio 01', 220, 500.0 FROM case2.contaminante WHERE cas = '79-00-5' UNION ALL
SELECT id, 'NC', 'Fechado', 0.7853692358043, 'Ficticio 01', 220, 500.0 FROM case2.contaminante WHERE cas = '79-00-5';

INSERT INTO case2.avaliacao_risco (contaminante_id, efeito, ambiente, concentracao_max, vor, valor_vor, solu_concentracao)
SELECT id, 'C', 'Aberto', 162.0577274029640, 'Ficticio 01', 160, 500.0 FROM case2.contaminante WHERE cas = '75-34-3' UNION ALL
SELECT id, 'C', 'Fechado', 15.8340629306255, 'Ficticio 01', 160, 500.0 FROM case2.contaminante WHERE cas = '75-34-3';

INSERT INTO case2.avaliacao_risco (contaminante_id, efeito, ambiente, concentracao_max, vor, valor_vor, solu_concentracao)
SELECT id, 'C',  'Aberto', 22.3958531046367, 'Ficticio 01', 250, 500.0 FROM case2.contaminante WHERE cas = '107-06-2' UNION ALL
SELECT id, 'C',  'Fechado', 2.9091163265438, 'Ficticio 01', 250, 500.0 FROM case2.contaminante WHERE cas = '107-06-2' UNION ALL
SELECT id, 'NC', 'Aberto', 129.9759331965520, 'Ficticio 01', 250, 500.0 FROM case2.contaminante WHERE cas = '107-06-2' UNION ALL
SELECT id, 'NC', 'Fechado', 16.8832643951205, 'Ficticio 01', 250, 500.0 FROM case2.contaminante WHERE cas = '107-06-2';

INSERT INTO case2.avaliacao_risco (contaminante_id, efeito, ambiente, concentracao_max, vor, valor_vor, solu_concentracao)
SELECT id, 'NC', 'Aberto', 386.4716170347990, 'Ficticio 01', 36, 500.0 FROM case2.contaminante WHERE cas = '74-87-3' UNION ALL
SELECT id, 'NC', 'Fechado', 35.7569419291723, 'Ficticio 01', 36, 500.0 FROM case2.contaminante WHERE cas = '74-87-3';

INSERT INTO case2.avaliacao_risco (contaminante_id, efeito, ambiente, concentracao_max, vor, valor_vor, solu_concentracao)
SELECT id, 'C',  'Aberto', 30103.4695469537, 'Ficticio 01', 1500, 500.0 FROM case2.contaminante WHERE cas = '75-09-2' UNION ALL
SELECT id, 'C',  'Fechado', 3164.89658023359, 'Ficticio 01', 1500, 500.0 FROM case2.contaminante WHERE cas = '75-09-2' UNION ALL
SELECT id, 'NC', 'Aberto', 5759.59238781002, 'Ficticio 01', 1500, 500.0 FROM case2.contaminante WHERE cas = '75-09-2' UNION ALL
SELECT id, 'NC', 'Fechado', 605.5286824426520, 'Ficticio 01', 1500, 500.0 FROM case2.contaminante WHERE cas = '75-09-2';

INSERT INTO case2.avaliacao_risco (contaminante_id, efeito, ambiente, concentracao_max, vor, valor_vor, solu_concentracao)
SELECT id, 'C',  'Aberto', 18.0396087609632, 'Ficticio 02', 0.01, 500.0 FROM case2.contaminante WHERE cas = '56-23-5' UNION ALL
SELECT id, 'C',  'Fechado', 1.6071875859021, 'Ficticio 02', 0.01, 500.0 FROM case2.contaminante WHERE cas = '56-23-5' UNION ALL
SELECT id, 'NC', 'Aberto', 345.1455757837340, 'Ficticio 02', 0.01, 500.0 FROM case2.contaminante WHERE cas = '56-23-5' UNION ALL
SELECT id, 'NC', 'Fechado', 30.7497624853721, 'Ficticio 02', 0.01, 500.0 FROM case2.contaminante WHERE cas = '56-23-5';

INSERT INTO case2.avaliacao_risco (contaminante_id, efeito, ambiente, concentracao_max, vor, valor_vor, solu_concentracao)
SELECT id, 'C',  'Aberto', 2.0749223282420, 'Ficticio 03', 29, 500.0 FROM case2.contaminante WHERE cas = '106-93-4' UNION ALL
SELECT id, 'C',  'Fechado', 0.3585889118665, 'Ficticio 03', 29, 500.0 FROM case2.contaminante WHERE cas = '106-93-4' UNION ALL
SELECT id, 'NC', 'Aberto', 357.2889213171760, 'Ficticio 03', 29, 500.0 FROM case2.contaminante WHERE cas = '106-93-4' UNION ALL
SELECT id, 'NC', 'Fechado', 61.7468151810970, 'Ficticio 03', 29, 500.0 FROM case2.contaminante WHERE cas = '106-93-4';