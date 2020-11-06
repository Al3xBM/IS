Ordinea in care programele trebuie rulate este:
	1. keyManager
	2. nodeB
	3. nodeA

Dupa ce ati rulat programele, nodeA este singurul care necesita input aditional, 
pt a specifica modul de comunicare: cbc sau ofb. Deoarece sincronizarea programelor
nu era mandatorie, am creat o fereastra de 7 secunde cu ajutorul unui sleep in care
puteti introduce modul de comunicare dorit. Daca au trecut 7 secunde si nu ati ales
modul de comunicare, nodeB nu se va mai putea conecta la nodeA si programele vor
trebui rulate din nou