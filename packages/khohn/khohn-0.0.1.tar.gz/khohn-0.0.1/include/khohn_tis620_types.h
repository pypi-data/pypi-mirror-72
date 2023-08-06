#ifndef KHOHN_TIS620_TYPES_H
#define KHOHN_TIS620_TYPES_H

#include <stdio.h>
#include <stdlib.h>

/**
 * A type representing text in the Thai-Industrial 620-2533 Standard
 */
typdef unsigned char tis620_t;

#define KHOHN_TIS620_IS_ENG(ch) (((ch) >= 0x20) && ((ch) <= 0x7e))



#endif // KHOHN_TIS620_TYPES_H