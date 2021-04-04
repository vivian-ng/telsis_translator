# How does the Telsis language translator work?

The Telsis language (called Nunkish by fans because the first word that was decoded was 'nunki' or 'thank you') is constructed by:

1. Translating the source text from Japanese into English
2. Translating the English text into an undisclosed language
3. Using a substitution cipher to swap certain letters; names are not processed by the cipher

This process was shared by Suzuki Takaaki at a [movie screening event](http://violet-evergarden.jp/special/greeting03/) that was held on December 3, 2020 at Shinjuku Piccadilly Cinema (read about the event [here](https://teck78.blogspot.com/2020/12/production-staff-event-at-screening-of.html)). The undisclosed language has been determined by fans as Tamil, as explained in this [Reddit post](https://www.reddit.com/r/anime/comments/88bbob/violet_evergarden_alphabet_and_language_part_2/). This means that we can create our own text in the Telsis language by:

1. Translating the source text into Tamil
2. Converting the Tamil script by denoting its pronunciation using unaccented characters
3. Using a substitution cipher to swap certain letters; names are not processed by the cipher

The above process can also be reversed to translate text in the Telsis language into the required real-world language. However, do note that because of the way language translations work, we do not have a one-to-one mapping between Telsis and a real-world language. Which means that when we translate a sentence from, say, English into Telsis, and then translate that same Telsis sentence back into English, we may not end up with the exact English sentence that we started with.

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
- The source text is preprocessed to find all names. These are then replaced with labels `XXX1`, `XXX2`, and so on corresponding to each name. (Note: `XXX` is used because `X` is a character that is not substituted when converting between Tamil and Telsis.)
- The processed source text is translated into Tamil.
- The pronunciation of the Tamil text is converted to unaccented characters.
- The Tamil text is then converted to Telsis by substituting using the alphabet table.
- The labels `XXX1`, `XXX2` and so on are replaced with their corresponding names to give the final target text.
