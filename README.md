# Python alexa

Název je potřeba brát s velkou rezervou

Takový voice assistant, využívá knihovny speech_recognition pro zaznamenávání hlasu a gtts pro odpovědi

Je potřeba na ni mluvit v angličtině, srozumitelně a pomalu, ale ne zas moc

Reaguje pouze na 'hey Alexa'

### Zatím umí:

1. Říct datum, když v textu zaznamená 'date'
2. Zastavit program, když zaznamená 'stop'
3. Velmi jednoduché matematické úkony, když v textu zaznamená 'what is' a integer (sčítání, odčítání, dělení; pouze s dvěma čísly, z nichž jedno musí být integer)
4. Generovat náhodná čísla (defaultně 1-100, nebo v zadaném rozsahu), když zaznamená 'random' a 'number' v textu
5. Setnout timer na určitý čas když zaznamená 'timer' v textu
6. Zadávání jednoduchého kvízu, když v textu zaznamená 'trivia'(otázky a oodpovědi jsou napsány přímo v kódu, v dictionary)
7. Odpovídání na některé otázky kladené uživatelem, když zaznamená 'favorite' (Co je tvoje oblíbené jídlo ap.)
8. Říkat vtipy, když zaznamená 'joke'(Taky v dictionary přímo v kódu)