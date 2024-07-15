-Bot-ana inicia sesión en Gmail mediante la API de Google y lee los correos no leídos del emisor configurado (usualmente correos de notificación de transferencia de un banco).

-Extrae datos relevantes del correo, como nombre del titular, fecha, hora y monto.

-Descompone el nombre porque casi nunca el titular del banco coincidía exactamente con el titular anunciado por el usuario de la plataforma.

-Guarda temporalmente estos datos en una hoja de cálculo.

-Bot-ana en la web inicia sesión, evalúa la liquidez y decide si se puede trabajar o no, encendiendo o apagando la recepción de solicitudes. Evalúa constantemente la liquidez y, si baja de cierto punto, apaga la recepción de solicitudes. También evalúa la hora, ya que la plataforma tiene un horario establecido.

-Detecta la solicitud, la abre, extrae datos relevantes y hace la comparación con la hoja de cálculo temporal.

-Si todo está bien, completa la solicitud de fondos.

-Si no, espera un tiempo prudente antes de decidir cancelarla.

-En caso de que el monto de la solicitud y el monto de la transferencia sean distintos, ajusta el monto de la solicitud y la confirma.
