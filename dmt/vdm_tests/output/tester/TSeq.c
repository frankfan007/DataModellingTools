// The template for class
#include "TSeq.h"
#include <stdio.h>
#include <string.h>


/* -------------------------------
 *
 * Memory management methods
 *
 --------------------------------- */

void TSeq_free_fields(struct TSeq *this)
{
		vdmFree(this->m_TSeq_component1);
			vdmFree(this->m_TSeq_component2);
	}

static void TSeq_free(struct TSeq *this)
{
	--this->_TSeq_refs;
	if (this->_TSeq_refs < 1)
	{
		TSeq_free_fields(this);
		free(this);
	}
}


/* -------------------------------
 *
 * Member methods 
 *
 --------------------------------- */
 

 void TSeq_const_init()	{

return ;
}



 void TSeq_const_shutdown()	{

return ;
}



 void TSeq_static_init()	{

return ;
}



 void TSeq_static_shutdown()	{

return ;
}




/* -------------------------------
 *
 * VTable
 *
 --------------------------------- */
 
// VTable for this class
 static  struct VTable VTableArrayForTSeq  [0]  ;

// Overload VTables


/* -------------------------------
 *
 * Internal memory constructor
 *
 --------------------------------- */
 
 
TSeqCLASS TSeq_Constructor(TSeqCLASS this_ptr)
{

	if(this_ptr==NULL)
	{
		this_ptr = (TSeqCLASS) malloc(sizeof(struct TSeq));
	}

	if(this_ptr!=NULL)
	{
	
			
		// TSeq init
		this_ptr->_TSeq_id = CLASS_ID_TSeq_ID;
		this_ptr->_TSeq_refs = 0;
		this_ptr->_TSeq_pVTable=VTableArrayForTSeq;

				this_ptr->m_TSeq_component1= NULL ;
						this_ptr->m_TSeq_component2= NULL ;
			}

	return this_ptr;
}

// Method for creating new "class"
static TVP new()
{
	TSeqCLASS ptr=TSeq_Constructor(NULL);

	return newTypeValue(VDM_CLASS, (TypedValueType)
			{	.ptr=newClassValue(ptr->_TSeq_id, &ptr->_TSeq_refs, (freeVdmClassFunction)&TSeq_free, ptr)});
}



/* -------------------------------
 *
 * Public class constructors
 *
 --------------------------------- */ 
 


 TVP _Z4TSeqEII(TSeqCLASS this, TVP param_component1, TVP param_component2)	{

 TVP __buf = NULL;

if ( this == NULL )
	
	{

__buf = new();

this = TO_CLASS_PTR(__buf, TSeq);
}
;

this->m_TSeq_component1 = param_component1;

this->m_TSeq_component2 = param_component2;

return __buf;
}




/* -------------------------------
 *
 * Global class fields
 *
 --------------------------------- */
 
// initialize globals - this is done last since they are declared in the header but uses init functions which are printet in any order
		
