#pragma once 

#include <exception>
#include <queue>
#include <string>
#include "debug.hpp"

/*
For now i will use raw pointer, because the implementation with shared_ptr and unique_ptr it's not trivial and presents severe bugs.
Honestly i don't like this design, it's like more C oriented than C++ oriented so i will try to think a new design.
*/

template <typename TElement, typename TPriority>
struct Node
{
    Node* parent{nullptr};
    Node* left{nullptr};
    Node* right{nullptr};

    TElement key;
    TPriority priority;


    Node() = default;


    // Node(const TElement& _key, const TPriority& _priority) : parent(nullptr), left(nullptr), right(nullptr),   
    //     key(_key), priority(_priority)
    // {

    // }

    // Node(TElement&& _key, TPriority&& _priority) : parent(nullptr), left(nullptr), right(nullptr),   
    //     key(std::move(_key)), priority(std::move(_priority))
    // {

    // }

    Node(TElement _key, TPriority _priority) : parent(nullptr), left(nullptr), right(nullptr),   
        key(std::move(_key)), priority(std::move(_priority))
    {

    }
    

    void SetLeft(Node* node)
    {
        left = node;
        if (node != nullptr)
        {
            node->parent = this;
        }
    }

    void SetRight(Node* node)
    {
        right = node;
        if (node != nullptr)
        {
            node->parent = this;
        }
    }
};



//TODO: add concept for types 
//Note: Treap are not balanced trees. To make them balanced we need to introduce randomization through priorities.
template <typename TElement, typename TPriority, typename TComparator>
class Treap
{
public:
    using NodeType = Node<TElement, TPriority>;

    Treap() = default;

    ~Treap()
    {
        Reset(root);
    }

    bool IsRoot(NodeType* node)
    {
        return node->parent == nullptr;
    }

    bool IsLeaf(NodeType* node)
    {
        return node->left == nullptr && node->right == nullptr;
    }

    NodeType* GetRoot() const
    {
        return root;
    }

    /*
    Perform a search starting from root node.
    Running time: O(log n in base 2).
    */
    NodeType* Search(const TElement& target)
    {
        return Search(root, target);
    }

    /*
    Perform a search starting from an argument node.
    Running time: O(log n in base 2).
    */
    NodeType* Search(NodeType* node, const TElement& target)
    {
        if (node == nullptr)
        {
            return nullptr;
        }

        if (node->key == target)
        {
            return node;
        }
        else if (target < node->key)
        {
            return Search(node->left, target);
        }
        else
        {
            return Search(node->right, target);
        }
    }


    /*
    Return the element with the highest priority.
    Running time: O(1).
    */
    const TElement& Peek() const
    {
        if (root == nullptr)
        {
            throw std::out_of_range("The treap is empty");
        }
        return root->key;
    }


    const TElement& Min()
    {
        if (root == nullptr)
        {
            throw std::out_of_range("The treap is empty");
        }

        NodeType* node = root;
        while (node->left != nullptr)
        {
            node = node->left;
        }
        return node->key;
    }

    const TElement& Min() const
    {
        if (root == nullptr)
        {
            throw std::out_of_range("The treap is empty");
        }

        NodeType* node = root;
        while (node->left != nullptr)
        {
            node = node->left;
        }
        return node->key;
    }

    const TElement& Max() const
    {
        if (root == nullptr)
        {
            throw std::out_of_range("The treap is empty");
        }

        NodeType* node = root;
        while (node->right != nullptr)
        {
            node = node->right;
        }
        return node->key;
    }


