from scrap import SIGAA

x, y = SIGAA.retorna_turmas('ECO', '2018', '1')

d = SIGAA.format(x, y)

for item, k in d.items():
        print(': '.join([str(len(k))]))
