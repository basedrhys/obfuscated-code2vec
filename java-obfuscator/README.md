# Java Obfuscator

The `java-tool.jar` can be used both for obfuscating a folder of files (folder mode) or splitting (into its methods) and obfuscating an individual `.java` file (file mode)

## Folder Mode

Provide args:
- `-s` - Source directory of java files
- `-t` - Target directory for obfuscated files
- `-pNum` - Partition number we are currently in (i.e. 1, 2, 3, ... up to `pTotal`)
- `-pTotal` - Total number of partitions (e.g. `4`: partition the folder of files into 4 parts)
- `-threads` - How many threads to use for the processing
- `-r` - Optional flag, obfuscate the files using Random obfuscation (default uses type obfuscation)

The `obfs-script.sh` script is the recommended way to use the tool, change the appropriate variables to suit your system and run the script file

## File Mode

In this mode, the script reads in a single file, applies some obfuscation (if any), then prints to standard out each individual method, delineated by `_METHOD_SPLIT_`. This output can then easily be parsed to get a list of all methods in a file.

Args:
- `-o` - Type (__O__)bfuscation
- `-r` - (__R__)andom obfuscation

Usage can be found in `pipeline\ClassPreprocessor.py`


