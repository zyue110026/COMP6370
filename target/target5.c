#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void read_elements(FILE *handle, int *buf, unsigned int byte_count) {
	/***********************************************************************
	* Read the byte-count bytes bytes from the file and store in the buffer.
	*
	* If an error is encountered while trying to read the file, stop reading
	* and ignore the error. The buffer may be partially filled upon return.
	***********************************************************************/
	unsigned int i;
	for (i=0; i < byte_count; i++) {
		if (fread(&buf[i], sizeof(unsigned int), 1, handle) < 1) {
			break;
		}
	}
}

void read_file(char *filename) {
	/***********************************************************************
	* Open the input file.
	***********************************************************************/
	FILE *handle = fopen(filename, "rb");
	if (!handle) {
		fprintf(stderr, "Error: Cannot open file\n");
		return;
	}

	/***********************************************************************
	* Read the byte-count at the start of the file.
	***********************************************************************/
	unsigned int byte_count;
	fread(&byte_count, sizeof(unsigned int), 1, handle);

	/***********************************************************************
	* Allocate the buffer based on the byte-count read from the file.
	***********************************************************************/
	unsigned int *buf = alloca(byte_count * sizeof(unsigned int));
	if (!buf) {
		return;
	}

	read_elements(handle, buf, byte_count);
}

int _main(int argc, char *argv[])
{
	if (argc != 2) {
		fprintf(stderr, "Error: Need an input filename\n");
		return 1;
	}
	read_file(argv[1]);
	return 0;
}
