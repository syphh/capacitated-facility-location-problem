from ortools.sat.python import cp_model


def capacitated_facility_location(demands: list[int], 
                                  capacities: list[int], 
                                  facilities_costs: list[float], 
                                  transportation_costs: list[list[float]]):

    model = cp_model.CpModel()
    nb_facilities = len(capacities)
    nb_customers = len(demands)
    build_facility_vars = [model.NewBoolVar(f'build_facility_{i}') for i in range(nb_facilities)]
    assigned_demand_vars = [[model.NewIntVar(0, demands[j], f'assigned_demand_{i}_{j}') for j in range(nb_customers)] for i in range(nb_facilities)]
    
    for j in range(nb_customers):
        model.Add(sum(assigned_demand_vars[i][j] for i in range(nb_facilities)) == demands[j])

    for i in range(nb_facilities):
        model.Add(sum(assigned_demand_vars[i][j] for j in range(nb_customers)) <= capacities[i] * build_facility_vars[i])

    total_build_cost = sum(build_facility_vars[i] * facilities_costs[i] for i in range(nb_facilities))
    total_transportation_cost = sum(assigned_demand_vars[i][j] * transportation_costs[i][j] for i in range(nb_facilities) for j in range(nb_customers))

    model.Minimize(total_build_cost + total_transportation_cost)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        build_facility = [solver.Value(build_facility_vars[i]) for i in range(nb_facilities)]
        assigned_demand = [[solver.Value(assigned_demand_vars[i][j]) for j in range(nb_customers)] for i in range(nb_facilities)]
        return build_facility, assigned_demand
    else:
        return None, None
