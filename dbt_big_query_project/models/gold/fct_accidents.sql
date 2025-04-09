WITH fact AS (
  SELECT
    id,
    {{dbt_utils.generate_surrogate_key([
        'CAST(date_time AS STRING)'
    ])}} AS datetime_id,
    {{dbt_utils.generate_surrogate_key([
    'city',
    'state_abbr'])}} AS city_id,
    {{dbt_utils.generate_surrogate_key([
      'region',
      'latitude',
      'longitude',
      'police_station',
      'operational_unity'])}} AS region_id,
    {{dbt_utils.generate_surrogate_key([
        'accident_cause', 
        'accident_type', 
        'accident_classification',
        'day_phase',
        'road_way', 
        'weather_condition', 
        'road_type', 
        'road_mark', 'ground_usage'])}} AS accident_id ,
    road,
    km_mark,
    people_count,
    deaths,
    light_injuries,
    seriously_injured,
    unharmed,
    ignored,
    injured,
    vehicles
FROM {{ref("stg_accidents_brazil")}}
)

SELECT
    fact.id,
    dt.id AS datetime_id,
    dc.id AS city_id,
    dr.id AS region_id,
    da.id AS accident_id,
    fact.road,
    fact.km_mark,
    fact.people_count,
    fact.deaths,
    fact.light_injuries,
    fact.seriously_injured,
    fact.unharmed,
    fact.ignored,
    fact.injured,
    fact.vehicles
FROM fact AS fact
INNER JOIN {{ref("dim_time")}} AS dt ON fact.datetime_id = dt.id
INNER JOIN {{ref("dim_city")}} AS dc ON fact.city_id = dc.id
INNER JOIN {{ref("dim_region")}} AS dr ON fact.region_id = dr.id
INNER JOIN {{ref("dim_accident")}} AS da ON fact.accident_id = da.id
