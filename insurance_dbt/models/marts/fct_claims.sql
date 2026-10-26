select c.claim_id, c.policy_id, c.claim_date,
       c.claim_amount, c.status
from {{ ref('stg_claims') }} c
inner join {{ ref('fct_policies_sold') }} p
    on c.policy_id = p.policy_id
