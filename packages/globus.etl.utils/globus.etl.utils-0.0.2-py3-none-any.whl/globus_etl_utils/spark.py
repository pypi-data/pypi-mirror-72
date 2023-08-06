from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *

def rec_ren(
    schema, 
    rename_fn
):
    struct_fields = list()
  
    for field in schema.fields:
        if type(field.dataType) is ArrayType:
            if (type(field.dataType.elementType) is StructType):
                struct_fields.append(
                    StructField(
                        rename_fn(field.name), 
                        ArrayType(rec_ren(field.dataType.elementType, rename_fn)), 
                        field.nullable
                    )
                )
            else:
                struct_fields.append(
                    StructField(
                        rename_fn(field.name), 
                        ArrayType(field.dataType.elementType), 
                        field.nullable
                    )
                )
      
        elif type(field.dataType) is StructType:
            struct_fields.append(
                StructField(
                    rename_fn(field.name), 
                    rec_ren(field.dataType, rename_fn), 
                    field.nullable
                )
            )
      
        else:
            struct_fields.append(
                StructField(
                    rename_fn(field.name), 
                    field.dataType, 
                    field.nullable
                )
            )
  
    return StructType(struct_fields)