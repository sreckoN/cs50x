#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
int comparator(const void *a, const void *b);
void sort_pairs(void);
bool creates_cyrcle(int a, int b);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < MAX; i++)
    {
        if (candidates[i] == NULL)
        {
            continue;
        }
        int result = strcmp(candidates[i], name);
        if (result == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 1 + i; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    pair_count = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            // Skips the diagonal and already conneced pairs
            if (i == j || preferences[i][j] == preferences[j][i])
            {
                continue;
            }
            
            // Adds a pair
            if (preferences[i][j] > 0 && preferences[i][j] > preferences[j][i])
            {
                pair p;
                p.winner = i;
                p.loser = j;
                pairs[pair_count] = p;
                pair_count++;
            }
        }
    }
    return;
}

// Comparator for qsort
int comparator(const void *a, const void *b)
{
    pair *orderA = (pair *)a;
    pair *orderB = (pair *)b;

    return (preferences[orderB->winner][orderB->loser] - preferences[orderA->winner][orderA->loser]);
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    qsort(pairs, pair_count, sizeof(pair), comparator);
}

// Checks if cycle would be created
bool creates_cyrcle(int a, int b)
{
    if (locked[b][a] == true)
    {
        return true;
    }

    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[i][a] == true)
        {
            return creates_cyrcle(i, b);
        }
    }
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        pair p = pairs[i];
        if (!creates_cyrcle(p.winner, p.loser))
        {
            if (locked[p.loser][p.winner] != true)
            {
                locked[p.winner][p.loser] = true;
            }
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    int winner;
    int rank;

    for (int i = 0; i < candidate_count; i++)
    {
        rank = 0;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i] == false)
            {
                rank++;
            }
        }
        if (rank == candidate_count)
        {
            printf("%s\n", candidates[i]);
        }
    }
}