#Autor Tomasz Hałas 
using JuMP
using GLPK
using LinearAlgebra

function zad4(n,m,range,containers)
    
    model = Model(GLPK.Optimizer)
    @variable(model, 0<=square[1:n, 1:m]<=4*range*100, Int) #number of squares

    @constraint(model, [i = 1:n , j=1:m; containers[i,j] == 1], square[i,j] == 0) #where is containers
    @constraint(model, [i = 1:n , j=1:m; containers[i,j] == 0], square[i,j] >= 1) #set some other value if there is not coinatiner
    @constraint(model, [i = 1:n, j=1:m; containers[i,j] == 1],
        sum(square[ranger(i-range):ranger_plus(i+range),j]) + sum(square[i,ranger(j-range):ranger_plus(j+range)]) >=4*range*100)
        #sum moving along with cameras range to find the best place to put one 
    
    @objective(model, Min, sum(square)); # Min number of cameras
    optimize!(model)
    println(sum(value.(square)))
    @show containers
    @show value.(square)
    solution = convert.(Float64, value.(square))
end

function ranger(range)
    if range < 1 return 1
    else return range
    end
end

function ranger_plus(range,size=5)
    if range > size 
        return size
    else return range
    end
end

containers = zeros(5,5)
containers[1,2]=1
containers[1,4]=1 
containers[2,1]=1
containers[2,3]=1
containers[2,5]=1
containers[3,5]=1
containers[3,4]=1
containers[4,1]=1

range = 1
n=5
m=5

zad4(n,m,range,containers)



