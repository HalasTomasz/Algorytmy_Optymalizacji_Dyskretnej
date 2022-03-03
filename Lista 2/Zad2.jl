#Autor Tomasz Hałas
using JuMP
using GLPK
using LinearAlgebra

function zad2(n,graph,times,start,ender)
    model = Model(GLPK.Optimizer)

    @variable(model, edge[1:n, 1:n], Bin) # edges in graph for model

    @constraint(model, [i = 1:n, j = 1:n; graph[i, j] == 0], edge[i, j] == 0) # edges in worthless donest exist

    @constraint(model, [i = 1:n; i != 1 && i != 2],sum(edge[i, :]) == sum(edge[:, i]))
    # Sum of incoming eq those outcoming (cycle)
    
    @constraint(model, sum(edge[start, :]) - sum(edge[:, start]) == 1) # Outcming plus Incoming (source flow == 1)
    @constraint(model, sum(edge[ender, :]) - sum(edge[:, ender]) == -1) # Outcming plus Incoming (destination flow == -1)
    @constraint(model, LinearAlgebra.dot(times, edge) <= 5000) # Check if we pass on time

    @objective(model, Min, LinearAlgebra.dot(graph, edge))# Min price

    optimize!(model)
    objective_value(model)
    value.(edge)
end

G = [
    32 22 30 0 6
    51 30 20 2 0
    52 10 40 10 60
    32 15 2 23 50
    33 2 2 55 56
]

M = [ 
    11 20 110 5 33
    23 35  100 5 0
    11 13 23  11 11
    33 100 0 2 13
    55 6  0  0 0
]
n = size(G)[1]

zad2(n,G,M,1,4)


