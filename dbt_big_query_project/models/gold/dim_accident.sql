WITH data_source AS (
  SELECT DISTINCT
    accident_cause,
    accident_type,
    accident_classification,
    day_phase,
    road_way,
    weather_condition,
    road_type,
    road_mark,
    ground_usage
  FROM {{ref("stg_accidents_brazil")}}

  WHERE accident_cause IS NOT NULL
)


SELECT 
    {{dbt_utils.generate_surrogate_key([
        'accident_cause', 
        'accident_type', 
        'accident_classification',
        'day_phase',
        'road_way', 
        'weather_condition', 
        'road_type', 
        'road_mark', 
        'ground_usage'])}} 
    AS id,
    accident_cause,
    accident_type,
    accident_classification,
    day_phase,
    road_way,
    weather_condition,
    road_type,
    road_mark,
    ground_usage
FROM data_source