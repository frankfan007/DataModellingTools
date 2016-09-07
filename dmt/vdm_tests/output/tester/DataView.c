// The template for class
#include "DataView.h"
#include <stdio.h>
#include <string.h>


/* -------------------------------
 *
 * Memory management methods
 *
 --------------------------------- */

void DataView_free_fields(struct DataView *this)
{
}

static void DataView_free(struct DataView *this)
{
	--this->_DataView_refs;
	if (this->_DataView_refs < 1)
	{
		DataView_free_fields(this);
		free(this);
	}
}


/* -------------------------------
 *
 * Member methods 
 *
 --------------------------------- */
 

 void DataView_const_init()	{

return ;
}



 void DataView_const_shutdown()	{

return ;
}



 void DataView_static_init()	{

return ;
}



 void DataView_static_shutdown()	{

return ;
}




/* -------------------------------
 *
 * VTable
 *
 --------------------------------- */
 
// VTable for this class
 static  struct VTable VTableArrayForDataView  [0]  ;

// Overload VTables


/* -------------------------------
 *
 * Internal memory constructor
 *
 --------------------------------- */
 
 
DataViewCLASS DataView_Constructor(DataViewCLASS this_ptr)
{

	if(this_ptr==NULL)
	{
		this_ptr = (DataViewCLASS) malloc(sizeof(struct DataView));
	}

	if(this_ptr!=NULL)
	{
	
			
		// DataView init
		this_ptr->_DataView_id = CLASS_ID_DataView_ID;
		this_ptr->_DataView_refs = 0;
		this_ptr->_DataView_pVTable=VTableArrayForDataView;

	}

	return this_ptr;
}

// Method for creating new "class"
static TVP new()
{
	DataViewCLASS ptr=DataView_Constructor(NULL);

	return newTypeValue(VDM_CLASS, (TypedValueType)
			{	.ptr=newClassValue(ptr->_DataView_id, &ptr->_DataView_refs, (freeVdmClassFunction)&DataView_free, ptr)});
}



/* -------------------------------
 *
 * Public class constructors
 *
 --------------------------------- */ 
 

/* DataTypes.vdmpp 1:7 */
 TVP _Z8DataViewEV(DataViewCLASS this)	{

 TVP __buf = NULL;

if ( this == NULL )
	
	{

__buf = new();

this = TO_CLASS_PTR(__buf, DataView);
}
;

return __buf;
}




/* -------------------------------
 *
 * Global class fields
 *
 --------------------------------- */
 
// initialize globals - this is done last since they are declared in the header but uses init functions which are printet in any order

