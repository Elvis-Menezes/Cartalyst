import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# --- Business Config ---
STOCK_VALUE = 656000
ROLLING_FUNDS = 150000
PURCHASE_BUDGET = 100000
MIN_PARTS_IN_PLAN = 25
BUDGET_UTILISATION_TARGET = 0.6

# --- Category to Description Mapping ---
CATEGORY_PARTS = {
    'Cooling System': ['Radiator', 'Water Pump', 'Thermostat', 'Coolant Hose', 'Radiator Cap'],
    'Suspension': ['Shock Absorber', 'Lower Arm Bush', 'Ball Joint', 'Strut Mount', 'Link Rod'],
    'Brakes': ['Brake Pad', 'Disc Rotor', 'Brake Shoe', 'Brake Caliper', 'ABS Sensor'],
    'Filtration': ['Oil Filter', 'Air Filter', 'Fuel Filter', 'Cabin Filter'],
    'Belts & Hoses': ['Timing Belt', 'Drive Belt', 'Hose Pipe', 'V-Belt', 'Serpentine Belt'],
    'AC Components': ['AC Compressor', 'AC Condenser', 'AC Evaporator', 'Expansion Valve'],
    'Engine Parts': ['Spark Plug', 'Piston Ring', 'Cylinder Head Gasket', 'Main Bearing', 'Crankshaft'],
    'Batteries': ['Lead Acid Battery', 'AGM Battery', 'Gel Battery']
}

# --- Dataset Synthesis ---
def synthesize_dataset(base_df, num_unique_parts=500, rows_per_part=4):
    base_df.columns = base_df.columns.str.strip()
    base_df['Date'] = pd.to_datetime(base_df['Date'], errors='coerce')

    categories = list(CATEGORY_PARTS.keys())
    vehicle_makes = base_df['VehicleMake'].dropna().unique().tolist() + [
        'Toyota', 'Nissan', 'Honda', 'Mitsubishi', 'Lexus', 'Mazda', 'Ford'
    ]
    sources = ['OEM', 'Aftermarket']

    min_date = datetime(2023, 1, 1)
    max_date = datetime(2025, 12, 31)

    synthetic_rows = []
    np.random.seed(42)

    for _ in range(num_unique_parts):
        category = random.choice(categories)
        description = random.choice(CATEGORY_PARTS[category])
        make = random.choice(vehicle_makes)
        source = random.choice(sources)
        rate = round(np.random.uniform(2, 50), 2)
        part_no = f"{description[:3].upper()}-{random.randint(1000,9999)}"

        for _ in range(rows_per_part):
            date = min_date + timedelta(days=np.random.randint(0, (max_date - min_date).days))
            qty = np.random.randint(1, 20)
            total_price = round(rate * qty, 2)
            synthetic_rows.append({
                'TransactionID': np.random.randint(10000, 99999),
                'Date': date,
                'CustomerID': f"CUST-{np.random.randint(1, 2000)}",
                'PartNo': part_no,
                'Quantity': qty,
                'Rate': rate,
                'TotalPrice': total_price,
                'PartDescription': description,
                'Category': category,
                'Source': source,
                'VehicleMake': make
            })

    synthetic_df = pd.DataFrame(synthetic_rows)
    return pd.concat([base_df, synthetic_df], ignore_index=True)

# --- Data Processing ---
def load_and_process_data(df):
    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    for col in ['Quantity', 'Rate', 'TotalPrice']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=['Quantity', 'Rate', 'Date'], inplace=True)
    df['Source'] = np.where(df['Source'].str.lower().isin(['oem', 'source']), 'OEM', 'Aftermarket')
    df['CostPrice'] = df['Rate'] * np.where(df['Source'] == 'OEM', 0.7, 0.5)
    df['Profit'] = (df['Rate'] - df['CostPrice']) * df['Quantity']
    df['ProfitMargin'] = ((df['Rate'] - df['CostPrice']) / df['Rate']).fillna(0)

    supplier_map = {
        'Mitsubishi': 'Al-Futtaim Group', 'Honda': 'Diamond', 'Toyota': 'Denso',
        'Nissan': 'MAP', 'Generic': 'Teikin'
    }
    df['SupplierName'] = df['VehicleMake'].map(supplier_map).fillna('Gulf Auto Supplies')

    if 'CurrentStock' not in df.columns:
        unique_parts = df[['PartNo']].drop_duplicates().copy()
        np.random.seed(42)
        unique_parts['CurrentStock'] = np.random.randint(10, 250, size=len(unique_parts))
        df = pd.merge(df, unique_parts, on='PartNo', how='left')
    return df

# --- Scoring ---
def get_brand_popularity_score(vehicle_make):
    make = str(vehicle_make).lower()
    if 'toyota' in make or 'lexus' in make: return 1.0
    if 'nissan' in make or 'mitsubishi' in make: return 0.7
    if 'honda' in make: return 0.6
    return 0.3

def get_climate_impact_score(category):
    return 1.0 if any(c in str(category).lower() for c in ['cooling', 'ac components', 'filtration', 'batteries']) else 0.2

