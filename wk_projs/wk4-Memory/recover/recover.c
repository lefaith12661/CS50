#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
    // open memory card
    FILE *inputptr = fopen(argv[1], "r");

    // Check for invalid usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // check for invalid file
    if (inputptr == NULL)
    {
        printf("Forensic image cannot be opened for reading\n");
        return 1;
    }

    // number of bytes in a block
    const int BLOCK_SIZE = 512;

    // buffer
    typedef uint8_t BYTE;
    BYTE buffer[BLOCK_SIZE];

    // counter for number of jpeg image
    int outputcounter = 0;

    // file pointer for recovered images
    FILE *outputptr = NULL;

    // allocate memory for the filename
    char filename[8]; // "000.jpeg\0"

    // found jpeg
    bool found_jpeg = false;

    // repeat until end of card:
    // read inputptr(512 bytes) into a buffer
    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, inputptr) == BLOCK_SIZE)
    {
        // if start of new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            found_jpeg = true;
            // if first JPEG
            if (outputcounter == 0)
            {
                // Start writing (000.jpeg)
                sprintf(filename, "%03i.jpg", outputcounter);
                outputptr = fopen(filename, "w");
                fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, outputptr);
                outputcounter++;
            }
            else
            {
                // close current file
                fclose(outputptr);

                // open new file to continue
                sprintf(filename, "%03i.jpg", outputcounter); // create filename 000.jpeg
                outputptr = fopen(filename, "w"); // open to write
                fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, outputptr); // write into outputptr
                outputcounter++;
            }
        }
        else
        {
            // if already found jpeg
            if (found_jpeg)
            {
                // keep writing to jpeg
                fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, outputptr);
            }
        }
    }
    // close any remaining files
    fclose(inputptr);
    fclose(outputptr);
    return 0;
}