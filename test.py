from scrap import SIGAA
import GenericDBConnection

x, y = SIGAA.retorna_turmas()

d = SIGAA.format(x,y)

SIGAA.save_obj(d, 'ECA')

print(SIGAA.load_obj('ECA'))

CONN = repository.GenericDBConnection.Database()

