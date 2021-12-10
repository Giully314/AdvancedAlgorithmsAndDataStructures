#pragma once

#include <string>
#include <string_view>
#include <unordered_map>
#include <memory>
#include <optional>


//Implementation use ASCII.
inline constexpr std::string_view c_alphabet{"abcdefghijklmnopqrstuvwxyz"};


struct Node 
{
    Node(bool stores_key) : key_node(stores_key)
    {
        for (const auto& c : c_alphabet)
        {
            children[c] = nullptr;
        }
    }

    //is this a "terminal" node? That is, the path until this node makes a word.
    bool key_node;
    std::unordered_map<char, std::unique_ptr<Node>> children;
};


class Trie
{
public:
    Trie() : root(std::make_unique<Node>(false))
    {

    }

    bool Contains(std::string_view s) const
    {
        if (root == nullptr)
        {
            return false;
        }
        return Contains(root.get(), s);
    }


    void Insert(std::string_view s)
    {
        Insert(root.get(), s);
    }

    
    //This version is faster than the version that physically remove the nodes.
    //Use this if there are few calls to Remove.
    //Use the other implementation (with pruning) if there are a lot of call to Remove and need to release memory.
    bool Remove(std::string_view s)
    {
        Node* n = Search(root.get(), s);
        if (n == nullptr || n->key_node == false)
        {
            return false;
        }

        n->key_node = false;
        return true;
    }

   
private:
    std::unique_ptr<Node> root;


    bool Contains(Node* n, std::string_view s) const
    {
        if (s.empty())
        {
            return n->key_node;
        }

        if (n->children[s[0]] == nullptr)
        {
            return false;
        }

        return Contains(n->children[s[0]].get(), s.substr(1));
    }


    Node* Search(Node* n, std::string_view s) const
    {
        if (s.empty())
        {
            return n;
        }

        if (n->children[s[0]] == nullptr)
        {
            return nullptr;
        }

        return Search(n->children[s[0]].get(), s.substr(1));
    }


    void Insert(Node* n, std::string_view s)
    {
        if (s.empty())
        {
            n->key_node = true;
            return;
        }

        if (n->children[s[0]] != nullptr)
        {
            Insert(n->children[s[0]].get(), s.substr(1));
            return;
        }

        AddNewBranch(n, s);
    }


    void AddNewBranch(Node* n, std::string_view s)
    {
        if (s.empty())
        {
            n->key_node = true;
            return;
        }

        n->children[s[0]] = std::make_unique<Node>(false);
        AddNewBranch(n->children[s[0]].get(), s.substr(1));
    }



};
