/** Grammars always start with a grammar header. This grammar is called
* ArrayInit and must match the filename: ArrayInit.g4
*/
grammar ArrayInit;
/** A rule called init that matches comma-separated values between {...}. */
init : '{' value (',' value)* '}' ; // must match at least one value

/** A value can be either a nested array/struct or a simple integer (INT) */
value : init
| INT
;

// parser rules start with lowercase letters, lexer rules with uppercase
INT : [0-9]+ ; // Define token INT as one or more digits
WS : [ \t\r\n]+ -> skip ; // Define whitespace rule, toss it out

/*
REGLAS A IMPLEMENTAR <:

VAR -> id VAR1
VAR1 -> = VAR2
VAR1 -> [ EA ] = EA
VAR1 -> ( PR )
VAR1 -> . size = VAR2
VAR2 -> Get next input
VAR2 -> EA
PR -> EA PRA
PR -> epsilon
PRA -> , EA PRA
PRA -> epsilon
*/