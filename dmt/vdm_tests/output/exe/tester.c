#include <stdio.h>
#include "Vdm_ASN1_Types.h"

int main(){
     
    printf("\n--\tArray of Bool\n");
    printf("--\tASN Source Bool Array\n");
    asn1SccMSeq s_ab = (asn1SccMSeq) { .arr= {FALSE, FALSE, TRUE, FALSE, FALSE}};    
    TVP out_seq;

    Convert_MSeq_from_ASN1SCC_to_VDM(&out_seq, &s_ab);
    
/*
 * 
    printf("--\t\tDest VDM Array: ");
    for (int i=1; i <= len->value.intVal; i++){
        TVP t_i = newInt(i);
        TVP t = vdmSeqIndex(d, t_i);
        printf("%d ", t->value.boolVal);
    }
    printf("\n");

  */ 
    
    
    return 0;

}