def get_seasonal_score(category, current_date):
    eid_periods = [(datetime(2025, 3, 15), datetime(2025, 4, 2)), (datetime(2025, 5, 22), datetime(2025, 6, 10))]
    is_pre_eid = any((start - timedelta(days=45)) <= current_date < end for start, end in eid_periods)
    if not is_pre_eid: return 0.0
    return 1.0 if any(c in str(category).lower() for c in ['tires', 'brakes', 'suspension', 'filtration', 'belts & hoses']) else 0.0

# --- Optimization ---
def run_inventory_optimization_model(sales_df, budget, weights):
    parts_df = sales_df.groupby('PartNo').agg({
        'PartDescription': 'first', 'Category': 'first', 'VehicleMake': 'first',
        'ProfitMargin': 'mean', 'CostPrice': 'first', 'CurrentStock': 'first',
        'Quantity': 'sum'
    }).reset_index()

    parts_df.rename(columns={'Quantity': 'TotalSales'}, inplace=True)
    max_demand = parts_df['TotalSales'].max()
    parts_df['DemandScore'] = parts_df['TotalSales'] / max_demand if max_demand > 0 else 0

    latest_date = sales_df['Date'].max()
    parts_df['ProfitScore'] = parts_df['ProfitMargin']
    parts_df['BrandScore'] = parts_df['VehicleMake'].apply(get_brand_popularity_score)
    parts_df['ClimateScore'] = parts_df['Category'].apply(get_climate_impact_score)
    parts_df['SeasonalScore'] = parts_df['Category'].apply(get_seasonal_score, current_date=latest_date)

    parts_df['SignificanceScore'] = (
        parts_df['DemandScore'] * weights['DEMAND_WEIGHT'] +
        parts_df['ProfitScore'] * weights['PROFIT_WEIGHT'] +
        parts_df['BrandScore'] * weights['BRAND_WEIGHT'] +
        parts_df['ClimateScore'] * weights['CLIMATE_WEIGHT'] +
        parts_df['SeasonalScore'] * weights['SEASONAL_WEIGHT']
    )

    ranked_parts = parts_df.sort_values(by='SignificanceScore', ascending=False)

    purchase_plan = []
    remaining_budget = budget
    for _, part in ranked_parts.iterrows():
        qty_to_order = max(1, int(np.ceil(part['TotalSales'] / 2)))
        cost = qty_to_order * part['CostPrice']
        if cost <= remaining_budget:
            part['RecOrderQty'] = qty_to_order
            part['TargetStock'] = part['CurrentStock'] + qty_to_order
            purchase_plan.append(part.copy())
            remaining_budget -= cost
        if len(purchase_plan) >= MIN_PARTS_IN_PLAN:
            break

    total_spend = sum(p['RecOrderQty'] * p['CostPrice'] for p in purchase_plan)
    idx = 0
    while total_spend < budget * BUDGET_UTILISATION_TARGET and remaining_budget > 0 and idx < len(purchase_plan):
        part = purchase_plan[idx]
        extra_qty = max(1, int(np.ceil(part['TotalSales'] / 4)))
        extra_cost = extra_qty * part['CostPrice']
        if extra_cost <= remaining_budget:
            part['RecOrderQty'] += extra_qty
            part['TargetStock'] += extra_qty
            remaining_budget -= extra_cost
            total_spend += extra_cost
        idx = (idx + 1) % len(purchase_plan)

    final_plan_df = pd.DataFrame(purchase_plan)
    final_plan_df['RecOrderQty'] = final_plan_df['RecOrderQty'].astype(int)
    final_plan_df['SignificanceScore'] = final_plan_df['SignificanceScore'].round(3)
    return final_plan_df

# --- MAIN EXECUTION ---
def main():
    # Load your Excel dataset here
    file_path = "datafull_synthesized.xlsx"  # Change if needed
    base_df = pd.read_excel(file_path)

    # Optionally synthesize more data
    base_df = synthesize_dataset(base_df, num_unique_parts=500)

    # Process data
    sales_df = load_and_process_data(base_df)

    # Define weights
    WEIGHTS = {
        'DEMAND_WEIGHT': 0.40,
        'PROFIT_WEIGHT': 0.30,
        'BRAND_WEIGHT': 0.15,
        'CLIMATE_WEIGHT': 0.10,
        'SEASONAL_WEIGHT': 0.05
    }

    # Run optimization
    plan_df = run_inventory_optimization_model(sales_df, PURCHASE_BUDGET, WEIGHTS)

    # Print results
    print("\n--- Recommended Purchase Plan ---")
    if not plan_df.empty:
        print(plan_df[['PartNo', 'PartDescription', 'SignificanceScore', 'CurrentStock', 'TargetStock', 'RecOrderQty']])
        total_cost = (plan_df['RecOrderQty'] * plan_df['CostPrice']).sum()
        print(f"\nTotal Planned Cost: {total_cost:,.2f} OMR / Budget: {PURCHASE_BUDGET:,.2f} OMR")
    else:
        print("No parts recommended for purchase.")

if __name__ == "__main__":
    main()
