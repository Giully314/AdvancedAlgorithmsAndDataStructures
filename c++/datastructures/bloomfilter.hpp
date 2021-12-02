#pragma once 

#include <functional>
#include <string>
#include <algorithm>
#include <random>
#include <vector>
#include <cmath>
#include <exception>
#include <iterator>


/*
Note:  this implementation is horrible. I'm designing a new implementation using std::bitset.
*/


struct Hash
{
    void Init(size_t num_hash_functions, size_t length_random_str)
    {
        constexpr char charset[] =
        "0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz";

        std::random_device r;
        std::default_random_engine e1(r());
        std::uniform_int_distribution<int> dist(0, sizeof(charset));

        random_strings.reserve(num_hash_functions);
        std::generate_n(std::back_inserter(random_strings), num_hash_functions, [&]()
        {
            std::string tmp;
            for (int i = 0; i < length_random_str; ++i)
            {
                tmp += charset[dist(e1)];
            }
            return tmp;
        });
    }


    size_t operator()(const std::string& s, size_t i)
    {
        return hash(s + random_strings[i]);
    }
    
    std::hash<std::string> hash;
    std::vector<std::string> random_strings;
};


//Simplified version that assume the type of the keys as string.
//Another optimization that could be done is using std::bitset if the size is know at compile time.
//Or i could use a simple vector<int> and implent that operations to access single bit.
template <unsigned K>
class BloomFilter
{
public:
    BloomFilter(size_t _max_size, float max_tolerance, int _seed) : size(0), max_size(_max_size), seed(_seed)
    {
        const ln_2 = std::log(2);
        size_t num_bits = -std::ceil(max_size * std::log(max_tolerance) / ln_2 / ln_2);

        if (num_bits > max_size)
        {
            throw std::invalid_argument("number of bits required to satisfy max_tolerance is greater than max_size");
        }

        num_hash_functions = -std::ceil(std::log(max_tolerance) / ln_2);
        
        //Reserve and initialize the bit array with 0.
        bits.reserve(num_bits);
        std::fill_n(std::back_inserter(bits), num_bits, false);

        hash.Init(num_hash_functions, 10);

        curr_key_2_pos.reserve(num_hash_functions);
        std::fill_n(std::back_inserter(curr_key_2_pos), num_hash_functions, 0);
    }


    void KeyToPosition(const std::string& key)
    {
        for (int i = 0; i < num_hash_functions; ++i)
        {
            curr_key_2_pos[i] = hash(key, i);
        }
    }

    //position = true means that the position is already computed
    bool Contains(const std::string& key, bool position=false)
    {
        if (!position)
            KeyToPosition(key);
        
        for (auto i : curr_key_2_pos)
        {
            if (!bits[i])
            {
                return false;
            }
        }
        return true;
    }

    void Insert(const std::string& key)
    {
        KeyToPosition(key);
        if (!Contains(key, true))
        {
            size += 1;
            for (auto i : curr_key_2_pos)
            {
                bits[i] = true;
            }
        }
    }

    
private:
    /*
    i'm inexperienced with hash functions, i only studied the basics a long time ago but i'm planning to 
    dive deep in the topic to understand better the field. For now i'm going to use the hash function implemented
    in the c++.
    */
   Hash hash;
   std::vector<bool> bits;
   size_t size;
   size_t max_size;
   int seed;
   size_t num_hash_functions;

   std::vector<size_t> curr_key_2_pos;
};