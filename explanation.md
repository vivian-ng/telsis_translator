# How does the Telsis language translator work?

## Determining source and target languages when used from the commandline
The script determines whether it is translating from Telsis or to Telsis based on the commandline arguments.

- If Telsis is given as the source language, it is translating from Telsis.
- If Telsis is given as the target language, it is translating to Telsis.
- If any other language is given as the source language, and the target language is not defined, it assumes it is translating to Telsis.
- If any other language is gien as the target language, and the source language is not defined, it assumes it is translating from Telsis.

Note: When used as a library, it is up to the programmer to determine which method (`lang2telsis` or `telsis2lang`) to call.

## Translating from Telsis language
- Telsis alphabet is substituted using the alphabet table to get the source text in Tamil. During this process, names enclosed in backslashes are copied over as they are without being converted.
- The Tamil source text is translated to the required target language.

## Translating to Telsis language
- The source text is preprocessed to find all names. These are then replaced with labels XXX1, XXX2, and so on corresponding to each name. (Note: XXX is used because X is a character that is not substituted when converting between Tamil and Telsis.)
- The processed source text is translated into Tamil.
- The pronunciation of the Tamil text is converted to unaccented characters.
- The Tamil text is then converted to Telsis by substituting using the alphabet table.
- The labels XXX1, XXX2 and so on are replaced with their corresponding names to give the final target text.
