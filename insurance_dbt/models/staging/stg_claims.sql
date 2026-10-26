select claim_id, policy_id, claim_date,
       claim_amount, status
from raw.claims
where claim_id is not null
