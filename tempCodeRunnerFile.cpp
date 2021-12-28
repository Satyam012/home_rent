#include <bits/stdc++.h>
using namespace std;

typedef pair < int, int > PI;

vector < vector < PI > > GRAPH;

// FUNCTION for ADDING EDGES TO GRAPH
void ADDEDGE(int X, int Y, int COST) {
    GRAPH[X].push_back(MAKE_pair(COST, Y));
    GRAPH[Y].push_back(MAKE_pair(COST, X));
}

// GIVES OUTPUT PATH HAVING LOWEST COST
void STEEP_HILL_CLIMB(int SOURCE, int TARGET, int N) {
    vector < bool > VISITED(N, FALSE);
    // MIN HEAP PRIORITY QUEUE
    priority_queue < PI, vector < PI > , greater < PI > > PQ;
    // SORTING IN PQ GETS DONE BY FIRST VALUE OF pair
    PQ.PUSH(MAKE_pair(0, SOURCE));
    int S = SOURCE;
    VISITED[S] = true;
    while (!PQ.EMPTY()) {
        int X = PQ.top().second;
        // DISPLAYING THE PATH HAVING LOWEST COST
        cout << X << " ";
        PQ.POP();
        if (X == TARGET)
            break;

        for (int I = 0; I < GRAPH[X].size(); I++) {
            if (!VISITED[GRAPH[X][I].second]) {
                VISITED[GRAPH[X][I].second] = true;
                PQ.PUSH(MAKE_pair(GRAPH[X][I].FIRST, GRAPH[X][I].second));
            }
        }
    }
}

// DRIVER CODE TO TEST ABOVE METHODS
int MAIN() {
    // NO. OF NODES
    int V = 14;
    GRAPH.resize(V);

    // THE NODES SHOWN IN ABOVE EXAMPLE(BY ALPHABETS) ARE
    // IMPLEMENTED USING intEGERS ADDEDGE(X,Y,COST);
    ADDEDGE(0, 1, 3);
    ADDEDGE(0, 2, 6);
    ADDEDGE(0, 3, 5);
    ADDEDGE(1, 4, 9);
    ADDEDGE(1, 5, 8);
    ADDEDGE(2, 6, 12);
    ADDEDGE(2, 7, 14);
    ADDEDGE(3, 8, 7);
    ADDEDGE(8, 9, 5);
    ADDEDGE(8, 10, 6);
    ADDEDGE(9, 11, 1);
    ADDEDGE(9, 12, 10);
    ADDEDGE(9, 13, 2);

    int SOURCE = 0;
    int TARGET = 6;

    // FUNCTION CALL
    STEEP_HILL_CLIMB(SOURCE, TARGET, V);

    cout << ENDL;

    return 0;
}
