select distinct agent_id, full_name, city
from {{ source('insurance_raw', 'agents') }}
where agent_id is not null

