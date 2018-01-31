/**
 * recover.c
 *
 * Computer Science 50
 * Problem Set 4
 *
 * Recovers JPEGs from a forensic image.
 */
 
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define FAT_SIZE 512

int main (void)
{
    // TODO Open memory card file
	FILE *inFile = fopen("card.raw", "r");
    if (inFile == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    
    FILE *outFile;
    outFile = NULL;
    
    char jpegMagicNumber[4] = {0xff, 0xd8, 0xff, 0xe0};
    char block[FAT_SIZE];
    int jpgName = 0;
    
    for (;;)
    {
        for (int i = 0; i < FAT_SIZE; i++)
            fread(&block[i], sizeof(char), 1, inFile);
            
        // TODO Find beginning of jpg
        if (memcmp(block, jpegMagicNumber, 4) == 0)
        {
            if (outFile != NULL)
                fclose(outFile);
                
            // TODO Open a new jpg    
            char jpgFile[4];
            sprintf(jpgFile, "%03d.jpg", jpgName++);

            if ((outFile = fopen(jpgFile, "w")) == NULL)
            {
                printf("Could not write file.\n");
                return 2;
            }
            
            // TODO Write 512 bytes until new jpg is found
            fwrite(&block[0], FAT_SIZE * sizeof(char), 1, outFile);
        } else if (outFile != NULL) {
            fwrite(&block[0], FAT_SIZE * sizeof(char), 1, outFile);
        }
        
        // TODO Detect end of file
        if (feof(inFile))
        {
            fclose(outFile);
            break;
        }
    }
 
    fclose(inFile);
    return 0;
}