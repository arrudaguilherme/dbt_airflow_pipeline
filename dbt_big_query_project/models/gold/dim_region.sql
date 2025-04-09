WITH data_source AS (
  SELECT DISTINCT
  region,
  latitude,
  longitude,
  police_station,
  operational_unity

FROM {{ref("stg_accidents_brazil")}}
WHERE region IS NOT NULL
)

SELECT 
    {{dbt_utils.generate_surrogate_key([
      'region',
      'latitude',
      'longitude',
      'police_station',
      'operational_unity'])}} AS 
    id,
    region,
    latitude,
    longitude,
    police_station,
    operational_unity
FROM data_source