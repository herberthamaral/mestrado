import random
from pontes import pontes, estagios, executa
OSES = (
    (400001,'A','CV02','','','CL03'),
    (400011,'A','CV01','FPA02','RH01','CL03'),
    (400021,'B','CV02','FPA01','','CC02'),
    (400031,'C','CV01','','','CL15'),
    (400041,'B','CV02','FPA01','','CC02'),
    (400051,'A','CV01','FPA02','','CC01'),
    (400061,'B','CV02','FPA01','','CC02'),
    (400071,'A','CV01','FPA02','','CC01'),
    (400081,'A','CV02','FPA01','','CC02'),
    (400091,'A','CV01','FPA02','','CC01'),
    (400101,'C','CV02','','','CL11'),
    (400111,'A','CV01','FPA01','','CC02'),
    (400121,'A','CV02','FPA01','','CC02'),
    (400131,'A','CV01','FPA02','','CC01'),
    (400141,'A','CV02','FPA02','','CC01'),
    (400151,'A','CV01','FPA02','','CC01'),
    (400161,'A','CV02','FPA02','','CC01'),
    (400171,'F','CV02','RH01','','CL21'),
    (410001,'A','CV01','','','CL03'),
    (410011,'A','CV02','FPA02','RH01','CL03'),
    (410021,'B','CV01','FPA01','','CC02'),
    (410031,'C','CV02','','','CL15'),
    (410041,'B','CV01','FPA01','','CC02'),
    (410051,'A','CV02','FPA02','','CC01'),
    (410061,'B','CV01','FPA01','','CC02'),
    (410071,'A','CV02','FPA02','','CC01'),
    (410081,'A','CV01','FPA01','','CC02'),
    (410091,'A','CV02','FPA02','','CC01'),
    (410101,'C','CV01','','','CL11'),
    (410111,'A','CV02','FPA01','','CC02'),
    (410121,'A','CV01','FPA01','','CC02'),
    (410131,'A','CV02','FPA02','','CC01'),
    (410141,'A','CV01','FPA02','','CC01'),
    (410151,'A','CV02','FPA02','','CC01'),
    (410161,'A','CV01','FPA02','','CC01'),
    (410171,'F','CV01','RH01','','CL21'), #modificado
    (410181,'A','CV02','FPA02','RH01','CL03'),
    (400191,'B','CV01','FPA01','','CC02'),
    (400201,'C','CV02','','','CL15'),
    (400211,'B','CV01','FPA01','','CC02'),
    (400221,'A','CV02','FPA02','','CC01'),
    (400231,'B','CV01','FPA01','','CC02'),
    (400241,'A','CV02','FPA02','','CC01'),
    (400251,'A','CV01','FPA01','','CC02'),
    (400261,'A','CV02','FPA02','','CC01'),
    (400271,'C','CV01','','','CL11'),
    (400281,'A','CV02','FPA01','','CC02'),
    (400291,'A','CV01','FPA01','','CC02'),
    (400301,'A','CV02','FPA02','','CC01'),
    (400311,'A','CV01','FPA02','','CC01'),
    (400321,'A','CV02','FPA02','','CC01'),
    (400331,'A','CV01','FPA02','','CC01'),
    (400341,'F','CV01','RH01','','CL21'), #modificado
    (400351,'A','CV02','FPA02','RH01','CL03'),
    (400361,'B','CV01','FPA01','','CC02'),
    (400371,'C','CV02','','','CL15'),
    (400381,'C','CV01','FPA01','','CC02'),
    (400391,'A','CV02','FPA02','','CC01'),
    (400401,'C','CV01','FPA01','','CC02'),
    (400411,'A','CV02','FPA02','','CC01'),
    (400421,'A','CV01','FPA01','','CC02'),
    (400431,'A','CV02','FPA02','','CC01'),
    (400441,'C','CV01','','','CL11'),
    (400451,'A','CV02','FPA01','','CC02'),
    (400461,'A','CV01','FPA01','','CC02'),
    (400471,'A','CV02','FPA02','','CC01'),
    (400481,'A','CV01','FPA02','','CC01'),
    (400491,'A','CV02','FPA02','','CC01'),
    (400501,'A','CV01','FPA02','','CC01'),
    (400511,'F','CV01','RH01','','CL21'),
    (400521,'A','CV02','FPA02','RH01','CL03'),
    (400531,'C','CV01','FPA01','','CC02'),
    (400541,'C','CV02','','','CL15'),
    (400551,'C','CV01','FPA01','','CC02'),
    (400561,'A','CV02','FPA02','','CC01'),
    (400571,'D','CV01','FPA01','','CC02'),
    (400581,'A','CV02','FPA02','','CC01'),
    (400591,'A','CV01','FPA01','','CC02'),
    (400601,'A','CV02','FPA02','','CC01'),
    (400611,'C','CV01','','','CL11'),
    (400621,'A','CV02','FPA01','','CC02'),
    (400631,'A','CV01','FPA01','','CC02'),
    (400641,'A','CV02','FPA02','','CC01'),
    (400651,'A','CV01','FPA02','','CC01'),
    (400661,'A','CV02','FPA02','','CC01'),
    (400671,'A','CV01','FPA02','','CC01'),
    (400681,'F','CV01','RH01','','CL21'), #modificado
    (400691,'A','CV02','FPA02','RH01','CL03'),
    (400701,'D','CV01','FPA01','','CC02'),
    (400711,'C','CV02','','','CL15'),
    (400721,'D','CV01','FPA01','','CC02'),
    (400731,'A','CV02','FPA02','','CC01'),
    (400741,'D','CV01','FPA01','','CC02'),
    (400751,'A','CV02','FPA02','','CC01'),
    (400761,'A','CV01','FPA01','','CC02'),
    (400771,'A','CV02','FPA02','','CC01'),
    (400781,'C','CV01','','','CL11'),
    (400791,'A','CV02','FPA01','','CC02'),
    (400801,'A','CV01','FPA01','','CC02'),
    (400811,'A','CV02','FPA02','','CC01'),
    (400821,'A','CV01','FPA02','','CC01'),
    (400831,'A','CV02','FPA02','','CC01'),
    (400841,'A','CV01','FPA02','','CC01'),
    (400851,'F','CV01','RH01','','CL21'), #modificado
    (400861,'A','CV02','FPA02','RH01','CL03'),
    (400871,'E','CV01','FPA01','','CC02'),
    (400881,'C','CV02','','','CL15'),
    (400891,'E','CV01','FPA01','','CC02'),
    (400901,'A','CV02','FPA02','','CC01'),
    (400911,'E','CV01','FPA01','','CC02'),
    (400921,'A','CV02','FPA02','','CC01'),
    (400931,'A','CV01','FPA01','','CC02'),
    (400941,'A','CV02','FPA02','','CC01'),
    (400951,'C','CV01','','','CL11'),
    (400961,'A','CV02','FPA01','','CC02'),
    (400971,'A','CV01','FPA01','','CC02'),
    (400981,'A','CV02','FPA02','','CC01'),
    (400991,'A','CV01','FPA02','','CC01'),
    (401001,'A','CV02','FPA02','','CC01'),
    (401011,'A','CV01','FPA02','','CC01'),
    (401021,'F','CV01','RH01','','CL21'), #modificado
    (401031,'A','CV02','FPA02','RH01','CL03'),
    (401041,'E','CV01','FPA01','','CC02'),
    (401051,'C','CV02','','','CL15'),
    (401061,'E','CV01','FPA01','','CC02'),
    (401071,'A','CV02','FPA02','','CC01'),
    (401081,'E','CV01','FPA01','','CC02'),
    (401091,'A','CV02','FPA02','','CC01'),
    (401101,'A','CV01','FPA01','','CC02'),
    (401111,'A','CV02','FPA02','','CC01'),
    (401121,'C','CV01','','','CL11'),
    (401131,'A','CV02','FPA01','','CC02'),
    (401141,'A','CV01','FPA01','','CC02'),
    (401151,'A','CV02','FPA02','','CC01'),
    (401161,'A','CV01','FPA02','','CC01'),
    (401171,'A','CV02','FPA02','','CC01'),
    (401181,'A','CV01','FPA02','','CC01'),
    (401191,'F','CV01','RH01','','CL21'), #modificado
    (401201,'A','CV02','FPA02','RH01','CL03'),
    (401211,'F','CV01','FPA01','','CC02'),
    (401221,'C','CV02','','','CL15'),
    (401231,'F','CV01','FPA01','','CC02'),
    (401241,'A','CV02','FPA02','','CC01'),
    (401251,'F','CV01','FPA01','','CC02'),
    (401261,'A','CV02','FPA02','','CC01'),
    (401271,'A','CV01','FPA01','','CC02'),
    (401281,'A','CV02','FPA02','','CC01'),
    (401291,'C','CV01','','','CL11'),
    (401301,'A','CV02','FPA01','','CC02'),
    (401311,'A','CV01','FPA01','','CC02'),
    (401321,'A','CV02','FPA02','','CC01'),
    (401331,'A','CV01','FPA02','','CC01'),
    (401341,'A','CV02','FPA02','','CC01'),
    (401351,'A','CV01','FPA02','','CC01'),
    (401361,'F','CV01','RH01','','CL21'), #modificado
    (401371,'A','CV02','FPA02','RH01','CL03'),
    (401381,'F','CV01','FPA01','','CC02'),
    (401391,'C','CV02','','','CL15'),
    (401401,'F','CV01','FPA01','','CC02'),
    (401411,'A','CV02','FPA02','','CC01'),
    (401421,'F','CV01','FPA01','','CC02'),
    (401431,'A','CV02','FPA02','','CC01'),
    (401441,'A','CV01','FPA01','','CC02'),
    (401451,'A','CV02','FPA02','','CC01'),
    (401461,'C','CV01','','','CL11'),
    (401471,'A','CV02','FPA01','','CC02'),
    (401481,'A','CV01','FPA01','','CC02'),
    (401491,'A','CV02','FPA02','','CC01'),
    (401501,'A','CV01','FPA02','','CC01'),
    (401511,'A','CV02','FPA02','','CC01'),
    (401521,'A','CV01','FPA02','','CC01'),
    (401531,'F','CV01','RH01','','CL21'), # modificado
    (401541,'A','CV02','FPA02','RH01','CL03'),
    (401551,'G','CV01','FPA01','','CC02'),
    (401561,'C','CV02','','','CL15'),
    (401571,'H','CV01','FPA01','','CC02'),
    (401581,'A','CV02','FPA02','','CC01'),
    (401591,'H','CV01','FPA01','','CC02'),
    (401601,'A','CV02','FPA02','','CC01'),
    (401611,'A','CV01','FPA01','','CC02'),
    (401621,'A','CV02','FPA02','','CC01'),
    (401631,'C','CV01','','','CL11'),
    (401641,'A','CV02','FPA01','','CC02'),
    (401651,'A','CV01','FPA01','','CC02'),
    (401661,'A','CV02','FPA02','','CC01'),
    (401671,'A','CV01','FPA02','','CC01'),
    (401681,'A','CV02','FPA02','','CC01'),
    (401691,'A','CV01','FPA02','','CC01'),
    (401701,'F','CV01','RH01','','CL21'), #modificado
    (401711,'A','CV02','FPA02','RH01','CL03'),
    (401721,'H','CV01','FPA01','','CC02'),
    (401731,'C','CV02','','','CL15'),
    (401741,'H','CV01','FPA01','','CC02'),
    (401751,'A','CV02','FPA02','','CC01'),
    (401761,'H','CV01','FPA01','','CC02'),
    (401771,'A','CV02','FPA02','','CC01'),
    (401781,'A','CV01','FPA01','','CC02'),
    (401791,'A','CV02','FPA02','','CC01'),
    (401801,'C','CV01','','','CL11'),
    (401811,'A','CV02','FPA01','','CC02'),
    (401821,'A','CV01','FPA01','','CC02'),
    (401831,'A','CV02','FPA02','','CC01'),
    (401841,'A','CV01','FPA02','','CC01'),
    (401851,'A','CV02','FPA02','','CC01'),
    (401861,'A','CV01','FPA02','','CC01'),
    (401871,'F','CV01','RH01','','CL21'), # modificado
    (401881,'A','CV02','FPA02','RH01','CL03'),
    (401891,'I','CV01','FPA01','','CC02'),
    (401901,'C','CV02','','','CL15'),
    (401911,'I','CV01','FPA01','','CC02'),
    (401921,'A','CV02','FPA02','','CC01'),
    (401931,'I','CV01','FPA01','','CC02'),
    (401941,'A','CV02','FPA02','','CC01'),
    (401951,'A','CV01','FPA01','','CC02'),
    (401961,'A','CV02','FPA02','','CC01'),
    (401971,'C','CV01','','','CL11'),
    (401981,'A','CV02','FPA01','','CC02'),
    (401991,'A','CV01','FPA01','','CC02'),
    (402001,'A','CV02','FPA02','','CC01'),
    (402011,'A','CV01','FPA02','','CC01'),
    (402021,'A','CV02','FPA02','','CC01'),
    (402031,'A','CV01','FPA02','','CC01'),
    (402041,'F','CV01','RH01','','CL21'), #modificado
    (402051,'A','CV02','FPA02','RH01','CL03'),
    (402061,'I','CV01','FPA01','','CC02'),
    (402071,'C','CV02','','','CL15'),
    (402081,'I','CV01','FPA01','','CC02'),
    (402091,'A','CV02','FPA02','','CC01'),
    (402101,'L','CV01','FPA01','','CC02'),
    (402111,'A','CV02','FPA02','','CC01'),
    (402121,'A','CV01','FPA01','','CC02'),
    (402131,'A','CV02','FPA02','','CC01'),
    (402141,'C','CV01','','','CL11'),
    (402151,'A','CV02','FPA01','','CC02'),
    (402161,'A','CV01','FPA01','','CC02'),
    (402171,'A','CV02','FPA02','','CC01'),
    (402181,'A','CV01','FPA02','','CC01'),
    (402191,'A','CV02','FPA02','','CC01'),
    (402201,'A','CV01','FPA02','','CC01'),
    (402211,'F','CV01','RH01','','CL21'), #modificado
    (402221,'A','CV02','FPA02','RH01','CL03'),
    (402231,'L','CV01','FPA01','','CC02'),
    (402241,'C','CV02','','','CL15'),
    (402251,'L','CV01','FPA01','','CC02'),
    (402261,'A','CV02','FPA02','','CC01'),
    (402271,'L','CV01','FPA01','','CC02'),
    (402281,'A','CV02','FPA02','','CC01'),
    (402291,'A','CV01','FPA01','','CC02'),
    (402301,'A','CV02','FPA02','','CC01'),
    (402311,'C','CV01','','','CL11'),
    (402321,'A','CV02','FPA01','','CC02'),
    (402331,'A','CV01','FPA01','','CC02'),
    (402341,'A','CV02','FPA02','','CC01'),
    (402351,'A','CV01','FPA02','','CC01'),
    (402361,'A','CV02','FPA02','','CC01'),
    (402371,'A','CV01','FPA02','','CC01'),
    (402381,'F','CV01','RH01','','CL21'), #modificado
    (402391,'A','CV02','FPA02','RH01','CL03'),
    (402401,'L','CV01','FPA01','','CC02'),
    (402411,'C','CV02','','','CL15'),
    (402421,'M','CV01','FPA01','','CC02'),
    (402431,'A','CV02','FPA02','','CC01'),
    (402441,'M','CV01','FPA01','','CC02'),
    (402451,'A','CV02','FPA02','','CC01'),
    (402461,'A','CV01','FPA01','','CC02'),
    (402471,'A','CV02','FPA02','','CC01'),
    (402481,'C','CV01','','','CL11'),
    (402491,'A','CV02','FPA01','','CC02'),
    (402501,'A','CV01','FPA01','','CC02'),
    (402511,'A','CV02','FPA02','','CC01'),
    (402521,'A','CV01','FPA02','','CC01'),
    (402531,'A','CV02','FPA02','','CC01'),
    (402541,'A','CV01','FPA02','','CC01'),
    (402551,'F','CV01','RH01','','CL21'), #modificado
    (402561,'A','CV02','FPA02','RH01','CL03'),
    (402571,'M','CV01','FPA01','','CC02'),
    (402581,'C','CV02','','','CL15'),
    (402591,'M','CV01','FPA01','','CC02'),
    (402601,'A','CV02','FPA02','','CC01'),
    (402611,'M','CV01','FPA01','','CC02'),
    (402621,'A','CV02','FPA02','','CC01'),
    (402631,'A','CV01','FPA01','','CC02'),
    (402641,'A','CV02','FPA02','','CC01'),
    (402651,'C','CV01','','','CL11'),
    (402661,'A','CV02','FPA01','','CC02'),
    (402671,'A','CV01','FPA01','','CC02'),
    (402681,'A','CV02','FPA02','','CC01'),
    (402691,'A','CV01','FPA02','','CC01'),
    (402701,'A','CV02','FPA02','','CC01'),
    (402711,'A','CV01','FPA02','','CC01'),
    (402721,'F','CV01','RH01','','CL21'), #modificado
    (402731,'A','CV02','FPA02','RH01','CL03'),
    (402741,'N','CV01','FPA01','','CC02'),
    (402751,'C','CV02','','','CL15'),
    (402761,'N','CV01','FPA01','','CC02'),
    (402771,'A','CV02','FPA02','','CC01'),
    (402781,'N','CV01','FPA01','','CC02'),
    (402791,'A','CV02','FPA02','','CC01'),
    (402801,'A','CV01','FPA01','','CC02'),
    (402811,'A','CV02','FPA02','','CC01'),
    (402821,'C','CV01','','','CL11'),
    (402831,'A','CV02','FPA01','','CC02'),
    (402841,'A','CV01','FPA01','','CC02'),
    (402851,'A','CV02','FPA02','','CC01'),
    (402861,'A','CV01','FPA02','','CC01'),
    (402871,'A','CV02','FPA02','','CC01'),
    (402881,'A','CV01','FPA02','','CC01'),
    (402891,'F','CV01','RH01','','CL21'), #modificado
    (402901,'A','CV02','FPA02','RH01','CL03'),
    (402911,'N','CV01','FPA01','','CC02'),
    (402921,'C','CV02','','','CL15'),
    (402931,'N','CV01','FPA01','','CC02'),
    (402941,'A','CV02','FPA02','','CC01'),
    (402951,'N','CV01','FPA01','','CC02'),
    (402961,'A','CV02','FPA02','','CC01'),
    (402971,'A','CV01','FPA01','','CC02'),
    (402981,'A','CV02','FPA02','','CC01'),
    (402991,'C','CV01','','','CL11'),
    (403001,'A','CV02','FPA01','','CC02'),
    (403011,'A','CV01','FPA01','','CC02'),
    (403021,'A','CV02','FPA02','','CC01'),
    (403031,'A','CV01','FPA02','','CC01'),
    (403041,'A','CV02','FPA02','','CC01'),
    (403051,'A','CV01','FPA02','','CC01'),
    (403061,'F','CV01','RH01','','CL21'), #modificado
    (403071,'A','CV02','FPA02','RH01','CL03'),
    (403081,'O','CV01','FPA01','','CC02'),
    (403091,'C','CV02','','','CL15'),
    (403101,'O','CV01','FPA01','','CC02'),
    (403111,'A','CV02','FPA02','','CC01'),
    (403121,'O','CV01','FPA01','','CC02'),
    (403131,'A','CV02','FPA02','','CC01'),
    (403141,'A','CV01','FPA01','','CC02'),
    (403151,'A','CV02','FPA02','','CC01'),
    (403161,'C','CV01','','','CL11'),
    (403171,'A','CV02','FPA01','','CC02'),
    (403181,'A','CV01','FPA01','','CC02'),
    (403191,'A','CV02','FPA02','','CC01'),
    (403201,'A','CV01','FPA02','','CC01'),
    (403211,'A','CV02','FPA02','','CC01'),
    (403221,'A','CV01','FPA02','','CC01'),
    (403231,'F','CV01','RH01','','CL21'), #modificado
    (403241,'A','CV02','FPA02','RH01','CL03'),
    (403251,'O','CV01','FPA01','','CC02'),
    (403261,'C','CV02','','','CL15'),
    (403271,'O','CV01','FPA01','','CC02'),
    (403281,'A','CV02','FPA02','','CC01'),
    (403291,'O','CV01','FPA01','','CC02'),
    (403301,'A','CV02','FPA02','','CC01'),
    (403311,'A','CV01','FPA01','','CC02'),
    (403321,'A','CV02','FPA02','','CC01'),
    (403331,'C','CV01','','','CL11'),
    (403341,'A','CV02','FPA01','','CC02'),
    (403351,'A','CV01','FPA01','','CC02'),
    (403361,'A','CV02','FPA02','','CC01'),
    (403371,'A','CV01','FPA02','','CC01'),
    (403381,'A','CV02','FPA02','','CC01'),
    (403391,'A','CV01','FPA02','','CC01'),
    (403401,'F','CV01','RH01','','CL21'), #modificado
    (403411,'A','CV02','FPA02','RH01','CL03'),
    (403421,'O','CV01','FPA01','','CC02'),
    (403431,'C','CV02','','','CL15'),
    (403441,'O','CV01','FPA01','','CC02'),
    (403451,'A','CV02','FPA02','','CC01'),
    (403461,'O','CV01','FPA01','','CC02'),
    (403471,'A','CV02','FPA02','','CC01'),
    (403481,'A','CV01','FPA01','','CC02'),
    (403491,'A','CV02','FPA02','','CC01'),
    (403501,'C','CV01','','','CL11'),
    (403511,'A','CV02','FPA01','','CC02'),
    (403521,'A','CV01','FPA01','','CC02'),
    (403531,'A','CV02','FPA02','','CC01'),
    (403541,'A','CV01','FPA02','','CC01'),
    (403551,'A','CV02','FPA02','','CC01'),
    (403561,'A','CV01','FPA02','','CC01'),
    (403571,'F','CV01','RH01','','CL21'), #modificado
    (403581,'A','CV02','FPA02','RH01','CL03'),
    (403591,'O','CV01','FPA01','','CC02'),
    (403601,'C','CV02','','','CL15'),
    (403611,'O','CV01','FPA01','','CC02'),
    (403621,'A','CV02','FPA02','','CC01'),
    (403631,'O','CV01','FPA01','','CC02'),
    (403641,'A','CV02','FPA02','','CC01'),
    (403651,'A','CV01','FPA01','','CC02'),
    (403661,'A','CV02','FPA02','','CC01'),
    (403671,'C','CV01','','','CL11'),
    (403681,'A','CV02','FPA01','','CC02'),
    (403691,'A','CV01','FPA01','','CC02'),
    (403701,'A','CV02','FPA02','','CC01'),
    (403711,'A','CV01','FPA02','','CC01'),
    (403721,'A','CV02','FPA02','','CC01'),
    (403731,'A','CV01','FPA02','','CC01'),
    (403741,'F','CV01','RH01','','CL21'), #modificado
    (403751,'A','CV02','FPA02','RH01','CL03'),
    (403761,'O','CV01','FPA01','','CC02'),
    (403771,'C','CV02','','','CL15'),
    (403781,'O','CV01','FPA01','','CC02'),
    (403791,'A','CV02','FPA02','','CC01'),
    (403801,'O','CV01','FPA01','','CC02'),
    (403811,'A','CV02','FPA02','','CC01'),
    (403821,'A','CV01','FPA01','','CC02'),
    (403831,'A','CV02','FPA02','','CC01'),
    (403841,'C','CV01','','','CL11'),
    (403851,'A','CV02','FPA01','','CC02'),
    (403861,'A','CV01','FPA01','','CC02'),
    (403871,'A','CV02','FPA02','','CC01'),
    (403881,'A','CV01','FPA02','','CC01'),
    (403891,'A','CV02','FPA02','','CC01'),
    (403901,'A','CV01','FPA02','','CC01'),
    (403911,'F','CV01','RH01','','CL21'), #modificado
    (403921,'A','CV02','FPA02','RH01','CL03'),
    (403931,'O','CV01','FPA01','','CC02'),
    (403941,'C','CV02','','','CL15'),
    (403951,'O','CV01','FPA01','','CC02'),
    (403961,'A','CV02','FPA02','','CC01'),
    (403971,'O','CV01','FPA01','','CC02'),
    (403981,'A','CV02','FPA02','','CC01'),
    (403991,'A','CV01','FPA01','','CC02'),
    (404001,'A','CV02','FPA02','','CC01'),
    (404011,'C','CV01','','','CL11'),
    (404021,'A','CV02','FPA01','','CC02'),
    (404031,'A','CV01','FPA01','','CC02'),
    (404041,'A','CV02','FPA02','','CC01'),
    (404051,'A','CV01','FPA02','','CC01'),
    (404061,'A','CV02','FPA02','','CC01'),
    (404071,'A','CV01','FPA02','','CC01'),
    (404081,'F','CV01','RH01','','CL21'), #modificado
    (404091,'A','CV02','FPA02','RH01','CL03'),
    (404101,'O','CV01','FPA01','','CC02'),
    (404111,'C','CV02','','','CL15'),
    (404121,'O','CV01','FPA01','','CC02'),
    (404131,'A','CV02','FPA02','','CC01'),
    (404141,'O','CV01','FPA01','','CC02'),
    (404151,'A','CV02','FPA02','','CC01'),
    (404161,'A','CV01','FPA01','','CC02'),
    (404171,'A','CV02','FPA02','','CC01'),
    (404181,'C','CV01','','','CL11'),
    (404191,'A','CV02','FPA01','','CC02'),
    (404201,'A','CV01','FPA01','','CC02'),
    (404211,'A','CV02','FPA02','','CC01'),
    (404221,'A','CV01','FPA02','','CC01'),
    (404231,'A','CV02','FPA02','','CC01'),
    (404241,'A','CV01','FPA02','','CC01'),
    (404251,'F','CV01','RH01','','CL21'), #modificado
    (404261,'A','CV02','FPA02','RH01','CL03'),
    (404271,'O','CV01','FPA01','','CC02'),
    (404281,'C','CV02','','','CL15'),
    (404291,'O','CV01','FPA01','','CC02'),
    (404301,'A','CV02','FPA02','','CC01'),
    (404311,'O','CV01','FPA01','','CC02'),
    (404321,'A','CV02','FPA02','','CC01'),
    (404331,'A','CV01','FPA01','','CC02'),
    (404341,'A','CV02','FPA02','','CC01'),
    (404351,'C','CV01','','','CL11'),
    (404361,'A','CV02','FPA01','','CC02'),
    (404371,'A','CV01','FPA01','','CC02'),
    (404381,'A','CV02','FPA02','','CC01'),
    (404411,'A','CV01','FPA02','','CC01'),
    (404421,'F','CV01','RH01','','CL21'), #modificado
    (404431,'A','CV02','FPA02','RH01','CL03'),
    (404441,'O','CV01','FPA01','','CC02'),
    (404451,'C','CV02','','','CL15'),
    (404461,'O','CV01','FPA01','','CC02'),
    (404471,'A','CV02','FPA02','','CC01'),
    (404481,'O','CV01','FPA01','','CC02'),
    (404491,'A','CV02','FPA02','','CC01'),
    (404501,'A','CV01','FPA01','','CC02'),
    (404511,'A','CV02','FPA02','','CC01'),
    (404521,'C','CV01','','','CL11'),
    (404531,'A','CV02','FPA01','','CC02'),
    (404541,'A','CV01','FPA01','','CC02'),
    (404551,'A','CV02','FPA02','','CC01'),
    (404561,'A','CV01','FPA02','','CC01'),
    (404571,'A','CV02','FPA02','','CC01'),
    (404581,'A','CV01','FPA02','','CC01'),
    (404591,'F','CV01','RH01','','CL21'), #modificado
    (404601,'A','CV02','FPA02','RH01','CL03'),
    (404611,'O','CV01','FPA01','','CC02'),
    (404621,'C','CV02','','','CL15'),
    (404631,'O','CV01','FPA01','','CC02'),
    (404641,'A','CV02','FPA02','','CC01'),
    (404651,'O','CV01','FPA01','','CC02'),
    (404661,'A','CV02','FPA02','','CC01'),
    (404671,'A','CV01','FPA01','','CC02'),
    (404681,'A','CV02','FPA02','','CC01'),
    (404691,'C','CV01','','','CL11'),
    (404701,'A','CV02','FPA01','','CC02'),
    (404711,'A','CV01','FPA01','','CC02'),
    (404721,'A','CV02','FPA02','','CC01'),
    (404731,'A','CV01','FPA02','','CC01'),
    (404741,'A','CV02','FPA02','','CC01'),
    (404751,'A','CV01','FPA02','','CC01'),
    (404761,'F','CV01','RH01','','CL21'), #modificado
    (404771,'A','CV02','FPA02','RH01','CL03'),
    (404781,'O','CV01','FPA01','','CC02'),
    (404791,'C','CV02','','','CL15'),
)

def gera_individuo():
    transicoes = []

    possiveis = lambda anterior: ('A', 'B', 'C') if anterior[:2] != 'CV' else ('A', 'B')
    ponte = lambda anterior: random.choice(possiveis(anterior))

    for os in OSES:
        transicoes.append(dict(origem=None, destino=os[2], os=os[:2], ponte='A'))
        anterior = os[2]
        if os[3]:
            transicoes.append(dict(origem=anterior, destino=os[3], os=os[:2], ponte=ponte(anterior), possiveis=possiveis(anterior)))
            anterior = os[3]
        if os[4]:
            transicoes.append(dict(origem=anterior, destino=os[4], os=os[:2], ponte=ponte(anterior), possiveis=possiveis(anterior)))
            anterior = os[4]
        if os[5]:
            transicoes.append(dict(origem=anterior, destino=os[5], os=os[:2], ponte=ponte(anterior), possiveis=possiveis(anterior)))
            anterior = os[5]
        transicoes.append(dict(origem=anterior, destino=None, os=os[:2], ponte=ponte(anterior), possiveis=possiveis(anterior)))
    return transicoes

print executa(pontes, estagios, gera_individuo())
