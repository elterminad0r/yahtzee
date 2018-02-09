#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <signal.h>

#include <sys/time.h>

#define BETWEEN_PRINT 500000

#define MAX_TRIALS 10000000

unsigned char target, curr_num, mode, mode_count, i, roll, dice;
unsigned char rolls[6];

unsigned long turns, total, trials;

struct timeval stop, start;
double seconds_taken;

bool verbose;

void interrupt_handler(int dummy) {
    if (!verbose) {
        printf("%d,%.9f\n", dice, (double)total / trials);
    }
    exit(EXIT_SUCCESS);
}

int main(int argc, char **argv) {
    signal(SIGINT, interrupt_handler);

    verbose = true;

    if (argc < 2) {
        dice = 5;
    } else {
        sscanf(argv[1], "%hhu", &dice);

        if (argc > 2) {
            if (strcmp(argv[2], "silent") == 0) {
                verbose = false;
            }
        }
    }

    if (verbose) {
        printf("using %d dice\n", dice);
    }

    gettimeofday(&start, NULL);

    total = 0;

    for (trials = 1;; trials++) {
        curr_num = 0;

        for (turns = 0; curr_num != dice; turns++) {

            for (i = 0; i < 6; i++) {
                rolls[i] = 0;
            }

            mode_count = 0;
            
            for (i = 0; i < dice - curr_num; i++) {
                roll = rand() % 6;

                rolls[roll]++;
                if (rolls[roll] > mode_count) {
                    mode = roll;
                    mode_count = rolls[roll];
                }
            }

            if (mode != target && mode_count > curr_num) {
                target = mode;
                curr_num = mode_count;
            } else {
                curr_num += rolls[target];
            }
        }

        total += turns;

        if (trials == MAX_TRIALS) {
            interrupt_handler(0);
        }

        if (trials % BETWEEN_PRINT == 0) {
            if (verbose) {
                gettimeofday(&stop, NULL);
                seconds_taken = (stop.tv_sec * 1000000 + stop.tv_usec - start.tv_sec * 1000000 - start.tv_usec) / 1000000.0;

                printf("\raverage %.9f - %.2e trials at %8.3fs <=> %.2e/s",
                            (double)total / trials, (double)trials, seconds_taken, trials / seconds_taken);
            }
            fflush(stdout);
        }
    }
    return 0;
}
