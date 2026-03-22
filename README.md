# -M3-Actividad-Computando-FIRST-y-FOLLOW

## Formato de entrada esperado

Cada produccion se escribe en una linea con:

NoTerminal -> simbolo simbolo ... | alternativa2

Ejemplo:
E  -> T E'
E' -> + T E' | ε
T  -> F T'
T' -> * F T' | ε
F  -> ( E ) | id

Notas:
- Use ε para epsilon.
- Se permiten varias lineas para el mismo no terminal (las producciones se acumulan).
- El simbolo inicial por defecto es el primer no terminal leido.

## Como ejecutar

1. Abrir terminal en la carpeta del proyecto.
2. Ejecutar: python first_follow.py

## Gramaticas de prueba y resultados esperados

### Caso 1: Expresiones aritmeticas clasicas

Gramatica:
E  -> T E'
E' -> + T E' | ε
T  -> F T'
T' -> * F T' | ε
F  -> ( E ) | id

FIRST esperado:
- FIRST(E)  = { (, id }
- FIRST(E') = { +, ε }
- FIRST(T)  = { (, id }
- FIRST(T') = { *, ε }
- FIRST(F)  = { (, id }

FOLLOW esperado:
- FOLLOW(E)  = { $, ) }
- FOLLOW(E') = { $, ) }
- FOLLOW(T)  = { $, ), + }
- FOLLOW(T') = { $, ), + }
- FOLLOW(F)  = { $, ), *, + }

### Caso 2: Cadena de anulables

Gramatica:
S -> A B
A -> a | ε
B -> b | ε

FIRST esperado:
- FIRST(S) = { a, b, ε }
- FIRST(A) = { a, ε }
- FIRST(B) = { b, ε }

FOLLOW esperado:
- FOLLOW(S) = { $ }
- FOLLOW(A) = { b, $ }
- FOLLOW(B) = { $ }

### Caso 3: Recursion con epsilon

Gramatica:
S -> ( S ) S | ε

FIRST esperado:
- FIRST(S) = { (, ε }

FOLLOW esperado:
- FOLLOW(S) = { $, ) }

### Caso 4: No terminal repetido en varias lineas

Gramatica:
S -> A
A -> a A
A -> ε

FIRST esperado:
- FIRST(S) = { a, ε }
- FIRST(A) = { a, ε }

FOLLOW esperado:
- FOLLOW(S) = { $ }
- FOLLOW(A) = { $ }
