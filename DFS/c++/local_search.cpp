#include <iostream>     // cout, endl
#include <fstream>      // fstream
#include <vector>
#include <string>
#include <algorithm>    // copy
#include <iterator>     // ostream_operator

#include <boost/tokenizer.hpp>
#include <boost/range/algorithm.hpp>
#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/io.hpp>

#include "utils.h"

using namespace std;
using namespace boost; //range
using namespace boost::numeric;//ublas.matrix, ublas.vector
using namespace boost::numeric::ublas;//matrix

/*
# IMPLEMENTACION DE PALS CON SUS MODIFICACIONES
######################################### REFERENCES ##############################################
#[1] "A New Local Search Algorithm for the DNA Fragment Assembly Problem"
#[2] "An improved problem aware local search algorithm for the DNA fragment assembly problem"
#[3] "A hybrid crow search algorithm for solving the DNA fragment assembly problem"
###################################################################################################

//compile: g++ local_search.cpp utils.h  -lboost_regex
*/

void calculateDeltas(ublas::vector<int> individual, int i, int j, ublas::matrix<int> matrix_w, int& delta_c, int &delta_f){
    //cout<<individual<<endl;
    //cout<<matrix_w<<endl;
    cout<<i<<" "<<j<<endl;
    //cout<<individual[i-1]<<individual[i]<<individual[j]<<individual[j+1]<<endl;
    delta_c = 0;
    delta_f = 0;
    delta_f = delta_f - matrix_w(individual[i-1], individual[i]) - matrix_w(individual[j], individual[j+1]);
    delta_f = delta_f + matrix_w(individual[i-1], individual[j]) + matrix_w(individual[i], individual[j+1]);
    if (matrix_w(individual[i-1], individual[i]) > CUTOFF)
        delta_c = delta_c + 1;
    if (matrix_w(individual[j], individual[j+1]) > CUTOFF)
        delta_c = delta_c + 1;
    if (matrix_w(individual[i-1], individual[j]) > CUTOFF)
        delta_c = delta_c - 1;
    if (matrix_w(individual[i], individual[j+1]) > CUTOFF)
        delta_c = delta_c - 1;
}

void selectMovement(ublas::matrix<int> L, int& i, int& j){
    x = L.size1();
}
/*
def selectMovement(L):
    # get the posible movement with minimun delta_c
    x = len(L)
    L_temp = np.matrix(L)
    delta_c_list = L_temp[:,3]
    min_delta_c = np.amin(delta_c_list)

    L_with_min_delta_c = []
    for i in range(x):
        if L_temp[i,3] == min_delta_c:
            L_with_min_delta_c.append(np.squeeze(np.asarray(L_temp[i,:])))

       
    # get the posible movement with maximun delta_f
    x = len(L_with_min_delta_c)
    L_temp = np.matrix(L_with_min_delta_c)
    delta_f_list = L_temp[:,2]
    max_delta_f = np.amax(delta_f_list)
    
    L_with_max_delta_f = []
    for i in range(x):
        if L_temp[i,2] == max_delta_f:
            L_with_max_delta_f.append(np.squeeze(np.asarray(L_temp[i,:])))

    L_temp = np.matrix(L_with_max_delta_f)
    
    #print(L_temp.shape)   
    #print(L_temp)
    return int(L_temp[0, 0]), int(L_temp[0, 1])*/

ublas::vector<int> PALS(int K, ublas::vector<int> individual, ublas::matrix<int> matrix_w){
    int iterations = 0;
    while (iterations < 3000){
        ublas::matrix<int> L;
        int l_index = 0;
        int delta_c, delta_f;
        for (int i = 1; i < K; i++){
            for (int j = 0; j < K-1; j++){    
                calculateDeltas(individual, i, j, matrix_w, delta_c, delta_f);
                if (delta_c < 0 || (delta_c == 0 && delta_f > 0)){
                    assign_to_matrix(L, l_index, 0, i);
                    assign_to_matrix(L, l_index, 1, j);
                    assign_to_matrix(L, l_index, 2, delta_f);
                    assign_to_matrix(L, l_index, 3, delta_c);
                    l_index++;
                }
            }
        }
        //cout<<L<<endl;
        //break;

        iterations++;
        if (L.size1() > 0){
            //###################################################################################################
            //PALS original [1]
            i, j = selectMovement(L)
            individual = applyMovement(individual, i, j)
        }
        else
            break;
    }

    return individual;
}

int main()
{

    ublas::matrix<int> m = read_csv("../x60189_4/matrix_conservative.csv");
    int num_fragments = m.size1();
    //cout<<m.size1()<<endl;
    
    //create individual
    std::vector<int> individual(num_fragments);
    for (int i = 0; i < individual.size(); i++)
        individual[i] = i;
    range::random_shuffle(individual);

    //individual to boost vector
    ublas::vector<int> individual_t(individual.size());
    std::copy(individual.begin(), individual.end(), individual_t.begin());
    //cout<<individual_t<<endl;
    
    //call PALS
    ublas::vector<int> solution = PALS(num_fragments, individual_t, m);
    //cout<<m<<endl;
    
}