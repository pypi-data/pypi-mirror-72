
struct Axis
    name::String
    values::Array
end

mutable struct ParameterSpace
    axes::Array{Axis}
    ParameterSpace() = new([])
    ParameterSpace(axis::Axis) = new([axis])
    ParameterSpace(axes::Array{Axis}) = new(axes)
end


function index_to_coords(i, axes_lengths)
    i′ = i - 1
    L = axes_lengths[1]
    c = (i′)%L + 1
    r = Int(floor(i′/L))
    
    if length(axes_lengths) == 1 return c end
    
    coords = [c; index_to_coords(r + 1, axes_lengths[2:end])]
end

Base.length(x::Axis) = length(x.values)
Base.length(p::ParameterSpace) = prod(map(x -> length(x.values), p.axes))
add_axis(p::ParameterSpace, axis) = push!(p.axes, axis)

function Base.getindex(p::ParameterSpace, I...)
    [p.axes[d].values[i] for (d,i) in enumerate(I)]
end

function get_param(p::ParameterSpace, t)
    if t > length(p) || t < 1  return nothing end
    c = index_to_coords(t, map(length, p.axes))
    p[c...]
end

function Base.iterate(iter::ParameterSpace, state=(get_param(iter, 1),1))
    element, count = state
    if count > length(iter)
       return nothing
    end

    return (element, (get_param(iter, count + 1), count + 1))
end


function find_coords(pspace::ParameterSpace, param)
    c = []
    for (i,p) in enumerate(param)
        res = findall(x->x==p, pspace.axes[i].values)
        if length(res) > 0
            push!(c, res[1])
        else
            push!(c, nothing)
        end
    end
    return c
end

function find_index(pspace, p)
	L = map(length, pspace.axes)
	c = find_coords(pspace, p) .- 1
	f = reduce((r, l)-> [r; r[end]*l], L; init=[1])[1:end-1]
	return sum(f.*c) + 1
end

find(pspace, p) = find_index(pspace, p)

