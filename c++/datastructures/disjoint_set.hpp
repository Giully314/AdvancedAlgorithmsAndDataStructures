#pragma once

#include <unordered_map>
#include <memory>

template <typename T> 
struct Info
{
    Info() = default;
    Info(const T& elem_, size_t rank_) : root(std::make_shared<const T>(elem_)), rank(rank_)
    {

    }


    std::shared_ptr<const T> root = nullptr;
    size_t rank = 0;
};


//TODO: concept for the type T (copyable, movable ecc)
//TODO: write it better, i feel like it's bad.
template <typename T> 
class DisjointSet
{
public:
    DisjointSet(const std::vector<T>& elems)
    {
        for (const auto& elem : elems)
        {
            set.insert(std::make_pair(elem, Info<T>(elem, 1)));
        }
    }
    
    //Running time: Same as FindPartition.
    bool AreDisjoint(const T& x, const T& y)
    {
        auto xp = FindPartition(x);
        auto yp = FindPartition(y);

        return xp.root != yp.root;
    }
    
    //Running time O(1).
    bool Merge(const T& x, const T& y)
    {
        auto& xp = FindPartition(x);
        auto& yp = FindPartition(y);

        if (xp.root == yp.root)
        {
            return false;
        }
        
        if (xp.rank >= yp.rank)
        {
            yp.root = xp.root;
            xp.rank += yp.rank;
        }
        else
        {
            xp.root = yp.root;
            yp.rank += xp.rank;
        }

        return true;
    }



    std::unordered_map<T, Info<T>> set;


    //Running time for m operations with n elements: O(m * inv_ack(n)) where inv_ack(n) is less than 5 for 
    //very very large number.
    Info<T>& FindPartition(const T& elem)
    {
        Info<T>& info = set[elem];

        if (*info.root == elem)
        {
            return info;
        }
        info.root = FindPartition(*info.root).root;
        return info;
    }
};