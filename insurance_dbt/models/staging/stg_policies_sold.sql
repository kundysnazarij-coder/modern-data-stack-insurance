select policy_id, holder_id, plan_id, agent_id,
       sale_date, premium
from raw.policies_sold
where policy_id is not null
