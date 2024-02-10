import numpy as np
import plotly.graph_objects as go
from solver import capacitated_facility_location


def generate_example(nb_facilities: int, 
                     nb_customers: int,
                     demand_range: tuple[int, int] = (30, 80),
                     customer_location_range: tuple[int, int] = (0, 1000),
                     capacity_range: tuple[int, int] = (100, 200),
                     facility_cost_range: tuple[float, float] = (1000, 10000)):

    demands = np.random.randint(demand_range[0], demand_range[1], nb_customers)
    customers_locations = np.random.randint(customer_location_range[0], customer_location_range[1], (nb_customers, 2))
    capacities = np.random.randint(capacity_range[0], capacity_range[1], nb_facilities)
    facilities_costs = np.random.uniform(facility_cost_range[0], facility_cost_range[1], nb_facilities)
    facilities_locations = np.random.randint(customer_location_range[0], customer_location_range[1], (nb_facilities, 2))
    transportation_costs = np.array([[np.linalg.norm(customers_locations[j] - facilities_locations[i]) for j in range(nb_customers)] for i in range(nb_facilities)])
    return demands, capacities, facilities_costs, transportation_costs, customers_locations, facilities_locations


def plot_result(customers_locations, facilities_locations, demands, capacities, build_facility, assigned_demand):
    fig = go.Figure()

    capacities = np.array(capacities)
    max_capacity = capacities.max()
    demands = np.array(demands)
    max_demand = demands.max()
    demands = (demands / capacities.max())*10*max_capacity/max_demand
    capacities = (capacities / capacities.max())*15
    assigned_demand = np.array(assigned_demand)
    assigned_demand = (assigned_demand / assigned_demand.max())*2

    for i in range(len(build_facility)):
        if build_facility[i]:
            for j in range(len(assigned_demand[i])):
                if assigned_demand[i][j] > 0:
                    fig.add_trace(go.Scatter(x=[facilities_locations[i][0], customers_locations[j][0]], y=[facilities_locations[i][1], customers_locations[j][1]], mode='lines', line=dict(width=assigned_demand[i][j], color='black'), name=f'Assigned demand', legendgroup='assigned_demand', showlegend=False, legendgrouptitle=dict(text='Assigned demand')))

    for i, (x, y) in enumerate(facilities_locations):
        if build_facility[i]:
            fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers', marker=dict(size=capacities[i], color='red'), name=f'Facility {i} (built)', legendgroup='built_facility', showlegend=True, legendgrouptitle=dict(text='Built facilities')))
        else:
            fig.add_trace(go.Scatter
            (x=[x], y=[y], mode='markers', marker=dict(size=capacities[i], color='red', opacity=0.2), name=f'Facility {i} (non_built)', legendgroup='non_built_facility', showlegend=True, legendgrouptitle=dict(text='Non-built facilities')))
    
    for j, (x, y) in enumerate(customers_locations):
        fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers', marker=dict(size=demands[j], color='blue'), name=f'Customer {j}', legendgroup='customer', showlegend=True, legendgrouptitle=dict(text='Customers')))

    fig.update_layout(title='Facilities', xaxis_title='x', yaxis_title='y', height=800, width=1200)
    return fig

    
if __name__ == '__main__':
    demands, capacities, facilities_costs, transportation_costs, customers_locations, facilities_locations = \
        generate_example(nb_facilities=30, 
                         nb_customers=50, 
                         demand_range=(30, 80), 
                         customer_location_range=(0, 1000), 
                         capacity_range=(100, 200), 
                         facility_cost_range=(1000, 10000))
    
    build_facility, assigned_demand = capacitated_facility_location(demands, capacities, facilities_costs, transportation_costs)
    if build_facility is not None:
        print("Number of facilities built:", sum(build_facility))
        print("Total construction cost:", sum(build_facility[i]*facilities_costs[i] for i in range(len(build_facility))))
        print("Total transportation cost:", sum(sum(assigned_demand[i][j]*transportation_costs[i][j] for j in range(len(assigned_demand[i]))) for i in range(len(assigned_demand))))
        fig = plot_result(customers_locations, facilities_locations, demands, capacities, build_facility, assigned_demand)
        fig.write_html('capacitated_facility_location.html', auto_open=True)
    else:
        print("No solution found.")
