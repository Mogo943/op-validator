# Bot-ana [Mi primer proyecto complejo]

Proyecto incompleto, en sus ultimos añadidos no se pudo probar porque cerró el area de la empresa.

-Bot-ana inicia sesion en gmail mediante la API de google, lee los correos sin leer del emisor que sea seteado (se usaba con los correos de notificacion de transferencia de un banco)
-Extrae datos relevantes del correo como nombre del titular, fecha, hora y monto.
-Descompone el nombre porque casi nunca el titular del banco coincidia exactamente con el titular anunciado por el usuario de la plataforma.
-Guarda temporalmente estos datos en un sheet.
-Bot-ana en la web inicia sesion, evalua la liquidez y decide si se puede trabajar o no, asi que enciende o no la recepcion de solicitudes, evalua constantemente la liquidez si esta baja de cierto punto apaga la recepcion de solicutdes
tambien evalua la hora pues tenia un horario establecido la plataforma.
-Detecta la solicitud, la abre, extrae datos relevantes y hace la comparacion con el sheet temporal
-Si todo esta bien completa la solicitud de fondos
-Si no, espera un tiempo prudente antes de decidir cancelarla
-En caso de que el monto de la solicitud y el monto de la transferencia sean distintos ajusta el monto de la solicitud y la confirma
