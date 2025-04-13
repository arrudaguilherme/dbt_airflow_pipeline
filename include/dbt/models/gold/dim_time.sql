WITH data_source AS (
  SELECT DISTINCT
  CAST(date_time AS STRING) AS date_time_str,
  date_time,
  weekday
FROM {{ref("stg_accidents_brazil")}}
WHERE date_time IS NOT NULL
)

SELECT
    {{dbt_utils.generate_surrogate_key([
        'date_time_str'
    ])}} AS 
    id,
    FORMAT_DATETIME('%d/%m/%Y %H:%M:%S', date_time) AS date_time,
    EXTRACT(DAY FROM date_time) AS day,
    EXTRACT(MONTH FROM date_time) AS month,
    EXTRACT(YEAR FROM date_time) AS year,
    EXTRACT(HOUR FROM date_time) AS hour,
    EXTRACT(MINUTE FROM date_time) AS minute,
    EXTRACT(DAYOFWEEK FROM date_time) AS weekday
FROM data_source