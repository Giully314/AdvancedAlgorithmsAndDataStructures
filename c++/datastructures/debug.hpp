#pragma once 

// #define DEBUG

#ifdef DEBUG
#define LOG(x)         std::cout << x << std::endl
#define ENTER(x)       std::cout << "enter " << x << std::endl
#define EXIT(x)        std::cout << "exit " << x << std::endl

#else
#define LOG(x)        
#define ENTER(x)      
#define EXIT(x)        
#endif