// The template for class header
#ifndef CLASSES_DataView_H_
#define CLASSES_DataView_H_

#define VDM_CG

#include "Vdm.h"

//include types used in the class
#include "DataView.h"


/* -------------------------------
 *
 * Quotes
 *
 --------------------------------- */ 
 
#ifndef QUOTE_SLAVE
#define QUOTE_SLAVE 109519319
#endif /* QUOTE_SLAVE */

#ifndef QUOTE_MASTER
#define QUOTE_MASTER -1081267614
#endif /* QUOTE_MASTER */



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
#define CLASS_ID_DataView_ID 0

#define DataViewCLASS struct DataView*

// The vtable ids
#define CLASS_DataView__Z4vdm5EI 0
#define CLASS_DataView__Z7vdm5funEI 1

struct DataView
{
	
/* Definition of Class: 'DataView' */
	VDM_CLASS_BASE_DEFINITIONS(DataView);
	 
	
};


/* -------------------------------
 *
 * Constructors
 *
 --------------------------------- */ 
 

	/* DataTypes.vdmpp 1:7 */
	TVP _Z8DataViewEV(DataViewCLASS this_);


/* -------------------------------
 *
 * public access functions
 *
 --------------------------------- */ 
 
	void DataView_const_init();
	void DataView_const_shutdown();
	void DataView_static_init();
	void DataView_static_shutdown();


/* -------------------------------
 *
 * Internal
 *
 --------------------------------- */ 
 

void DataView_free_fields(DataViewCLASS);
DataViewCLASS DataView_Constructor(DataViewCLASS);


#endif /* CLASSES_DataView_H_ */
