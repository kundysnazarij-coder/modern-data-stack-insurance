select distinct plan_id, plan_name, price
from raw.insurance_plans
where plan_id is not null
