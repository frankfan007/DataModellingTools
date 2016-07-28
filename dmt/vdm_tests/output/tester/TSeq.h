// The template for class header
#ifndef CLASSES_TSeq_H_
#define CLASSES_TSeq_H_

#define VDM_CG

#include "Vdm.h"

//include types used in the class
#include "TSeq.h"


/* -------------------------------
 *
 * Quotes
 *
 --------------------------------- */ 
 


/* -------------------------------
 *
 * values / global const
 *
 --------------------------------- */ 
 


/* -------------------------------
 *
 * The class
 *
 --------------------------------- */ 
 

//class id
#define CLASS_ID_TSeq_ID 16

#define TSeqCLASS struct TSeq*

// The vtable ids

struct TSeq
{
	
/* Definition of Class: 'TSeq' */
	VDM_CLASS_BASE_DEFINITIONS(TSeq);
	 
	VDM_CLASS_FIELD_DEFINITION(TSeq,component1);
	VDM_CLASS_FIELD_DEFINITION(TSeq,component2);
	
};


/* -------------------------------
 *
 * Constructors
 *
 --------------------------------- */ 
 

	
	TVP _Z4TSeqEII(TSeqCLASS this_, TVP param_component1, TVP param_component2);


/* -------------------------------
 *
 * public access functions
 *
 --------------------------------- */ 
 
	void TSeq_const_init();
	void TSeq_const_shutdown();
	void TSeq_static_init();
	void TSeq_static_shutdown();


/* -------------------------------
 *
 * Internal
 *
 --------------------------------- */ 
 

void TSeq_free_fields(TSeqCLASS);
TSeqCLASS TSeq_Constructor(TSeqCLASS);



#endif /* CLASSES_TSeq_H_ */