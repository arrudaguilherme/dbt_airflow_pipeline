WITH data_source AS (
  SELECT DISTINCT
  city,
  state_abbr

FROM {{ref("stg_accidents_brazil")}}
WHERE city IS NOT NULL
)

SELECT 
{{dbt_utils.generate_surrogate_key([
    'city',
    'state_abbr'])}} AS 
    id,
    city,
    state_abbr

FROM data_source