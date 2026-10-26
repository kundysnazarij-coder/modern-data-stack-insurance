select holder_id, full_name, email, city
from (
    select *,
        row_number() over (
            partition by holder_id order by full_name
        ) as rn
    from raw.policy_holders
    where email is not null and trim(email) <> ''
) t
where rn = 1
