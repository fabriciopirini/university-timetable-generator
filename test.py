from scrap import SIGAA

x, y = SIGAA.retorna_turmas()

d = SIGAA.format(x,y)

SIGAA.save_obj(d, 'ECA')

print(SIGAA.load_obj('ECA'))
