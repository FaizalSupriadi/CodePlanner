# CodePlanner
Gekozen taal: Eigen Taal(CodePlanner)

# Turing-compleet:
Uit een stackoverflow post van Ixrec heeft hij heuristics beschreven die een taal als Turing-compleet kan zien:

https://softwareengineering.stackexchange.com/questions/315919/how-is-brainfuck-turing-complete#:~:text=Conditional%20branching%20is,an%20infinite%20loop.

Mijn taal ondersteund Conditional branching zoals if, else en elif. Dit is mogelijk in alle Turing-complete talen. 

Daarnaast ondersteund deze taal while loops, for loops en ook recursie, waardoor er oneindig veel iteraties of willekeurig veel eindige iteraties zijn. 

Zoals ixrec zegt: "Most Brainfuck implementations arguably fail the memory criteria, but that argument applies to all programming languages since in the real world computers always have finite memory."
Mijn taal heeft dus ook het probleem dat computers maar een eindig geheugen hebben, maar zoals gezegd kan dit argument op alle programmeer talen gelden.
Verder kan deze taal menselijke input binnenkrijgen en deze taal kan ook niet het halt probleem oplossen doordat er een paradox onstaat.

Doordat mijn taal deze criteria bevat, kan ik dus zeggen dat deze taal Turing Compleet is.

# Taal Gebruik
Om de voorbeelden te runnen moet shell.py gestart worden, daarna moet men een pad naam geven van het gewenste file. bv: "python ATP/shell.py" en dan bijvoorbeeld RUN("for_loop.traffic"). Met PRINT() kan men dan variabelen etc lezen.

# Must Haves

For Loops Voorbeeld: [for_loop.traffic] - [Hele file]

While Loops Voorbeeld: [while_loop.traffic] - [Hele file]

Classes met inheritance: bijvoorbeeld [myParser.py] - [7 - 136]

Object-printing voor elke class: [ja]

Decorator: functiedefinitie op [myClock] - [hele file], toegepast op [shell.py] - [31]

Type-annotatie: Haskell-stijl in comments: [nee]; Python-stijl in functiedefinities: [ja]

Minstens drie toepassingen van hogere-orde functies:

1. [myLexer.py] - [178]: Gebruik van filter om None weg te filteren

2. [myParser] - [146]: Functie 

3. [myParser] - [523]

4. [myParser] - [533]

# Interpreter-functionaliteit Must-have:

Functies: [meer per file]

Functie-parameters kunnen aan de interpreter meegegeven worden door: Het is mogelijk om in de command line te schrijven. Om een functie te roepen moet men de functie naam met de parameters invullen bv: functie(args)

Functies kunnen andere functies aanroepen: zie voorbeeld [excercises\even_odd.traffic] - [8]

Functie resultaat wordt op de volgende manier weergegeven: Er is een ingebouwde print functie die gebruikt moet worden om het resultaat te lezen op de command line. Daaruit komt: PRINT: value.

Interpreter-functionaliteit (should/could-have):

[PRINT functie] geïmplementeerd door middel van de volgende functies:  a) [statement_keywords] in [myParser] op regel [173]
b) [PrintNode] in [myParser] op regel [136] c) [visit_PrintNode] in [myInterpreter] op regel [357]


[Comments support in taal] geïmplementeerd door middel van de volgende functies: a) [skip_comment] in [myLexer] op regel [180]

[Extra functionaliteit overlegd met docent, goedkeuring: datum e-mail; overeengekomen max. aantal punten: X]
# AST
![image](https://user-images.githubusercontent.com/43231255/136706440-da27e8c7-68fd-41ca-ba8e-bfa8cc78feb9.png)
# LANGUAGE


## Symbols
De + - * / kunnen nog wel gebruikt worden met die tekens, andere symbolen niet.

'+' = and

'-' = returns

'*' = shortcuts

'/' = ghostrides

'<' = less

'>' = more

'==' = equals

'=' = travels

'!=' = travels cancelled

'!' = NOT

## Keywords
false = RED

true = GREEN

return = DESTINATION

if = TRAFFIC

elif = BYPASS

else = FLEE

then = GPS

end = REFUEL

def = ROUTE

var = VEHICLE

for = DRIVING

while = SPEEDING
