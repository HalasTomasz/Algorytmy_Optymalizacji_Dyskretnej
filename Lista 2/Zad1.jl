#Autor Tomasz Hałas
using JuMP
using GLPK

function zad1(airports_min,airports_supplay,derilver_cap,price)
    #Create optimizer
    model = Model(GLPK.Optimizer)
    
    #number of conection between airports and firms which delivers oil
    @variable(model,0<=x[i = 1:length(airports_min)*length(derilver_cap)], Int) 

    for i in 1:length(airports_min)
        @constraint(model, x[i] + x[i+4] + x[i+8] >= airports_supplay[i]) #We have to give some amount to the airport so 
    end                                                                   #airport runs on 100 %
    j = 1
    for i in 1:4:length(derilver_cap)*length(airports_min)
        @constraint(model, x[i] + x[i+1] + x[i+2] + x[i+3] <= derilver_cap[j]) # We can't give more fuel that company have
        j= j +1
    end


    @objective(model, Min, sum(price[i]* x[i] for i in 1:length(price))) #Find the best prices
    optimize!(model)
    @show objective_value(model)
    @show value.(x)
    solution = convert.(Int, value.(x))
end

airports_min = [1,2,3,4]
airports_supplay = [110000,220000,330000,440000]
derilver_cap = [275000,550000,660000]
price = [10,10,9,11,7,11,12,13,8,14,4,9]

zad1(airports_min,airports_supplay,derilver_cap,price)
