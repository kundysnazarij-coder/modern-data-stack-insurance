select claim_id, policy_id, claim_date,
       claim_amount, status
from {{ source('insurance_raw', 'claims') }}
where claim_id is not null

