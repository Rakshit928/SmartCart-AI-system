import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="SmartCart AI | Zepto Demo",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #34495e;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-container {
        padding: 1rem;
        border-radius: 5px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #3498db;
    }
    .metric-label {
        font-size: 1rem;
        color: #7f8c8d;
    }
    .highlight {
        color: #e74c3c;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("SmartCart AI")
    st.subheader("Inventory & Demand Prediction")
    
    # Demo navigation
    page = st.radio(
        "Navigate",
        ["Dashboard", "Demand Forecasting", "Inventory Optimization", "Customer Segmentation"]
    )
    
    st.markdown("---")
    st.markdown("Demo created by **Rakshit Anand**")
    st.markdown("[GitHub](https://github.com/Rakshit928) | [LinkedIn](https://www.linkedin.com/in/rakshit-anand/)")

# Generate sample data for demo
@st.cache_data
def generate_demo_data():
    # Time range for demo data
    now = datetime.now()
    
    # Sales data by hour
    hourly_timestamps = [now - timedelta(hours=i) for i in range(168)]
    hourly_timestamps.reverse()
    
    # Generate pattern with peak at noon and evening
    base_demand = [20 + 15 * np.sin(np.pi * i / (24/2)) + 5 * np.sin(np.pi * i / (24/4)) for i in range(168)]
    
    # Add day of week pattern (weekends higher)
    for i in range(168):
        day_of_week = (now - timedelta(hours=i)).weekday()
        if day_of_week >= 5:  # Weekend
            base_demand[i] *= 1.3
    
    # Add random noise
    hourly_demand = [max(0, int(d + np.random.normal(0, d * 0.1))) for d in base_demand]
    
    # Forecast data (slightly different from actual)
    hourly_forecast = [max(0, int(d + np.random.normal(0, d * 0.15))) for d in base_demand]
    
    hourly_data = pd.DataFrame({
        'timestamp': hourly_timestamps,
        'demand': hourly_demand,
        'forecast': hourly_forecast,
        'hour': [t.hour for t in hourly_timestamps],
        'day_of_week': [t.weekday() for t in hourly_timestamps]
    })
    
    # Store data
    stores = ['Indiranagar', 'Koramangala', 'HSR Layout', 'Whitefield', 'Electronic City']
    store_data = pd.DataFrame({
        'name': stores,
        'current_inventory': [78, 92, 65, 45, 83],
        'optimal_inventory': [85, 95, 70, 60, 80],
        'stockout_risk': ['Low', 'Very Low', 'Medium', 'High', 'Low'],
        'lat': [12.9784, 12.9316, 12.9141, 12.9698, 12.8499],
        'lon': [77.6408, 77.6271, 77.6380, 77.7499, 77.6699]
    })
    
    # Product data
    products = ['Milk 1L', 'Bread', 'Eggs 6pk', 'Bananas', 'Tomatoes', 'Chicken', 'Rice 1kg', 'Bottled Water', 'Yogurt']
    product_data = pd.DataFrame({
        'name': products,
        'category': ['Dairy', 'Bakery', 'Dairy', 'Fruits', 'Vegetables', 'Meat', 'Groceries', 'Beverages', 'Dairy'],
        'reorder_frequency': [1, 1, 2, 2, 2, 3, 7, 3, 2],
        'shelf_life_days': [7, 3, 14, 5, 7, 3, 180, 365, 14],
        'avg_daily_sales': [42, 35, 28, 31, 25, 18, 12, 45, 22]
    })
    
    # Customer segments
    segments = ['High-value Shoppers', 'Regular Customers', 'Occasional Buyers', 'New Users']
    segment_data = pd.DataFrame({
        'name': segments,
        'size': [25, 40, 20, 15],
        'avg_order_value': [520, 320, 180, 220],
        'order_frequency': [4.5, 2.8, 1.2, 1.0],
        'retention_rate': [92, 78, 45, 60]
    })
    
    return {
        'hourly_data': hourly_data,
        'store_data': store_data,
        'product_data': product_data,
        'segment_data': segment_data
    }

# Load demo data
data = generate_demo_data()

# Dashboard Page
if page == "Dashboard":
    st.markdown("<h1 class='main-header'>SmartCart AI Dashboard</h1>", unsafe_allow_html=True)
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value'>98.7%</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Inventory Accuracy</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value'>12.5 min</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Avg Delivery Time</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value'>2.4%</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Stockout Rate</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value'>₹320</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Avg Order Value</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main dashboard charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='sub-header'>Demand Forecast vs Actual</h2>", unsafe_allow_html=True)
        
        # Prepare forecast chart data
        forecast_df = data['hourly_data'].copy()
        forecast_df['date'] = forecast_df['timestamp'].dt.strftime('%m-%d %H:00')
        forecast_chart = forecast_df.iloc[-24:][['date', 'demand', 'forecast']]
        
        # Create Plotly chart
        fig = px.line(
            forecast_chart, 
            x='date', 
            y=['demand', 'forecast'],
            labels={'date': 'Time', 'value': 'Orders'},
            title='',
            color_discrete_map={'demand': '#3498db', 'forecast': '#e74c3c'}
        )
        fig.update_layout(
            legend_title_text='',
            xaxis_title='',
            yaxis_title='Orders',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='sub-header'>Store Inventory Status</h2>", unsafe_allow_html=True)
        
        # Prepare store inventory data
        inventory_df = data['store_data'][['name', 'current_inventory', 'optimal_inventory']]
        
        # Create Plotly chart
        fig = px.bar(
            inventory_df,
            x='name',
            y=['current_inventory', 'optimal_inventory'],
            barmode='group',
            labels={'name': 'Store', 'value': 'Units'},
            color_discrete_map={'current_inventory': '#2ecc71', 'optimal_inventory': '#3498db'}
        )
        fig.update_layout(
            legend_title_text='',
            xaxis_title='',
            yaxis_title='Inventory Units',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Second row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='sub-header'>Customer Segments</h2>", unsafe_allow_html=True)
        
        # Prepare segment data
        segment_df = data['segment_data']
        
        # Create pie chart
        fig = px.pie(
            segment_df,
            values='size',
            names='name',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='sub-header'>Delivery Times</h2>", unsafe_allow_html=True)
        
        # Create sample delivery time data
        delivery_df = pd.DataFrame({
            'time': ['<10 min', '10-15 min', '15-20 min', '>20 min'],
            'count': [245, 175, 85, 35]
        })
        
        # Create bar chart
        fig = px.bar(
            delivery_df,
            x='time',
            y='count',
            color='count',
            color_continuous_scale=['#3498db', '#2ecc71', '#f1c40f', '#e74c3c'],
            labels={'time': 'Delivery Time', 'count': 'Number of Orders'}
        )
        fig.update_layout(
            xaxis_title='',
            yaxis_title='Number of Orders',
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Demand Forecasting Page
elif page == "Demand Forecasting":
    st.markdown("<h1 class='main-header'>Demand Forecasting Engine</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    The SmartCart demand forecasting system uses LSTM neural networks to predict product demand with high accuracy. 
    It factors in historical sales data, time patterns, seasonality, local events, and even weather conditions.
    """)
    
    # Interactive date selector
    forecast_date = st.date_input("Select forecast date:", datetime.now().date())
    
    # Tabs for different views
    forecast_tab1, forecast_tab2, forecast_tab3 = st.tabs(["Store Level", "Product Level", "Time Patterns"])
    
    with forecast_tab1:
        st.subheader("Store-Level Demand Forecast")
        
        # Create store forecast data
        store_names = data['store_data']['name'].tolist()
        
        # Generate forecasts for each store
        store_forecast_data = []
        base = np.array(data['hourly_data']['demand'].iloc[-24:].values)
        
        for store in store_names:
            # Add some variation for each store
            variation = np.random.uniform(0.7, 1.3)
            forecast = base * variation
            
            for hour in range(24):
                store_forecast_data.append({
                    'store': store,
                    'hour': hour,
                    'forecast': int(forecast[hour])
                })
        
        store_forecast_df = pd.DataFrame(store_forecast_data)
        
        # Create heatmap
        heatmap_df = store_forecast_df.pivot(index='store', columns='hour', values='forecast')
        
        fig = px.imshow(
            heatmap_df,
            labels=dict(x="Hour of Day", y="Store", color="Demand"),
            x=[f"{h}:00" for h in range(24)],
            y=store_names,
            color_continuous_scale="Viridis"
        )
        fig.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Store",
            coloraxis_colorbar=dict(title="Orders")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Insights:**
        - Indiranagar and Koramangala show higher demand during evening hours (6-9 PM)
        - Weekend demand is 30% higher across all stores
        - Weather affects demand by 15-20% (rainy days show higher order volumes)
        """)
    
    with forecast_tab2:
        st.subheader("Product-Level Demand Patterns")
        
        # Sample product categories
        categories = ['Dairy', 'Fruits & Vegetables', 'Bakery', 'Beverages', 'Meat & Seafood']
        
        # Create product category forecast data
        category_data = []
        for hour in range(24):
            for category in categories:
                # Create different patterns for different categories
                if category == 'Dairy':
                    forecast = 30 + 15 * np.sin(np.pi * hour / 12)
                elif category == 'Fruits & Vegetables':
                    forecast = 40 + 20 * np.sin(np.pi * (hour - 2) / 12)
                elif category == 'Bakery':
                    forecast = 25 + 20 * np.sin(np.pi * (hour - 1) / 12)
                elif category == 'Beverages':
                    forecast = 35 + 10 * np.sin(np.pi * hour / 12)
                else:
                    forecast = 20 + 30 * np.sin(np.pi * (hour - 4) / 12)
                
                category_data.append({
                    'category': category,
                    'hour': hour,
                    'forecast': max(5, int(forecast + np.random.normal(0, 3)))
                })
        
        category_df = pd.DataFrame(category_data)
        
        # Create line chart
        fig = px.line(
            category_df,
            x='hour',
            y='forecast',
            color='category',
            labels={'hour': 'Hour of Day', 'forecast': 'Predicted Demand'},
            markers=True
        )
        fig.update_layout(
            xaxis=dict(tickmode='array', tickvals=list(range(24)), ticktext=[f"{h}:00" for h in range(24)]),
            xaxis_title="Hour of Day",
            yaxis_title="Predicted Orders",
            legend_title="Category"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Product Insights:**
        - Dairy peaks in morning (6-8 AM) and evening (5-7 PM)
        - Bakery items peak in morning hours
        - Meat & Seafood show highest demand in evening hours
        - Beverages maintain steady demand throughout the day with slight evening peak
        """)
    
    with forecast_tab3:
        st.subheader("Temporal Patterns in Demand")
        
        # Create weekly pattern data
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Sample data for weekly patterns
        weekly_data = pd.DataFrame({
            'day': days,
            'demand': [85, 82, 88, 90, 105, 125, 130],
            'day_num': list(range(7))
        })
        
        fig = px.bar(
            weekly_data,
            x='day',
            y='demand',
            color='demand',
            color_continuous_scale=['#3498db', '#2ecc71', '#f1c40f', '#e74c3c'],
            labels={'day': 'Day of Week', 'demand': 'Relative Demand'}
        )
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Relative Demand (%)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Temporal Insights:**
        - Weekend demand is 30-40% higher than weekdays
        - Friday shows ~15% higher demand than earlier weekdays
        - Order volumes tend to peak between 6-9 PM across all days
        - Monday mornings show higher than average breakfast item orders
        """)

# Inventory Optimization Page
elif page == "Inventory Optimization":
    st.markdown("<h1 class='main-header'>Inventory Optimization System</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    SmartCart's inventory optimization system ensures the right products are available at the right stores at the right time.
    It calculates optimal inventory levels, generates reorder recommendations, and allocates stock across dark stores.
    """)
    
    # Interactive store selector
    selected_store = st.selectbox("Select Store:", data['store_data']['name'].tolist())
    
    # Tabs for different views
    inv_tab1, inv_tab2, inv_tab3 = st.tabs(["Inventory Health", "Product Optimization", "Reorder Recommendations"])
    
    with inv_tab1:
        st.subheader(f"Inventory Health for {selected_store}")
        
        # Generate inventory health metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
            st.markdown("<div class='metric-value'>98.2%</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-label'>In-stock Rate</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
            st.markdown("<div class='metric-value'>92.5%</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-label'>Inventory Accuracy</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
            st.markdown("<div class='metric-value'>1.8%</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-label'>Wastage Rate</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Inventory health by category
        st.subheader("Category-level Inventory Health")
        
        # Create sample data for category-level inventory
        categories = ['Dairy', 'Fruits', 'Vegetables', 'Bakery', 'Beverages', 'Meat', 'Grocery']
        
        category_inventory = pd.DataFrame({
            'category': categories,
            'current': [92, 85, 88, 95, 97, 90, 99],
            'target': [95, 90, 90, 95, 95, 95, 98],
            'status': ['Good', 'Low', 'Good', 'Optimal', 'Optimal', 'Low', 'Optimal']
        })
        
        # Color map for status
        color_map = {
            'Optimal': '#2ecc71',
            'Good': '#3498db',
            'Low': '#f1c40f',
            'Critical': '#e74c3c'
        }
        
        status_colors = [color_map[status] for status in category_inventory['status']]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=category_inventory['category'],
            y=category_inventory['current'],
            name='Current Inventory Level',
            marker_color=status_colors
        ))
        
        fig.add_trace(go.Scatter(
            x=category_inventory['category'],
            y=category_inventory['target'],
            mode='markers',
            name='Target Level',
            marker=dict(
                color='rgba(0, 0, 0, 0.8)',
                size=10,
                symbol='line-ns'
            )
        ))
        
        fig.update_layout(
            xaxis_title='',
            yaxis_title='Inventory Level (%)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with inv_tab2:
        st.subheader("Product-level Optimization")
        
        # Create sample product data
        products = data['product_data'].copy()
        products['current_stock'] = np.random.randint(5, 50, size=len(products))
        products['optimal_stock'] = np.random.randint(10, 60, size=len(products))
        products['days_to_stockout'] = np.random.randint(1, 15, size=len(products))
        
        # Calculate stock status
        products['stock_status'] = products.apply(
            lambda x: 'Critical' if x['days_to_stockout'] <= 1 else
                     'Low' if x['days_to_stockout'] <= 3 else
                     'Good' if x['days_to_stockout'] <= 7 else 'Optimal',
            axis=1
        )
        
        # Display as dataframe
        st.dataframe(
            products[['name', 'category', 'current_stock', 'optimal_stock', 'days_to_stockout', 'stock_status']],
            use_container_width=True,
            hide_index=True
        )
        
        # Create a chart for critical/low items
        critical_low = products[products['stock_status'].isin(['Critical', 'Low'])]
        
        if not critical_low.empty:
            st.subheader("Products Requiring Attention")
            
            fig = px.bar(
                critical_low,
                x='name',
                y=['current_stock', 'optimal_stock'],
                barmode='group',
                color_discrete_map={'current_stock': '#e74c3c', 'optimal_stock': '#3498db'},
                labels={'name': 'Product', 'value': 'Units'}
            )
            fig.update_layout(
                xaxis_title='',
                yaxis_title='Stock Units',
                legend_title=''
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with inv_tab3:
        st.subheader("Reorder Recommendations")
        
        # Create sample reorder data
        reorder_data = []
        
        for i, row in products.iterrows():
            if row['current_stock'] < row['optimal_stock']:
                reorder_data.append({
                    'product': row['name'],
                    'category': row['category'],
                    'current_stock': row['current_stock'],
                    'reorder_quantity': row['optimal_stock'] - row['current_stock'],
                    'priority': 'High' if row['stock_status'] in ['Critical', 'Low'] else 'Medium'
                })
        
        reorder_df = pd.DataFrame(reorder_data)
        
        if not reorder_df.empty:
            # Sort by priority and reorder quantity
            reorder_df = reorder_df.sort_values(['priority', 'reorder_quantity'], ascending=[True, False])
            
            # Display reorder recommendations
            st.dataframe(
                reorder_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Summary
            total_items = len(reorder_df)
            total_quantity = reorder_df['reorder_quantity'].sum()
            high_priority = len(reorder_df[reorder_df['priority'] == 'High'])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Items to Reorder", total_items)
            
            with col2:
                st.metric("Total Quantity", total_quantity)
            
            with col3:
                st.metric("High Priority Items", high_priority)
        
        else:
            st.info("No reorder recommendations at this time.")

# Customer Segmentation Page
elif page == "Customer Segmentation":
    st.markdown("<h1 class='main-header'>Customer Segmentation & Personalization</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    SmartCart uses K-means clustering and behavioral analysis to segment customers into meaningful groups,
    enabling personalized recommendations and targeted marketing strategies.
    """)
    
    # Tabs for different views
    segment_tab1, segment_tab2, segment_tab3 = st.tabs(["Segment Overview", "Behavioral Analysis", "Recommendation Strategies"])
    
    with segment_tab1:
        st.subheader("Customer Segment Overview")
        
        # Use segment data from earlier
        segment_df = data['segment_data']
        
        # Pie chart for segment distribution
        fig = px.pie(
            segment_df,
            values='size',
            names='name',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Segment characteristics
        st.subheader("Segment Characteristics")
        
        # Create a radar chart for each segment
        metrics = ['order_frequency', 'avg_order_value', 'retention_rate']
        
        # Normalize values for radar chart
        normalized_df = segment_df.copy()
        for metric in metrics:
            normalized_df[metric] = normalized_df[metric] / normalized_df[metric].max() * 100
        
        # Create radar chart
        fig = go.Figure()
        
        for i, row in normalized_df.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[row[metric] for metric in metrics],
                theta=['Order Frequency', 'Order Value', 'Retention Rate'],
                fill='toself',
                name=row['name']
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with segment_tab2:
        st.subheader("Customer Behavioral Analysis")
        
        # Create synthetic purchasing behavior data
        purchase_data = []
        
        hour_ranges = ['6-9 AM', '9-12 PM', '12-3 PM', '3-6 PM', '6-9 PM', '9-12 AM']
        
        for segment in segment_df['name']:
            for hour_range in hour_ranges:
                # Create different patterns for different segments
                if segment == 'High-value Shoppers':
                    value = np.random.normal(25, 5) if hour_range in ['6-9 PM', '9-12 AM'] else np.random.normal(10, 3)
                elif segment == 'Regular Customers':
                    value = np.random.normal(18, 4) if hour_range in ['6-9 PM'] else np.random.normal(12, 3)
                elif segment == 'Occasional Buyers':
                    value = np.random.normal(10, 3) if hour_range in ['3-6 PM', '6-9 PM'] else np.random.normal(5, 2)
                else:  # New Users
                    value = np.random.normal(8, 3)  # More evenly distributed
                
                purchase_data.append({
                    'segment': segment,
                    'hour_range': hour_range,
                    'value': max(0, value)
                })
        
        purchase_df = pd.DataFrame(purchase_data)
        
        # Create heatmap
        heatmap_df = purchase_df.pivot(index='segment', columns='hour_range', values='value')
        
        fig = px.imshow(
            heatmap_df,
            labels=dict(x="Time of Day", y="Customer Segment", color="Order Volume"),
            x=hour_ranges,
            y=segment_df['name'],
            color_continuous_scale="Viridis"
        )
        fig.update_layout(
            xaxis_title="Time of Day",
            yaxis_title="Customer Segment",
            coloraxis_colorbar=dict(title="Order Volume")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Behavioral Insights:**
        - High-value shoppers show strong evening purchasing patterns (6 PM - midnight)
        - Regular customers peak during evening hours (6-9 PM)
        - New users show more distributed purchasing patterns throughout the day
        - Weekend purchasing is 35% higher across all segments
        """)
        
        # Category preferences by segment
        st.subheader("Category Preferences by Segment")
        
        # Create category preference data
        categories = ['Dairy', 'Fresh Produce', 'Snacks', 'Beverages', 'Ready-to-eat']
        category_prefs = []
        
        for segment in segment_df['name']:
            for category in categories:
                # Different preferences for different segments
                if segment == 'High-value Shoppers':
                    value = 85 if category in ['Fresh Produce', 'Ready-to-eat'] else 65
                elif segment == 'Regular Customers':
                    value = 75 if category in ['Dairy', 'Beverages'] else 60
                elif segment == 'Occasional Buyers':
                    value = 70 if category in ['Snacks', 'Beverages'] else 50
                else:  # New Users
                    value = 60 if category in ['Snacks', 'Beverages'] else 45
                
                # Add some random variation
                value = max(0, min(100, int(value + np.random.normal(0, 5))))
                
                category_prefs.append({
                    'segment': segment,
                    'category': category,
                    'preference': value
                })
        
        category_pref_df = pd.DataFrame(category_prefs)
        
        # Create grouped bar chart
        fig = px.bar(
            category_pref_df,
            x='category',
            y='preference',
            color='segment',
            barmode='group',
            labels={'category': 'Product Category', 'preference': 'Preference Score'},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            xaxis_title='',
            yaxis_title='Preference Score',
            legend_title=''
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with segment_tab3:
        st.subheader("Personalization Strategies")
        
        # Sample personalization strategies
        st.markdown("""
        <div class='card' style='margin-bottom: 1rem;'>
            <h3>High-value Shoppers</h3>
            <p><strong>Strategy:</strong> Premium Product Recommendations & Early Access</p>
            <p>Target with premium products, organic options, and early access to new items. 
            Personalized notifications for restocking of frequently purchased items.</p>
            <p><strong>Engagement Rate:</strong> <span class='highlight'>78%</span></p>
        </div>
        
        <div class='card' style='margin-bottom: 1rem;'>
            <h3>Regular Customers</h3>
            <p><strong>Strategy:</strong> Subscription Offers & Bundle Discounts</p>
            <p>Encourage recurring purchases with subscription offers for regular items.
            Bundle recommendations based on purchase history to increase basket size.</p>
            <p><strong>Engagement Rate:</strong> <span class='highlight'>65%</span></p>
        </div>
        
        <div class='card' style='margin-bottom: 1rem;'>
            <h3>Occasional Buyers</h3>
            <p><strong>Strategy:</strong> Limited-time Offers & Re-engagement Campaigns</p>
            <p>Flash sales and limited-time offers aligned with previous purchase categories.
            Re-engagement campaigns with targeted incentives during typical purchase times.</p>
            <p><strong>Engagement Rate:</strong> <span class='highlight'>42%</span></p>
        </div>
        
        <div class='card'>
            <h3>New Users</h3>
            <p><strong>Strategy:</strong> Onboarding Promotions & Discovery Suggestions</p>
            <p>First-time purchase incentives and guided product discovery based on initial browsing behavior.
            Educational content about quick commerce benefits and express delivery options.</p>
            <p><strong>Engagement Rate:</strong> <span class='highlight'>53%</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        # ROI and impact visualization
        st.subheader("Personalization Impact")
        
        impact_data = pd.DataFrame({
            'segment': segment_df['name'],
            'engagement_lift': [78, 65, 42, 53],
            'revenue_lift': [35, 28, 15, 22],
            'retention_lift': [25, 18, 12, 15]
        })
        
        # Melt the dataframe for grouped bar chart
        impact_melted = impact_data.melt(
            id_vars='segment',
            value_vars=['engagement_lift', 'revenue_lift', 'retention_lift'],
            var_name='metric',
            value_name='percentage'
        )
        
        # Clean up the metric names
        impact_melted['metric'] = impact_melted['metric'].apply(lambda x: x.replace('_lift', '').title())
        
        # Create grouped bar chart
        fig = px.bar(
            impact_melted,
            x='segment',
            y='percentage',
            color='metric',
            barmode='group',
            labels={'segment': 'Customer Segment', 'percentage': 'Lift (%)'},
            color_discrete_sequence=['#3498db', '#2ecc71', '#9b59b6']
        )
        fig.update_layout(
            xaxis_title='',
            yaxis_title='Improvement (%)',
            legend_title=''
        )
        st.plotly_chart(fig, use_container_width=True)

# Run the app with: streamlit run app.py
if __name__ == "__main__":
    st.sidebar.info("Note: This is a demo application. All data shown is simulated.")
