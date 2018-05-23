# Argument Mining

Visualizing call-outs and targets the content and comments of web documents as marked by annotators.

## Summary
*	Returning a document marked up by an annotator in HTML
*	Comparing annotations (+/-/=) across annotators
*	Grouping annotators (lumpers vs. splitters)
*	Clustering commonalities vs. left overs by ADU type
*	Change annotation format to another type, like TREC or something else standard

## Marking HTML
*	Tags that indicate how many annotators marked that text, making a heat map.
    *	<1>This is a </1><4>callout</4> <2>for the target.</2>
*	Annotating by spans of text by unique Knowtator Target ID and Callout IDs.
    *	[Can then be connected using JavaScript and SVG ](https://gist.github.com/alojzije/11127839)

## Node Networks

## Other

## Technical Issues:
*	Position of CO are off, and get worse as they move along. According to Shawon this may be due to Mac vs. PC issue where the new line characters were handled differently.
*	What is the relationship of callouts to targets? A5 had a single call-out for two targets. Is this a one-to-many? I guess it has to assume possibly many-to-many since a target can be called out by multiple call outs, and a call out can be used for multiple targets.

## Assumptions
*	No annotator creates overlapping targets or callouts.
*	Finding multiples of the same annotation in the text is thrown out.
*	Special characters and other errors

## Next steps:
*	comparing annotators (A to B, A to B to C)
*	walking through a chain of callouts and targets
*	comparing chains/trees between annotators
*	comparing chains/trees between commenters

## Future Work:
*	Transplant the same process on a new set of unseen articles
*	Reformatting the annotations into a different format, or maybe different tagging, such as output as formalized xml, output the core annotation as well as the overlap/difference between annotators
*	You can test how the system automatically adjusts to adding more annotations from different people to define cores, targets, and etc. being able to add annotations into a dump and have it aggregate automatically is a value add to a researcher.

