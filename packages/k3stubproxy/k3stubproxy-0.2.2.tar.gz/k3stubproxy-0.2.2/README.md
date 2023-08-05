# k3stubproxy

An proxy implementation to be used by embedded c stub implementations

## Stub generation
Use the cli tool k3stubproxy-generate-stub included in this package.

Requirements:
 - Stub functions begin with extern
 - In the code documnetation a parameter is labled in/out in the following style
   - param [in] variableName
   - param [out] variableName


__Example CLI Usage__
```
k3stubproxy-generate-stub -v ../Code/HAL/HAL_*.c --func_prefix HAL_ -o ../Code/HAL/high_level_stub/ --filename_suffix _teststub --file_header defheader.txt --stub_function_definition_out stub_function_definition.json
```


## Other CLI Tools (Version 0.2.1)

* k3stubproxy-generate-target-stub (Generate a python target stub using the stub function definition created by k3stubproxy-generate-stub
* k3stubproxy-analyse-stub-function-definition (Given the stub function definition, show stub functions and used input, output and return types)

## Example usage within C

**C API usage**
```C
#include "Stub_Connector_Interface.h"
...
if initStubConnector(NULL) != 0
{
    // error
    return 1;
}
```

Provide Implementations for the following functions:
```C
PyObject* convert_input_to_python_object(va_list valist, int parameterPos, char* typeString);
int convert_python_object_to_output(va_list valist, int parameterPos, char* typeString, PyObject* outputObject);
```
And include the files Stub_Connector_Implementation.c,Stub_Connector_Interface.h from within k3stubproxy/c_stub and the replace the standard implementation with generated stub when compiling and linking. 


### General Information About Embedding Python Within C


```c
char* phDir = "/some/path/to/a/venv";
printf("INFO: Using virutalenv: %s", phDir);
// This should not be some hard code palth like /home/annoying_user/temp/project123
// For example in some usages of the k3stubproxy this is set dynamically to look
// beside the exe vor the venv

// Note: Need to check return of Py_DecodeLocale is != NULL
Py_SetPythonHome(Py_DecodeLocale(phDir, NULL));

//optional but recommended
wchar_t *program = Py_DecodeLocale("stub_program", NULL);
Py_SetProgramName(program);

Py_Initialize();

// Then any lib within the venv can be used via cpython
PyRun_SimpleString("import k3stubproxy;");
```