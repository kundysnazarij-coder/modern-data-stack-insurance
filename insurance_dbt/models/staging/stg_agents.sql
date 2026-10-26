select distinct agent_id, full_name, city
from raw.agents
where agent_id is not null
