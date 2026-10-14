import pandas as pd
from faker import Faker
import random
import os

fake = Faker('uk_UA')
Faker.seed(42)
random.seed(42)

os.makedirs('data_lake', exist_ok=True)

def generate_policy_holders(n=500):
    data = []
    for i in range(1, n + 1):
        data.append({
            'holder_id': i,
            'full_name': fake.name(),
            'email': fake.email() if random.random() > 0.1 else None,
            'city': fake.city()
        })
    return pd.DataFrame(data)

def generate_insurance_plans():
    plans = [
        'Автострахування',
        'Медичне страхування',
        'Страхування житла',
        'Туристичне страхування',
        'Страхування життя'
    ]
    return pd.DataFrame([
        {
            'plan_id': i + 1,
            'plan_name': name,
            'price': round(random.uniform(1000, 15000), 2)
        }
        for i, name in enumerate(plans)
    ])

def generate_agents(n=30):
    return pd.DataFrame([
        {
            'agent_id': i,
            'full_name': fake.name(),
            'city': fake.city()
        }
        for i in range(1, n + 1)
    ])
def generate_policies_sold(n, holder_ids, plan_ids, agent_ids):
    data = []
    for i in range(1, n + 1):
        data.append({
            'policy_id': i,
            'holder_id': random.choice(holder_ids),
            'plan_id': random.choice(plan_ids),
            'agent_id': random.choice(agent_ids),
            'sale_date': fake.date_between(start_date='-1y', end_date='today'),
            'premium': round(random.uniform(1000, 15000), 2)
        })
    return pd.DataFrame(data)


def generate_claims(n, policy_ids):
    data = []
    for i in range(1, n + 1):
        data.append({
            'claim_id': i,
            'policy_id': random.choice(policy_ids),
            'claim_date': fake.date_between(start_date='-1y', end_date='today'),
            'claim_amount': round(random.uniform(500, 50000), 2),
            'status': random.choice(['approved', 'pending', 'rejected'])
        })
    return pd.DataFrame(data)


print("Починаємо генерацію даних...")

df_holders = generate_policy_holders()
df_plans = generate_insurance_plans()
df_agents = generate_agents()

df_policies = generate_policies_sold(
    3000,
    df_holders['holder_id'].tolist(),
    df_plans['plan_id'].tolist(),
    df_agents['agent_id'].tolist()
)

df_claims = generate_claims(
    1000,
    df_policies['policy_id'].tolist()
)

tables = {
    'policy_holders': df_holders,
    'insurance_plans': df_plans,
    'agents': df_agents,
    'policies_sold': df_policies,
    'claims': df_claims
}

for name, df in tables.items():
    df.to_parquet(f'data_lake/raw_{name}.parquet', index=False)
    print(f"{name}: {len(df)} записів")

print("Генерацію даних успішно завершено!")