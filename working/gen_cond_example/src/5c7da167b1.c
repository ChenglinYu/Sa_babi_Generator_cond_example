#include <stdlib.h>           // Tag.OTHER
int main()                    // Tag.OTHER
{                             // Tag.OTHER
    char entity_7[86];        // Tag.BODY
    int entity_1;             // Tag.BODY
    int entity_2;             // Tag.BODY
    int entity_0;             // Tag.BODY
    entity_2 = 4;             // Tag.BODY
    entity_0 = 63;            // Tag.BODY
    char entity_6[41];        // Tag.BODY
    entity_1 = 53;            // Tag.BODY
    if(entity_0 < entity_2){  // Tag.BODY
    entity_0 = 39;            // Tag.BODY
    } else {                  // Tag.BODY
    entity_0 = 59;            // Tag.BODY
    }                         // Tag.BODY
    entity_6[entity_0] = '3'; // Tag.BUFWRITE_COND_UNSAFE
    entity_7[entity_1] = 'k'; // Tag.BUFWRITE_TAUT_SAFE
    return 0;                 // Tag.BODY
}                             // Tag.OTHER