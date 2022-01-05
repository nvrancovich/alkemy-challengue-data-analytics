import logging as log

# Se define la configuracion de los logs

log.basicConfig(level=log.DEBUG, 
                format='%(asctime)s: %(levelname)s [%(filename)s] %(message)s', datefmt='%I:%M:%S %p')