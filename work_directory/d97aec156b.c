#include <stdlib.h>           // Tag.OTHER
int main()                    // Tag.OTHER
{                             // Tag.OTHER
    int entity_8;             // Tag.BODY
    int entity_1;             // Tag.BODY
    char entity_7[45];        // Tag.BODY
    entity_1 = 27;            // Tag.BODY
    entity_8 = 74;            // Tag.BODY
    if(entity_8 < entity_1){  // Tag.BODY
    entity_8 = 64;            // Tag.BODY
    } else {                  // Tag.BODY
    entity_8 = 17;            // Tag.BODY
    }                         // Tag.BODY
    entity_7[entity_8] = 'i'; // Tag.BUFWRITE_COND_SAFE
    return 0;                 // Tag.BODY
}                             // Tag.OTHER