#pragma once

#include <vector>
#include <utility>
#include <algorithm>
#include <exception>
#include <iostream>
#include <cmath>

/*TODO: refactor the code to maximize cache usage. I can split elements and priorities into 2 vectors.
Because most of the time we work only with priorities, we can maximize the number of priorities we put into
the cache in one operation.
If i keep elements and priorities into a vector of pairs, when i use PushDown or BubbleUp, i put into the cache
useless information (the elements) while i need to work only on priorities.
*/

#define DEBUG

#ifdef DEBUG
#define LOG(x)         std::cout << x << std::endl
#define ENTER(x)       std::cout << "enter " << x << std::endl
#define EXIT(x)        std::cout << "exit " << s << std::endl

#else
#define LOG(x)        
#define ENTER(x)      
#define EXIT(x)        
#endif



//TODO: implement Heapify (construct an heap from a vector of elements/priorities).
template <typename TElement, typename TPriority, typename TComparator>
class DHeap
{
public:
    DHeap() : pairs(), d(2), comparator()
    {

    }

    DHeap(int _branching_factor, TComparator _comparator) : pairs(), d(_branching_factor), comparator(_comparator)
    {

    }

    


    /*
    Insert an element with the associated priority into the heap.
    Running time: O(log n in base d).
    */
    void Insert(const TElement& element, const TPriority& priority)
    {
        ENTER("insert");
        pairs.emplace_back(element, priority);
        BubbleUp(pairs.size() - 1);
        EXIT("insert");
    }

    /*
    Remove the element/priority pair with the highest priority from the heap and return the element.
    Running time: O(log n in base d).
    */
    TElement Top()
    {
        ENTER("top");
        if (pairs.empty())
        {
            throw std::out_of_range("Heap is empty");
        }
        
        auto last = std::move(pairs.back());
        pairs.pop_back();
        if (pairs.empty())
        {
            return last.first;
        }

        //If there is more than one element, put the "last" element at the root and call PushDown.
        auto first = std::move(pairs[0]);
        
        //I do this to "force" the compiler to use the move constructor for the returned value.
        //If i return first.first, the compiler will make a copy. (with clang c++20)
        auto element = std::move(first.first); 
        
        pairs[0] = std::move(last);
        PushDown(0);

        EXIT("top");
        return element;
    }

    /*
    Running time: O(n).
    */
    bool Update(const TElement& element, const TPriority& priority)
    {
        int idx = Find(element);
        if (idx >= 0)
        {
            auto old_priority = std::move(pairs[idx].second);
            pairs[idx].second = priority;

            if (comparator(priority, old_priority))
            {
                BubbleUp(idx);
            }
            else
            {
                PushDown(idx);
            }
            return true;
        }

        return false;
    }

    /*
    Running time: O(n).
    */
    bool Contains(const TElement& element)
    {
        return Find(element) >= 0;
    }


    constexpr size_t size() const noexcept
    {
        return pairs.size();
    }

    /*
    Checks that the three invariants for heaps are abided by.
        1.	Every node has at most `D` children. (Guaranteed by construction)
        2.	The heap tree is complete and left-adjusted.(Also guaranteed by construction)
        3.	Every node holds the highest priority in the subtree rooted at that node.
        Returns: True if all the heap invariants are met.
    */
    bool validate()
    {
        int curr_idx = 0;

        while (curr_idx < GetFirstLeafIndex())
        {
            auto curr_prio = GetPriority(curr_idx);
            auto first_child = GetFirstChildrenIndex(curr_idx);
            auto last_child =  std::min(first_child + d, (int)size());
            for (int i = first_child; i < last_child; ++i)
            {
                if (!comparator(curr_prio, GetPriority(i)))
                {
                    return false;
                }
            }
            curr_idx += 1;
        }

        return true;
    }


private:
    std::vector<std::pair<TElement, TPriority>> pairs;
    int d; //Branching factor
    TComparator comparator;


private:

    constexpr int GetParentIndex(int child_idx) const
    {
        return (child_idx - 1) / d;
    }

    constexpr int GetFirstChildrenIndex(int parent_idx) const 
    {
        return d * parent_idx + 1;
    }

    constexpr int GetFirstLeafIndex() const 
    {
        return std::floor((pairs.size() - 2.0) / d) + 1;
    }

    int GetHighestPriorityChildIndex(int parent_idx)
    {
        const int first_child_idx = GetFirstChildrenIndex(parent_idx);
        const int last_child_idx = std::min(first_child_idx + d, (int)pairs.size());

        int current_idx = first_child_idx;

        for (int i = first_child_idx; i < last_child_idx; ++i)
        {
            if (!comparator(GetPriority(current_idx), GetPriority(i)))
            {
                current_idx = i;
            }
        }    
        return current_idx;
    }


    TElement& GetElement(int idx)
    {
        return pairs[idx].first;
    }

    const TElement& GetElement(int idx) const
    {
        return pairs[idx].first;
    }

    TPriority& GetPriority(int idx)
    {
        return pairs[idx].second;
    }

    const TPriority& GetPriority(int idx) const
    {
        return pairs[idx].second;
    }

    /*
    Find an element and, if present return the index otherwise -1.
    Running time: O(n).
    This could be improved using O(n) space with a map from element to index.
    */
    int Find(const TElement& e)
    {   
        auto it = std::find_if(std::begin(pairs), std::end(), [&](const auto& v) { return v.first == e ;});
        
        if (it != std::end(pairs))
            return it - std::begin(pairs); //or maybe std::distance

        return -1;
    }



    /*
    Move an element with higher priority up the heap.
    Running time: O(log n in base d).
    */
    void BubbleUp(int idx)
    {
        ENTER("bubbleup");
        auto current = std::move(pairs[idx]);
        const auto current_priority = current.second;

        while (idx > 0)
        {
            int parent_idx = GetParentIndex(idx);
            const auto parent_priority = GetPriority(parent_idx);

            if (comparator(current_priority, parent_priority))
            {
                pairs[idx] = std::move(pairs[parent_idx]); 
                idx = parent_idx;
            }
            else
            {
                break;
            }
        }
        pairs[idx] = std::move(current);

        EXIT("bubbleup");
    }

    /*
    Move an element with lower priority down the heap.
    Running time: O(log n in base d).
    */
    void PushDown(int idx)
    {
        ENTER("pushdown");
        auto current = std::move(pairs[idx]);
        const auto current_priority = current.second;


        while (idx < GetFirstLeafIndex())
        {
            const int highest_child_idx = GetHighestPriorityChildIndex(idx);
            if (comparator(GetPriority(highest_child_idx), current_priority))
            {
                pairs[idx] = std::move(pairs[highest_child_idx]);
                idx = highest_child_idx;
            }
            else
            {
                break;
            }
        }
        pairs[idx] = std::move(current);
        EXIT("pushdown");
    }
};