    void Insert(TElement element, TPriority priority)
    {
        ENTER("Insert");

        NodeType* new_node = new NodeType(std::move(element), std::move(priority));
        NodeType* node = root;
        NodeType* parent = nullptr;
        
        while (node != nullptr)
        {
            parent = node;

            if (new_node->key <= node->key)
            {
                node = node->left;
            }
            else
            {
                node = node->right;
            }
        }

        if (parent == nullptr)
        {
            root = new_node;
            return;
        }
        else if (new_node->key <= parent->key)
        {
            parent->SetLeft(new_node);
        }
        else
        {
            parent->SetRight(new_node);
        }

        while (new_node->parent != nullptr && comparator(new_node->priority, new_node->parent->priority))
        {
            if (new_node == new_node->parent->left)
            {
                LOG("right rotate");
                RightRotate(new_node);
            }
            else
            {
                LOG("left rotate");
                LeftRotate(new_node);
            }
        }

        LOG("Exit heap invariant validation");
        if (new_node->parent == nullptr)
        {
            root = new_node;
        }

        EXIT("Insert");
    }

    /*
    Remove and delete the node associated with key, if present.
    Running time: O(log n in base 2).
    */
    bool Remove(const TElement& key)
    {
        ENTER("Remove");
        NodeType* node = Search(key);

        if (node == nullptr)
        {
            return false;
        }

        if (IsRoot(node) and IsLeaf(node))
        {
            delete root;
            root = nullptr;
            return true;
        }

        while (!IsLeaf(node))
        {
            if (node->left != nullptr && 
                (node->right == nullptr || comparator(node->left->priority, node->right->priority)))
            {
                RightRotate(node->left);
            }
            else
            {
                LeftRotate(node->right);
            }

            if (IsRoot(node->parent))
            {
                root = node->parent;
            }
        }

        if (node->parent->left == node)
        {
            delete node->parent->left;
            node->parent->left = nullptr;
        }
        else
        {
            delete node->parent->right;
            node->parent->right = nullptr;
        }

        EXIT("Remove");
        return true;
    }


    bool Validate()
    {
        std::queue<NodeType*> tree;
        tree.push(root);
        NodeType* node = nullptr;
        while (!tree.empty())
        {
            node = tree.front();
            tree.pop();
            
            if (node != nullptr)
            {
                if (node->left != nullptr)
                {
                    tree.push(node->left);
                }
                if (node->right != nullptr)
                {
                    tree.push(node->right);
                }

                //Check that the key invariant is holding.
                if (node->left != nullptr && node->key < node->left->key)
                {
                    return false;
                }
                else if (node->right != nullptr && node->key > node->right->key)
                {
                    return false;
                }
            }
        }

        return true;
    }


private:
    NodeType* root{nullptr};
    TComparator comparator{};

    void RightRotate(NodeType* node)
    {
        if (node == nullptr || IsRoot(node))
        {
            throw std::invalid_argument{"node is null or root"};
        }
        auto p = node->parent;

        if (p->left != node)
        {
            throw std::domain_error{"node is not left child of the parent, can't perform right rotate"};
        }

        auto gp = p->parent;

        if (gp != nullptr)
        {   
            if (gp->left == p)
            {
                gp->SetLeft(node);
            }
            else
            {
                gp->SetRight(node);
            }
        }
        else
        {
            root = node;
            node->parent = nullptr;
        }

        p->SetLeft(node->right);
        node->SetRight(p);
    }

    void LeftRotate(NodeType* node)
    {
        if (node == nullptr || IsRoot(node))
        {
            throw std::invalid_argument{"node is null or root"};
        }
        auto p = node->parent;

        if (p->right != node)
        {
            throw std::domain_error{"node is not right child of the parent, can't perform left rotate"};
        }

        auto gp = p->parent;

        if (gp != nullptr)
        {   
            if (gp->left == p)
            {
                gp->SetLeft(node);
            }
            else
            {
                gp->SetRight(node);
            }
        }
        else
        {
            root = node;
            node->parent = nullptr;
        }

        p->SetRight(node->left);
        node->SetLeft(p);    
    }


    //Free the memory of the sub tree rooted at node. (node will be deleted too).
    void Reset(NodeType* node)
    {
        //Free memory
    }
};