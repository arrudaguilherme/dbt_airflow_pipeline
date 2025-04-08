

WITH data_source AS (
  SELECT * 
  FROM {{source('acidentes_brasil','raw_acidentes_brasil')}}
),

transformed_data AS (
  SELECT
    CAST(id AS STRING) AS id,
    FORMAT_DATETIME('%d/%m/%Y %H:%M:%S', PARSE_DATETIME('%Y-%m-%d %H:%M:%S', CONCAT(data_inversa, ' ', horario))) AS date_time,
    TRIM(dia_semana) AS weekday,
    TRIM(uf) AS state_abbr,
    TRIM(municipio) AS city,
    TRIM(causa_acidente) AS accident_cause,
    TRIM(tipo_acidente) AS accident_type,
    TRIM(classificacao_acidente) AS accident_classification,
    TRIM(fase_dia) AS day_phase,
    TRIM(sentido_via) AS road_way,
    TRIM(condicao_metereologica) AS weather_condition,
    TRIM(tipo_pista) AS road_type,
    TRIM(tracado_via) AS road_mark,
    CASE
      WHEN uso_solo = 'Sim' THEN 1
      WHEN uso_solo = 'Não' THEN 0
    ELSE
      NULL
    END AS ground_usage,
    br AS road,
    km as km_mark,
    CAST(pessoas AS INT) AS people_count,
    CAST(mortos AS  INT) AS deaths,
    CAST(feridos_leves AS INT) AS light_injuries,
    CAST(ilesos AS INT) AS unharmed,
    CAST(ignorados AS INT) AS ignored,
    CAST(feridos AS INT) AS injured,
    CAST(veiculos AS INT) AS vehicles,
    TRIM(CAST(latitude AS STRING)) AS latitude,
    TRIM(CAST(longitude AS STRING)) AS longitude,
    TRIM(regional) AS region,
    TRIM(delegacia) AS police_station

  FROM data_source

)

SELECT * FROM transformed_data