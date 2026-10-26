select p.policy_id, p.holder_id, p.plan_id,
       p.agent_id, p.sale_date, p.premium
from {{ ref('stg_policies_sold') }} p
inner join {{ ref('dim_policy_holders') }} h
    on p.holder_id = h.holder_id
inner join {{ ref('dim_insurance_plans') }} pl
    on p.plan_id = pl.plan_id
inner join {{ ref('dim_agents') }} a
    on p.agent_id = a.agent_id
