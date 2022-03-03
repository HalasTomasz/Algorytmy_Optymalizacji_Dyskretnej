#Autor Tomasz Hałas
using JuMP
using GLPK

function zad2(num_police,num_shifts,min,max,min_per_shift,min_per_state)
    
    model = Model(GLPK.Optimizer)
        
    @variable(model,0<=shifts[1:num_police,1:num_shifts], Int) #number of shifts mulitply states of city 
    @variable(model,1.0<=shift_back[1:num_police,1:num_shifts], Int) #number vehicle returning from
                                                                    #shifts mulitply state of city

    for j in 1:num_shifts
        for i in 1:num_police
            @constraint(model, min[j][i] <= shifts[j,i] <= max[j][i]) #min and max on current shift
        end
    end

    for j in 1:num_shifts
        for i in 1:num_police
            @constraint(model,  min[j][i] <= shift_back[range(j+1),range(i+1)] <= max[j][i]) 
            #min and max coming back from current shift
        end
    end

    for i in 1:num_shifts
        @constraint(model,min_per_shift[i] <=sum(shifts[i,:])) #min vehicle per shift
        @constraint(model, sum(shift_back[range(i+1),:]) <= sum(shifts[i,:])) # set sum of return vehicle to be less than
                                                                              # newly added vehicle
    end

    for i in 1:num_shifts
        @constraint(model,min_per_state[i] <=sum(shifts[:,i]))  #min vehicle per state of city
    end

    @objective(model, Min, sum(shift_back)) #min vehicle in use
    optimize!(model)
    @show objective_value(model)
    @show value.(shifts)
    @show value.(shifts-shift_back)
end

min = [
    [2,4,3],
    [3,6,5],
    [5,7,6]
]
max = [
    [3,7,5],
    [5,7,10],
    [8,12,10]
]
min_per_shift = [10,20,18]
min_per_state = [10,20,13]
num_police = 3
num_shifts = 3

zad2(num_police,num_shifts,min,max,min_per_shift,min_per_state)

function ranger(range,size=3)
    if range <1 return size
    else return range
    end
end

function range(range,size=3)
    if range > size  return 1
    else return range
    end
end
