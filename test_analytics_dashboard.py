#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced employee analytics dashboard
"""

from rag import PartsRAG
import json

def test_analytics_features():
    print("Testing Enhanced Employee Analytics Dashboard")
    print("=" * 60)
    
    # Initialize RAG system
    rag_system = PartsRAG()
    
    # Load data from database
    if not rag_system.load_data_from_db('parts.db'):
        print("ERROR: Failed to load database")
        return
    
    # Load Excel data for employee insights
    if not rag_system.load_data_from_excel('model-data.xlsx'):
        print("ERROR: Failed to load Excel data")
        return
    
    # Get comprehensive insights
    insights = rag_system.get_employee_insights()
    
    print("Analytics Data Overview:")
    print("-" * 40)
    print(f"Total Inventory Value: Rs.{insights['total_inventory_value']:,.2f}")
    print(f"Total Transactions: {insights['total_transactions']:,}")
    print(f"Average Transaction Value: Rs.{insights['average_transaction_value']:,.2f}")
    print(f"Low Stock Items: {len(insights['low_stock_items'])}")
    
    print("\nRevenue by Category:")
    print("-" * 30)
    for category, revenue in insights['category_revenue'].items():
        print(f"  - {category}: Rs.{revenue:,.2f}")
    
    print("\nTop 5 Fast Moving Items:")
    print("-" * 35)
    for i, item in enumerate(insights['fast_moving_items'][:5], 1):
        print(f"  {i}. {item['PartDescription']}")
        print(f"     Sales: {item['TotalTransactions']} | Revenue: Rs.{item['Revenue']:,.2f}")
        print(f"     Part No: {item['PartNo']}")
        print()
    
    print("Top 5 Suppliers by Revenue:")
    print("-" * 32)
    for i, supplier in enumerate(insights['top_suppliers'][:5], 1):
        print(f"  {i}. {supplier['name']}: Rs.{supplier['revenue']:,.2f}")
    
    print("\nMonthly Revenue Trend (Last 12 Months):")
    print("-" * 45)
    for month_data in insights['monthly_revenue'][-6:]:  # Show last 6 months
        print(f"  - {month_data['month']}: Rs.{month_data['revenue']:,.2f} ({month_data['transactions']} transactions)")
    
    print("\n" + "=" * 60)
    print("Dashboard Visualization Features:")
    print("-" * 40)
    print("- Revenue by Category - Doughnut Chart")
    print("   - Color-coded categories with hover tooltips")
    print("   - Interactive legend with click-to-hide functionality")
    print()
    print("- Fast Moving Items - Bar Chart")
    print("   - Top 5 selling parts with transaction counts")
    print("   - Detailed tooltips showing revenue and part numbers")
    print()
    print("- Monthly Revenue Trend - Line Chart")
    print("   - Dual-axis chart showing revenue and transaction volume")
    print("   - 12-month historical data with smooth curves")
    print()
    print("- Enhanced Metrics Cards")
    print("   - Total inventory value, transactions, and low stock alerts")
    print("   - Color-coded indicators for quick status assessment")
    print()
    print("- Top Suppliers & Fast Moving Items Lists")
    print("   - Detailed breakdowns with revenue figures")
    print("   - Clean, organized presentation with hover effects")

def test_chart_data_format():
    print("\n" + "=" * 60)
    print("Chart Data Format Testing:")
    print("-" * 40)
    
    rag_system = PartsRAG()
    if not rag_system.load_data_from_db('parts.db'):
        print("ERROR: Failed to load database")
        return
    
    # Load Excel data for employee insights
    if not rag_system.load_data_from_excel('model-data.xlsx'):
        print("ERROR: Failed to load Excel data")
        return
    
    insights = rag_system.get_employee_insights()
    
    # Test JSON serialization for charts
    print("Category Revenue Data (for Doughnut Chart):")
    category_data = insights['category_revenue']
    print(f"   Labels: {list(category_data.keys())}")
    print(f"   Values: {list(category_data.values())}")
    
    print("\nFast Moving Items Data (for Bar Chart):")
    fast_moving = insights['fast_moving_items'][:5]
    print(f"   Parts: {[item['PartDescription'][:30] + '...' for item in fast_moving]}")
    print(f"   Sales: {[item['TotalTransactions'] for item in fast_moving]}")
    
    print("\nMonthly Revenue Data (for Line Chart):")
    monthly = insights['monthly_revenue'][-3:]  # Last 3 months
    for month in monthly:
        print(f"   {month['month']}: Rs.{month['revenue']:,.2f} revenue, {month['transactions']} transactions")

if __name__ == "__main__":
    test_analytics_features()
    test_chart_data_format()