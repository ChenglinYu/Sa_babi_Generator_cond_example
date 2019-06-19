#include <stdlib.h>           // Tag.OTHER
int main()                    // Tag.OTHER
{                             // Tag.OTHER
    int entity_9;             // Tag.BODY
    int entity_5;             // Tag.BODY
    entity_5 = 93;            // Tag.BODY
    int entity_8;             // Tag.BODY
    char entity_6[56];        // Tag.BODY
    entity_8 = 61;            // Tag.BODY
    char entity_1[31];        // Tag.BODY
    entity_9 = 70;            // Tag.BODY
    if(entity_8 < entity_9){  // Tag.BODY
    entity_8 = 66;            // Tag.BODY
    entity_1[entity_5] = 'k'; // Tag.BUFWRITE_TAUT_UNSAFE
    } else {                  // Tag.BODY
    entity_8 = 33;            // Tag.BODY
    }                         // Tag.BODY
    entity_6[entity_8] = '3'; // Tag.BUFWRITE_COND_UNSAFE
    return 0;                 // Tag.BODY
}                             // Tag.OTHER